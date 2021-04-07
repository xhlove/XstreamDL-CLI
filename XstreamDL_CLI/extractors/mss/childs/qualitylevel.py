from ..ismitem import ISMItem


class QualityLevel(ISMItem):
    def __init__(self, name: str):
        super(QualityLevel, self).__init__(name)
        self.Index = None # type: int
        self.Bitrate = None # type: int
        self.CodecPrivateData = None # type: str
        self.MaxWidth = None # type: str
        self.MaxHeight = None # type: int
        self.FourCC = None # type: str