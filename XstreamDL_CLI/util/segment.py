import re
import click
from typing import List
from pathlib import Path
from ..extractors.hls.ext.xkey import XKey
from ..extractors.hls.ext.xprivinf import XPrivinf


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
        self.index = 0
        self.suffix = '.ts'
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
        self.filesize = 0
        self.duration = 0.0
        self.byterange = [] # type: list
        # <---临时存放二进制内容--->
        self.content = [] # type: List[bytes]
        # <---分段临时下载文件夹--->
        self.folder = None # type: Path
        # 加密信息
        self.xkeys = [] # type: List[XKey]
        self.__xprivinf = None # type: XPrivinf
        # 分段类型 map or 常规
        self.segment_type = 'normal'
        self.has_set_key = False

    def is_encrypt(self):
        if self.__xprivinf is not None:
            return self.__xprivinf.drm_notencrypt
        elif len(self.xkeys) > 0:
            return True
        else:
            return False

    def add_offset_for_name(self, offset: int):
        self.index += offset
        self.name = f'{self.index:0>4}{self.suffix}'

    def set_index(self, index: str):
        self.index = index
        self.name = f'{self.index:0>4}{self.suffix}'
        return self

    def set_suffix(self, suffix: str):
        self.suffix = suffix
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
        对于分段来说 标签的属性值 应该归属在标签下面 计算时需要注意
        不过也可以在解析标签信息之后 进行赋值处理 这样便于调用
        '''
        self.__xprivinf = XPrivinf().set_attrs_from_line(line)
        if self.__xprivinf.filesize is not None:
            self.filesize = self.__xprivinf.filesize

    def set_url(self, home_url: str, base_url: str, line: str):
        if line.startswith('http://') or line.startswith('https://') or line.startswith('ftp://'):
            self.url = line
        elif line.startswith('/'):
            self.url = f'{home_url}/{line}'
        else:
            self.url = f'{base_url}/{line}'

    def set_map_url(self, home_url: str, base_url: str, line: str):
        map_uri = re.match('#EXT-X-MAP:URI="(.*?)"', line.strip())
        if map_uri is None:
            click.secho('find #EXT-X-MAP tag, however has no uri')
            return
        map_uri = map_uri.group(1)
        if map_uri.startswith('http://') or map_uri.startswith('https://') or map_uri.startswith('ftp://'):
            self.url = map_uri
        elif map_uri.startswith('/'):
            self.url = f'{home_url}/{map_uri}'
        else:
            self.url = f'{base_url}/{map_uri}'
        self.segment_type = 'map'
        if self.index > 0:
            self.name = f'map{self.index}.mp4'
        else:
            self.name = 'map.mp4'

    def get_path(self) -> str:
        return (self.folder / self.name).resolve().as_posix()

    def set_key(self, home_url: str, base_url: str, line: str):
        self.has_set_key = True
        self.xkeys.append(XKey().set_attrs_from_line(home_url, base_url, line))

    def get_xkeys(self):
        return self.xkeys

    def set_xkeys(self, last_segment_has_xkeys: bool, xkeys: List[XKey]):
        '''
        如果已经因为#EXT-X-KEY而设置过xkeys了
        那就不使用之前分段的xkeys了
        '''
        if last_segment_has_xkeys is False:
            return
        if self.has_set_key is True:
            return
        if xkeys is None:
            return
        self.xkeys = xkeys