import asyncio
from typing import List
from pathlib import Path
from urllib.request import getproxies
from aiohttp import ClientSession, ClientResponse
from XstreamDL_CLI.cmdargs import CmdArgs
from XstreamDL_CLI.util.stream import Stream
from XstreamDL_CLI.extractors.hls.parser import HLSParser


class Extractor:
    '''
    请求DASH/HLS链接内容，也就是下载元数据
    或者读取含有元数据的文件
    或者读取含有多个元数据文件的文件夹
    最终得到一个Stream（流）对象供Downloader（下载器）下载
    '''
    def __init__(self, args: CmdArgs):
        self.args = args
        self.proxies = getproxies()
        self.headers = {
            'user-agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/87.0.4280.141 Safari/537.36'
            )
        }

    def fetch_metadata(self, uri: str):
        '''
        从链接/文件/文件夹等加载内容 解析metadata
        '''
        if uri.startswith('http://') or uri.startswith('https://') or uri.startswith('ftp://'):
            loop = asyncio.get_event_loop()
            return self.raw2streams('url', uri, loop.run_until_complete(self.fetch(uri)))
        illegal_symbols = ["\\", "/", ":", "：", "*", "?", "\"", "<", ">", "|", "\r", "\n", "\t"]
        is_illegal_path = True
        for illegal_symbol in illegal_symbols:
            if illegal_symbol in uri:
                is_illegal_path = False
                break
        if is_illegal_path is False:
            return
        if Path(uri).exists() is False:
            return
        if Path(uri).is_file():
            return self.raw2streams('path', uri, Path(uri).read_text(encoding='utf-8'))
        if Path(uri).is_dir() is False:
            return
        streams = []
        for path in Path(uri).iterdir():
            _streams = self.raw2streams('path', path.name, path.read_text(encoding='utf-8'))
            if _streams is None:
                continue
            streams.extend(_streams)
        return streams

    async def fetch(self, url: str) -> str:
        proxy, headers = self.args.proxy, self.args.headers
        async with ClientSession() as client: # type: ClientSession
            async with client.get(url, proxy=proxy, headers=headers) as resp: # type: ClientResponse
                return await resp.text(encoding='utf-8')

    def raw2streams(self, uri_type: str, uri: str, content: str) -> List[Stream]:
        '''
        解析解码后的返回结果
        '''
        if not content:
            return []
        if content.startswith('#EXTM3U'):
            return self.parse_as_hls(uri_type, uri, content)
        elif '<MPD' in content and '</MPD>' in content:
            return self.parse_as_dash(uri, content)
        else:
            return []

    def parse_as_hls(self, uri_type: str, uri: str, content: str) -> List[Stream]:
        _streams = HLSParser(self.args, uri_type).parse(uri, content)
        streams = []
        for stream in _streams:
            # 针对master类型加载详细内容
            if stream.tag != '#EXT-X-STREAM-INF' and stream.tag != '#EXT-X-MEDIA':
                streams.append(stream)
                continue
            new_streams = self.fetch_metadata(stream.origin_url)
            if new_streams is None:
                continue
            streams.extend(new_streams)
        # 在全部流解析完成后 再处理key
        for stream in streams:
            stream.try_fetch_key(self.args)
        return streams

    def parse_as_dash(self, uri: str, content: str) -> List[Stream]:
        streams = []
        stream = Stream('dash')
        streams.append(stream)
        return streams