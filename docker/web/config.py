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

# DIRS
CURRENT_DIR = Path.cwd() / env.str('WORK_DIR', default='.')

RESOURCES_DIR = CURRENT_DIR / 'resources'

LOG_DIR = RESOURCES_DIR / 'logs'

# Logs config
LOG_MODE = env.str("LOG_MODE", 'dev')

if LOG_MODE == "prod":
    # logging in prod mode
    if not Path.exists(LOG_DIR):
        Path.mkdir(LOG_DIR)
    logging.basicConfig(
        format=u'%(threadName)s\t%(filename)s\t[LINE:%(lineno)d]# %(levelname)-8s\t [%(asctime)s]  %(message)s',
        level="INFO",
        handlers=[logging.FileHandler(LOG_DIR / "log.log", 'w', 'utf-8')]
    )
elif LOG_MODE == "dev":
    # logging in dev mode
    logging.basicConfig(
        format=u'%(threadName)s\t%(filename)s\t[LINE:%(lineno)d]# %(levelname)-8s\t [%(asctime)s]  %(message)s',
        level="DEBUG",
        handlers=[logging.StreamHandler()]
    )


DEBUG = env.bool('DEBUG', default=True)

TIME_ZONE = timezone(env.str('TIME_ZONE', 'UTC'))

FORMAT_NOTIFICATION = env.str('FORMAT_NOTIFICATION', None)

DISCOVERY_PERIOD_SEC = env.int('DISCOVERY_PERIOD_SEC', default=30)
DISCOVERY_WORKER_POOL = env.int('DISCOVERY_WORKER_POOL', default=10) 

IMPL = env.str('EXECUTOR_SERVICE_IMPL', 'PingExecutorService')

# Telegram_bot
BOT_TOKEN = env.str('BOT_TOKEN', default='')
CHATS_ID = env.list('CHATS_ID', default=[])

# Gotify_server
GOTIFY_IP = env.str('GOTIFY_IP', default='localhost')
GOTIFY_PORT = env.int('GOTIFY_PORT', default=8080)
GOTIFY_APP_TOKEN = env.str('GOTIFY_APP_TOKEN', default='')
