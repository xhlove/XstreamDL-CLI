import sys
import click
from argparse import ArgumentParser

from .version import __version__
from .downloader import Downloader


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
    parser.add_argument('-split', '--split', action='store_true', help='Split by Period for each full stream')
    parser.add_argument('-repl', '--repl', action='store_true', help='Repl mode')

    dump_group = parser.add_argument_group('Dump options')
    dump_group.add_argument('-n', '--name', default=None, help='Specific stream base name')

    parser.add_argument('URI', nargs='*', help='URL/FILE/FOLDER string')

    args = parser.parse_args()
    if args.help:
        print_version()
        parser.print_help()
        sys.exit()
    if args.version:
        print_version()
        sys.exit()
    if len(args.URI) == 0:
        sys.exit('Paste your URL/FILE/FOLDER string at the end of commands, plz')
    downloader = Downloader()
    downloader.daemon(args)


if __name__ == '__main__':
    main()