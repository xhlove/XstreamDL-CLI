from .x import X


class XKey(X):
    '''
    一组加密参数
    - METHOD
        - AES-128
        - SAMPLE-AES
    - URI
        - data:text/plain;base64,...
        - skd://...
    - IV
        - 0x/0X...
    - KEYFORMAT
        - urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed
        - com.apple.streamingkeydelivery
    '''
    def __init__(self):
        self.method = None # type: str
        self.uri = None # type: str
        self.keyid = None # type: str
        self.iv = None # type: str
        self.keyformatversions = None # type: str
        self.keyformat = None # type: str
        self.known_attrs = {
            'METHOD': 'method',
            'URI': 'uri',
            'KEYID': 'keyid',
            'IV': 'iv',
            'KEYFORMATVERSIONS': 'keyformatversions',
            'KEYFORMAT': 'keyformat',
        }

    def set_attrs_from_line(self, home_url: str, base_url: str, line: str):
        '''
        key的链接可能不全 用home_url或base_url进行补齐 具体处理后面做
        '''
        line = line.replace('MEATHOD', 'METHOD')
        return super(XKey, self).set_attrs_from_line(line)

    def gen_hls_key_uri(self, uri: str):
        '''
        解析时 不具体调用这个函数 需要的地方再转换
        data:text/plain;base64,AAAASnBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAACoSEKg079lX5xeK9g/zZPwXENESEKg079lX5xeK9g/zZPwXENFI88aJmwY=
        skd://a834efd957e7178af60ff364fc1710d1
        '''
        if uri.startswith('data:text/plain;base64,'):
            return 'base64', uri.split(',', maxsplit=1)[-1]
        elif uri.startswith('skd://'):
            return 'skd', uri.split('/', maxsplit=1)[-1]
        else:
            return 'unknow', uri

    def load(self):
        if self.uri.startswith('http://') or self.uri.startswith('https://'):
            pass
        elif self.uri.startswith('ftp://'):
            return False
        return True