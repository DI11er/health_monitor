import config

from peewee import SqliteDatabase


db = SqliteDatabase(config.RESOURCES_DIR / 'db' / 'HealthMonitor.db')
