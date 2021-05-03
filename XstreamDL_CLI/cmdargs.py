from typing import Union


class CmdArgs:

    def __init__(self):
        self.name = None # type: str
        self.base_url = None # type: str
        self.save_dir = None # type: str
        self.ffmpeg = None # type: str
        self.mp4decrypt = None # type: str
        self.select = None # type: bool
        self.disable_force_close = None # type: bool
        self.limit_per_host = None # type: int
        self.user_agent = None # type: str
        self.referer = None # type: str
        self.headers = None # type: Union[str, dict]
        self.overwrite = None # type: bool
        self.raw_concat = None # type: bool
        self.disable_auto_concat = None # type: bool
        self.enable_auto_delete = None # type: bool
        self.disable_auto_decrypt = None # type: bool
        self.key = None # type: str
        self.b64key = None # type: str
        self.hexiv = None # type: str
        self.proxy = None # type: Union[str, None]
        self.split = None # type: bool
        self.repl = None # type: bool
        self.URI = None # type: list