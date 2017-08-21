from flask import request
from flask.views import View
from playhouse.shortcuts import model_to_dict
from database import db_main
from database.check import CheckIn, CheckOut
from database.store import Storage
import json
from datetime import datetime, timedelta


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
        start = datetime.now() - timedelta(days=1)
        q = CheckIn.select().where(CheckIn.TimeStamp > start)
        js = json.dumps({
            'total': 200,
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @classmethod
    def SetCheckIn(cls):
        cls.check_book_code()
        r1 = CheckIn.new(request.form)
        r2 = CheckOut.new(request.form)
        with db_main.atomic():
            r1.save()
            r2.save()
        r1 = CheckIn.get(Name=r1.Name)
        return str(r1)

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
        t = request.form.get('BookTime')
        tm = datetime.strptime(t, '%Y-%m-%d %H:%M')
        if min_time < tm < max_time:
            return
        raise Exception('登记时间应在12小时以内')

    @staticmethod
    def RemoveCheckIn():
        rid = request.form['id']
        r = CheckOut.get_by_id(rid)
        q1 = CheckIn.delete().where(CheckIn.Name == r.Name)
        q2 = CheckOut.delete().where(CheckOut.Name == r.Name)
        with db_main.atomic():
            Storage.SubStorage(r.StoreCode, r.RealWeight)           # 删除前减库存
            q1.execute()
            q2.execute()
        return 'true'

    @staticmethod
    def ListCheckOut():
        start = datetime.now() - timedelta(days=1)
        q = CheckOut.select().where(CheckOut.TimeStamp > start)
        return '[' + ','.join([str(r) for r in q]) + ']'

    @staticmethod
    def SetCheckOut():
        r_form = CheckOut.new(request.form)         # type:CheckOut
        if not r_form.ID:
            raise Exception('错误操作：检测记录不可添加')
        r_db = CheckOut.get_by_id(r_form.ID)        # type:CheckOut
        r_in = CheckIn.get(Name=r_db.Name)          # type:CheckIn
        r_in.StoreCode = r_form.StoreCode
        with db_main.atomic():
            r_form.save()
            r_in.save()
            Storage.MoveStorage(r_db.StoreCode, r_form.StoreCode, r_db.RealWeight)      # 调整库存

        r = CheckOut.get(Name=r_form.Name)
        return str(r)

    @staticmethod
    def SumCheckIn():
        args = request.args
        start, end = args.get('start'), args.get('end')
        Locality, CoalType, StoreCode = args.get('Locality'), args.get('CoalType'), args.get('StoreCode')
        if not start or not end:
            return '[]'
        q = CheckIn.select(CheckIn.Name, CheckIn.Locality, CheckIn.CarCode,
                           CheckIn.CoalType, CheckIn.StoreCode, CheckIn.RealWeight)\
            .where(start <= CheckIn.BookTime <= end)
        if Locality:
            q = q.where(CheckIn.Locality.contains(Locality))
        if CoalType:
            q = q.where(CheckIn.CoalType.contains(CoalType))
        if StoreCode:
            q = q.where(CheckIn.StoreCode.contains(StoreCode))
        return '[' + ','.join([str(r) for r in q]) + ']'
