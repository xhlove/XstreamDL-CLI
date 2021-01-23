import click
from typing import List
from .segment import Segment
from ..extractors.hls.ext.xkey import XKey
from ..extractors.hls.ext.xmedia import XMedia


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
    def __init__(self, name: str, stream_type: str):
        self.name = name
        self.segments = [] # type: List[Segment]
        self.duration = 0.0
        self.file_size = 0
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

    def set_name(self, name: str):
        self.name = name
        return self

    def set_tag(self, tag: str):
        self.tag = tag

    def calc(self):
        self.calc_duration()
        self.calc_file_size()

    def calc_duration(self):
        for segment in self.segments:
            self.duration += segment.duration

    def calc_file_size(self):
        for segment in self.segments:
            self.file_size += segment.file_size
        self.file_size = self.file_size / 1024 / 1024

    def read_stream_header(self):
        '''
        读取一部分数据 获取流的信息
        '''
        pass

    def dump_segments(self):
        '''
        将全部分段保存到本地
        '''
        click.secho(
            f'dump {len(self.segments)} segments\n\t'
            f'duration -> {self.duration:.2f}s\n\t'
            f'filesize -> {self.file_size:.2f}MB'
        )

    def append_segment(self):
        '''
        新增一个分段
        '''
        name = f'{len(self.segments):0>4}.ts'
        segment = Segment().set_name(name).set_folder(self.name)
        self.segments.append(segment)

    def set_straem_type(self, stream_type: str):
        self.stream_type = stream_type

    def set_stream_info(self, line: str):
        '''
        #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1470188,SIZE=468254984,FPS=25,RESOLU=1080,CODECS="avc1,mp4a",QUALITY=5,STREAMTYPE="mp4hd3"
        '''
        try:
            for item in line.split(':', maxsplit=1)[-1].split(','):
                kv = item.split('=', maxsplit=1)
                if len(kv) != 2:
                    continue
                if kv[0] == 'PROGRAM-ID':
                    self.program_id = int(kv[1])
                elif kv[0] == 'BANDWIDTH':
                    self.bandwidth = int(kv[1])
                elif kv[0] == 'AVERAGE-BANDWIDTH':
                    self.average_bandwidth = int(kv[1])
                elif kv[0] == 'SIZE':
                    self.size = int(kv[1])
                elif kv[0] == 'FPS':
                    self.fps = int(kv[1])
                elif kv[0] == 'CODECS':
                    self.codecs = kv[1]
                elif kv[0] == 'RESOLU':
                    self.resolution = kv[1]
                elif kv[0] == 'RESOLUTION':
                    self.resolution = kv[1]
                elif kv[0] == 'FRAME-RATE':
                    self.frame_rate = kv[1]
                elif kv[0] == 'VIDEO-RANGE':
                    self.video_range = kv[1]
                elif kv[0] == 'AUDIO':
                    self.audio = kv[1]
                elif kv[0] == 'QUALITY':
                    self.quality = kv[1]
                elif kv[0] == 'STREAMTYPE':
                    self.stream_type = kv[1]
                else:
                    click.secho(f'unsupport attribute <{item}> of tag #EXT-X-STREAM-INF')
        except Exception:
            pass

    def set_url(self, home_url: str, base_url: str, line: str):
        if line.startswith('http://') or line.startswith('https://') or line.startswith('ftp://'):
            self.origin_url = line
        elif line.startswith('/'):
            self.origin_url = f'{home_url}/{line}'
        else:
            self.origin_url = f'{base_url}/{line}'

    def set_key(self, home_url: str, base_url: str, line: str):
        self.xkeys.append(XKey().set_key(home_url, base_url, line))

    def set_media(self, home_url: str, base_url: str, line: str):
        xmedia = XMedia().set_media(home_url, base_url, line)
        # 这里应当处理成 origin_url
        if xmedia.media_uri.startswith('http://') or line.startswith('https://') or line.startswith('ftp://'):
            self.origin_url = xmedia.media_uri
        elif xmedia.media_uri.startswith('/'):
            self.origin_url = f'{home_url}/{xmedia.media_uri}'
        else:
            self.origin_url = f'{base_url}/{xmedia.media_uri}'
        # self.xmedias.append(XMedia().set_media(home_url, base_url, line))