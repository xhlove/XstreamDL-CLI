import time
import click
import signal
import asyncio
import binascii
import logging
from typing import List, Set, Dict
from asyncio import new_event_loop
from asyncio import AbstractEventLoop, Future, Task
from aiohttp import ClientSession, ClientResponse, TCPConnector, client_exceptions
from concurrent.futures._base import TimeoutError, CancelledError
from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
    TaskID,
)
from XstreamDL_CLI.cmdargs import CmdArgs
from XstreamDL_CLI.models.stream import Stream
from XstreamDL_CLI.models.segment import Segment
from XstreamDL_CLI.util.decryptors.aes import CommonAES
from XstreamDL_CLI.util.texts import t_msg


def get_selected_index(length: int) -> list:
    selected = []
    try:
        text = input(t_msg.input_stream_number).strip()
    except EOFError:
        click.secho(t_msg.select_without_any_stream)
        return []
    if text == '':
        return [index for index in range(length + 1)]
    elif text.isdigit():
        return [int(text)]
    elif '-' in text and len(text.split('-')) == 2:
        start, end = text.split('-')
        if start.strip().isdigit() and end.strip().isdigit():
            return [index for index in range(int(start.strip()), int(end.strip()) + 1)]
    elif text.replace(' ', '').isdigit():
        for index in text.split(' '):
            if index.strip().isdigit():
                if int(index.strip()) <= length:
                    selected.append(int(index))
        return selected
    elif text.replace(',', '').replace(' ', '').isdigit():
        for index in text.split(','):
            if index.strip().isdigit():
                if int(index.strip()) <= length:
                    selected.append(int(index))
        return selected
    return selected


def get_left_segments(stream: Stream):
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


def get_connector(args: CmdArgs):
    '''
    connector在一个ClientSession使用后可能就会关闭
    若需要再次使用则需要重新生成
    '''
    return TCPConnector(
        ttl_dns_cache=500,
        ssl=False,
        limit_per_host=args.limit_per_host,
        limit=500,
        force_close=not args.disable_force_close,
        enable_cleanup_closed=not args.disable_force_close
    )


class Downloader:

    def __init__(self, args: CmdArgs):
        self.logger = logging.getLogger('downloader')
        self.args = args
        # <---进度条--->
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[name]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.2f}%",
            "•",
            DownloadColumn(binary_units=True),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn()
        )
        self.terminate = False
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, signum: int, frame):
        self.terminate = True

    def download_streams(self, streams: List[Stream]):
        ts = time.time()
        if streams is None:
            return
        if len(streams) == 0:
            return
        for index, stream in enumerate(streams):
            stream.show_info(index, show_init=self.args.show_init, add_index_to_name=self.args.add_index_to_name)
        if self.args.select is True:
            selected = get_selected_index(len(streams))
        else:
            selected = [index for index in range(len(streams) + 1)]
        all_results = []
        for index, stream in enumerate(streams):
            if self.terminate is True:
                break
            if index not in selected:
                continue
            stream.dump_segments()
            max_failed = 5
            if self.args.parse_only:
                if len(stream.segments) <= 5:
                    stream.show_segments()
                continue
            click.secho(f'{stream.get_name()} {t_msg.download_start}.')
            while max_failed > 0:
                loop = new_event_loop()
                results = loop.run_until_complete(self.do_with_progress(loop, stream))
                loop.close()
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
                # if stream.stream_type == 'text':
                #     # mpd中text类型 一般是字幕直链 跳过合并
                #     pass
                if self.args.disable_auto_concat is False:
                    stream.concat(self.args)
                break
        print(f'下载耗时 {time.time() - ts:.2f}s')
        return all_results

    def init_progress(self, stream: Stream, completed: int):
        stream_id = self.progress.add_task("download", name=stream.get_name(), start=False) # TaskID
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
                    pass
                    # print('下载过程中出现已知异常 需重新下载\n')
                elif flag is False:
                    # 某几类已知异常 如状态码不对 返回头没有文件大小 视为无法下载 主动退出
                    cancel_all_task()
                    if status in ['STATUS_CODE_ERROR', 'NO_CONTENT_LENGTH']:
                        click.secho(f'{status} {t_msg.segment_cannot_download}')
                    elif status == 'EXIT':
                        pass
                    else:
                        click.secho(f'{status} {t_msg.segment_cannot_download_unknown_status}')
                results[segment] = flag
            else:
                # 出现未知异常 强制退出全部task
                click.secho(f'{t_msg.segment_cannot_download_unknown_exc} => {_future.exception()}\n')
                cancel_all_task()
                results['未知segment'] = False

        def cancel_all_task() -> None:
            for task in tasks:
                task.remove_done_callback(_done_callback)
            for task in filter(lambda task: not task.done(), tasks):
                task.cancel()
        # limit_per_host 根据不同网站和网络状况调整 如果与目标地址连接性较好 那么设置小一点比较好
        completed, _left = get_left_segments(stream)
        if len(_left) == 0:
            return results
        # 没有需要下载的则尝试合并 返回False则说明需要继续下载完整
        with self.progress:
            stream_id = self.init_progress(stream, completed)
            client = ClientSession(connector=get_connector(self.args)) # type: ClientSession
            for segment in _left:
                task = loop.create_task(self.download(client, stream_id, stream, segment))
                task.add_done_callback(_done_callback)
                tasks.add(task)
            # 阻塞并等待运行完成
            finished, unfinished = await asyncio.wait(tasks)
            # 关闭ClientSession
            await client.close()
        return results

    async def download(self, client: ClientSession, stream_id: TaskID, stream: Stream, segment: Segment):
        proxy, headers = self.args.proxy, self.args.headers
        status, flag = 'EXIT', True
        try:
            async with client.get(segment.url, proxy=proxy, headers=headers) as resp: # type: ClientResponse
                _flag = True
                if resp.status in [403, 404]:
                    status = 'STATUS_SKIP'
                    flag = False
                    segment.skip_concat = True
                if resp.status == 405:
                    status = 'STATUS_CODE_ERROR'
                    flag = False
                if resp.headers.get('Content-length') is not None:
                    stream.filesize += int(resp.headers["Content-length"])
                    self.progress.update(stream_id, total=stream.filesize)
                else:
                    _flag = False
                if flag:
                    self.progress.start_task(stream_id)
                    while self.terminate is False:
                        data = await resp.content.read(512)
                        if not data:
                            break
                        segment.content.append(data)
                        self.progress.update(stream_id, advance=len(data))
                        if _flag is False:
                            stream.filesize += len(data)
                            self.progress.update(stream_id, total=stream.filesize)
        except TimeoutError:
            return segment, 'TimeoutError', None
        except client_exceptions.ClientConnectorError:
            return segment, 'ClientConnectorError', None
        except client_exceptions.ClientPayloadError:
            return segment, 'ClientPayloadError', None
        except client_exceptions.ClientOSError:
            return segment, 'ClientOSError', None
        except client_exceptions.ServerDisconnectedError:
            return segment, 'ServerDisconnectedError', None
        except client_exceptions.InvalidURL:
            return segment, 'EXIT', False
        except CancelledError:
            return segment, 'EXIT', False
        except Exception as e:
            self.logger.error(f'! -> {segment.url}', exc_info=e)
            return segment, status, False
        if self.terminate:
            return segment, 'EXIT', False
        if segment.skip_concat:
            return segment, status, True
        if flag is False:
            return segment, status, False
        return segment, 'SUCCESS', await self.decrypt(segment, stream)

    async def decrypt(self, segment: Segment, stream: Stream) -> bool:
        '''
        解密部分
        '''
        if segment.is_encrypt() is False and segment.is_ism():
            segment.fix_header(stream)
        if self.args.disable_auto_decrypt is True:
            return segment.dump()
        if segment.is_encrypt() and segment.is_supported_encryption():
            cipher = CommonAES(segment.xkey.key, binascii.a2b_hex(segment.xkey.iv))
            return cipher.decrypt(segment)
        else:
            return segment.dump()
