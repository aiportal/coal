import peewee
from playhouse.signals import pre_save
from .database import MainModel, db_main


class CheckIn(MainModel):
    class Meta:
        db_table = 'CheckIn'
    ID = peewee.IntegerField(db_column='CheckId', primary_key=True)
    Name = peewee.CharField(db_column='BookCode', unique=True, help_text='票据号')
    Group = peewee.CharField(index=True, help_text='当班班组')
    BookTime = peewee.DateTimeField(index=True, help_text='登记时间')
    LeaveTime = peewee.DateTimeField(help_text='离场时间')
    Locality = peewee.CharField(help_text='产地', null=True)
    CarCode = peewee.CharField(help_text='车牌号', null=True)
    CoalType = peewee.CharField(help_text='煤种')
    TypeDesc = peewee.CharField(help_text='煤种说明', null=True)
    StoreCode = peewee.CharField(null=True, help_text='卸车场地')
    BookWeight = peewee.FloatField(help_text='矿发量/登记重量')
    RealWeight = peewee.FloatField(help_text='复秤量/实测重量')
    Difference = peewee.FloatField(help_text='误差重量')


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
    CarCode = peewee.CharField(help_text='车牌号', null=True)
    CoalType = peewee.CharField(help_text='煤种', null=True)
    StoreCode = peewee.CharField(help_text='卸车场地', null=True)
    BlackList = peewee.BooleanField(help_text='黑名单', null=True)
    WholeSeal = peewee.BooleanField(help_text='封条完好', null=True)
    WholeHeap = peewee.BooleanField(help_text='堆型完好', null=True)
    CheckResult = peewee.CharField(max_length=2000, help_text='检测结果', null=True)
    ExamResult = peewee.CharField(max_length=2000, help_text='抽检结果', null=True)
    ViolateRule = peewee.BooleanField(help_text='违规', null=True)
    ViolateReason = peewee.CharField(max_length=2000, help_text='违规原因', null=True)
    # Timestamp = peewee.DateTimeField(default=datetime.now, help_text='时间戳')

    @staticmethod
    def get_by_id(rid: str):
        r_in = CheckIn.get(ID=rid)      # type:CheckIn
        r_out = CheckOut.get(Name=r_in.Name)
        r_out.RealWeight = r_in.RealWeight
        return r_out


@pre_save(sender=CheckOut)
def check_parse_bool(sender, instance, created):
    r = instance                                                # type: CheckOut
    r.BlackList = str(r.BlackList).lower() == 'true'
    r.WholeSeal = str(r.WholeSeal).lower() == 'true'
    r.WholeHeap = str(r.WholeHeap).lower() == 'true'
    r.ViolateRule = str(r.ViolateRule).lower() == 'true'

if not CheckOut.table_exists():
    CheckOut.create_table()
