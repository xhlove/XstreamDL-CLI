import json
import click
from typing import List
from pathlib import Path
from datetime import datetime
from .segment import Segment
from ..extractors.hls.ext.xkey import XKey
from ..extractors.hls.ext.xmedia import XMedia
from ..extractors.hls.ext.xdaterange import XDateRange
from ..extractors.hls.ext.xstream_inf import XStreamInf
from ..extractors.hls.ext.xprogram_date_time import XProgramDateTime


class Stream:
    '''
    自适应流的具体实现，HLS/DASH等，为了下载对应的流，
    每一条流应当具有以下基本属性：
    - 名称
    - 分段链接列表
    - 分辨率
    - 码率
    - 时长
    - 编码
    一些可选的属性
    - 语言
    '''
    def __init__(self, name: str, save_dir: Path, stream_type: str):
        self.name = name
        self.save_dir = (save_dir / name).resolve().as_posix()
        self.segments = [] # type: List[Segment]
        self.duration = 0.0
        self.filesize = 0
        self.lang = ''
        # <---解析过程中需要设置的属性--->
        self.program_id = None # type: int
        self.bandwidth = None # type: int
        self.average_bandwidth = None # type: int
        self.size = None # type: int
        self.fps = None # type: int
        self.resolution = None # type: str
        self.codecs = None # type: str
        self.quality = None # type: str
        self.stream_type = None # type: str
        self.xkeys = [] # type: List[XKey]
        self.xmedias = [] # type: List[XMedia]
        # 初始化默认设定流类型
        self.set_straem_type(stream_type)
        # 初始化默认设定一个分段
        self.append_segment()

    def segments_extend(self, segments: List[Segment]):
        '''
        由#EXT-X-DISCONTINUITY引起的合并 需要更新一下新增分段的文件名
        '''
        offset = len(self.segments)
        for segment in segments:
            segment.add_offset_for_name(offset)
        self.segments.extend(segments)

    def set_name(self, name: str):
        self.name = name
        return self

    def set_tag(self, tag: str):
        self.tag = tag

    def calc(self):
        self.calc_duration()
        self.calc_filesize()

    def calc_duration(self):
        for segment in self.segments:
            self.duration += segment.duration

    def calc_filesize(self):
        for segment in self.segments:
            self.filesize += segment.filesize
        self.filesize = self.filesize / 1024 / 1024

    def read_stream_header(self):
        '''
        读取一部分数据 获取流的信息
        '''
        pass

    def show_info(self, index: int):
        '''
        显示信息 让用户选择下载哪些Stream
        '''
        click.secho(
            f'{index:>3} {self.name} 共计{len(self.segments)}个分段 '
            f'{self.duration:.2f}s {self.filesize:.2f}MB '
        )
        self.dump_segments()

    def dump_segments(self):
        '''
        将全部分段保存到本地
        '''
        # click.secho(
        #     f'dump {len(self.segments)} segments\n\t'
        #     f'duration -> {self.duration:.2f}s\n\t'
        #     f'filesize -> {self.filesize:.2f}MB'
        # )
        info = {
            'name': self.name,
            'path': self.save_dir,
            'creatTime': f'{datetime.now()}',
            'segments': [],
        }
        for segment in self.segments:
            info['segments'].append(
                {
                    'url': segment.url,
                    'size': segment.filesize,
                }
            )
        data = json.dumps(info, ensure_ascii=False, indent=4)
        Path(self.save_dir, 'raw.json').write_text(data, encoding='utf-8')

    def append_segment(self):
        '''
        新增一个分段
        '''
        segment = Segment().set_index(len(self.segments)).set_suffix('.ts').set_folder(self.save_dir)
        self.segments.append(segment)

    def try_fetch_key(self):
        '''
        在解析过程中 已经设置了key的信息了
        但是没有请求key 这里是独立加载key的部分
        放在这个位置的原因是
            - 解析过程其实很短，没必要在解析时操作
            - 解析后还有合并流的过程
        所以最佳的方案是在解析之后再进行key的加载
        '''
        if len(self.xkeys) == 0:
            return
        for xkey in self.xkeys:
            if xkey.load() is False:
                continue
            self.set_segments_key(xkey)

    def set_segments_key(self, xkey: XKey):
        '''
        和每个分段的key对比 设定对应的解密信息
        '''
        pass

    def set_straem_type(self, stream_type: str):
        self.stream_type = stream_type

    def set_xstream_inf(self, line: str):
        self.xstream_inf = XStreamInf().set_attrs_from_line(line)

    def set_url(self, home_url: str, base_url: str, line: str):
        if line.startswith('http://') or line.startswith('https://') or line.startswith('ftp://'):
            self.origin_url = line
        elif line.startswith('/'):
            self.origin_url = f'{home_url}/{line}'
        else:
            self.origin_url = f'{base_url}/{line}'

    def set_key(self, home_url: str, base_url: str, line: str):
        self.xkeys.append(XKey().set_attrs_from_line(home_url, base_url, line))

    def set_media(self, home_url: str, base_url: str, line: str):
        self.xmedia = XMedia().set_attrs_from_line(line)
        self.xmedia.uri = self.set_origin_url(home_url, base_url, self.xmedia.uri)

    def set_origin_url(self, home_url: str, base_url: str, uri: str):
        # 某些标签 应该被视作一个新的Stream 所以要设置其对应的原始链接
        if uri.startswith('http://') or uri.startswith('https://') or uri.startswith('ftp://'):
            self.origin_url = uri
        elif uri.startswith('/'):
            self.origin_url = f'{home_url}/{uri}'
        else:
            self.origin_url = f'{base_url}/{uri}'
        return self.origin_url

    def set_daterange(self, line: str):
        self.xdaterange = XDateRange().set_attrs_from_line(line)

    def set_xprogram_date_time(self, line: str):
        self.xprogram_date_time = XProgramDateTime().set_attrs_from_line(line)