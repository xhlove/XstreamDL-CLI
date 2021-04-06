from typing import Union


class CmdArgs:

    def __init__(self):
        self.save_dir = None # type: str
        self.base_url = None # type: str
        self.disable_force_close = None # type: bool
        self.limit_per_host = None # type: int
        self.user_agent = None # type: str
        self.referer = None # type: str
        self.headers = None # type: Union[str, dict]
        self.overwrite = None # type: bool
        self.raw_concat = None # type: bool
        self.disable_auto_concat = None # type: bool
        self.b64key = None # type: str
        self.hexiv = None # type: str
        self.proxy = None # type: Union[str, None]
        self.split = None # type: bool
        self.repl = None # type: bool
        self.name = None # type: str
        self.URI = None # type: list