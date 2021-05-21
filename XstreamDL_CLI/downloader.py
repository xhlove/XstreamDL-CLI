import click
import signal
import binascii
import logging
import requests
from typing import List, Set, Dict
from concurrent.futures import Future, CancelledError, ThreadPoolExecutor, as_completed
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
from XstreamDL_CLI.extractor import Extractor
from XstreamDL_CLI.models.segment import Segment
from XstreamDL_CLI.util.decryptors.aes import CommonAES


class Downloader:

    def __init__(self, args: CmdArgs):
        self.logger = logging.getLogger('downloader')
        self.args = args
        self.exit = False
        # <---来自命令行的设置--->
        self.max_concurrent_downloads = 1
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

    def get_conn(self):
        '''
        connector在一个ClientSession使用后可能就会关闭
        若需要再次使用则需要重新生成
        '''
        return TCPConnector(
            ttl_dns_cache=300,
            ssl=False,
            limit_per_host=self.args.limit_per_host,
            limit=500,
            force_close=not self.args.disable_force_close,
            enable_cleanup_closed=not self.args.disable_force_close
        )

    def daemon(self):
        '''
        一直循环调度下载和更新进度
        '''
        if self.args.repl is False:
            self.download_stream()
            return
        while self.exit:
            break

    def download_stream(self):
        extractor = Extractor(self.args)
        streams = extractor.fetch_metadata(self.args.URI[0])
        self.download_all_segments(streams)

    def get_selected_index(self, length: int) -> list:
        selected = []
        try:
            text = input('请输入要下载流的序号：\n').strip()
        except EOFError:
            click.secho('未选择流，退出')
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

    def download_all_segments(self, streams: List[Stream]):
        if streams is None:
            return
        if len(streams) == 0:
            return
        for index, stream in enumerate(streams):
            stream.show_info(index)
        if self.args.select is True:
            selected = self.get_selected_index(len(streams))
        else:
            selected = [index for index in range(len(streams) + 1)]
        all_results = []
        for index, stream in enumerate(streams):
            if self.terminate is True:
                break
            if index not in selected:
                continue
            click.secho(f'{stream.get_name()} download start.')
            stream.dump_segments()
            max_failed = 5
            while max_failed > 0:
                results = self.do_with_progress(stream)
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
                    # if stream.stream_type == 'text':
                    #     # mpd中text类型 一般是字幕直链 跳过合并
                    #     pass
                    if self.args.disable_auto_concat is False:
                        stream.concat(self.args)
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
        stream_id = self.progress.add_task("download", name=stream.get_name(), start=False)  # TaskID
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

    def do_with_progress(self, stream: Stream):
        '''
        下载过程输出进度 并合理处理异常
        '''
        executor = ThreadPoolExecutor()
        results = {}  # type: Dict[bool]
        tasks = set()  # type: Set[Task]

        def _done_callback(_future: Future) -> None:
            nonlocal results
            error = False
            if _future.exception() is None:
                segment, status, flag = _future.result()
                if flag is None:
                    pass
                    # print('下载过程中出现已知异常 需重新下载\n')
                elif flag is False:
                    # 某几类已知异常 如状态码不对 返回头没有文件大小 视为无法下载 主动退出
                    error = True
                    if status in ['STATUS_CODE_ERROR', 'NO_CONTENT_LENGTH']:
                        print(f'无法下载的m3u8 {status} 退出其他下载任务\n')
                    elif status == 'EXIT':
                        pass
                    else:
                        print(f'出现未知status -> {status} 退出其他下载任务\n')
                results[segment] = flag
            else:
                # 出现未知异常 强制退出全部task
                error = True
                print('出现未知异常 强制退出全部task\n')
                results['未知segment'] = False
            return error

        # limit_per_host 根据不同网站和网络状况调整 如果与目标地址连接性较好 那么设置小一点比较好
        completed, _left = self.get_left_segments(stream)
        if len(_left) == 0:
            return results
        # 没有需要下载的则尝试合并 返回False则说明需要继续下载完整
        with self.progress:
            stream_id = self.init_progress(stream, completed)
            # client = ClientSession(connector=self.get_conn()) # type: ClientSession
            client = requests.Session()
            for segment in _left:
                task = executor.submit(self.download, client, stream_id, stream, segment)
                tasks.add(task)
            for task in as_completed(tasks):
                error = _done_callback(task)
                if error:
                    break
            # 关闭ClientSession
            client.close()
        return results

    def download(self, client: requests.Session, stream_id: TaskID, stream: Stream, segment: Segment):
        proxy, headers = self.args.proxy, self.args.headers
        status, flag = 'EXIT', True
        try:
            resp = client.get(segment.url, proxies=proxy, headers=headers)
            _flag = True
            if resp.status_code == 405:
                status = 'STATUS_CODE_ERROR'
                flag = False
            if resp.headers.get('Content-length') is not None:
                stream.filesize += int(resp.headers["Content-length"])
                self.progress.update(stream_id, total=stream.filesize)
            else:
                _flag = False
            if flag:
                self.progress.start_task(stream_id)
                data = resp.content
                segment.content.append(data)
                self.progress.update(stream_id, advance=len(data))
                if _flag is False:
                    stream.filesize += len(data)
                    self.progress.update(stream_id, total=stream.filesize)
        except TimeoutError:
            return segment, 'TimeoutError', None
        except requests.exceptions.ConnectionError:
            return segment, 'ConnectionError', None
        except requests.exceptions.InvalidURL:
            return segment, 'EXIT', False
        except CancelledError:
            return segment, 'EXIT', False
        except Exception as e:
            self.logger.error(f'! -> {segment.url}', exc_info=e)
            return segment, status, False
        if self.terminate:
            return segment, 'EXIT', False
        if flag is False:
            return segment, status, False
        return segment, 'SUCCESS', self.decrypt(segment)

    def decrypt(self, segment: Segment) -> bool:
        '''
        解密部分
        '''
        if self.args.disable_auto_decrypt is True:
            return segment.dump()
        if segment.is_encrypt() and segment.is_supported_encryption():
            cipher = CommonAES(segment.xkey.key, binascii.a2b_hex(segment.xkey.iv))
            return cipher.decrypt(segment)
        else:
            return segment.dump()
