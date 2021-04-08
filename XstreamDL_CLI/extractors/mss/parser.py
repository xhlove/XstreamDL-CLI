from typing import List
from .ism import ISM
from .childs.c import c as Cc
from .childs.streamindex import StreamIndex
from .childs.qualitylevel import QualityLevel
from .handler import xml_handler

from .stream import MSSStream
from ..base import BaseParser
from XstreamDL_CLI.cmdargs import CmdArgs


class MSSParser(BaseParser):
    def __init__(self, args: CmdArgs, uri_type: str):
        super(MSSParser, self).__init__(args, uri_type)
        self.suffix = '.ism'

    def init_stream(self, sindex: int, uris: list) -> MSSStream:
        name, home_url, base_url = uris
        return MSSStream(sindex, name, home_url, base_url, self.args.save_dir)

    def parse(self, uri: str, content: str) -> List[MSSStream]:
        uris = self.parse_uri(uri)
        assert uris is not None, f'parse {uri} failed'
        name, home_url, base_url = uris
        # 解析转换内容为期望的对象
        ism = xml_handler(content)
        return self.walk_streamindex(ism, uris)

    def walk_streamindex(self, ism: ISM, uris: list) -> List[MSSStream]:
        streamindexs = ism.find('StreamIndex') # type: List[StreamIndex]
        assert len(streamindexs) > 0, 'there is no StreamIndex'
        # 遍历处理streamindexs
        streams = [] # type: List[MSSStream]
        for streamindex in streamindexs:
            streams.extend(self.walk_qualitylevel(streamindex, len(streams), uris))
        # 处理空分段
        for stream in streams:
            if stream.segments[-1].url == '':
                _ = stream.segments.pop(-1)
        return streams

    def walk_qualitylevel(self, streamindex: StreamIndex, sindex: int, uris: list) -> List[MSSStream]:
        streams = [] # type: List[MSSStream]
        qualitylevels = streamindex.find('QualityLevel') # type: List[QualityLevel]
        if len(qualitylevels) == 0:
            return streams
        for qualitylevel in qualitylevels:
            stream = self.init_stream(sindex + len(streams), uris)
            streams.extend(self.walk_c(qualitylevel, streamindex, stream))
        return streams

    def walk_c(self, qualitylevel: QualityLevel, streamindex: StreamIndex, stream: MSSStream) -> List[MSSStream]:
        cs = streamindex.find('c') # type: List[Cc]
        if len(cs) == 0:
            return []
        # 设置基本信息
        stream.set_stream_type(streamindex.Type)
        stream.set_codecs(qualitylevel.FourCC)
        stream.set_bandwidth(qualitylevel.Bitrate)
        stream.set_lang(streamindex.Language)
        stream.set_resolution(qualitylevel.MaxWidth, qualitylevel.MaxHeight)
        last_end_time = None # type: int
        for c in cs:
            media_url = streamindex.get_media_url()
            if last_end_time is None and c.t is not None:
                last_end_time = c.t
            if '{bitrate}' in media_url:
                media_url = media_url.replace('{bitrate}', str(qualitylevel.Bitrate))
            if '{start time}' in media_url:
                media_url = media_url.replace('{start time}', str(last_end_time))
            duration = c.d / streamindex.TimeScale
            stream.set_segment_duration(duration)
            stream.set_media_url(media_url)
            last_end_time += c.d
        return [stream]