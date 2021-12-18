import sys
import json
from pathlib import Path


class ArgsHandler:

    def __init__(self):
        self.live_utc_offset = None # type: int
        self.live_refresh_interval = None # type: int
        self.resolution = None # type: str
        self.best_quality = None # type: bool
        self.video_only = None # type: bool
        self.audio_only = None # type: bool
        self.all_videos = None # type: bool
        self.all_audios = None # type: bool
        self.save_dir = None # type: Path
        self.select = None # type: bool
        self.disable_force_close = None # type: bool
        self.limit_per_host = None # type: int
        self.overwrite = None # type: bool
        self.raw_concat = None # type: bool
        self.disable_auto_concat = None # type: bool
        self.enable_auto_delete = None # type: bool
        self.disable_auto_decrypt = None # type: bool
        self.proxy = None # type: str
        self.use_proxy = None # type: str
        self.disable_auto_exit = None # type: bool
        self.parse_only = None # type: bool
        self.show_init = None # type: bool
        self.index_to_name = None # type: bool
        self.log_level = None # type: str
        self.redl_code = None # type: list
        self.hide_load_metadata = None # type: bool
        self.config = None # type: dict

    def load_config(self):
        if getattr(sys, 'frozen', False):
            config_path = Path(sys.executable).parent / 'config.json'
        else:
            config_path = Path(__file__).parent.parent / 'config.json'
        try:
            self.config = json.loads(config_path.read_text(encoding='utf-8'))
        except Exception:
            print('load config failed')
        if self.config is None:
            self.config = {}
        self.live_utc_offset = int(self.config.get('live_utc_offset', 0))
        self.live_refresh_interval = int(self.config.get('live_refresh_interval', 3))
        self.resolution = self.config.get('resolution', '')
        self.best_quality = self.config.get('best_quality', False)
        self.video_only = self.config.get('video_only', False)
        self.audio_only = self.config.get('audio_only', False)
        self.all_videos = self.config.get('all_videos', False)
        self.all_audios = self.config.get('all_audios', False)
        self.save_dir = self.config.get('save_dir', 'Downloads')
        self.select = self.config.get('select', True)
        self.disable_force_close = self.config.get('disable_force_close', False)
        self.limit_per_host = int(self.config.get('limit_per_host', 4))
        self.overwrite = self.config.get('overwrite', False)
        self.raw_concat = self.config.get('raw_concat', False)
        self.disable_auto_concat = self.config.get('disable_auto_concat', False)
        self.enable_auto_delete = self.config.get('enable_auto_delete', False)
        self.disable_auto_decrypt = self.config.get('disable_auto_decrypt', False)
        self.proxy = self.config.get('proxy', '')
        self.use_proxy = self.config.get('use_proxy', False)
        self.disable_auto_exit = self.config.get('disable_auto_exit', True)
        self.parse_only = self.config.get('parse_only', False)
        self.show_init = self.config.get('show_init', False)
        self.index_to_name = self.config.get('index_to_name', False)
        self.log_level = self.config.get('log_level', 'INFO')
        self.redl_code = self.config.get('redl_code', '')
        self.hide_load_metadata = self.config.get('hide_load_metadata', False)
        return self

    def save_config(self):
        if getattr(sys, 'frozen', False):
            config_path = Path(sys.executable).parent / 'config.json'
        else:
            config_path = Path(__file__).parent.parent / 'config.json'
        config = {
            'live_utc_offset': self.live_utc_offset,
            'live_refresh_interval': self.live_refresh_interval,
            'resolution': self.resolution,
            'best_quality': self.best_quality,
            'video_only': self.video_only,
            'audio_only': self.audio_only,
            'all_videos': self.all_videos,
            'all_audios': self.all_audios,
            'save_dir': self.save_dir,
            'select': self.select,
            'disable_force_close': self.disable_force_close,
            'limit_per_host': self.limit_per_host,
            'overwrite': self.overwrite,
            'raw_concat': self.raw_concat,
            'disable_auto_concat': self.disable_auto_concat,
            'enable_auto_delete': self.enable_auto_delete,
            'disable_auto_decrypt': self.disable_auto_decrypt,
            'proxy': self.proxy,
            'use_proxy': self.use_proxy,
            'disable_auto_exit': self.disable_auto_exit,
            'parse_only': self.parse_only,
            'show_init': self.show_init,
            'index_to_name': self.index_to_name,
            'log_level': self.log_level,
            'redl_code': self.redl_code,
            'hide_load_metadata': self.hide_load_metadata,
        }
        try:
            config_path.write_text(json.dumps(config, ensure_ascii=False, indent=4), encoding='utf-8')
        except Exception:
            print('save config failed')
        return self