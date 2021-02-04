import os
import json
import click
import base64
from typing import List
from pathlib import Path
from datetime import datetime
from .concat import Concat
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
        self.xkey = None # type: XKey
        self.bakcup_xkey = None # type: XKey
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
        self.calc()
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
        if self.xkey is not None:
            key = base64.b64encode(self.xkey.key).decode('utf-8')
            iv = self.xkey.iv
        else:
            key = ''
            iv = '0' * 32
        info = {
            'name': self.name,
            'path': self.save_dir,
            'creatTime': f'{datetime.now()}',
            'xkey': {
                'key': key,
                'iv': iv,
            },
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

    def try_fetch_key(self, custom_key: str, custom_iv: str):
        '''
        在解析过程中 已经设置了key的信息了
        但是没有请求key 这里是独立加载key的部分
        放在这个位置的原因是
            - 解析过程其实很短，没必要在解析时操作
            - 解析后还有合并流的过程
        所以最佳的方案是在解析之后再进行key的加载
        '''
        custom_xkey = XKey()
        if custom_key is not None:
            _key = base64.b64decode(custom_key.encode('utf-8'))
            custom_xkey.set_key(_key)
            if custom_iv is not None:
                custom_xkey.set_iv(custom_iv)
        if self.xkey is None:
            if custom_key:
                # 如果解析后没有密钥相关信息
                # 而命令行又指定了 也进行设定
                self.set_segments_key(custom_xkey)
            return
        if self.xkey.load(custom_xkey) is True:
            self.set_segments_key(self.xkey)

    def set_segments_key(self, xkey: XKey):
        '''
        和每个分段的key对比 设定对应的解密信息
        '''
        self.xkey = xkey
        for segment in self.segments:
            segment.xkey = xkey

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
        xkey = XKey().set_attrs_from_line(home_url, base_url, line)
        if xkey is None:
            return
        if self.xkey is None:
            self.xkey = xkey
        else:
            self.bakcup_xkey = xkey

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

    def concat(self):
        out = Path(self.save_dir).with_suffix('.mp4')
        if out.exists() is True:
            click.secho(f'尝试合并 {self.name} 但是已经存在合并文件')
            return
        names = []
        for segment in self.segments:
            segment_path = Path(self.save_dir) / segment.name
            if segment_path.exists() is False:
                continue
            names.append(segment.name)
        if len(names) != len(self.segments):
            click.secho(f'尝试合并 {self.name} 但是未下载完成')
            return
        cmd = Concat.gen_cmd(out.resolve().as_posix(), names)
        ori_path = os.getcwd()
        os.chdir(self.save_dir)
        os.system(cmd)
        os.chdir(ori_path)