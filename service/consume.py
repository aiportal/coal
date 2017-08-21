from flask import request
from flask.views import View
from database import db_main
from database.consume import ConsumeSend, ConsumeFire, FireRecord
from database.store import Storage
import json
from datetime import datetime, timedelta


class ConsumeService(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        try:
            m = request.args['$m']
            f = getattr(self, m)
            return f()
        except Exception as e:
            return json.dumps({"Exception": str(e)}, ensure_ascii=False)

    @staticmethod
    def ListSendOut():
        start = datetime.now() - timedelta(days=1)
        q = ConsumeSend.select().where(ConsumeSend.TimeStamp > start)
        return '[' + ','.join([str(r) for r in q]) + ']'

    @staticmethod
    def SetSendOut():
        r = ConsumeSend.new(request.form)                   # type:ConsumeSend
        r_old = r.ID and ConsumeSend.get(ID=r.ID) or None   # type:ConsumeSend
        with db_main.atomic():
            r.save()
            if r_old:
                Storage.AddStorage(r_old.StoreCode, float(r_old.Amount))        # 恢复库存
            Storage.SubStorage(r.StoreCode, float(r.Amount))                    # 减库存
        r = ConsumeSend.get(Name=r.Name)
        return str(r)

    @staticmethod
    def RemoveSendOut():
        rid = request.form['id']
        r = ConsumeSend.get(ID=rid)                         # type:ConsumeSend
        with db_main.atomic():
            Storage.AddStorage(r.StoreCode, float(r.Amount))                    # 恢复库存
            r.delete().execute()
        return 'true'

    @staticmethod
    def ListFireIn():
        t = 'type' in request.args and request.args['type'] or 'Boil'
        start = datetime.now() - timedelta(days=1)
        q = ConsumeFire.select().where(ConsumeFire.ConsumeType == t).where(ConsumeFire.TimeStamp > start)
        return '[' + ','.join([str(r) for r in q]) + ']'

    @staticmethod
    def SetFireIn():
        t = request.args.get('type') or 'Boil'
        r = ConsumeFire.new(request.form)                   # type:ConsumeFire
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
    def RemoveFireIn():
        rid = request.form['id']
        r = ConsumeFire.get(ID=rid)
        with db_main.atomic():
            Storage.AddStorage(r.StoreCode, float(r.Amount))                    # 恢复库存
            r.delete().execute()
        return 'true'

    @staticmethod
    def ListRecord():
        start = datetime.now() - timedelta(days=1)
        q = FireRecord.select().where(FireRecord.TimeStamp > start)
        return '[' + ','.join([str(r) for r in q]) + ']'

    @staticmethod
    def SetRecord():
        r = FireRecord.new(request.form)
        r.save()
        r = FireRecord.get(Name=r.Name)
        return str(r)

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
