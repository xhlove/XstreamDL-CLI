from .ismitem import ISMItem


class ISM(ISMItem):
    def __init__(self, name: str):
        super(ISM, self).__init__(name)
        self.MajorVersion = None # type: str
        self.MinorVersion = None # type: str
        self.TimeScale = None # type: str
        self.Duration = None # type: str