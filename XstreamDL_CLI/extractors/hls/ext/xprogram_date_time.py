from datetime import datetime
from .x import X


class XProgramDateTime(X):
    '''
    #EXT-X-PROGRAM-DATE-TIME 第一个分段的绝对时间
    - 2019-01-01T00:00:00.000Z
    '''
    def __init__(self):
        super(XProgramDateTime, self).__init__('#EXT-X-PROGRAM-DATE-TIME')
        self.time = None # type: datetime

    def get_time(self, text: str):
        if text.endswith('Z') is True:
            text = f'{text[:-1]}+00:00'
        try:
            time = datetime.fromisoformat(text)
        except Exception:
            raise
        return time

    def set_time(self, text: str):
        self.time = self.get_time(text)

    def set_attrs_from_line(self, line: str):
        self.set_time(self.get_tag_info(line))
        return self