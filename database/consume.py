import peewee
from playhouse.signals import pre_save
from playhouse.hybrid import hybrid_property
from .database import MainModel
import uuid
from datetime import datetime


class ConsumeSend(MainModel):
    class Meta:
        db_table = 'ConsumeSend'
    ID = peewee.IntegerField(db_column='ConsumeId', primary_key=True)
    Name = peewee.CharField(db_column='ConsumeCode', unique=True, help_text='唯一标识')
    Group = peewee.CharField(index=True, help_text='当班班组')
    ConsumeTime = peewee.DateTimeField(index=True, help_text='发煤时间')
    ConsumeType = peewee.CharField(default='Send', help_text='发煤类型')
    StoreCode = peewee.CharField(help_text='堆场')
    BalanceCode = peewee.CharField(help_text='地磅', null=True)
    Amount = peewee.FloatField(help_text='数量')
    CoalType = peewee.CharField(help_text='煤种')
    Locality = peewee.CharField(help_text='产地')
    Destination = peewee.CharField(null=True, help_text='收货单位')


@pre_save(sender=ConsumeSend)
def consume_send_name(sender, instance, created):
    r = instance                                                    # type:ConsumeSend
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
    ConsumeTime = peewee.DateTimeField(index=True, help_text='发煤时间')
    ConsumeType = peewee.CharField(help_text='发煤类型')
    StoreCode = peewee.CharField(help_text='堆场')
    OutBalance = peewee.CharField(help_text='出库电子秤')
    OutStart = peewee.FloatField(help_text='接班值')
    OutEnd = peewee.FloatField(help_text='交班值')
    OutAmount = peewee.FloatField(help_text='出库计量数')
    InBalance = peewee.CharField(help_text='入炉电子秤')
    InStart = peewee.FloatField(help_text='接班值')
    InEnd = peewee.FloatField(help_text='交班值')
    InAmount = peewee.FloatField(help_text='入炉计量数')
    BufferCode = peewee.CharField(help_text='锅炉')

    # BalanceCode = peewee.CharField(default='', help_text='地磅')
    Amount = peewee.FloatField(help_text='加料数量')


@pre_save(sender=ConsumeFire)
def consume_fire_name(sender, instance, created):
    r = instance                                                # type:ConsumeFire
    r.OutAmount = float(r.OutEnd) - float(r.OutStart)
    r.InAmount = float(r.InEnd) - float(r.InStart)
    r.Amount = r.OutAmount
    if created:
        r.Name = str(uuid.uuid1()).replace('-', '').lower()


if not ConsumeFire.table_exists():
    ConsumeFire.create_table()


class FireRecord(MainModel):
    class Meta:
        db_table = 'ConsumeRecord'
    ID = peewee.IntegerField(db_column='RecordId', primary_key=True)
    Name = peewee.CharField(db_column='RecordCode', unique=True, help_text='唯一标识')
    Group = peewee.CharField(index=True, help_text='当班班组')
    RecordTime = peewee.DateTimeField(index=True, help_text='填报时间')
    PowerStart = peewee.FloatField(help_text='用电量/接班值')
    PowerEnd = peewee.FloatField(help_text='用电量/交班值')
    PowerAmount = peewee.FloatField(help_text='用电量/计量值')
    CoalStart = peewee.FloatField(help_text='用煤量/接班值')
    CoalEnd = peewee.FloatField(help_text='用煤量/交班值')
    CoalAmount = peewee.FloatField(help_text='用煤量/计量值')
    Ratio = peewee.FloatField(help_text='吨煤用电')
    Dust = peewee.FloatField(help_text='含粉量')
    Rock = peewee.FloatField(help_text='含矸量')


@pre_save(sender=FireRecord)
def consume_record_name(sender, instance, created):
    r = instance    # type:FireRecord
    r.PowerAmount = float(r.PowerEnd) - float(r.PowerStart)
    r.CoalAmount = float(r.CoalEnd) - float(r.CoalStart)
    r.Ratio = r.PowerAmount / r.CoalAmount
    if created:
        r.Name = str(uuid.uuid1()).replace('-', '').lower()


if not FireRecord.table_exists():
    FireRecord.create_table()
