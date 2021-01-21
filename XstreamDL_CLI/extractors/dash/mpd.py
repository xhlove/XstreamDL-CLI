from .mpditem import MPDItem


class MPD(MPDItem):
    def __init__(self, name: str):
        super(MPD, self).__init__(name)