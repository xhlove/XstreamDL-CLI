import re
import click


class XKey:
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
        self.encrypt_method = None # type: str
        self.encrypt_uri = None # type: str
        self.encrypt_keyid = None # type: str
        self.encrypt_iv = None # type: str
        self.encrypt_keyformat_ver = None # type: str
        self.encrypt_keyformat = None # type: str

    def set_key(self, home_url: str, base_url: str, line: str):
        # https://stackoverflow.com/questions/34081567
        # re.findall('([A-Z]+[0-9]*)=("[^"]*"|[^,]*)', s)
        line = line.replace('#EXT-X-KEY:', '')
        try:
            for key, value in re.findall('(.*?)=("[^"]*?"|[^,]*?),', line):
                value = value.strip('"')
                if key == 'METHOD':
                    self.encrypt_method = value
                elif key == 'MEATHOD':
                    # 某些网站会故意这样
                    self.encrypt_method = value
                elif key == 'URI':
                    self.encrypt_uri_type, self.encrypt_uri = self.gen_hls_key_uri(value)
                elif key == 'KEYID':
                    self.encrypt_keyid = value
                elif key == 'IV':
                    self.encrypt_iv = value
                elif key == 'KEYFORMATVERSIONS':
                    self.encrypt_keyformat_ver = value
                elif key == 'KEYFORMAT':
                    self.encrypt_keyformat = value
                else:
                    click.secho(f'unsupport attribute <{key}-{value}> of tag #EXT-X-KEY')
        except Exception:
            pass
        return self

    def gen_hls_key_uri(self, uri: str):
        '''
        data:text/plain;base64,AAAASnBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAACoSEKg079lX5xeK9g/zZPwXENESEKg079lX5xeK9g/zZPwXENFI88aJmwY=
        skd://a834efd957e7178af60ff364fc1710d1
        '''
        if uri.startswith('data:text/plain;base64,'):
            return 'base64', uri.split(',', maxsplit=1)[-1]
        elif uri.startswith('skd://'):
            return 'skd', uri.split('/', maxsplit=1)[-1]
        else:
            return 'unknow', uri