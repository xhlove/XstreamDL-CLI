
import aiohttp
import asyncio
from .x import X


DEFAULT_IV = '0' * 32


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
        super(XKey, self).__init__('#EXT-X-KEY')
        self.method = 'AES-128' # type: str
        self.uri = None # type: str
        self.key = b'' # type: bytes
        self.keyid = None # type: str
        self.iv = DEFAULT_IV # type: str
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

    def set_key(self, key: bytes):
        self.key = key
        return self

    def set_iv(self, iv: str):
        if iv is None:
            return
        self.iv = iv
        return self

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

    async def fetch(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.content.read()

    def load(self, custom_xkey: 'XKey'):
        '''
        如果custom_xkey存在key 那么覆盖解析结果中的key
        并且不进行请求key的动作 同时覆盖iv 如果有自定义iv的话
        '''
        if custom_xkey.iv != DEFAULT_IV:
            self.iv = custom_xkey.iv
        if custom_xkey.key != b'':
            self.key = custom_xkey.key
            return
        if self.uri.startswith('http://') or self.uri.startswith('https://'):
            loop = asyncio.get_event_loop()
            self.key = loop.run_until_complete(self.fetch(self.uri))
        elif self.uri.startswith('ftp://'):
            return False
        return True