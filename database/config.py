import peewee
from playhouse.signals import pre_save
from .database import MainModel
from hashlib import md5


class SysConfig(MainModel):
    class Meta:
        db_table = 'Configuration'
        indexes = (
            (("Subject", "ItemName"), True),
        )
    ID = peewee.IntegerField(db_column='ConfigId', primary_key=True)
    Subject = peewee.CharField(help_text='分类')
    ItemName = peewee.CharField(help_text='配置项名称')
    ItemValue = peewee.CharField(null=True, max_length=2000, help_text='配置项内容')
    ItemDesc = peewee.CharField(null=True, max_length=2000, help_text='配置项说明')
    ItemType = peewee.CharField(null=True, help_text='配置项数据类型')

    @staticmethod
    def getItem(subject: str, name: str):
        r, _ = SysConfig.get_or_create(Subject=subject, ItemName=name)
        return r

    @staticmethod
    def setItem(subject: str, name: str, value: str):
        r, _ = SysConfig.get_or_create(Subject=subject, ItemName=name)
        r.ItemValue = value
        r.save()

if not SysConfig.table_exists():
    SysConfig.create_table()
    pwd = md5(('bfbd'+'admin'+'bfbd').encode()).hexdigest()
    SysConfig.create(Subject='login', ItemName='admin', ItemValue=pwd)

