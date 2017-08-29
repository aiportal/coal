from flask import request, session
from flask.views import View
from playhouse.shortcuts import model_to_dict
from database.config import SysConfig
import json
from datetime import datetime, timedelta
from hashlib import md5


class ConfigService(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        try:
            m = request.args['$m']
            f = getattr(self, m)
            return f()
        except Exception as e:
            return json.dumps({"Exception": str(e)}, ensure_ascii=False)

    @staticmethod
    def ListItem():
        sub = request.args.get('subject')
        q = SysConfig.select().where(SysConfig.Subject == sub)

        js = json.dumps({
            'total': q.count(True),
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @staticmethod
    def SetItem():
        r = SysConfig.new(request.form)                                     # type:SysConfig
        if not r.ID:
            r.Subject = request.args.get('subject')
            r = SysConfig.get_or_create(Suject=r.Subject, ItemName=r.ItemName, defaults=r)
        r.save()

    @staticmethod
    def RemoveItem():
        rid = request.form['id']
        r = SysConfig.get(ID=rid)                                           # type:SysConfig
        r.delete().execute()
        return 'true'

    @staticmethod
    def SetAdminPassword():
        user, pwd = session.get('user', ''), request.form.get('pwd')
        if user and pwd:
            val = md5(('bfbd' + str(pwd) + 'bfbd').encode()).hexdigest()
            SysConfig.setItem('login', user, val)
        return json.dumps(True)

