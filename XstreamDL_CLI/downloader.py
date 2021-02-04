import click
import asyncio
import binascii
from typing import List
from aiohttp import request
from argparse import Namespace
from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
    TaskID,
)

from .extractor import Extractor
from .util.stream import Stream
from .util.segment import Segment
from .util.decryptors.aes import CommonAES


class Downloader:

    def __init__(self):
        self.exit = False
        # <---来自命令行的设置--->
        self.max_concurrent_downloads = 1
        # <---进度条--->
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[name]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.2f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )

    def daemon(self, args: Namespace):
        '''
        一直循环调度下载和更新进度
        '''
        if args.repl is False:
            self.download_one_stream(args)
            # click.secho('Download end.')
            return
        while self.exit:
            break

    def download_one_stream(self, args: Namespace):
        extractor = Extractor(args)
        streams = extractor.fetch_metadata(args.URI[0])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.download_all_segments(loop, streams))

    async def download_all_segments(self, loop: asyncio.AbstractEventLoop, streams: List[Stream]):
        for index, stream in enumerate(streams):
            stream.show_info(index)
        all_results = []
        for stream in streams:
            click.secho(f'{stream.name} download start.')
            _left_segments = []
            for segment in stream.segments:
                segment_path = segment.get_path()
                if segment_path.exists() is True:
                    # 文件落盘 说明下载一定成功了
                    if segment_path.stat().st_size == 0:
                        segment_path.unlink()
                    else:
                        continue
                _left_segments.append(segment)
            if len(_left_segments) == 0:
                stream.concat()
                continue
            with self.progress:
                stream_id = self.progress.add_task("download", name=stream.name, start=False) # TaskID
                tasks = []
                for segment in _left_segments:
                    task = loop.create_task(self.download(stream_id, stream, segment))
                    tasks.append(task)
                finished, unfinished = await asyncio.wait(tasks)
                results = []
                for task in finished:
                    result = task.result()
                    results.append(result)
                all_results.append(results)
                # click.secho(f'{stream.name} download end.')
            stream.concat()
        return all_results

    async def download(self, stream_id: TaskID, stream: Stream, segment: Segment):
        async with request('GET', segment.url, headers=segment.headers) as response:
            stream.filesize += int(response.headers["Content-length"])
            self.progress.update(stream_id, total=stream.filesize)
            self.progress.start_task(stream_id)
            while True:
                data = await response.content.read(1024)
                if not data:
                    break
                segment.content.append(data)
                self.progress.update(stream_id, advance=len(data))
        return await self.decrypt(segment)

    async def decrypt(self, segment: Segment):
        '''
        解密部分
        '''
        if segment.is_encrypt():
            cipher = CommonAES(segment.xkey.key, binascii.a2b_hex(segment.xkey.iv))
            cipher.decrypt(segment)
        else:
            return segment.dump()