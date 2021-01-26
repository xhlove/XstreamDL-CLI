import os
import click
import asyncio
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
        with self.progress:
            for stream in streams:
                click.secho(f'{stream.name} download start.')
                stream_id = self.progress.add_task("download", name=stream.name, start=False) # TaskID
                tasks = []
                for segment in stream.segments:
                    if os.path.exists(segment.get_path()) is True:
                        # 文件落盘 说明下载一定成功了
                        continue
                    task = loop.create_task(self.download(stream_id, stream, segment))
                    tasks.append(task)
                finished, unfinished = await asyncio.wait(tasks)
                results = []
                for task in finished:
                    result = task.result()
                    results.append(result)
                all_results.append(results)
                # click.secho(f'{stream.name} download end.')
        return all_results

    async def download(self, stream_id: TaskID, stream: Stream, segment: Segment):
        async with request('GET', segment.url, headers=segment.headers) as r:
            stream.filesize += int(r.headers["Content-length"])
            self.progress.update(stream_id, total=stream.filesize)
            self.progress.start_task(stream_id)
            while True:
                data = await r.content.read(1024)
                if not data:
                    break
                segment.content.append(data)
                self.progress.update(stream_id, advance=len(data))
        return self.decrypt(segment)

    def decrypt(self, segment: Segment):
        '''
        解密部分 后面再写
        '''
        return self.dump(segment)

    def dump(self, segment: Segment):
        # click.secho(f'{segment.name} download end.')
        with open(segment.get_path(), 'wb') as f:
            f.write(b''.join(segment.content))