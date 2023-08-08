import logging

import config

import threading

import time

import pytz

import requests

from models import db, Device

from flask import Flask, render_template, url_for, request, redirect

from services.discoveryService import DiscoveryService
from services.deviceRegistryService import DeviceRegistryService
from services.notificationService import NotificationService

from datetime import datetime

notificationService = NotificationService.get_instance()
discoveryService = DiscoveryService.get_instance()
deviceRegistryService = DeviceRegistryService.get_instance()

_log = logging.getLogger(__name__)

def do_discovery():
    while True:
        try:
            discoveryService.discover_divices()
        except Exception as _ex:
            message = f'ERROR DISCOVERY! {_ex}'
            notificationService.notify(message, title='ERROR', priority=10)
            _log.error(message)
        time.sleep(config.DISCOVERY_PERIOD_SEC)

threading.Thread(target=do_discovery, args=(), daemon=True).start()


app = Flask(__name__)


@app.route('/')
def index():
    def _pretty_view(value):
        return '-' if value is None or not value else value

    def _pretty_datetime(data):
        try:
            if data is not None:
                return datetime.fromtimestamp(data, config.TIME_ZONE).strftime("%d.%m.%Y %H:%M:%S")
        except Exception as _ex:
            _log.error(f"Cannot format for datetime: {_ex}")
        return "-"

    context = {
        'title': 'Монитор устройств',
        'devices': [{
            'id': device.id,
            'name': _pretty_view(device.name),
            'ip': _pretty_view(device.ip),
            'port': _pretty_view(device.port),
            'status': device.status,
            'last_discovery': _pretty_datetime(device.last_discovery),
            'last_online': _pretty_datetime(device.last_online),
            'monitoring': device.monitoring
        } for device in deviceRegistryService.get_all_devices()],
        'menu': (
            {'url': url_for('add_device'), 'title': 'Регистрация устройства'},
        )
    }

    return render_template('index.html', **context)

@app.route('/add_device/', methods=['post', 'get'])
def add_device():
    if request.method == 'POST':
        name = request.form.get('name','')
        ip = request.form.get('ip', '')
        port = request.form.get('port', '')
        monitoring = True if request.form.get('monitoring', False) == 'on' else False
        notification = True if request.form.get('notification', False) == 'on' else False
        position_index = request.form.get('position_index', 10)
        
        deviceRegistryService.add_device(
            name=name, 
            ip=ip, 
            port=port, 
            monitoring=monitoring, 
            notification=notification, 
            position_index=position_index
        )
        return redirect(url_for('index'))
    context = {
        'title': 'Регистрация устройства',
        'menu': (
        )
    }
    return render_template('add_device.html', **context)

@app.route('/edit_device/<int:id_device>', methods=['post', 'get'])
def edit_device(id_device):
    context = {
        'title': 'Настройка устройства',
        'menu': (
            {'url': url_for('add_device'), 'title': 'Регистрация устройства'},
        )
    }

    if request.method == 'POST' and request.form.get('update'):
        name = request.form.get('name', '')
        ip = request.form.get('ip', '')
        port = request.form.get('port', '')
        monitoring = True if request.form.get('monitoring', False) == 'on' else False
        notification = True if request.form.get('notification', False) == 'on' else False
        position_index = request.form.get('position_index', 10)
        
        deviceRegistryService.update_device(
            id_device, 
            name=name, 
            ip=ip, 
            port=port, 
            monitoring=monitoring, 
            notification=notification, 
            position_index=position_index
        )
        return redirect(url_for('index'))
    elif request.method == 'POST' and request.form.get('delete'):
        deviceRegistryService.delete_device(id_device)
        return redirect(url_for('index'))
    else:
        context['device'] = Device.get_by_id(id_device)
        if context['device'].port:
            context['url_device'] = f"http://{context['device'].ip}:{context['device'].port}"
        else:
            try:
                requests.get(f"http://{context['device'].ip}", timeout=1)
                context['url_device'] = f"http://{context['device'].ip}"
            except:
                _log.info('На устройстве отсутствует веб-сервер')

    return render_template('edit_device.html', **context)



if __name__ == "__main__":
    with db:
        if not 'Device' in db.get_tables():
            db.create_tables([Device])

    app.run(
        host='0.0.0.0',
        port=5090,
        debug=config.DEBUG,
        use_reloader=False # отключает автоматическую перезагрузку приложения при изменении в коде
    )
