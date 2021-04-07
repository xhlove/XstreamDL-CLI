from ..mpditem import MPDItem


class BaseURL(MPDItem):
    def __init__(self, name: str):
        super(BaseURL, self).__init__(name)