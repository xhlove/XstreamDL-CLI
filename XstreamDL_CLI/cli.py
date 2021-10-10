import sys
import base64
import platform
from pathlib import Path
from logging import Logger
from argparse import ArgumentParser

from XstreamDL_CLI.cmdargs import CmdArgs
from XstreamDL_CLI.daemon import Daemon
from XstreamDL_CLI.version import __version__
from XstreamDL_CLI.headers.default import Headers
from XstreamDL_CLI.log import setup_logger


def command_handler(logger: Logger, args: CmdArgs):
    '''
    对命令参数进行校验和修正
    '''
    if args.live_duration == '':
        args.live_duration = 0.0
    else:
        hms = args.live_duration.split(':')
        assert len(hms) == 3, '--live-duration format is HH:MM:SS, example: 00:00:30'
        assert len(hms[1]) <= 2, '--live-duration minute length must less than or equal to 2'
        assert len(hms[2]) <= 2, '--live-duration second length must less than or equal to 2'
        if hms[0].isdigit() and hms[1].isdigit() and hms[2].isdigit():
            assert float(hms[1]) <= 60.0, '--live-duration minute must less than or equal to 60'
            assert float(hms[2]) <= 60.0, '--live-duration second must less than or equal to 60'
            args.live_duration = float(hms[0]) * 60 * 60 + float(hms[1]) * 60 + float(hms[2])
    logger.debug(f'set --live-duration to {args.live_duration}')
    args.save_dir = Path(args.save_dir)
    if args.save_dir.exists() is False:
        args.save_dir.mkdir()
    logger.debug(f'set --save-dir to {args.save_dir.resolve().as_posix()}')
    args.headers = Headers(logger).get(args)
    args.limit_per_host = int(args.limit_per_host)
    logger.debug(f'set --limit-per-host to {args.limit_per_host}')
    if args.key is not None:
        infos = args.key.split(':')
        assert len(infos) == 2, 'DASH Stream decryption key format error !'
        # assert len(infos[0]) == 32, 'DASH Stream decryption key @KID must be 32 length hex string !'
        assert len(infos[1]) == 32, 'DASH Stream decryption key @k must be 32 length hex string !'
    logger.debug(f'set --key to {args.key}')
    if args.b64key is not None:
        try:
            _ = base64.b64decode(args.b64key)
        except Exception as e:
            raise e
    if args.hexiv is not None:
        if args.hexiv.lower().startswith('0x'):
            args.hexiv = args.hexiv.lower()[2:]
    logger.debug(f'set --b64key to {args.b64key}')
    logger.debug(f'set --hexiv to {args.hexiv}')

    if getattr(sys, 'frozen', False):
        bin_path = Path(sys.executable).parent / 'binaries'
    else:
        bin_path = Path(__file__).parent.parent / 'binaries'
    if bin_path.exists() is False:
        logger.warning(f'binaries folder is not exist > {bin_path}')
    else:
        if platform.system() == 'Windows':
            args.ffmpeg = bin_path / 'ffmpeg.exe'
            args.mp4decrypt = bin_path / 'mp4decrypt.exe'
            args.mp4box = bin_path / 'mp4box.exe'
        else:
            args.ffmpeg = bin_path / 'ffmpeg'
            args.mp4decrypt = bin_path / 'mp4decrypt'
            args.mp4box = bin_path / 'mp4box'
        logger.debug(f'ffmpeg {args.ffmpeg.resolve().as_posix()}')
        logger.debug(f'mp4decrypt {args.mp4decrypt.resolve().as_posix()}')
        logger.debug(f'mp4box {args.mp4box.resolve().as_posix()}')
    try:
        args.re_download_status = [int(_.strip()) for _ in args.re_download_status.split(',') if _ != '']
    except Exception as e:
        logger.error(f'parse --re-download-status option failed', exc_info=e)
        args.re_download_status = []


def main():
    def print_version():
        print(f'version {__version__}, A downloader that download the HLS/DASH stream.')

    parser = ArgumentParser(prog='XstreamDL-CLI', usage='XstreamDL-CLI [OPTION]... URL/FILE/FOLDER...', description='A downloader that download the HLS/DASH stream', add_help=False)
    parser.add_argument('-v', '--version', action='store_true', help='print version and exit')
    parser.add_argument('-h', '--help', action='store_true', help='print help message and exit')
    parser.add_argument('-live', '--live', action='store_true', help='live mode')
    parser.add_argument('-live-duration', '--live-duration', default='', help='live record time, format HH:MM:SS, example 00:00:30 will record about 30s')
    parser.add_argument('-name', '--name', default='', help='specific stream base name')
    parser.add_argument('-base-url', '--base-url', default='', help='set base url for Stream')
    parser.add_argument('-prefer-content-base-url', '--prefer-content-base-url', action='store_true', help='prefer use content base url for Stream')
    parser.add_argument('-service-location', '--service-location', help='set serviceLocation for BaseURL choose')
    parser.add_argument('-save-dir', '--save-dir', default='Downloads', help='set save dir for Stream')
    # parser.add_argument('--ffmpeg', default='ffmpeg', help='set executable ffmpeg path')
    # parser.add_argument('--mp4decrypt', default='mp4decrypt', help='set executable mp4decrypt path')
    parser.add_argument('--select', action='store_true', help='show stream to select and download, default is to download all')
    parser.add_argument('--disable-force-close', action='store_true', help='default make all connections closed securely, but it will make DL speed slower')
    parser.add_argument('--limit-per-host', default=4, help='increase the value if your connection to the stream host is poor, suggest >100 for DASH stream')
    parser.add_argument('--user-agent', default='', help='set user-agent headers for request')
    parser.add_argument('--referer', default='', help='set custom referer for request')
    parser.add_argument('--headers', default='', help='set custom headers for request, separators is |, e.g. "header1:value1|header2:value2"')
    parser.add_argument('--url-patch', default='', help='add some custom strings for all segments link')
    parser.add_argument('--overwrite', action='store_true', help='overwrite output files')
    parser.add_argument('--raw-concat', action='store_true', help='concat content as raw')
    parser.add_argument('--disable-auto-concat', action='store_true', help='disable auto-concat')
    parser.add_argument('--enable-auto-delete', action='store_true', help='enable auto-delete files after concat success')
    parser.add_argument('--disable-auto-decrypt', action='store_true', help='disable auto-decrypt segments before dump to disk')
    parser.add_argument('--key', default=None, help='<id>:<k>, <id> is either a track ID in decimal or a 128-bit KID in hex, <k> is a 128-bit key in hex')
    parser.add_argument('--b64key', default=None, help='base64 format aes key, only for HLS standard AES-128-CBC encryption')
    parser.add_argument('--hexiv', default=None, help='hex format aes iv')
    parser.add_argument('--proxy', default=None, help='use http proxy, e.g. http://127.0.0.1:1080')
    parser.add_argument('--split', action='store_true', help='dash option, split one stream to multi sections')
    parser.add_argument('--disable-auto-exit', action='store_true', help='disable auto exit after download end, GUI will use this option')
    parser.add_argument('--parse-only', action='store_true', help='parse only, not to download')
    parser.add_argument('--show-init', action='store_true', help='show initialization to help you identify same name stream')
    parser.add_argument('--add-index-to-name', action='store_true', help='some dash live have the same name for different stream, use this option to avoid')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='set log level, default is INFO')
    parser.add_argument('--re-download-status', default='', help='re-download set of response status codes , e.g. 408,500,502,503,504')
    parser.add_argument('URI', nargs='*', help='URL/FILE/FOLDER string')
    args = parser.parse_args()
    if args.help:
        print_version()
        parser.print_help()
        sys.exit()
    if args.version:
        print_version()
        sys.exit()
    logger = setup_logger('XstreamDL', args.log_level)
    command_handler(logger, args)
    if len(args.URI) == 0:
        try:
            uri = input('Paste your URL/FILE/FOLDER string at the end of commands, plz.\nCtrl C to exit or input here:')
        except KeyboardInterrupt:
            sys.exit()
        if uri.strip() != '':
            args.URI.append(uri.strip())
    if len(args.URI) == 0:
        sys.exit('No URL/FILE/FOLDER input')
    logger.info(f'set URI to {args.URI}')
    daemon = Daemon(logger, args)
    daemon.daemon()
    if args.disable_auto_exit:
        _ = input('press any key to exit.')


if __name__ == '__main__':
    main()