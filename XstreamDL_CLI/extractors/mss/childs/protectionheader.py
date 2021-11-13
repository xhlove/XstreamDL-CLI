import re
import base64
from ..ismitem import ISMItem


class ProtectionHeader(ISMItem):
    def __init__(self, name: str):
        super(ProtectionHeader, self).__init__(name)
        self.SystemID = None # type: str
        self.kid = None # type: bytes

    def generate(self):
        '''
        get kid from innertext
        '''
        # dAIAAAEAAQBqAjwAVwBSAE0ASABFAEEARABFAFIAIAB4AG0AbABuAHMAPQAiAGgAdAB0AHAAOgAvAC8AcwBjAGgAZQBtAGEAcwAuAG0AaQBjAHIAbwBzAG8AZgB0AC4AYwBvAG0ALwBEAFIATQAvADIAMAAwADcALwAwADMALwBQAGwAYQB5AFIAZQBhAGQAeQBIAGUAYQBkAGUAcgAiACAAdgBlAHIAcwBpAG8AbgA9ACIANAAuADAALgAwAC4AMAAiAD4APABEAEEAVABBAD4APABQAFIATwBUAEUAQwBUAEkATgBGAE8APgA8AEsARQBZAEwARQBOAD4AMQA2ADwALwBLAEUAWQBMAEUATgA+ADwAQQBMAEcASQBEAD4AQQBFAFMAQwBUAFIAPAAvAEEATABHAEkARAA+ADwALwBQAFIATwBUAEUAQwBUAEkATgBGAE8APgA8AEsASQBEAD4ATwBXAGoAaAB0AHIAMwB1ADkAawArAHIAZABvADEASQBMAFkAMAByAGEAZwA9AD0APAAvAEsASQBEAD4APABDAEgARQBDAEsAUwBVAE0APgBOADgAVABvAEsASABKADEAZABKAGMAPQA8AC8AQwBIAEUAQwBLAFMAVQBNAD4APABMAEEAXwBVAFIATAA+AGgAdAB0AHAAcwA6AC8ALwBhAHAAaQAuAGIAbABpAG0ALgBjAG8AbQAvAGwAaQBjAGUAbgBzAGUALwBwAGwAYQB5AHIAZQBhAGQAeQA8AC8ATABBAF8AVQBSAEwAPgA8AC8ARABBAFQAQQA+ADwALwBXAFIATQBIAEUAQQBEAEUAUgA+AA==
        try:
            data = base64.b64decode(self.innertext).replace(b'\x00', b'')
            b64_kid = re.findall(b'<KID>(.+?)</KID>', data)[0].decode('utf-8')
            self.kid = base64.b64decode(b64_kid)
        except Exception as e:
            print(f'ProtectionHeader generate failed, reason:{e}')