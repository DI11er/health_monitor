import sys

import subprocess

import requests

import logging

class PingExecutorService:
    _log = None

    def __init__(self) -> None:
        self._log = logging.getLogger(__name__)
        self._os_info = sys.platform

    def exec_ping(self, ip, port=None, count=1, timeout=5) -> bool:  
        if port:
            try:
                response = requests.get(f'http://{ip}:{port}', timeout=timeout)
            except Exception as _ex:
                self._log.error(f'{_ex}')
                return False
            else:
                self._log.debug(f'Device: {ip}:{port} Response {response}')
                if response.status_code == '200':
                    return True

        if self._os_info in ('win32', 'cygwin'):
            command = ['ping', '-n', f'{count}', '-w', f'{timeout}', f'{ip}']
        elif self._os_info in ('linux', 'darwin'):
            command = ['ping', '-c', f'{count}', '-W', f'{timeout}', f'{ip}']

        response = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _ = response.communicate()
        response_code = response.returncode
        self._log.debug(f'Device: {ip} Response {response_code}')
        
        return response_code == 0