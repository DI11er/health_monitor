import config

from queue import Queue

from models import Device

from services.discoveryWorker import DiscoveryWorker
from services.deviceRegistryService import DeviceRegistryService


class DiscoveryService:
    _instance = None
    _deviceRegistryService = None
    _discoveryWorkerPool = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """ Патерн Singleton """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self._deviceRegistryService = DeviceRegistryService.get_instance()
        self._discoveryWorkerPool = config.DISCOVERY_WORKER_POOL

    def discover_divices(self):
        queue = Queue()
        devices: Device = self._deviceRegistryService.get_all_devices()

        for _ in range(len(devices) if len(devices) < self._discoveryWorkerPool else self._discoveryWorkerPool):
            t = DiscoveryWorker(queue)
            t.setDaemon(True)
            t.start()

        for device in devices:
            if device.monitoring:
                queue.put(device)
        
        queue.join()

