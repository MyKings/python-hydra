#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import sys

from hydra.core.exception import HydraNotFoundException
from hydra.core.exception import HydraRunTimeoutException
from hydra.core.log import logger


class HydraBase(object):

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self._version = ''
        self._process = None
        self._timeout = kwargs.get('timeout', -1)
        search_path = kwargs.get('search_path', None)
        self._hydra_proxy = kwargs.get('hydra_proxy', None)
        self._hydra_proxy_http = kwargs.get('hydra_proxy_http', None)
        self._hydra_proxy_auth = kwargs.get('hydra_proxy_auth', None)

        if search_path and isinstance(search_path, str):
            self._hydra_path = search_path
        else:
            search_path = [
                'hydra',
                '/usr/bin/hydra',
                '/usr/local/bin/hydra',
                '/opt/local/bin/hydra'
            ]
            for path in search_path:
                try:
                    self.run_command([path])
                except OSError:
                    pass
                else:
                    self._hydra_path = path
                    break
            else:
                raise HydraNotFoundException(
                    'hydra program was not found in path. PATH is : {0}'.format(
                        os.getenv('PATH')
                    )
                )

    def run_command(self, cmd):
        """

        :param cmd:
        :return:
        """
        result = ''
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)
        #print(cmd)

        if self._hydra_proxy:
            os.environ['HYDRA_PROXY'] = self._hydra_proxy
        if self._hydra_proxy_http:
            os.environ['HYDRA_PROXY_HTTP'] = self._hydra_proxy_http
        if self._hydra_proxy_auth:
            os.environ['HYDRA_PROXY_AUTH'] = self._hydra_proxy_auth

        if sys.platform.startswith('freebsd') \
                or sys.platform.startswith('linux') \
                or sys.platform.startswith('darwin'):
            self._process = subprocess.Popen(
                cmd,
                bufsize=10000,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                close_fds=True
            )
        else:
            self._process = subprocess.Popen(
                cmd,
                bufsize=10000,
                stdout=subprocess.PIPE
            )

        try:
            if self._timeout > 0:
                self._process.wait(self._timeout)
            else:
                self._process.wait()

            out, cmd_err = self._process.communicate()
            if not cmd_err:
                result = out.decode()
            else:
                raise Exception(cmd_err)
        except subprocess.TimeoutExpired as ex:
            logger.warning('[-] {0}'.format(ex))
            raise ex
        except Exception as ex:
            raise ex
        finally:
            self._process.kill()

        return result

    @property
    def version(self):
        if not self._version:
            self._version = self.run_command([self._hydra_path])
            self._version = self.version.decode().split('\n')[0]
            self._version = self._version.split('-')[0]

        return self._version

    @property
    def path(self):
        return self._hydra_path

    @property
    def process(self):
        return self._process
