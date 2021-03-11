from .mpditem import MPDItem


class MPD(MPDItem):
    def __init__(self, name: str):
        super(MPD, self).__init__(name)
        self.maxSegmentDuration = None # type: str
        self.mediaPresentationDuration = None # type: str
        self.minBufferTime = None # type: str

    def generate(self):
        if isinstance(self.maxSegmentDuration, str):
            self.maxSegmentDuration = self.match_duration(self.maxSegmentDuration)
        if isinstance(self.mediaPresentationDuration, str):
            self.mediaPresentationDuration = self.match_duration(self.mediaPresentationDuration)
        if isinstance(self.minBufferTime, str):
            self.minBufferTime = self.match_duration(self.minBufferTime)