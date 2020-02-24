# coding: utf-8

import re

from hydra.core.base import HydraBase
from hydra.core.log import logger


class FtpBrute(object):

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self._hydra_proxy = kwargs.get('hydra_proxy', None)
        self._hydra_proxy_http = kwargs.get('hydra_proxy_http', None)
        self._hydra_proxy_auth = kwargs.get('hydra_proxy_auth', None)
        self._host = kwargs.get('host',)
        self._port = kwargs.get('port', 21)
        self._task = kwargs.get('task', 1)
        self._hydra = HydraBase(
            hydra_proxy=self._hydra_proxy,
            hydra_proxy_http=self._hydra_proxy_http,
            hydra_proxy_auth=self._hydra_proxy_auth,
        )
        self._nsr = None

    def start(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        result = {
            'login': '',
            'password': '',
            'host': self._host,
            'port': self._port,
            'service': 'ftp',
        }
        userfile = kwargs.get('user_file')
        pwdfile = kwargs.get('pwd_file')
        username = kwargs.get('username', 'anonymous')
        password = kwargs.get('password')

        if not any((pwdfile, password)):
            self._nsr = True
            logger.info('[*] Enable null password detection.')

        cmd = [self._hydra.path, '-o', '-', '-t', '{0}'.format(self._task), '-I'] + \
              ['-L', userfile] * (True if userfile else False) + \
              ['-P', pwdfile] * (True if pwdfile else False) + \
              ['-l', username] * (True if username else False) + \
              ['-p', password] * (True if password else False) + \
              ['-e', 'nsr'] * (True if self._nsr else False) + \
              ['ftp://{0}:{1}'.format(self._host, self._port), '|', 'cat']

        out = self._hydra.run_command(cmd)

        if out:
            for item in out.split('\n'):
                g = re.search(r'login:\s{1}(.+?)\s+password:\s{1}(.+)', item)
                if g:
                    result['login'] = g.group(1)
                    result['password'] = g.group(2)

        return result
