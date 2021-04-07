from ..ismitem import ISMItem


class ProtectionHeader(ISMItem):
    def __init__(self, name: str):
        super(ProtectionHeader, self).__init__(name)
        self.SystemID = None # type: str