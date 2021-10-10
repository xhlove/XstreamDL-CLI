import json
from logging import Logger
from XstreamDL_CLI.cmdargs import CmdArgs


class Headers:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.referer = ''
        self.user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/88.0.4324.190 Safari/537.36'
        )
        self.headers = {}

    def get(self, args: CmdArgs) -> dict:
        self.__generate(args)
        return self.headers

    def __generate(self, args: CmdArgs):
        '''
        - 不指定user-agent 使用默认值
        - 指定user-agent 使用指定值 如果为"" 那么user-agent就是""
        - 不指定referer 就不设定referer 否则设定
        '''
        if args.user_agent != '':
            self.headers['user-agent'] = args.user_agent
        else:
            self.headers['user-agent'] = self.user_agent
        if args.referer != '':
            self.headers['referer'] = args.referer
        if args.headers != '':
            self.__add_headers(args.headers)
        self.logger.debug(f'use headers:\n{json.dumps(self.headers, ensure_ascii=False, indent=4)}')

    def __add_headers(self, text: str):
        text = text.strip()
        for one_header in text.split('|'):
            data = one_header.strip().split(':', maxsplit=1)
            if len(data) == '':
                continue
            if len(data) == 1:
                self.headers[data[0]] = ''
            else:
                self.headers[data[0]] = data[1]