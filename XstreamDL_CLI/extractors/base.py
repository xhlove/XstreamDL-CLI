from pathlib import Path
from argparse import Namespace


class BaseParser:

    def __init__(self, args: Namespace):
        self.args = args
        self.save_dir = Path(args.save_dir)

    def parse_uri(self, uri: str) -> tuple:
        name = self.args.name
        home_url, base_url = '', ''
        if uri.startswith('http://') or uri.startswith('https://') or uri.startswith('ftp://'):
            uris = uri.split('?', maxsplit=1)
            if name == '':
                name = uris[0][::-1].split('/', maxsplit=1)[0][::-1]
            if name.endswith('.m3u8'):
                name = name[:-5]
            home_url = '/'.join(uris[0].split('/', maxsplit=3)[:-1])
            base_url = uris[0][::-1].split('/', maxsplit=1)[-1][::-1]
        elif Path(uri).exists():
            if name == '':
                name = Path(uri).stem
        if self.args.base_url != '':
            base_url = self.args.base_url
            home_url = '/'.join(base_url.split('/', maxsplit=3)[:-1])
        return name, home_url, base_url