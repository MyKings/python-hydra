# coding: utf-8

import re
import os
import logging

from hydra.core.base import HydraBase
from hydra.core.log import logger


class VNCBrute(object):

    def __init__(self, **kwargs):
        self._hydra_proxy = kwargs.get('hydra_proxy', None)
        self._hydra_proxy_http = kwargs.get('hydra_proxy_http', None)
        self._hydra_proxy_auth = kwargs.get('hydra_proxy_auth', None)
        self._host = kwargs.get('host', )
        self._port = kwargs.get('port', 5901)
        self._task = kwargs.get('task', 1)
        self._hydra = HydraBase(
            hydra_proxy=self._hydra_proxy,
            hydra_proxy_http=self._hydra_proxy_http,
            hydra_proxy_auth=self._hydra_proxy_auth,
        )

    def start(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        result = {
            'host': '',
            'password': '',
            'port': self._port,
            'service': 'vnc',
        }
        pwdfile = kwargs.get('pwd_file')
        password = kwargs.get('password')

        if pwdfile and not os.path.isfile(pwdfile):
            raise FileNotFoundError(pwdfile)

        cmd = [self._hydra.path, '-o', '-', '-I', '-t', '{0}'.format(self._task)] + \
              ['-P', pwdfile] * (True if pwdfile else False) + \
              ['-p', '{0}'.format(password)] * (True if password else False) + \
              ['vnc://{0}:{1}'.format(self._host, self._port), '|', 'cat']

        out = self._hydra.run_command(cmd)

        if out:
            for item in out.split('\n'):
                g = re.search(r'host:\s{1}(.+?)\s+password:\s{1}(.+)', item)
                if g:
                    result['host'] = g.group(1)
                    result['password'] = g.group(2)

        return result
