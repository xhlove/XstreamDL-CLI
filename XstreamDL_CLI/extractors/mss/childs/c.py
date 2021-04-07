from ..ismitem import ISMItem


class c(ISMItem):
    def __init__(self, name: str):
        super(c, self).__init__(name)
        self.t = None # type: int
        self.d = None # type: int