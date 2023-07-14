import peewee

import config

from .controler import db


class BaseModel(peewee.Model):
    id = peewee.AutoField()

    class Meta:
        database = db


class Device(BaseModel):
    name = peewee.CharField(null=True)
    ip = peewee.CharField(max_length=15, null=True)
    port = peewee.CharField(max_length=5, null=True)
    status = peewee.CharField(default=config.Status.un_status.value, null=True)
    last_discovery = peewee.FloatField(default=None, null=True)
    last_online = peewee.FloatField(default=None, null=True)
    monitoring = peewee.BooleanField()
    notification = peewee.BooleanField()
    position_index = peewee.IntegerField()

    class Meta:
        order_by = 'position_index'
