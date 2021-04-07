from ..ismitem import ISMItem


class StreamIndex(ISMItem):
    def __init__(self, name: str):
        super(StreamIndex, self).__init__(name)
        self.Type = None # type: str
        self.QualityLevels = None # type: str
        self.TimeScale = None # type: int
        self.Name = None # type: str
        self.Chunks = None # type: int
        self.Url = None # type: str
        self.MaxWidth = None # type: str
        self.MaxHeight = None # type: str
        self.DisplayWidth = None # type: str
        self.DisplayHeight = None # type: str