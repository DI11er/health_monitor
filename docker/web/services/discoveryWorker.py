import logging

import threading

import time

import config

from models import Device

from datetime import datetime

from services.executorService import ExecutorService
from services.notificationService import NotificationService
from services.deviceRegistryService import DeviceRegistryService


class DiscoveryWorker(threading.Thread):
    _queue = None
    _log = None
    _ns = None
    _deviceRegistryService = None
    _executorService = None

    def __init__(self, queue, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._queue = queue
        self._log = logging.getLogger(__name__)
        self._ns = NotificationService.get_instance()
        self._deviceRegistryService = DeviceRegistryService.get_instance()
        self._executorService = ExecutorService.get_instance()

    def run(self) -> None:
        while True:
            device_dto: Device = self._queue.get()
            self._discovery_device(device_dto)
            self._queue.task_done()
            
    def _discovery_device(self, device_dto: Device):
        self._log.debug(f'Start discovery device {device_dto.name} ip: {device_dto.ip} port: {device_dto.port}')
        ping_response = self._executorService.exec_ping(ip=device_dto.ip, port=device_dto.port, count=1, timeout=5)
        
        if not ping_response:
            time.sleep(2)
            ping_response = self._executorService.exec_ping(ip=device_dto.ip, port=device_dto.port, count=3, timeout=15)

        if not ping_response:
            if device_dto.status in (config.Status.live.value, config.Status.un_status.value): 
                device_dto.status = config.Status.dead.value
                if device_dto.notification:
                    self._ns.notify(message=f'{device_dto.name} is offline!', title='WARNING', priority=10)
        else:
            device_dto.last_online = datetime.now().timestamp()
            if device_dto.status in (config.Status.dead.value, config.Status.un_status.value):
                device_dto.status = config.Status.live.value
                if device_dto.notification:
                    self._ns.notify(message=f'{device_dto.name} is online!', title='INFO', priority=1)
        device_dto.last_discovery = datetime.now().timestamp()
        device_dto.save()





