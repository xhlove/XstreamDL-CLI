import re
import click


class XMedia:
    '''
    #EXT-X-MEDIA 外挂媒体
    - TYPE
        - AUDIO
    - URI
        - data:text/plain;base64,...
        - skd://...
    - NAME
    - AUTOSELECT
        - YES/NO
    - CHANNELS
    '''
    def __init__(self):
        self.media_method = None # type: str
        self.media_uri = None # type: str
        self.media_keyid = None # type: str
        self.media_iv = None # type: str
        self.media_keyformat_ver = None # type: str
        self.media_keyformat = None # type: str

    def set_media(self, home_url: str, base_url: str, line: str):
        # https://stackoverflow.com/questions/34081567
        # re.findall('([A-Z]+[0-9]*)=("[^"]*"|[^,]*)', s)
        line = line.replace('#EXT-X-MEDIA:', '')
        if line.endswith(',') is False:
            # 末尾缺少逗号会影响正则判断
            line += ','
        try:
            for key, value in re.findall('(.*?)=("[^"]*?"|[^,]*?),', line):
                value = value.strip('"')
                if key == 'TYPE':
                    self.media_method = value
                elif key == 'URI':
                    self.media_uri_type, self.media_uri = self.gen_hls_media_uri(value)
                elif key == 'GROUP-ID':
                    self.media_groupid = value
                elif key == 'NAME':
                    self.media_name = value
                elif key == 'AUTOSELECT':
                    self.media_auto_select = value
                elif key == 'CHANNELS':
                    self.media_channels = value
                else:
                    click.secho(f'unsupport attribute <{key}-{value}> of tag #EXT-X-MEDIA')
        except Exception:
            pass
        return self

    def gen_hls_media_uri(self, uri: str):
        '''
        data:text/plain;base64,AAAASnBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAACoSEKg079lX5xeK9g/zZPwXENESEKg079lX5xeK9g/zZPwXENFI88aJmwY=
        '''
        if uri.startswith('data:text/plain;base64,'):
            return 'base64', uri.split(',', maxsplit=1)[-1]
        elif uri.startswith('skd://'):
            return 'skd', uri.split('/', maxsplit=1)[-1]
        else:
            return 'unknow', uri