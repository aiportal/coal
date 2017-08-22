from flask import request
from flask.views import View
from peewee import fn
from playhouse.shortcuts import model_to_dict
from database import db_main
from database.store import StoreMove, Storage
import json
from datetime import datetime, timedelta


DATETIME_FMT = '%Y-%m-%d %H:%M'


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
        view_all = request.args.get('view') == 'all'
        q = StoreMove.select().order_by(-StoreMove.MoveTime)
        if not view_all:
            start = datetime.now() - timedelta(days=1)
            q = q.where(StoreMove.TimeStamp > start)

        page, rows = request.form.get('page') or 1, request.form.get('rows') or 50
        q = q.paginate(int(page), int(rows))

        args = request.args
        MoveType = args.get('type')
        if MoveType:
            q = q.where(StoreMove.MoveType == request.args['type'])

        start, end = args.get('start'), args.get('end')
        if start:
            q = q.where(StoreMove.MoveTime > datetime.strptime(start, DATETIME_FMT))
        if end:
            q = q.where(StoreMove.MoveTime < datetime.strptime(end, DATETIME_FMT))

        StoreCode, DestStore = args.get('StoreCode'), args.get('DestStore')
        if StoreCode:
            q = q.where(StoreMove.StoreCode.contains(StoreCode))
        if DestStore:
            q = q.where(StoreMove.DestStore.contains(DestStore))

        js = json.dumps({
            'total': q.count(True),
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @classmethod
    def SetMove(cls):
        cls.check_move_time()
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
    def check_move_time():
        min_time = datetime.now() - timedelta(hours=12)
        max_time = datetime.now() + timedelta(hours=1)
        tm = request.form.get('MoveTime')
        tm = datetime.strptime(tm, DATETIME_FMT)
        if min_time < tm < max_time:
            return
        raise Exception('操作时间应在12小时以内')

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
