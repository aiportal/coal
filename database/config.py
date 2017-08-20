import peewee
from playhouse.signals import pre_save
from .database import MainModel
from hashlib import md5


class Configuration(MainModel):
    class Meta:
        db_table = 'Configuration'
    ID = peewee.IntegerField(db_column='ConfigId', primary_key=True)
    Subject = peewee.CharField(help_text='分类')
    ItemName = peewee.CharField(help_text='配置项名称')
    ItemValue = peewee.CharField(null=True, max_length=2000, help_text='配置项内容')
    ItemDesc = peewee.CharField(null=True, max_length=2000, help_text='配置项说明')
    ItemType = peewee.CharField(null=True, help_text='配置项数据类型')


if not Configuration.table_exists():
    Configuration.create_table()
    pwd = md5(('bfbd'+'admin'+'bfbd').encode()).hexdigest()
    Configuration.create(Subject='login', ItemName='admin', ItemValue=pwd)
