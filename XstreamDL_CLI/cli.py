import sys
import click
import base64
from pathlib import Path
from argparse import ArgumentParser, Namespace

from .version import __version__
from .downloader import Downloader


def command_handler(args: Namespace):
    '''
    对命令参数进行校验和修正
    '''
    if Path(args.save_dir).exists() is False:
        Path(args.save_dir).mkdir()
    if args.b64key is not None:
        try:
            _ = base64.b64decode(args.b64key)
        except Exception as e:
            raise e
    if args.hexiv is not None:
        if args.hexiv.lower().startswith('0x'):
            args.hexiv = args.hexiv.lower()[2:]


def main():
    def print_version():
        click.secho(f'version {__version__}, A downloader that download the HLS/DASH stream.')

    parser = ArgumentParser(
        prog='XstreamDL-CLI',
        usage='XstreamDL-CLI [OPTION]... URL/FILE/FOLDER...',
        description='A downloader that download the HLS/DASH stream',
        add_help=False,
    )
    parser.add_argument('-V', '--version', action='store_true', help='Print version and exit')
    parser.add_argument('-h', '--help', action='store_true', help='Print this help message and exit')
    parser.add_argument('-save-dir', '--save-dir', default='Downloads', help='Set save dir for Stream')
    parser.add_argument('-base', '--base-url', default='', help='Set base url for Stream')
    parser.add_argument(
        '-select',
        '--select',
        action='store_true',
        help='Show stream to select and download, default is to download all')
    parser.add_argument(
        '-force-close',
        '--force-close',
        action='store_true',
        help='Make all connections closed securely, but it will make DL speed slower'
    )
    parser.add_argument('-b64key', '--b64key', default=None, help='base64 format aes key')
    parser.add_argument('-hexiv', '--hexiv', default=None, help='hex format aes iv')
    parser.add_argument('-repl', '--repl', action='store_true', help='Repl mode')

    dump_group = parser.add_argument_group('Dump options')
    dump_group.add_argument('-name', '--name', default='', help='Specific stream base name')

    parser.add_argument('URI', nargs='*', help='URL/FILE/FOLDER string')
    args = parser.parse_args()
    print(type(args.URI))
    exit()
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