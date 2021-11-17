from datetime import datetime
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
        # time of client to fetch the mpd content
        self.publishTime = None # type: datetime
        self.availabilityStartTime = None # type: float
        self.timeShiftBufferDepth = None # type: str
        self.suggestedPresentationDelay = None # type: str

    def generate(self):
        if isinstance(self.maxSegmentDuration, str):
            self.maxSegmentDuration = self.match_duration(self.maxSegmentDuration)
        if isinstance(self.mediaPresentationDuration, str):
            self.mediaPresentationDuration = self.match_duration(self.mediaPresentationDuration)
        if isinstance(self.minBufferTime, str):
            self.minBufferTime = self.match_duration(self.minBufferTime)
        if isinstance(self.availabilityStartTime, str):
            if self.availabilityStartTime == '1970-01-01T00:00:00Z':
                self.availabilityStartTime = 0.0
            try:
                self.availabilityStartTime = datetime.strptime(self.availabilityStartTime, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
            except Exception:
                try:
                    self.availabilityStartTime = datetime.strptime(self.availabilityStartTime, '%Y-%m-%dT%H:%M:%SZ').timestamp()
                except Exception:
                    pass
        if isinstance(self.publishTime, str):
            try:
                self.publishTime = datetime.strptime(self.publishTime, '%Y-%m-%dT%H:%M:%S.%fZ')
            except Exception:
                try:
                    self.publishTime = datetime.strptime(self.publishTime, '%Y-%m-%dT%H:%M:%SZ')
                except Exception:
                    pass