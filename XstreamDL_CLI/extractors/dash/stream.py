from typing import List
from XstreamDL_CLI.models.stream import Stream
from .segment import DASHSegment


class DASHStream(Stream):
    def __init__(self, index: int, name: str, home_url: str, base_url: str, save_dir: str):
        super(DASHStream, self).__init__(index, name, home_url, base_url, save_dir, 'dash')
        self.segments = [] # type: List[DASHSegment]
        self.suffix = '.mp4'
        self.has_init_segment = False
        self.append_segment()

    def append_segment(self):
        index = len(self.segments)
        if self.has_init_segment:
            index -= 1
        segment = DASHSegment().set_index(index).set_folder(self.save_dir)
        self.segments.append(segment)

    def set_init_url(self, url: str):
        self.has_init_segment = True
        self.segments[-1].set_init_url(self.fix_url(url))
        self.append_segment()

    def set_media_url(self, url: str):
        self.segments[-1].set_media_url(self.fix_url(url))
        self.append_segment()