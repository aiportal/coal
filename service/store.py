from flask import request
from flask.views import View
from peewee import fn
from database import db_main
from database.store import StoreMove, Storage
import json
from datetime import datetime, timedelta


class StoreService(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        try:
            m = request.args['$m']
            f = getattr(self, m)
            return f()
        except Exception as e:
            return json.dumps({"Exception": str(e)}, ensure_ascii=False)

    @staticmethod
    def ListMove():
        start = datetime.now() - timedelta(days=1)
        q = StoreMove.select().where(StoreMove.TimeStamp > start)
        if 'type' in request.args:
            q = StoreMove.select().where(StoreMove.MoveType == request.args['type'])
        return '[' + ','.join([str(r) for r in q]) + ']'

    @staticmethod
    def SetMove():
        r = StoreMove.new(request.form)                             # type:StoreMove
        if 'MoveType' in request.args:
            r.MoveType = request.args['MoveType']
        if 'CoalType' in request.args:
            r.CoalType = request.args['CoalType']
        if 'DestCoal' in request.args:
            r.DestCoal = request.args['DestCoal']
        r_old = r.ID and StoreMove.get(ID=r.ID) or None             # type:StoreMove
        with db_main.atomic():
            r.save()
            if r_old:
                Storage.MoveStorage(r_old.DestStore, r_old.StoreCode, float(r.Amount))      # 恢复库存
            Storage.MoveStorage(r.StoreCode, r.DestStore, float(r.Amount))                  # 移动库存
        r = StoreMove.get(Name=r.Name)
        return str(r)

    @staticmethod
    def RemoveMove():
        rid = request.form['id']
        r = StoreMove.get(ID=rid)                                   # type:StoreMove
        with db_main.atomic():
            r.delete().execute()
            Storage.MoveStorage(r.DestStore, r.StoreCode, float(r.Amount))                  # 恢复库存
        return 'true'

    @staticmethod
    def SumStore():
        q = Storage.select(Storage.ID, Storage.Name, fn.sum(Storage.Amount).alias('Amount'))\
            .group_by(Storage.ID, Storage.Name)
        return '[' + ','.join([str(r) for r in q]) + ']'
