import logging

from pathlib import Path

from environs import Env

from enum import Enum

from pytz import timezone

env = Env()
env.read_env()

class Status(Enum):
    live = 'green'
    dead = 'red'
    stopped = 'grey'
    un_status = None

CURRENT_DIR = Path.cwd() / env.str('WORK_DIR', default='.')

RESOURCES_DIR = CURRENT_DIR / 'resources'

logging.basicConfig(filename=RESOURCES_DIR / 'logs' / 'sample.log', level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)

HOST = env.str('HOST', default='0.0.0.0')
PORT = env.int('PORT', default=8000)
DEBUG = env.bool('DEBUG', default=True)

TIME_ZONE = timezone(env.str('TIME_ZONE', 'UTC'))

FORMAT_NOTIFICATION = env.str('FORMAT_NOTIFICATION', 'bot')

DISCOVERY_PERIOD_SEC = env.int('DISCOVERY_PERIOD_SEC', default=30)
DISCOVERY_WORKER_POOL = env.int('DISCOVERY_WORKER_POOL', default=10) 

IMPL = env.str('EXECUTOR_SERVICE_IMPL', 'PingExecutorService')

BOT_TOKEN = env.str('BOT_TOKEN', default='')
CHAT_ID = env.str('CHAT_ID', default='')

GOTIFY_IP = env.str('GOTIFY_IP', default='localhost')
GOTIFY_PORT = env.int('GOTIFY_PORT', default=8080)
GOTIFY_APP_TOKEN = env.str('GOTIFY_APP_TOKEN', default='')
