import os
import json
import click
from typing import List
from pathlib import Path
from datetime import datetime
from .key import StreamKey
from ..util.concat import Concat
from .segment import Segment


class Stream:
    '''
    自适应流具体实现的父类
    每一条流应当具有以下基本属性：
        - 名称
        - 分段链接列表
        - 分辨率
        - 码率
        - 时长
        - 编码
        - 语言
    具有以下函数
        - 扩展分段 某些情况下需要合并两或多条流
        - 计算全部分段时长和大小
        - 显示流信息 总时长和大小
        - 从第一个分段读取流信息
        - 保存流相关信息至本地
        - 增加分段
        - 增加密钥信息
        - 合并 一般在下载完成之后
    '''
    def __init__(self, index: int, name: str, home_url: str, base_url: str, save_dir: str):
        self.index = index
        self.name = name
        self.home_url = home_url
        self.base_url = base_url
        self.save_dir = Path(save_dir) / name
        self.segments = [] # type: List[Segment]
        self.duration = 0.0
        self.filesize = 0
        self.lang = ''
        self.bandwidth = None # type: int
        self.fps = None # type: int
        self.resolution = None # type: str
        self.codecs = None # type: str
        self.streamkeys = [] # type: List[StreamKey]
        # 初始化默认设定流类型
        self.stream_type = None # type: str
        self.suffix = '.mp4'

    def segments_extend(self, segments: List[Segment]):
        ''' 某些情况下对流进行合并 需要更新一下新增分段的文件名 '''
        offset = len(self.segments)
        for segment in segments:
            segment.add_offset_for_name(offset)
        self.segments.extend(segments)

    def calc(self):
        for segment in self.segments:
            self.duration += segment.duration
            self.filesize += segment.filesize
        self.filesize = self.filesize / 1024 / 1024

    def show_info(self, index: int):
        ''' 显示信息 '''
        self.calc()
        click.secho(
            f'{index:>3} {self.name} 共计{len(self.segments)}个分段 '
            f'{self.duration:.2f}s {self.filesize:.2f}MiB '
        )

    def read_stream_header(self):
        ''' 读取一部分数据 获取流的信息 '''
        pass

    def dump_segments(self):
        ''' 保存分段信息 '''
        if self.save_dir.exists() is False:
            self.save_dir.mkdir()
        keys = []
        if len(self.streamkeys) > 0:
            for streamkey in self.streamkeys:
                keys.append(streamkey.dump())
        info = {
            'name': self.name,
            'path': self.save_dir.resolve().as_posix(),
            'creatTime': f'{datetime.now()}',
            'key': keys,
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
        (self.save_dir / 'raw.json').write_text(data, encoding='utf-8')

    def append_segment(self):
        ''' 新增分段 '''
        pass

    def append_key(self, streamkey: StreamKey):
        ''' 新增key '''
        self.streamkeys.append(streamkey)

    def fix_url(self, url: str) -> str:
        if url.startswith('http://') or url.startswith('https://') or url.startswith('ftp://'):
            return url
        elif url.startswith('/'):
            return f'{self.home_url}{url}'
        else:
            return f'{self.base_url}/{url}'

    def concat(self):
        ''' 合并视频 '''
        out = self.save_dir.with_suffix(self.suffix)
        if out.exists() is True:
            click.secho(f'尝试合并 {self.name} 但是已经存在合并文件')
            return True
        names = []
        for segment in self.segments:
            segment_path = self.save_dir / segment.name
            if segment_path.exists() is False:
                continue
            names.append(segment.name)
        if len(names) != len(self.segments):
            click.secho(f'尝试合并 {self.name} 但是未下载完成')
            return False
        cmd = Concat.gen_cmd(out.resolve().as_posix(), names)
        ori_path = os.getcwd()
        os.chdir(self.save_dir.resolve().as_posix())
        os.system(cmd)
        os.chdir(ori_path)
        return True