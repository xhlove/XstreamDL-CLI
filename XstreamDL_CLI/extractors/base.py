from pathlib import Path


class BaseParser:
    def parse_uri(self, uri: str) -> tuple:
        if uri == '':
            return '', ''
        elif uri.startswith('http://') or uri.startswith('https://') or uri.startswith('ftp://'):
            uris = uri.split('?', maxsplit=1)
            name = uris[0][::-1].split('/', maxsplit=1)[0][::-1]
            if name.endswith('.m3u8'):
                name = name[:-5]
            home_url = '/'.join(uris[0].split('/', maxsplit=3)[:-1])
            base_url = uris[0][::-1].split('/', maxsplit=1)[-1][::-1]
            return name, home_url, base_url
        elif Path(uri).exists():
            return Path(uri).stem, '', ''