import click
import aiohttp
import asyncio
from typing import List
from pathlib import Path
from argparse import Namespace
from urllib.request import getproxies

from .util.stream import Stream
from .extractors.hls.parser import Parser as hls_parser


class Extractor:
    '''
    请求DASH/HLS链接内容，也就是下载元数据
    或者读取含有元数据的文件
    或者读取含有多个元数据文件的文件夹
    最终得到一个Stream（流）对象供Downloader（下载器）下载
    '''
    def __init__(self, args: Namespace):
        self.args = args
        self.proxies = getproxies()

    def fetch_metadata(self, url: str):
        if url.startswith('http://') or url.startswith('https://') or url.startswith('ftp://'):
            loop = asyncio.get_event_loop()
            return self.raw2streams(url, loop.run_until_complete(self.fetch(url)))
        else:
            return self.raw2streams(url, self.load_as_file(url))

    def load_as_file(self, path: str):
        if Path(path).exists():
            if Path(path).is_dir():
                click.secho('not support folder now')
            else:
                return Path(path).read_text(encoding='utf-8')
        else:
            click.secho(f'unknow type for URI -> {path}')

    async def fetch(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text(encoding='utf-8')

    def raw2streams(self, uri: str, content: str) -> List[Stream]:
        '''
        解析解码后的返回结果
        '''
        if not content:
            return
        if content.startswith('#EXTM3U'):
            return self.parse_as_hls(uri, content)
        elif '<MPD' in content and '</MPD>' in content:
            return self.parse_as_dash(uri, content)
        else:
            return

    def parse_as_hls(self, uri: str, content: str) -> List[Stream]:
        _streams = hls_parser(self.args).parse(uri, content)
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
        return streams

    def parse_as_dash(self, uri: str, content: str) -> List[Stream]:
        streams = []
        stream = Stream('dash')
        streams.append(stream)
        return streams