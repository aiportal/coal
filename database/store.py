import peewee
from playhouse.signals import pre_save
from .database import MainModel
import uuid
from datetime import datetime


class Storage(MainModel):
    class Meta:
        db_table = 'Storage'
    ID = peewee.IntegerField(db_column='StoreId', primary_key=True)
    Name = peewee.CharField(db_column='StoreCode', help_text='唯一标识')
    Description = peewee.CharField(null=True, max_length=2000, help_text='说明')
    CoalType = peewee.CharField(null=True, help_text='煤种')
    Amount = peewee.FloatField(default=0, help_text='数量')

    @staticmethod
    def AddStorage(store_code: str, weight: float):
        weight = abs(weight)
        q = Storage.select().where(Storage.Name == store_code)
        if not q.exists():
            Storage.create(Name=store_code)
        s = q[0]
        s.Amount += weight
        s.save()

    @staticmethod
    def SubStorage(store_code: str, weight: float):
        weight = abs(weight)
        q = Storage.select().where(Storage.Name == store_code)
        if not q.exists():
            raise Exception('库存不足')
        s = q[0]
        if s.Amount < weight:
            raise Exception('库存不足')
        s.Amount -= weight
        s.save()

    @classmethod
    def MoveStorage(cls, src_store: str, dst_store: str, weight: float):
        if src_store == dst_store:
            return
        if src_store:
            cls.SubStorage(src_store, weight)
        if dst_store:
            cls.AddStorage(dst_store, weight)

if not Storage.table_exists():
    Storage.create_table()


class StoreMove(MainModel):
    class Meta:
        db_table = 'StoreMove'
    ID = peewee.IntegerField(db_column='MoveId', primary_key=True)
    Name = peewee.CharField(db_column='MoveCode', unique=True, help_text='唯一标识')
    Group = peewee.CharField(index=True, help_text='当班班组')
    MoveTime = peewee.DateTimeField(index=True, help_text='操作时间')
    MoveType = peewee.CharField(help_text='操作类型')
    StoreCode = peewee.CharField(help_text='来源堆场')
    BalanceCode = peewee.CharField(help_text='地磅/输送带', null=True)
    BalanceStart = peewee.FloatField(null=True, help_text='接班值')
    BalanceEnd = peewee.FloatField(null=True, help_text='交班值')
    Locality = peewee.CharField(help_text='产地', null=True)
    CoalType = peewee.CharField(help_text='煤种')
    DestStore = peewee.CharField(help_text='卸车地点')
    Amount = peewee.FloatField(help_text='数量')


@pre_save(sender=StoreMove)
def store_name(sender, instance, created):
    r = instance                                                        # type:StoreMove
    if r.BalanceStart and r.BalanceEnd:
        r.Amount = float(r.BalanceEnd) - float(r.BalanceStart)
    if created:
       r.Name = str(uuid.uuid1()).replace('-', '').lower()


if not StoreMove.table_exists():
    StoreMove.create_table()
