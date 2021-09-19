from XstreamDL_CLI.cmdargs import CmdArgs
from XstreamDL_CLI.extractor import Extractor
from XstreamDL_CLI.downloader import Downloader


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
            return Downloader(self.args).download_streams(streams)
        while self.exit:
            break