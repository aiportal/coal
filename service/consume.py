from flask import request, session
from flask.views import View
from playhouse.shortcuts import model_to_dict
from database import db_main
from database.consume import ConsumeSend, ConsumeFire, FireRecord
from database.store import Storage
from database.config import Account
import json
from datetime import datetime, timedelta
from typing import Union


DATETIME_FMT = '%Y-%m-%d %H:%M'


class ConsumeService(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        try:
            m = request.args['$m']
            f = getattr(self, m)
            return f()
        except Exception as e:
            return json.dumps({"Exception": str(e)}, ensure_ascii=False)

    @classmethod
    def ListSendOut(cls):
        view_all = request.args.get('view') == 'all'
        q = ConsumeSend.select().order_by(+ConsumeSend.ConsumeTime)
        if not view_all:
            start = datetime.now() - timedelta(days=1)
            q = q.where(ConsumeSend.ConsumeTime > start)
            q = cls.filter_by_user(q)

        page, rows = request.form.get('page') or 1, request.form.get('rows') or 50
        q = q.paginate(int(page), int(rows))

        args = request.args
        start, end = args.get('start'), args.get('end')
        if start:
            q = q.where(ConsumeSend.ConsumeTime > datetime.strptime(start, DATETIME_FMT))
        if end:
            q = q.where(ConsumeSend.ConsumeTime < datetime.strptime(end, DATETIME_FMT))

        StoreCode = args.get('StoreCode')
        if StoreCode:
            q = q.where(ConsumeSend.StoreCode.contains(StoreCode))

        js = json.dumps({
            'total': q.count(True),
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @classmethod
    def SetSendOut(cls):
        cls.check_send_time()
        r = ConsumeSend.new(request.form)                   # type:ConsumeSend
        cls.set_user(r)
        r_old = r.ID and ConsumeSend.get(ID=r.ID) or None   # type:ConsumeSend
        with db_main.atomic():
            r.save()
            if r_old:
                Storage.AddStorage(r_old.StoreCode, float(r_old.Amount))        # 恢复库存
            Storage.SubStorage(r.StoreCode, float(r.Amount))                    # 减库存
        r = ConsumeSend.get(Name=r.Name)
        return str(r)

    @staticmethod
    def check_send_time():
        min_time = datetime.now() - timedelta(hours=12)
        max_time = datetime.now() + timedelta(hours=1)
        tm = request.form.get('ConsumeTime')
        tm = datetime.strptime(tm, DATETIME_FMT)
        if min_time < tm < max_time:
            return
        raise Exception('发煤时间应在12小时以内')

    @staticmethod
    def RemoveSendOut():
        rid = request.form['id']
        r = ConsumeSend.get(ID=rid)                         # type:ConsumeSend
        with db_main.atomic():
            Storage.AddStorage(r.StoreCode, float(r.Amount))                    # 恢复库存
            r.delete().execute()
        return 'true'

    @classmethod
    def ListFireIn(cls):
        q = ConsumeFire.select().order_by(+ConsumeFire.ConsumeTime)
        view_all = request.args.get('view') == 'all'
        if not view_all:
            start = datetime.now() - timedelta(days=1)
            q = q.where(ConsumeFire.ConsumeTime > start)
            q = cls.filter_by_user(cls)

        page, rows = request.form.get('page') or 1, request.form.get('rows') or 50
        q = q.paginate(int(page), int(rows))

        args = request.args
        ConsumeType = args.get('type')
        if ConsumeType:
            q = q.where(ConsumeFire.ConsumeType.contains(ConsumeType))

        start, end = args.get('start'), args.get('end')
        if start:
            q = q.where(ConsumeFire.ConsumeTime > datetime.strptime(start, DATETIME_FMT))
        if end:
            q = q.where(ConsumeFire.ConsumeTime < datetime.strptime(end, DATETIME_FMT))

        StoreCode, BufferCode = args.get('StoreCode'), args.get('BufferCode')
        if StoreCode:
            q = q.where(ConsumeFire.StoreCode.contains(StoreCode))
        if BufferCode:
            q = q.where(ConsumeFire.BufferCode.contains(BufferCode))

        js = json.dumps({
            'total': q.count(True),
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @classmethod
    def SetFireIn(cls):
        cls.check_fire_time()
        t = request.args.get('type')
        r = ConsumeFire.new(request.form)                   # type:ConsumeFire
        cls.set_user(r)
        r.ConsumeType = t
        r_old = r.ID and ConsumeFire.get(ID=r.ID) or None   # type:ConsumeFire
        with db_main.atomic():
            r.save()
            if r_old:
                Storage.AddStorage(r_old.StoreCode, float(r_old.Amount))        # 恢复库存
            Storage.SubStorage(r.StoreCode, float(r.Amount))                    # 减库存
        r = ConsumeFire.get(Name=r.Name)
        return str(r)

    @staticmethod
    def check_fire_time():
        min_time = datetime.now() - timedelta(hours=12)
        max_time = datetime.now() + timedelta(hours=1)
        tm = request.form.get('ConsumeTime')
        tm = datetime.strptime(tm, DATETIME_FMT)
        if min_time < tm < max_time:
            return
        raise Exception('上料时间应在12小时以内')

    @staticmethod
    def RemoveFireIn():
        rid = request.form['id']
        r = ConsumeFire.get(ID=rid)
        with db_main.atomic():
            Storage.AddStorage(r.StoreCode, float(r.Amount))                    # 恢复库存
            r.delete().execute()
        return 'true'

    @classmethod
    def ListRecord(cls):
        q = FireRecord.select().order_by(+FireRecord.RecordTime)
        view_all = request.args.get('view') == 'all'
        if not view_all:
            start = datetime.now() - timedelta(days=1)
            q = FireRecord.select().where(FireRecord.RecordTime > start)
            q = cls.filter_by_user(q)

        page, rows = request.form.get('page') or 1, request.form.get('rows') or 50
        q = q.paginate(int(page), int(rows))

        args = request.args
        start, end = args.get('start'), args.get('end')
        if start:
            q = q.where(FireRecord.RecordTime > datetime.strptime(start, DATETIME_FMT))
        if end:
            q = q.where(FireRecord.RecordTime < datetime.strptime(end, DATETIME_FMT))

        js = json.dumps({
            'total': q.count(True),
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @classmethod
    def SetRecord(cls):
        cls.check_record_time()
        r = FireRecord.new(request.form)                                        # type: FireRecord
        cls.set_user(r)
        r.save()
        r = FireRecord.get(Name=r.Name)
        return str(r)

    @staticmethod
    def check_record_time():
        min_time = datetime.now() - timedelta(hours=12)
        max_time = datetime.now() + timedelta(hours=1)
        tm = datetime.strptime(request.form['RecordTime'], DATETIME_FMT)
        if min_time < tm < max_time:
            return
        raise Exception('开始时间应在12小时以内')

    @staticmethod
    def RemoveRecord():
        rid = request.form['id']
        q = FireRecord.delete().where(FireRecord.ID == rid)
        q.execute()
        return 'true'

    @staticmethod
    def SumConsume():
        args = request.args
        start, end = args.get('start'), args.get('end')
        Group, StoreCode = args.get('Group'), args.get('StoreCode')

        q = ConsumeFire.select().where(start <= ConsumeFire.ConsumeTime < end)
        if Group:
            q = q.where(ConsumeFire.Group.contains(Group))
        if StoreCode:
            q = q.where(ConsumeFire.StoreCode.contains(StoreCode))

        return '[' + ','.join([str(r) for r in q]) + ']'

    @staticmethod
    def set_user(r: Union[ConsumeSend, ConsumeFire, FireRecord]):
        a = Account.get(Name=session.get('user'))   # type: Account
        r.User = a.Alias
        r.Group = a.Group

    @staticmethod
    def filter_by_user(q):
        a = Account.get(Name=session.get('user'))   # type: Account
        if a.Role != 'admin':
            return q.where(q.model_class.User == a.Alias)
        else:
            return q
