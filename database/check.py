import peewee
from playhouse.signals import pre_save
from .database import MainModel, db_main


class CheckIn(MainModel):
    class Meta:
        db_table = 'CheckIn'
    ID = peewee.IntegerField(db_column='CheckId', primary_key=True)
    Name = peewee.CharField(db_column='BookCode', unique=True, help_text='票据号')
    SeqNum = peewee.CharField(help_text='编号')
    Group = peewee.CharField(index=True, help_text='当班班组')
    User = peewee.CharField(help_text='操作员')
    BookTime = peewee.DateTimeField(index=True, help_text='登记时间')
    Locality = peewee.CharField(help_text='产地', null=True)
    CarCode = peewee.CharField(help_text='车牌号', null=True)
    CoalType = peewee.CharField(help_text='煤种')
    StoreCode = peewee.CharField(help_text='卸车地点')
    BookWeight = peewee.FloatField(help_text='矿发量/登记重量')
    RealWeight = peewee.FloatField(help_text='复秤量/实测重量')
    Difference = peewee.FloatField(help_text='误差重量')
    LeaveTime = peewee.DateTimeField(null=True, help_text='离场时间')
    LeaveGroup = peewee.CharField(null=True, help_text='离场班组')
    LeaveUser = peewee.CharField(null=True, help_text='离场操作员')


@pre_save(sender=CheckIn)
def check_difference(sender, instance, created):
    r = instance                                                    # type:CheckIn
    r.Difference = float(r.RealWeight) - float(r.BookWeight)

if not CheckIn.table_exists():
    CheckIn.create_table()


class CheckOut(MainModel):
    class Meta:
        db_table = 'CheckOut'
    ID = peewee.IntegerField(db_column='CheckId', primary_key=True)
    Name = peewee.CharField(db_column='BookCode', unique=True, help_text='票据号')
    Group = peewee.CharField(index=True, help_text='当班班组')
    User = peewee.CharField(index=True, help_text='操作员')
    CarCode = peewee.CharField(null=True, help_text='车牌号')
    CoalType = peewee.CharField(null=True, help_text='煤种')
    # Check
    Water = peewee.FloatField(null=True, help_text='水分')
    Impurity = peewee.FloatField(null=True, help_text='灰分')
    ViolateRule = peewee.BooleanField(null=True, help_text='违规')
    ViolateReason = peewee.CharField(null=True, max_length=2000, help_text='违规原因')
    # Gps
    StartTime = peewee.DateTimeField(null=True, help_text='开始时间')
    ArriveTime = peewee.DateTimeField(null=True, help_text='到场时间')
    CheckResult = peewee.CharField(null=True, max_length=2000, help_text='查询情况')
    WholeHeap = peewee.BooleanField(null=True, help_text='堆型完好')
    Comment = peewee.CharField(null=True, max_length=2000, help_text='备注')


@pre_save(sender=CheckOut)
def check_parse_fields(sender, instance, created):
    r = instance                                                # type: CheckOut
    r.Water = r.Water and float(r.Water) or None
    r.Impurity = r.Impurity and float(r.Impurity) or None
    r.ViolateRule = str(r.ViolateRule).lower() == 'true'
    r.WholeHeap = str(r.WholeHeap).lower() == 'true'

if not CheckOut.table_exists():
    CheckOut.create_table()
