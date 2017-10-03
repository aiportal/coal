from flask import request, session
from flask.views import View
from playhouse.shortcuts import model_to_dict
from database import db_main
from database.check import CheckIn, CheckOut
from database.store import Storage
from database.config import Account
import json
from datetime import datetime, timedelta


DATETIME_FMT = '%Y-%m-%d %H:%M'


class CheckService(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        try:
            m = request.args['$m']
            f = getattr(self, m)
            return f()
        except Exception as e:
            return json.dumps({"Exception": str(e)}, ensure_ascii=False)

    @staticmethod
    def ListCheckIn():
        view_all = request.args.get('view') == 'all'
        q = CheckIn.select().order_by(+CheckIn.BookTime)
        if not view_all:
            # 编辑页面只显示24小时内的信息
            start = datetime.now() - timedelta(days=1)
            q = q.where(CheckIn.TimeStamp > start)

        page, rows = request.form.get('page') or 1, request.form.get('rows') or 50
        q = q.paginate(int(page), int(rows))

        args = request.args
        start, end = args.get('start'), args.get('end')
        if start:
            q = q.where(CheckIn.BookTime > datetime.strptime(start, DATETIME_FMT))
        if end:
            q = q.where(CheckIn.BookTime < datetime.strptime(end, DATETIME_FMT))

        Name, CarCode, StoreCode = args.get('Name'), args.get('CarCode'), args.get('StoreCode')
        if Name:
            q = q.where(CheckIn.Name.contains(Name))
        if CarCode:
            q = q.where(CheckIn.CarCode.contains(CarCode))
        if StoreCode:
            q = q.where(CheckIn.StoreCode.contains(StoreCode))

        js = json.dumps({
            'total': q.count(True),
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @classmethod
    def SetCheckIn(cls):
        cls.check_book_code()
        cls.check_book_time()
        r = CheckIn.new(request.form)                                       # type:CheckIn
        r_db = r.ID and CheckIn.get(ID=r.ID) or None                        # type:CheckIn
        r_copy = CheckOut.new(request.form)                                 # type:CheckOut
        cls.set_user(r)
        cls.set_user(r_copy)
        with db_main.atomic():
            r.save()
            if r_db:
                Storage.SubStorage(r_db.StoreCode, r_db.RealWeight)         # 恢复库存
            Storage.AddStorage(r.StoreCode, float(r.RealWeight))            # 加库存
            r_copy.save()

        r = CheckIn.get(Name=r.Name)
        return str(r)

    @staticmethod
    def check_book_code():  # 检查表单编号是否存在
        if request.form.get('ID'):
            return
        name = request.form.get('Name')
        q = CheckIn.select().where(CheckIn.Name == name)
        if q.exists():
            raise Exception('表单编号已存在')

    @staticmethod
    def check_book_time():
        min_time = datetime.now() - timedelta(hours=12)
        max_time = datetime.now() + timedelta(hours=1)
        book_time = request.form.get('BookTime')
        book_time = datetime.strptime(book_time, DATETIME_FMT)
        if min_time < book_time < max_time:
            return
        raise Exception('登记时间应在12小时以内')

    @staticmethod
    def RemoveCheckIn():
        rid = request.form['id']
        r = CheckIn.get(ID=rid)
        q1 = CheckIn.delete().where(CheckIn.Name == r.Name)
        q2 = CheckOut.delete().where(CheckOut.Name == r.Name)
        with db_main.atomic():
            Storage.SubStorage(r.StoreCode, r.RealWeight)           # 删除前减库存
            q1.execute()
            q2.execute()
        return 'true'

    @staticmethod
    def ListCheckOut():
        view_all = request.args.get('view') == 'all'
        q = CheckOut.select().order_by(+CheckOut.TimeStamp)
        if not view_all:
            start = datetime.now() - timedelta(days=1)
            q = q.where(CheckOut.TimeStamp > start)

        page, rows = request.form.get('page') or 1, request.form.get('rows') or 50
        q = q.paginate(int(page), int(rows))

        args = request.args
        start, end = args.get('start'), args.get('end')
        if start:
            q = q.where(CheckOut.TimeStamp > datetime.strptime(start, DATETIME_FMT))
        if end:
            q = q.where(CheckOut.TimeStamp < datetime.strptime(end, DATETIME_FMT))

        startGps, endGps = args.get('startGps'), args.get('endGps')
        if startGps:
            q = q.where(CheckOut.StartTime > datetime.strptime(startGps, DATETIME_FMT))
        if endGps:
            q = q.where(CheckOut.StartTime < datetime.strptime(endGps, DATETIME_FMT))

        Name, CarCode = args.get('Name'), args.get('CarCode')
        if Name:
            q = q.where(CheckOut.Name.contains(Name))
        if CarCode:
            q = q.where(CheckOut.CarCode.contains(CarCode))

        js = json.dumps({
            'total': q.count(True),
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @staticmethod
    def SetCheckOut():
        r_form = CheckOut.new(request.form)         # type:CheckOut
        if not r_form.ID:
            raise Exception('错误操作：检测记录不可添加')
        with db_main.atomic():
            r_form.TimeStamp = ('{0:' + DATETIME_FMT + '}').format(datetime.now())
            r_form.save()

        r = CheckOut.get(Name=r_form.Name)
        return str(r)

    @staticmethod
    def SumCheckIn():
        args = request.args
        start, end = args.get('start'), args.get('end')
        Group, Locality = args.get('Group'), args.get('Locality')
        CoalType, StoreCode  = args.get('CoalType'), args.get('StoreCode')
        if not start or not end:
            return '[]'
        q = CheckIn.select().where(start <= CheckIn.BookTime <= end)
        if Group:
            q = q.where(CheckIn.Group.contains(Group))
        if Locality:
            q = q.where(CheckIn.Locality.contains(Locality))
        if CoalType:
            q = q.where(CheckIn.CoalType.contains(CoalType))
        if StoreCode:
            q = q.where(CheckIn.StoreCode.contains(StoreCode))
        return '[' + ','.join([str(r) for r in q]) + ']'

    @staticmethod
    def set_user(r: CheckIn):
        a = Account.get(Name=session.get('user'))   # type: Account
        r.User = a.Name
        r.Group = a.Group
