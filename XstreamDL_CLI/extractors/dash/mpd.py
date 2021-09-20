from .mpditem import MPDItem


class MPD(MPDItem):
    def __init__(self, name: str):
        super(MPD, self).__init__(name)
        self.maxSegmentDuration = None # type: str
        self.mediaPresentationDuration = None # type: str
        self.minBufferTime = None # type: str
        # live profile
        # - urn:mpeg:dash:profile:isoff-live:2011
        # - urn:mpeg:dash:profile:isoff-ext-live:2014
        self.profiles = None # type: str
        # dynamic -> live
        # static -> live playback
        self.type = None # type: str
        # only use when type is 'dynamic' which specifies the smallest period between potential changes to the MPD
        self.minimumUpdatePeriod = None # type: str
        self.publishTime = None # type: str
        self.availabilityStartTime = None # type: str
        self.timeShiftBufferDepth = None # type: str
        self.suggestedPresentationDelay = None # type: str

    def generate(self):
        if isinstance(self.maxSegmentDuration, str):
            self.maxSegmentDuration = self.match_duration(self.maxSegmentDuration)
        if isinstance(self.mediaPresentationDuration, str):
            self.mediaPresentationDuration = self.match_duration(self.mediaPresentationDuration)
        if isinstance(self.minBufferTime, str):
            self.minBufferTime = self.match_duration(self.minBufferTime)