from typing import List
from XstreamDL_CLI.cmdargs import CmdArgs
from XstreamDL_CLI.extractor import Extractor
from XstreamDL_CLI.downloader import Downloader
from XstreamDL_CLI.models.stream import Stream
from XstreamDL_CLI.extractors.hls.stream import HLSStream
from XstreamDL_CLI.extractors.dash.stream import DASHStream


class Daemon:

    def __init__(self, args: CmdArgs):
        self.args = args
        self.exit = False
        # <---来自命令行的设置--->
        self.max_concurrent_downloads = 1

    def daemon(self):
        '''
        - 解析
        - 下载
        - 合并
        '''
        extractor = Extractor(self.args)
        streams = extractor.fetch_metadata(self.args.URI[0])
        if self.args.repl is False:
            if self.args.live is False:
                return Downloader(self.args).download_streams(streams)
            else:
                return self.live_record(streams)
        while self.exit:
            break

    def live_record(self, streams: List[Stream]):
        '''
        - 第一轮解析 判断类型
        - 选择流 交给下一个函数具体下载-刷新-下载...
        - TODO
        -   提供录制时长设定
        '''
        if isinstance(streams[0], DASHStream):
            self.live_record_dash(streams)
        if isinstance(streams[0], HLSStream):
            self.live_record_hls(streams)
        assert False, f'unsupported live stream type {type(streams[0])}'

    def live_record_dash(self, streams: List[DASHStream]):
        '''
        dash直播流
        重复拉取新的mpd后
        判断是否和之前的重复关键在于url的path部分是不是一样的
        也就是说 文件是不是一个
        那么主要逻辑如下
        - 再次解析 这一轮解析的时候 select 复用第一轮的选择 用skey来判断
        - 判断合并 下载已经解析好的分段
        - 再次解析 再次下载 直到满足结束条件
        Q 为何先再次解析而不是先下载完第一轮解析的分段再下载
        A 第一轮解析时有手动选择流的过程 而dash流刷新时间一般都很短 往往只有几秒钟 所以最好是尽快拉取一次最新的mpd
        Q 为什么不拉取新mpd单独开一个线程
        A 下载的时候很可能会占满网速 个人认为循环会好一点
        Q 万一下载卡住导致mpd刷新不及时怎么办
        A 还没有想好 不过这种情况概率蛮小的吧... 真的发生了说明你的当前网络不适合录制
        '''
        assert False, 'not support dash live stream, wait plz'

    def live_record_hls(self, streams: List[HLSStream]):
        '''
        hls直播流
        '''
        assert False, 'not support hls live stream, wait plz'