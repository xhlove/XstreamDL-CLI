import os
import json
import click
import shutil
from typing import List
from pathlib import Path
from datetime import datetime
from .key import StreamKey
from ..util.concat import Concat
from .segment import Segment
from XstreamDL_CLI.cmdargs import CmdArgs
from XstreamDL_CLI.util.texts import Texts

t_msg = Texts()


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
        self.base_url = base_url[:-1] if base_url.endswith('/') else base_url
        self.save_dir = Path(save_dir) / name
        self.segments = [] # type: List[Segment]
        self.duration = 0.0
        self.filesize = 0
        self.lang = ''
        self.bandwidth = None # type: int
        self.fps = None # type: int
        self.resolution = '' # type: str
        self.codecs = None # type: str
        self.streamkeys = [] # type: List[StreamKey]
        # 初始化默认设定流类型
        self.stream_type = '' # type: str
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

    def get_name(self):
        return self.name

    def show_info(self, index: int):
        ''' 显示信息 '''
        self.calc()
        if self.filesize > 0:
            click.secho(
                f'{index:>3} {t_msg.total_segments_info_1} {len(self.segments):>4} {t_msg.total_segments_info_2} '
                f'{self.duration:>7.2f}s {self.filesize:.2f}MiB {self.get_name()}'
            )
        else:
            click.secho(
                f'{index:>3} {t_msg.total_segments_info_1} {len(self.segments):>4} {t_msg.total_segments_info_2} '
                f'{self.duration:>7.2f}s {self.get_name()}'
            )

    def read_stream_header(self):
        ''' 读取一部分数据 获取流的信息 '''
        pass

    def show_segments(self):
        for segment in self.segments:
            click.secho(segment.url)

    def dump_segments(self):
        ''' 保存分段信息 '''
        self.save_dir = self.save_dir.parent / self.get_name()
        if self.save_dir.exists() is False:
            self.save_dir.mkdir()
        keys = []
        if len(self.streamkeys) > 0:
            for streamkey in self.streamkeys:
                keys.append(streamkey.dump())
        info = {
            'name': self.get_name(),
            'path': self.save_dir.resolve().as_posix(),
            'creatTime': f'{datetime.now()}',
            'key': keys,
            'segments': [],
        }
        for segment in self.segments:
            segment.folder = self.save_dir
            info['segments'].append(
                {
                    'url': segment.url,
                    'size': segment.filesize,
                    'byterange': segment.byterange,
                    'name': segment.name,
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
        elif url.startswith('../'):
            fixed_base_url = '/'.join(self.base_url.split("/")[:-1])
            return f'{fixed_base_url}{url[2:]}'
        else:
            return f'{self.base_url}/{url}'

    def fix_base_url(self, url: str) -> str:
        if url.startswith('http://') or url.startswith('https://') or url.startswith('ftp://'):
            self.base_url = url
        elif url.startswith('/'):
            self.base_url = f'{self.home_url}{url}'
        else:
            self.base_url = f'{self.base_url}/{url}'

    def concat(self, args: CmdArgs):
        ''' 合并视频 '''
        out = Path(self.save_dir.absolute().as_posix() + self.suffix)
        if args.overwrite is False and out.exists() is True:
            click.secho(f'{t_msg.try_to_concat} {self.get_name()} {t_msg.cancel_concat_reason_1}')
            return True
        names = []
        for segment in self.segments:
            segment_path = self.save_dir / segment.name
            if segment_path.exists() is False:
                continue
            names.append(segment.name)
        if len(names) != len(self.segments):
            click.secho(f'{t_msg.try_to_concat} {self.get_name()} {t_msg.cancel_concat_reason_2}')
            return False
        if hasattr(self, "xkey") and self.xkey is not None and self.xkey.method.upper() == "SAMPLE-AES":
            click.secho(t_msg.force_use_raw_concat_for_sample_aes)
            args.raw_concat = True
        ori_path = os.getcwd()
        # 需要在切换目录前获取
        os.chdir(self.save_dir.absolute().as_posix())
        cmds, _outs = Concat.gen_cmds_outs(out, names, args)
        for cmd in cmds:
            os.system(cmd)
        # 执行完合并命令后即刻返回原目录
        os.chdir(ori_path)
        # 合并成功则根据设定删除临时文件
        if out.exists():
            click.secho(f'{out.as_posix()} was merged successfully')
            if args.enable_auto_delete:
                shutil.rmtree(self.save_dir.absolute().as_posix())
                click.secho(f'{self.save_dir.absolute().as_posix()} was deleted')
        # 针对DASH流 如果有key 那么就解密 注意 HLS是边下边解密
        # 加密文件合并输出和临时文件夹同一级 所以前面的删除动作并不影响进一步解密
        if args.key is not None:
            Concat.call_mp4decrypt(out, args)
        if args.enable_auto_delete and self.save_dir.exists():
            shutil.rmtree(self.save_dir.absolute().as_posix())
        return True