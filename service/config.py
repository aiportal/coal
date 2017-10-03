from flask import request, session
from flask.views import View
from playhouse.shortcuts import model_to_dict
from database.config import SysConfig, Account
import json
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
            r = SysConfig.get_or_create(Subject=r.Subject, ItemName=r.ItemName, defaults=r)
        r.save()

    @staticmethod
    def RemoveItem():
        rid = request.form['id']
        q = SysConfig.delete().where(SysConfig.ID == rid)
        q.execute()
        return 'true'

    @staticmethod
    def ListUser():
        if session.get('user', '') != 'admin':
            return json.dumps([])

        q = Account.select().where(Account.Role != 'admin')
        rs = [x for x in q]
        for r in rs:
            r.Password = PASSWORD_MASK
        js = json.dumps({
            'total': q.count(True),
            'rows': [model_to_dict(x) for x in q]
        }, ensure_ascii=False)
        return js

    @staticmethod
    def SetUser():
        if session.get('user', '') != 'admin':
            raise PermissionError()

        r = Account.new(request.form)
        if not r.ID or r.Password != PASSWORD_MASK:
            r.Password = md5(('bfbd' + str(r.Password) + 'bfbd').encode()).hexdigest()
        if r.Password == PASSWORD_MASK:
            r.Password = Account.get(Name=r.Name).Password

        r.save()
        r = Account.get(Name=r.Name)
        r.Password = PASSWORD_MASK
        return str(r)

    @staticmethod
    def RemoveUser():
        if session.get('user', '') != 'admin':
            raise PermissionError()

        rid = request.form.get('id')
        q = Account.delete().where(Account.ID == rid)
        q.execute()
        return json.dumps(True)

    @staticmethod
    def ChangePassword():
        name, pwd = session.get('user', ''), request.form.get('pwd')
        if name and pwd:
            r = Account.get(Account.Name == name)
            r.Password = md5(('bfbd' + str(pwd) + 'bfbd').encode()).hexdigest()
            r.save()
            return json.dumps(True)
        else:
            return json.dumps(False)

PASSWORD_MASK = '********'
