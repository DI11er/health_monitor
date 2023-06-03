import peewee

import config

from .controler import db


class BaseModel(peewee.Model):
    id = peewee.AutoField()

    class Meta:
        database = db
        orders_by = 'id'


class Device(BaseModel):
    name = peewee.CharField(default='')
    ip = peewee.CharField(max_length=15, default='')
    port = peewee.IntegerField(null=True, default=None)
    status = peewee.CharField(default=config.Status.un_status.value, null=True)
    last_discovery = peewee.TimestampField(null=True, utc=True)
    last_online = peewee.TimestampField(null=True, utc=True)
    monitoring = peewee.BooleanField(default=True)
    notification = peewee.BooleanField(default=False)
    position_index = peewee.IntegerField(default=1)

    class Meta:
        order_by = 'position_index'