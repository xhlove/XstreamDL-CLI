import sys
import click
import base64
import shutil
from pathlib import Path
from argparse import ArgumentParser

from XstreamDL_CLI.cmdargs import CmdArgs
from XstreamDL_CLI.version import __version__
from XstreamDL_CLI.downloader import Downloader
from XstreamDL_CLI.headers.default import Headers


def command_handler(args: CmdArgs):
    '''
    对命令参数进行校验和修正
    '''
    if Path(args.save_dir).exists() is False:
        Path(args.save_dir).mkdir()
    args.headers = Headers().get(args)
    args.limit_per_host = int(args.limit_per_host)
    if args.key is not None:
        infos = args.key.split(':')
        assert len(infos) == 2, 'DASH Stream decryption key format error !'
        assert len(infos[0]) == 32, 'DASH Stream decryption key @KID must be 32 length hex string !'
        assert len(infos[1]) == 32, 'DASH Stream decryption key @k must be 32 length hex string !'
    if args.b64key is not None:
        try:
            _ = base64.b64decode(args.b64key)
        except Exception as e:
            raise e
    if args.hexiv is not None:
        if args.hexiv.lower().startswith('0x'):
            args.hexiv = args.hexiv.lower()[2:]
    # ffmpeg 优先使用文件夹内的
    if Path(args.ffmpeg).exists():
        args.ffmpeg = Path(args.ffmpeg).absolute().as_posix()
    elif Path(f'{args.ffmpeg}.exe').exists():
        args.ffmpeg = Path(f'{args.ffmpeg}.exe').absolute().as_posix()
    elif shutil.which('ffmpeg') is not None:
        args.ffmpeg = Path(args.ffmpeg).absolute().as_posix()
    else:
        click.secho(f'Warning: cannot find executable ffmpeg')
    # mp4decrypt 优先使用文件夹内的
    if Path(args.mp4decrypt).exists():
        args.mp4decrypt = Path(args.mp4decrypt).absolute().as_posix()
    elif Path(f'{args.mp4decrypt}.exe').exists():
        args.mp4decrypt = Path(f'{args.mp4decrypt}.exe').absolute().as_posix()
    elif shutil.which('mp4decrypt') is not None:
        args.mp4decrypt = Path(shutil.which('mp4decrypt')).absolute().as_posix()
    elif shutil.which('ffmpeg') is not None:
        args.mp4decrypt = Path(shutil.which('ffmpeg')).absolute().as_posix()
    else:
        if args.key is not None:
            click.secho(f'Warning: cannot find executable mp4decrypt')


def main():
    def print_version():
        click.secho(f'version {__version__}, A downloader that download the HLS/DASH stream.')

    parser = ArgumentParser(
        prog='XstreamDL-CLI',
        usage='XstreamDL-CLI [OPTION]... URL/FILE/FOLDER...',
        description='A downloader that download the HLS/DASH stream',
        add_help=False,
    )
    parser.add_argument('-v', '--version', action='store_true', help='Print version and exit')
    parser.add_argument('-h', '--help', action='store_true', help='Print help message and exit')
    parser.add_argument('-name', '--name', default='', help='Specific stream base name')
    parser.add_argument('-base', '--base-url', default='', help='Set base url for Stream')
    parser.add_argument('-save-dir', '--save-dir', default='Downloads', help='Set save dir for Stream')
    parser.add_argument('--ffmpeg', default='ffmpeg', help='Set executable ffmpeg path')
    parser.add_argument('--mp4decrypt', default='mp4decrypt', help='Set executable mp4decrypt path')
    parser.add_argument(
        '--select',
        action='store_true',
        help='Show stream to select and download, default is to download all')
    parser.add_argument(
        '--disable-force-close',
        action='store_true',
        help='Default make all connections closed securely, but it will make DL speed slower'
    )
    parser.add_argument(
        '--limit-per-host',
        default=4,
        help='Increase the value if your connection to the stream host is poor, suggest >100 for DASH stream'
    )
    parser.add_argument('--user-agent', default='', help='set user-agent headers for request')
    parser.add_argument('--referer', default='', help='set custom referer for request')
    parser.add_argument(
        '--headers',
        default='',
        help='set custom headers for request, separators is |, e.g. "header1:value1|header2:value2"'
    )
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output files')
    parser.add_argument('--raw-concat', action='store_true', help='Concat content as raw')
    parser.add_argument('--disable-auto-concat', action='store_true', help='Disable auto-concat')
    parser.add_argument('--enable-auto-delete', action='store_true', help='Enable auto-delete files after concat success')
    parser.add_argument(
        '--key',
        default=None,
        help='<id>:<k>, <id> is either a track ID in decimal or a 128-bit KID in hex, <k> is a 128-bit key in hex'
    )
    parser.add_argument('--b64key', default=None, help='base64 format aes key, only for HLS standard AES-128-CBC encryption')
    parser.add_argument('--hexiv', default=None, help='hex format aes iv')
    parser.add_argument('--proxy', default=None, help='use http proxy, e.g. http://127.0.0.1:1080')
    parser.add_argument('--split', action='store_true', help='Dash option, split one stream to multi sections')
    parser.add_argument('--repl', action='store_true', help='REPL mode')
    parser.add_argument('URI', nargs='*', help='URL/FILE/FOLDER string')
    args = parser.parse_args()
    command_handler(args)
    if args.help:
        print_version()
        parser.print_help()
        sys.exit()
    if args.version:
        print_version()
        sys.exit()
    if len(args.URI) == 0:
        try:
            uri = input('Paste your URL/FILE/FOLDER string at the end of commands, plz.\nCtrl C to exit or input here:')
        except KeyboardInterrupt:
            sys.exit()
        if uri.strip() != '':
            args.URI.append(uri.strip())
    if len(args.URI) == 0:
        sys.exit('No URL/FILE/FOLDER input')
    downloader = Downloader(args)
    downloader.daemon()


if __name__ == '__main__':
    main()