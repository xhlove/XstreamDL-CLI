import click
from typing import List
from pathlib import Path

from .mpd import MPD
from .links import Links
from .funcs import tree, dump
from .handler import xml_handler

from .childs.adaptationset import AdaptationSet
from .childs.baseurl import BaseURL
from .childs.contentprotection import ContentProtection
from .childs.period import Period
from .childs.representation import Representation
from .childs.s import S
from .childs.segmenttemplate import SegmentTemplate
from .childs.segmenttimeline import SegmentTimeline

from .stream import DASHStream
from ..base import BaseParser
from .key import DASHKey
from XstreamDL_CLI.cmdargs import CmdArgs


class DASHParser(BaseParser):
    def __init__(self, args: CmdArgs, uri_type: str):
        super(DASHParser, self).__init__(args, uri_type)
        self.suffix = '.mpd'

    def parse(self, uri: str, content: str) -> List[DASHStream]:
        uris = self.parse_uri(uri)
        if uris is None:
            click.secho(f'parse {uri} failed')
            return []
        name, home_url, base_url = uris
        # 解析转换内容为期望的对象
        mpd = xml_handler(content)
        # 检查有没有baseurl
        base_urls = mpd.find('BaseURL') # type: List[BaseURL]
        if len(base_urls) > 0:
            base_url = base_urls[0].innertext
            uris = [name, home_url, base_url]
        return self.walk_period(mpd, uris)

    def walk_period(self, mpd: MPD, uris: list):
        periods = mpd.find('Period')  # type: List[Period]
        # 根据Period数量处理时长参数
        if len(periods) == 1 and periods[0].duration is None:
            # 当只存在一条流 且当前Period没有duration属性
            # 则使用mediaPresentationDuration作为当前Period的时长
            if hasattr(mpd, 'mediaPresentationDuration'):
                periods[0].duration = mpd.mediaPresentationDuration
            else:
                periods[0].duration = 0.0
        # 遍历处理periods
        streams = []
        for period in periods:
            _streams = self.walk_adaptationset(period, len(streams), uris)
            streams.extend(_streams)
        return streams

    def walk_adaptationset(self, period: Period, sindex: int, uris: list):
        adaptationsets = period.find('AdaptationSet')  # type: List[AdaptationSet]
        streams = []
        for adaptationset in adaptationsets:
            _streams = self.walk_representation(adaptationset, period, sindex + len(streams), uris)
            streams.extend(_streams)
        return streams

    def walk_representation(self, adaptationset: AdaptationSet, period: Period, sindex: int, uris: list):
        '''
        每一个<Representation></Representation>都对应轨道的一/整段
        '''
        name, home_url, base_url = uris
        representations = adaptationset.find('Representation') # type: List[Representation]
        segmenttemplates = adaptationset.find('SegmentTemplate') # type: List[SegmentTemplate]
        streams = []
        for representation in representations:
            track_type, suffix = representation.mimeType.split('/')
            _name = f'{name}_{sindex}_{track_type}_{representation.id}'
            stream = DASHStream(sindex, _name, home_url, base_url, self.args.save_dir)
            sindex += 1
            self.walk_contentprotection(representation, stream)
            if len(segmenttemplates) == 0:
                self.walk_segmenttemplate(representation, stream)
            else:
                # SegmentTemplate 和多个 Representation 在同一级
                # 那么 SegmentTemplate 的时长参数等就是多个 Representation 的参数
                # 同一级的时候 只有一个 SegmentTemplate
                self.generate_v1(period, representation.id, segmenttemplates[0], stream)
            streams.append(stream)
        return streams

    def walk_contentprotection(self, representation: Representation, stream: DASHStream):
        ''' 流的加密方案 '''
        contentprotections = representation.find('ContentProtection') # type: List[ContentProtection]
        for contentprotection in contentprotections:
            # DASH流的解密通常是合并完整后一次解密
            # 不适宜每个分段单独解密
            # 那么这里就不用给每个分段设置解密key了
            # 而且往往key不好拿到 所以这里仅仅做一个存储
            stream.append_key(DASHKey(contentprotection))

    def walk_segmenttemplate(self, representation: Representation):
        '''
        进入这个函数的条件是SegmentTemplate是Representation子一级
        '''
        segmenttemplates = representation.find('SegmentTemplate') # type: List[SegmentTemplate]
        if len(segmenttemplates) == 0:
            return
        for segmenttemplate in segmenttemplates:
            self.walk_segmenttimeline(segmenttemplate)

    def walk_segmenttimeline(self, segmenttemplate: SegmentTemplate, **kwargs):
        segmenttimelines = segmenttemplate.find('SegmentTimeline') # type: List[SegmentTimeline]
        for segmenttimeline in segmenttimelines:
            self.walk_s(segmenttimeline, **kwargs)

    def walk_s(self, segmenttimeline: SegmentTimeline, **kwargs):
        ss = segmenttimeline.find('S') # type: List[S]

        _SegmentTemplate = kwargs['_SegmentTemplate'] # type: SegmentTemplate
        _media = _SegmentTemplate.media
        _Number = _SegmentTemplate.startNumber
        _Time = _SegmentTemplate.presentationTimeOffset
        _Representation = kwargs['_Representation'] # type: Representation
        _RepresentationID = _Representation.id
        for s in ss:
            for offset in range(s.r):
                if '$Number$' in _media:
                    _media = _media.replace('$Number$', str(_Number))
                    _Number += 1
                if '$RepresentationID$' in _media:
                    _media = _media.replace('$RepresentationID$', _RepresentationID)
                if '$Time$' in _media:
                    _media = _media.replace('$Time$', str(_Time))
                    _Time += s.d
                    yield _media

    def generate_v1(self, period: Period, rid: str, st: SegmentTemplate, stream: DASHStream):
        init_url = st.get_url()
        if '$RepresentationID$' in init_url:
            init_url = init_url.replace('$RepresentationID$', rid)
        stream.set_init_url(init_url)
        interval = float(int(st.duration) / int(st.timescale))
        repeat = int(round(period.duration / interval))
        for number in range(int(st.startNumber), repeat + int(st.startNumber)):
            media_url = st.get_media_url()
            if '$Number$' in media_url:
                media_url = media_url.replace('$Number$', str(number))
            if '$RepresentationID$' in media_url:
                media_url = media_url.replace('$RepresentationID$', rid)
            stream.set_media_url(media_url)

    def generate(self, baseurl: str, _Period: Period, _AdaptationSet: AdaptationSet, _Representation: Representation, isInnerSeg: bool = True):
        _contentType = _AdaptationSet.get_contenttype()
        if _contentType is None:
            _contentType = _Representation.get_contenttype()
        if _contentType is None:
            _contentType = 'UNKONWN'
        if _AdaptationSet.codecs is not None:
            _codecs = _AdaptationSet.codecs
        elif _Representation.codecs is not None:
            _codecs = _Representation.codecs
        else:
            _Roles = _AdaptationSet.find('Role')
            _codecs = _Roles[0].value
        if isInnerSeg is True:
            key = f'{_AdaptationSet.id}-{_Representation.id}-{_contentType}'
        else:
            key = f'{_Representation.id}-{_contentType}'
        if self.args.split and _Period.id is not None:
            key = f'{_Period.id}-' + key
        if _Period.duration == 0.0 and self.mediaPresentationDuration is not None:
            _Period.duration = self.mediaPresentationDuration
        key = key.replace('/', '_')
        links = Links(self.args.name, _Period.duration, key, _Representation.bandwidth, _codecs)
        if _AdaptationSet.lang is not None:
            links.lang = _AdaptationSet.lang
        if _AdaptationSet.mimeType is not None:
            links.suffix = _AdaptationSet.get_suffix()
        else:
            links.suffix = _Representation.get_suffix()
        if _Representation.width is not None:
            links.resolution = _Representation.get_resolution()
        elif _AdaptationSet.width is not None:
            links.resolution = _AdaptationSet.get_resolution()
        if isInnerSeg is True:
            SegmentTemplates = _Representation.find('SegmentTemplate') # type: List[SegmentTemplate]
        else:
            SegmentTemplates = _AdaptationSet.find('SegmentTemplate') # type: List[SegmentTemplate]
        for _SegmentTemplate in SegmentTemplates:
            start_number = int(_SegmentTemplate.startNumber)  # type: int
            if self.tracks.get(links.key) is None:
                _initialization = _SegmentTemplate.get_initialization()
                if '$RepresentationID$' in _initialization:
                    _initialization = _initialization.replace('$RepresentationID$', _Representation.id)
                if baseurl is not None:
                    _initialization = baseurl + _initialization
                links.urls.append(_initialization)
                self.tracks[links.key] = links
            else:
                if self.args.split is True:
                    self.tracks[links.key] = links
                else:
                    self.tracks[links.key].update(_Period.duration, _Representation.bandwidth)
            SegmentTimelines = _SegmentTemplate.find('SegmentTimeline') # type: List[SegmentTimeline]
            urls = []
            if len(SegmentTimelines) == 0:
                if _SegmentTemplate.presentationTimeOffset is None:
                    _Segment_duration = _Period.duration
                else:
                    _Segment_duration = _Period.duration
                interval_duration = float(int(_SegmentTemplate.duration) / int(_SegmentTemplate.timescale))
                repeat = int(round(_Segment_duration / interval_duration))
                for number in range(start_number, repeat + start_number):
                    _media = _SegmentTemplate.get_media()
                    if '$Number$' in _media:
                        _media = _media.replace('$Number$', str(number))
                    if '$RepresentationID$' in _media:
                        _media = _media.replace('$RepresentationID$', _Representation.id)
                    _url = _media
                    if baseurl is not None:
                        _url = baseurl + _url
                    urls.append(_url)
            else:
                for _SegmentTimeline in SegmentTimelines:
                    # repeat = 0
                    _last_time_offset = 0  # _Period.start
                    SS = _SegmentTimeline.find('S') # type: List[S]
                    for _S in SS:
                        repeat = 1 if _S.r is None else int(_S.r) + 1
                        for offset in range(repeat):
                            _media = _SegmentTemplate.get_media()
                            if '$Number$' in _media:
                                _media = _media.replace('$Number$', str(start_number))
                                start_number += 1
                            if '$RepresentationID$' in _media:
                                _media = _media.replace('$RepresentationID$', _Representation.id)
                            if '$Time$' in _media:
                                _media = _media.replace('$Time$', str(_last_time_offset))
                                _last_time_offset += int(_S.d)
                            _url = _media
                            if baseurl is not None:
                                _url = baseurl + _url
                            urls.append(_url)
            self.tracks[links.key].urls.extend(urls)
            if self.args.split is True:
                self.tracks[links.key].dump_urls()


if __name__ == '__main__':
    from argparse import ArgumentParser
    command = ArgumentParser(
        prog='mpd content parser v1.6@xhlove',
        description=('Mpd Content Parser, '
                     'generate all tracks download links easily. '
                     'Report bug to vvtoolbox.dev@gmail.com'))
    command.add_argument('-p', '--path', help='mpd file path.')
    command.add_argument('-s', '--split', action='store_true', help='generate links for each Period.')
    command.add_argument('-tree', '--tree', action='store_true', help='print mpd tree.')
    command.add_argument('-baseurl', '--baseurl', default='', help='set mpd base url.')
    args = command.parse_args()
    if args.path is None:
        args.path = input('paste mpd file path plz:\n')
    xmlpath = Path(args.path).resolve()
    if xmlpath.exists():
        xmlraw = xmlpath.read_text(encoding='utf-8')
        parser = DASHParser(xmlpath.stem, xmlraw, args.split)
        parser.work()
        if args.tree:
            tree(parser.obj)
        tracks = parser.parse(args.baseurl)
        dump(tracks)
    else:
        print(f'{str(xmlpath)} is not exists!')