import click
from typing import List
from pathlib import Path


class Segment:
    '''
    每一个分段应当具有以下基本属性：
    - 名称
    - 链接
    - Range
    - User-Agent
    '''
    def __init__(self):
        self.name = ''
        self.url = ''
        self.range = ''
        self.user_agent = ''
        self.headers = {
            'user-agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/87.0.4280.141 Safari/537.36'
            )
        }
        self.file_size = 0
        self.duration = 0.0
        self.byterange = [] # type: list
        # <---临时存放二进制内容--->
        self.content = [] # type: List[bytes]
        # <---分段临时下载文件夹--->
        self.folder = None # type: Path

    def set_name(self, name: str):
        self.name = name
        return self

    def set_folder(self, name: str):
        self.folder = Path(name)
        if self.folder.exists() is False:
            self.folder.mkdir()
        return self

    def set_duration(self, line: str):
        try:
            self.duration = float(line.split(':', maxsplit=1)[-1].strip(','))
        except Exception:
            pass

    def set_byterange(self, line: str):
        try:
            _ = line.split(':', maxsplit=1)[-1].split('@')
            total, offset = int(_[0]), int(_[1])
            self.byterange = [total, offset]
        except Exception:
            pass

    def set_privinf(self, line: str):
        '''
        #EXT-X-PRIVINF:FILESIZE=720416,DRM_NOTENCRYPT
        '''
        try:
            for item in line.split(':', maxsplit=1)[-1].split(','):
                kv = item.split('=', maxsplit=1)
                if kv[0] == 'DRM_NOTENCRYPT':
                    self.youku_drm_not_encrypt = True
                if len(kv) != 2:
                    continue
                if kv[0] == 'FILESIZE':
                    self.file_size = int(kv[1])
                else:
                    click.secho(f'unsupport attribute <{item}> of tag #EXT-X-PRIVINF')
        except Exception:
            pass

    def set_url(self, home_url: str, base_url: str, line: str):
        if line.startswith('http://') or line.startswith('https://') or line.startswith('ftp://'):
            self.url = line
        elif line.startswith('/'):
            self.url = f'{home_url}/{line}'
        else:
            self.url = f'{base_url}/{line}'

    def get_path(self) -> str:
        return (self.folder / self.name).resolve().as_posix()