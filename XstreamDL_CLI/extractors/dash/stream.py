import re
from typing import List, Union
from XstreamDL_CLI.models.stream import Stream
from XstreamDL_CLI.util.maps.codecs import AUDIO_CODECS
from .segment import DASHSegment


class DASHStream(Stream):
    def __init__(self, index: int, name: str, home_url: str, base_url: str, save_dir: str):
        super(DASHStream, self).__init__(index, name, home_url, base_url, save_dir)
        self.segments = [] # type: List[DASHSegment]
        self.suffix = '.mp4'
        self.has_init_segment = False
        self.skey = None # type: str
        self.append_segment()

    def get_name(self):
        base_name = f'{self.name}_{self.stream_type}'
        base_name += f'_{self.codecs}'
        if self.stream_type == 'subtitle' and self.lang != '':
            base_name += f'_{self.lang}'
        elif self.stream_type == 'video' and self.resolution != '':
            base_name += f'_{self.resolution}'
        elif self.stream_type == 'audio' and self.lang != '':
            base_name += f'_{self.lang}'
        return base_name

    def append_segment(self):
        index = len(self.segments)
        if self.has_init_segment:
            index -= 1
        segment = DASHSegment().set_index(index).set_folder(self.save_dir)
        self.segments.append(segment)

    def update(self, stream: 'DASHStream'):
        '''
        Representation id相同可以合并
        这个时候应该重新计算时长和码率
        '''
        total_duration = self.duration + stream.duration
        if total_duration > 0:
            self.bandwidth = (stream.duration * stream.bandwidth + self.duration * self.bandwidth) / (self.duration + stream.duration)
        self.duration += stream.duration
        for segment in stream.segments:
            # 被合并的流的init分段 避免索引计算错误
            if segment.segment_type == 'init':
                stream.segments.remove(segment)
                break
        self.segments_extend(stream.segments)

    def set_init_url(self, url: str):
        self.has_init_segment = True
        self.segments[-1].set_init_url(self.fix_url(url))
        self.append_segment()

    def set_media_url(self, url: str):
        self.segments[-1].set_media_url(self.fix_url(url))
        self.append_segment()

    def set_segment_duration(self, duration: float):
        self.segments[-1].set_duration(duration)

    def set_segments_duration(self, duration: float):
        '''' init分段没有时长 这里只用设置普通分段的 '''
        for segment in self.segments:
            if segment.segment_type == 'init':
                continue
            segment.set_duration(duration)

    def set_skey(self, aid: str, rid: str):
        self.skey = f'{aid}_{rid}'

    def set_lang(self, lang: str):
        if lang is None:
            return
        self.lang = lang

    def set_bandwidth(self, bandwidth: Union[str, int]):
        if bandwidth is None:
            return
        if isinstance(bandwidth, str):
            bandwidth = int(bandwidth)
        self.bandwidth = bandwidth

    def set_codecs(self, codecs: str):
        if codecs is None:
            return
        # https://chromium.googlesource.com/chromium/src/media/+/master/base/mime_util_internal.cc
        if re.match('avc(1|3)*', codecs):
            codecs = 'H264'
        if re.match('(hev|hvc)1*', codecs):
            codecs = 'H265'
        if re.match('vp(09|9)*', codecs):
            codecs = 'VP9'
        if codecs in ['wvtt', 'ttml']:
            codecs = codecs.upper()
        if AUDIO_CODECS.get(codecs) is not None:
            if 'AAC' in AUDIO_CODECS[codecs]:
                codecs = 'AAC'
            else:
                codecs = AUDIO_CODECS[codecs]
        self.codecs = codecs

    def set_resolution(self, width: str, height: str):
        if width is None or height is None:
            return
        self.resolution = f'{width}x{height}'

    def set_stream_type(self, stream_type: str):
        if stream_type is None:
            return
        stream_type, stream_suffix = stream_type.split('/')
        if stream_suffix == 'ttml+xml':
            stream_type = 'subtitle'
        elif stream_type == 'application':
            if self.codecs.lower() in ['wvtt', 'ttml']:
                stream_type = 'subtitle'
            else:
                return
        self.stream_type = stream_type