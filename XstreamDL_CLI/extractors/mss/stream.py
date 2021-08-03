import re
from typing import List
from XstreamDL_CLI.models.stream import Stream
from .segment import MSSSegment


class MSSStream(Stream):
    def __init__(self, index: int, name: str, home_url: str, base_url: str, save_dir: str):
        super(MSSStream, self).__init__(index, name, home_url, base_url, save_dir)
        self.timescale = 10000000
        self.channels = 2
        self.bits_per_sample = 16
        self.sampling_rate = 16
        self.codec_private_data = None # type: str
        self.nal_unit_length_field = 4
        self.segments = [] # type: List[MSSSegment]
        self.suffix = '.mp4'
        self.has_init_segment = False
        self.skey = '' # type: str
        self.append_segment()

    def get_name(self):
        if self.stream_type != '':
            base_name = f'{self.name}_{self.stream_type}'
        else:
            base_name = self.name
        if self.codecs is not None:
            base_name += f'_{self.codecs}'
        if self.stream_type == 'text' and self.lang != '':
            base_name += f'_{self.lang}'
        elif self.stream_type == 'video' and self.resolution != '':
            base_name += f'_{self.resolution}'
        elif self.stream_type == 'audio' and self.lang != '':
            base_name += f'_{self.lang}'
        if self.stream_type in ['audio', 'video'] and self.bandwidth is not None:
            base_name += f'_{self.bandwidth / 1000:.2f}kbps'
        return base_name

    def get_ism_params(self):
        height_width = self.resolution.split('x')
        if len(height_width) == 2:
            height, width = height_width
        else:
            height, width = 0, 0
        return {
            'fourcc': self.codecs,
            'duration': int(self.duration),
            'timescale': self.timescale,
            'language': 'und' if self.lang == '' else self.lang,
            'height': int(height),
            'width': int(width),
            'stream_type': self.stream_type,
            'channels': self.channels,
            'bits_per_sample': self.bits_per_sample,
            'sampling_rate': self.sampling_rate,
            'codec_private_data': self.codec_private_data,
            'nal_unit_length_field': self.nal_unit_length_field,
        }

    def append_segment(self):
        index = len(self.segments)
        if self.has_init_segment:
            index -= 1
        segment = MSSSegment().set_index(index).set_folder(self.save_dir)
        self.segments.append(segment)

    def update(self, stream: 'MSSStream'):
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

    def set_subtitle_url(self, url: str):
        self.has_init_segment = True
        self.segments[-1].set_subtitle_url(self.fix_url(url))
        # self.append_segment()

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
            segment.set_duration(duration)

    def set_protection_flag(self, flag: bool):
        for segment in self.segments:
            segment.set_protection_flag(flag)

    def set_lang(self, lang: str):
        if lang is None:
            return
        self.lang = lang

    def set_bandwidth(self, bandwidth: int):
        self.bandwidth = bandwidth

    def set_codecs(self, codecs: str):
        if re.match('avc(1|3)*', codecs.lower()):
            codecs = 'H264'
        if re.match('(hev|hvc)1*', codecs.lower()):
            codecs = 'H265'
        if re.match('vp(09|9)*', codecs.lower()):
            codecs = 'VP9'
        if codecs != 'AACL' and re.match('aac*', codecs.lower()):
            codecs = 'AAC'
        if codecs.lower() in ['wvtt', 'ttml']:
            codecs = codecs.upper()
        self.codecs = codecs

    def set_resolution(self, width: str, height: str):
        if width is None or height is None:
            return
        self.resolution = f'{width}x{height}'

    def set_stream_type(self, stream_type: str):
        if stream_type is None:
            return
        self.stream_type = stream_type

    def set_timescale(self, timescale: int):
        if timescale is None:
            return
        self.timescale = timescale

    def set_bits_per_sample(self, bits_per_sample: str):
        if bits_per_sample is None:
            return
        self.bits_per_sample = bits_per_sample

    def set_sampling_rate(self, sampling_rate: str):
        if sampling_rate is None:
            return
        self.sampling_rate = sampling_rate

    def set_channels(self, channels: str):
        if channels is None:
            return
        self.channels = channels

    def set_codec_private_data(self, codec_private_data: str):
        if codec_private_data is None:
            return
        self.codec_private_data = codec_private_data

    def set_nal_unit_length_field(self, nal_unit_length_field: int):
        if nal_unit_length_field is None:
            return
        self.nal_unit_length_field = nal_unit_length_field