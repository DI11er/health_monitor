import logging

import json

import config

from models import Device


class DeviceRegistryService:
    _instance = None
    _log = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """ Патерн Singleton """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self._log = logging.getLogger(__name__)

    def get_all_devices(self):
        self._add_device_for_json()
        return Device.select().order_by(Device.position_index)
    
    def update_device(self, id, *args, **kwargs):
        """ name: str, ip: str, port: str, last_discovery: datetime, 
        last_online: datetime, monitoring: bool, notification: bool """
        d: Device = Device.get_by_id(pk=id)
        d.name=kwargs.pop('name', None)
        d.ip = kwargs.pop('ip', None)
        d.port = kwargs.pop('port', None)
        d.monitoring = kwargs.pop('monitoring', True)
        d.notification = kwargs.pop('notification', False)
        d.position_index = kwargs.pop('position_index', 1)
        d.save()

    def delete_device(self, id):
        Device.get_by_id(pk=id).delete_instance()

    def add_device(self, *args, **kwargs):
        """ name: str, ip: str, port: int, last_discovery: datetime, 
        last_online: datetime, monitoring: bool, notification: bool """
        Device.create(
            name=kwargs.pop('name', None), 
            ip = kwargs.pop('ip', None),
            port = kwargs.pop('port', None),
            monitoring = kwargs.pop('monitoring', True),
            notification = kwargs.pop('notification', False),
            position_index = kwargs.pop('position_index', 1)
        )
    
    def _add_device_for_json(self):
        path_dir = config.RESOURCES_DIR / 'devices'
        if path_dir:
            try:
                for i in path_dir.iterdir():
                    with open(i, 'r', encoding='utf-8') as f:
                        self.add_device(**json.load(f))
                    i.unlink()
            except Exception as _ex:
                self._log.error(f'{_ex}')
        return
