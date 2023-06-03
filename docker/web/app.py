import logging

import config

import threading

import time

from models import db, Device

from flask import Flask, render_template, url_for

from services.discoveryService import DiscoveryService
from services.deviceRegistryService import DeviceRegistryService
from services.notificationService import NotificationService


notificationService = NotificationService.get_instance()
discoveryService = DiscoveryService.get_instance()
deviceRegistryService = DeviceRegistryService.get_instance()

def do_discovery():
    while True:
        try:
            discoveryService.discover_divices()
        except Exception as _ex:
            notificationService.notify(f'ERROR DISCOVERY! {_ex}')
        time.sleep(config.DISCOVERY_PERIOD_SEC)


threading.Thread(target=do_discovery, args=(), daemon=True).start()


app = Flask(__name__)
app.logger = logging.getLogger(__name__)


@app.route('/')
def index():
    def _pretty_view(value):
        return '-' if value is None else value
    
    devices = []
    for device in deviceRegistryService.get_all_devices():
        devices.append({
            'id': device.id,
            'name': _pretty_view(device.name),
            'ip': _pretty_view(device.ip),
            'port': _pretty_view(device.port),
            'status': device.status,
            'last_discovery': _pretty_view(device.last_discovery),
            'last_online': _pretty_view(device.last_online),
            'monitoring': device.monitoring
        })
    context = {
        'title': 'Монитор устройств',
        'devices': devices,
    }
    deviceRegistryService._add_device_for_json()

    return render_template('index.html', **context)


if __name__ == "__main__":
    with db:
        if not 'Device' in db.get_tables():
            db.create_tables([Device])

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
