import peewee
from playhouse.signals import pre_save
from .database import MainModel
import uuid
from datetime import datetime


class ConsumeSend(MainModel):
    class Meta:
        db_table = 'ConsumeSend'
    ID = peewee.IntegerField(db_column='ConsumeId', primary_key=True)
    Name = peewee.CharField(db_column='ConsumeCode', unique=True, help_text='唯一标识')
    Group = peewee.CharField(index=True, help_text='当班班组')
    ConsumeTime = peewee.DateTimeField(help_text='发煤时间')
    ConsumeType = peewee.CharField(default='Send', help_text='发煤类型')
    StoreCode = peewee.CharField(help_text='堆场')
    BalanceCode = peewee.CharField(help_text='地磅', null=True)
    Amount = peewee.FloatField(help_text='数量')
    CoalType = peewee.CharField(help_text='煤种')
    Destination = peewee.CharField(null=True, help_text='收货单位')
    # Timestamp = peewee.DateTimeField(help_text='时间戳')


@pre_save(sender=ConsumeSend)
def consume_send_name(sender, instance, created):
    r = instance    # type:ConsumeSend
    if created:
        r.Name = str(uuid.uuid1()).replace('-', '').lower()


if not ConsumeSend.table_exists():
    ConsumeSend.create_table()


class ConsumeFire(MainModel):
    class Meta:
        db_table = 'ConsumeFire'
    ID = peewee.IntegerField(db_column='ConsumeId', primary_key=True)
    Name = peewee.CharField(db_column='ConsumeCode', unique=True, help_text='唯一标识')
    Group = peewee.CharField(index=True, help_text='当班班组')
    ConsumeTime = peewee.DateTimeField(help_text='发煤时间')
    ConsumeType = peewee.CharField(help_text='发煤类型')
    StoreCode = peewee.CharField(help_text='堆场')
    BalanceCode = peewee.CharField(help_text='地磅')
    Amount = peewee.FloatField(help_text='加料数量')
    OutBalance = peewee.CharField(help_text='出库电子秤')
    OutAmount = peewee.FloatField(help_text='出库计量数')
    InBalance = peewee.CharField(help_text='入炉电子秤')
    InAmount = peewee.FloatField(help_text='入炉计量数')
    BufferCode = peewee.CharField(help_text='锅炉')


@pre_save(sender=ConsumeFire)
def consume_fire_name(sender, instance, created):
    r = instance    # type:ConsumeFire
    if created:
        r.Name = str(uuid.uuid1()).replace('-', '').lower()


if not ConsumeFire.table_exists():
    ConsumeFire.create_table()


class FireRecord(MainModel):
    class Meta:
        db_table = 'ConsumeRecord'
    ID = peewee.IntegerField(db_column='ConsumeId', primary_key=True)
    Name = peewee.CharField(db_column='ConsumeCode', unique=True, help_text='唯一标识')
    Group = peewee.CharField(index=True, help_text='当班班组')
    StartTime = peewee.DateTimeField(help_text='起始时间')
    EndTime = peewee.DateTimeField(help_text='结束时间')
    RecordType = peewee.CharField(help_text='记录项目')
    Amount = peewee.FloatField(help_text='数值')


@pre_save(sender=FireRecord)
def consume_record_name(sender, instance, created):
    r = instance    # type:FireRecord
    if created:
        r.Name = str(uuid.uuid1()).replace('-', '').lower()


if not FireRecord.table_exists():
    FireRecord.create_table()
