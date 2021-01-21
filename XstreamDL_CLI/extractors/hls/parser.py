import click
from typing import List
from ...util.stream import Stream
from ..base import BaseParser


class Parser(BaseParser):
    def parse(self, uri: str, content: str) -> List[Stream]:
        uris = self.parse_uri(uri)
        if uris is None:
            click.secho(f'parse {uri} failed')
            return []
        name, home_url, base_url = uris
        streams = []
        stream = Stream(name, 'hls')
        lines = [line.strip() for line in content.split('\n')]
        offset = 0
        content_is_master_type = False
        do_not_append_at_end_list_tag = False
        while offset < len(lines):
            segment = stream.segments[-1]
            line = lines[offset]
            if line == '':
                pass
            elif line.startswith('#EXTM3U'):
                stream.set_tag('#EXTM3U')
            elif line.startswith('#EXT-X-VERSION'):
                pass
            elif line.startswith('#EXT-X-ALLOW-CACHE'):
                pass
            elif line.startswith('#EXT-X-MEDIA-SEQUENCE'):
                pass
            elif line.startswith('#EXT-X-TARGETDURATION'):
                pass
            elif line.startswith('#EXT-X-PLAYLIST-TYPE'):
                pass
            elif line.startswith('#EXT-X-DISCONTINUITY'):
                # 此标签后面的分段都认为是一个新的Stream 直到结束或下一个相同标签出现
                # 对于优酷 根据特征字符匹配 移除不需要的Stream 然后将剩余的Stream合并
                streams.append(stream)
                stream = Stream(name, 'hls')
                stream.set_tag('#EXT-X-DISCONTINUITY')
            elif line.startswith('#EXTINF'):
                segment.set_duration(line)
            elif line.startswith('#EXT-X-PRIVINF'):
                segment.set_privinf(line)
            elif line.startswith('#EXT-X-BYTERANGE'):
                segment.set_byterange(line)
            elif line.startswith('#EXT-X-ENDLIST'):
                pass
            elif line.startswith('#EXT-X-STREAM-INF'):
                stream.set_tag('#EXT-X-STREAM-INF')
                stream.set_stream_info(line)
                content_is_master_type = True
            else:
                if offset > 0 and lines[offset - 1].startswith('#EXT-X-BYTERANGE'):
                    segment.set_url(home_url, base_url, line)
                    stream.append_segment()
                elif offset > 0 and lines[offset - 1].startswith('#EXT-X-PRIVINF'):
                    segment.set_url(home_url, base_url, line)
                    stream.append_segment()
                elif offset > 0 and lines[offset - 1].startswith('#EXTINF'):
                    segment.set_url(home_url, base_url, line)
                    stream.append_segment()
                elif offset > 0 and lines[offset - 1].startswith('#EXT-X-STREAM-INF'):
                    stream.set_url(home_url, base_url, line)
                    streams.append(stream)
                    stream = Stream(name, 'hls')
                    do_not_append_at_end_list_tag = True
                else:
                    click.secho(f'unknow what to do here ->\n\t{line}')
            offset += 1
        if do_not_append_at_end_list_tag is False:
            streams.append(stream)
        # 下面的for循环中stream/segment是浅拷贝
        _streams = []
        for stream in streams:
            # 处理掉末尾空的分段
            if stream.segments[-1].url == '':
                _ = stream.segments.pop(-1)
            # 过滤掉广告片段
            _segments = []
            for segment in stream.segments:
                if '/ad/' not in segment.url:
                    _segments.append(segment)
            stream.segments = _segments
            # 保留过滤掉广告片段分段数大于0的Stream
            if len(stream.segments) > 0 or stream.tag == '#EXT-X-STREAM-INF':
                _streams.append(stream)
        if content_is_master_type is False and len(_streams) > 0:
            # 合并去除#EXT-X-DISCONTINUITY后剩下的Stream
            stream = _streams[0]
            for _stream in _streams[1:]:
                stream.segments.extend(_stream.segments)
            _streams = [stream]
        return _streams