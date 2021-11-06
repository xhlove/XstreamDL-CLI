from typing import Union
from pathlib import Path


class CmdArgs:

    def __init__(self):
        self.live = None # type: bool
        self.live_duration = None # type: float
        self.name = None # type: str
        self.base_url = None # type: str
        self.resolution = None # type: str
        self.best_quality = None # type: bool
        self.video_only = None # type: bool
        self.audio_only = None # type: bool
        self.service = None # type: str
        self.save_dir = None # type: Path
        self.ffmpeg = None # type: str
        self.mp4decrypt = None # type: str
        self.mp4box = None # type: str
        self.select = None # type: bool
        self.disable_force_close = None # type: bool
        self.limit_per_host = None # type: int
        self.user_agent = None # type: str
        self.referer = None # type: str
        self.headers = None # type: Union[str, dict]
        self.url_patch = None # type: str
        self.overwrite = None # type: bool
        self.raw_concat = None # type: bool
        self.disable_auto_concat = None # type: bool
        self.enable_auto_delete = None # type: bool
        self.disable_auto_decrypt = None # type: bool
        self.key = None # type: str
        self.b64key = None # type: str
        self.hexiv = None # type: str
        self.proxy = None # type: Union[str, None]
        self.disable_auto_exit = None # type: bool
        self.parse_only = None # type: bool
        self.show_init = None # type: bool
        self.index_to_name = None # type: bool
        self.log_level = None # type: str
        self.redl_code = None # type: list
        self.URI = None # type: list