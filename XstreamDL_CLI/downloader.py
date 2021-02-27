import click
import asyncio
import binascii
from typing import List, Set, Dict
from asyncio import get_event_loop
from asyncio import AbstractEventLoop, Future, Task
from aiohttp import request, TCPConnector
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError
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
        loop = get_event_loop()
        loop.run_until_complete(self.download_all_segments(loop, streams))
        loop.close()

    async def download_all_segments(self, loop: AbstractEventLoop, streams: List[Stream]):
        for index, stream in enumerate(streams):
            stream.show_info(index)
        all_results = []
        for stream in streams:
            click.secho(f'{stream.name} download start.')
            max_failed = 5
            while max_failed > 0:
                results = await self.do_with_progress(loop, stream)
                all_results.append(results)
                count_none, count_true, count_false = 0, 0, 0
                for _, flag in results.items():
                    if flag is True:
                        count_true += 1
                    elif flag is False:
                        count_false += 1
                    else:
                        count_none += 1
                # 出现False则说明无法下载
                if count_false > 0:
                    break
                # False 0 出现None则说明需要继续下载 否则合并
                if count_none > 0:
                    max_failed -= 1
                    continue
                else:
                    stream.concat()
                    break
        return all_results

    def get_left_segments(self, stream: Stream):
        completed = 0
        _left_segments = []
        for segment in stream.segments:
            segment_path = segment.get_path()
            if segment_path.exists() is True:
                # 文件落盘 说明下载一定成功了
                if segment_path.stat().st_size == 0:
                    segment_path.unlink()
                else:
                    completed += segment_path.stat().st_size
                    continue
            _left_segments.append(segment)
        return completed, _left_segments

    def init_progress(self, stream: Stream, completed: int):
        stream_id = self.progress.add_task("download", name=stream.name, start=False) # TaskID
        if completed > 0:
            if stream.filesize > 0:
                total = stream.filesize
            else:
                total = completed
                stream.filesize = total
            self.progress.update(stream_id, completed=completed, total=total)
        else:
            if stream.filesize > 0:
                total = stream.filesize
            else:
                total = 0
                stream.filesize = total
            self.progress.update(stream_id, total=total)
        return stream_id

    async def do_with_progress(self, loop: AbstractEventLoop, stream: Stream):
        '''
        下载过程输出进度 并合理处理异常
        '''
        results = {} # type: Dict[bool]
        tasks = set() # type: Set[Task]

        def _done_callback(_future: Future) -> None:
            nonlocal results
            if _future.exception() is None:
                segment, status, flag = _future.result()
                if flag is None:
                    print('下载过程中出现已知异常 需重新下载\n')
                elif flag is False:
                    # 某几类已知异常 如状态码不对 返回头没有文件大小 视为无法下载 主动退出
                    if status in ['STATUS_CODE_ERROR', 'NO_CONTENT_LENGTH']:
                        # print('无法下载的m3u8 退出其他下载任务\n')
                        cancel_all_task()
                    else:
                        print(f'出现未知status -> {status} 退出其他下载任务\n')
                        cancel_all_task()
                results[segment] = flag
            else:
                # 出现未知异常 强制退出全部task
                print('出现未知异常 强制退出全部task\n')
                cancel_all_task()
                results[segment] = False

        def cancel_all_task() -> None:
            for task in tasks:
                task.remove_done_callback(_done_callback)
            for task in filter(lambda task: not task.done(), tasks):
                task.cancel()

        completed, _left = self.get_left_segments(stream)
        if len(_left) == 0:
            return results
        # 没有需要下载的则尝试合并 返回False则说明需要继续下载完整
        with self.progress:
            stream_id = self.init_progress(stream, completed)
            connector = TCPConnector(ttl_dns_cache=300, limit_per_host=4, limit=100, force_close=True, enable_cleanup_closed=True)
            for segment in _left:
                task = loop.create_task(self.download(connector, stream_id, stream, segment))
                task.add_done_callback(_done_callback)
                tasks.add(task)
            finished, unfinished = await asyncio.wait(tasks)
            # 阻塞并等待运行完成
        return results

    async def download(self, connector: TCPConnector, stream_id: TaskID, stream: Stream, segment: Segment):
        status, flag = 'EXIT', True
        try:
            async with request('GET', segment.url, connector=connector, headers=segment.headers) as response:
                if response.status == 405:
                    status = 'STATUS_CODE_ERROR'
                    flag = False
                elif response.headers.get('Content-length') is None:
                    status = 'NO_CONTENT_LENGTH'
                    flag = False
                else:
                    stream.filesize += int(response.headers["Content-length"])
                    self.progress.update(stream_id, total=stream.filesize)
                    self.progress.start_task(stream_id)
                    while True:
                        data = await response.content.read(512)
                        if not data:
                            break
                        segment.content.append(data)
                        self.progress.update(stream_id, advance=len(data))
        except ClientConnectorError:
            return segment, 'ClientConnectorError', None
        except ClientPayloadError:
            return segment, 'ClientPayloadError', None
        except ConnectionResetError:
            return segment, 'ConnectionResetError', None
        except Exception:
            # print(e, f'{status}\n')
            return segment, status, False
        if flag is False:
            return segment, status, False
        return segment, 'SUCCESS', await self.decrypt(segment)

    async def decrypt(self, segment: Segment) -> bool:
        '''
        解密部分
        '''
        if segment.is_encrypt():
            cipher = CommonAES(segment.xkey.key, binascii.a2b_hex(segment.xkey.iv))
            return cipher.decrypt(segment)
        else:
            return segment.dump()