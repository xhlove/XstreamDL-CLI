import click
from typing import List, Dict

from .ism import ISM
from .handler import xml_handler

from .stream import MSSStream
from ..base import BaseParser
from XstreamDL_CLI.cmdargs import CmdArgs


class MSSParser(BaseParser):
    def __init__(self, args: CmdArgs, uri_type: str):
        super(MSSParser, self).__init__(args, uri_type)
        self.suffix = '.ism'

    def parse(self, uri: str, content: str) -> List[MSSStream]:
        uris = self.parse_uri(uri)
        if uris is None:
            click.secho(f'parse {uri} failed')
            return []
        name, home_url, base_url = uris
        # 解析转换内容为期望的对象
        ism = xml_handler(content)
        print(f'developing... -> {ism}')