from pathlib import Path
from XstreamDL_CLI.cmdargs import CmdArgs


class BaseParser:
    def __init__(self, args: CmdArgs, uri_type: str):
        self.args = args
        self.uri_type = uri_type
        self.suffix = '.SUFFIX'

    def parse_uri(self, uri: str) -> tuple:
        '''
        进入此处的uri不可能是文件夹
        '''
        name = self.args.name
        if self.uri_type == 'path':
            name = Path(uri).stem
        home_url, base_url = '', ''
        if uri.startswith('http://') or uri.startswith('https://') or uri.startswith('ftp://'):
            uris = uri.split('?', maxsplit=1)
            if name == '':
                name = uris[0][::-1].split('/', maxsplit=1)[0][::-1]
            if name.endswith(self.suffix):
                name = name[:-len(self.suffix)]
            home_url = '/'.join(uris[0].split('/', maxsplit=3)[:-1])
            base_url = uris[0][::-1].split('/', maxsplit=1)[-1][::-1]
        elif Path(uri).exists():
            if name == '':
                name = Path(uri).stem
        if base_url == '' and self.args.base_url != '':
            base_url = self.args.base_url
            home_url = '/'.join(base_url.split('/', maxsplit=3)[:-1])
        return name, home_url, base_url