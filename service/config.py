from flask import request, session
from flask.views import View
from database import db_main
from database.check import CheckIn, CheckOut
from database.store import Storage
import json
from datetime import datetime, timedelta
from database.config import SysConfig
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
    def SetAdminPassword():
        user, pwd = session.get('user', ''), request.form.get('pwd')
        if user and pwd:
            val = md5(('bfbd' + str(pwd) + 'bfbd').encode()).hexdigest()
            SysConfig.setItem('login', user, val)
        return json.dumps(True)
