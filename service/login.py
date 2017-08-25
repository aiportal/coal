from flask import request, session, make_response
from flask.views import View
import json
from database.config import SysConfig


class LoginService(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        try:
            m = request.args['$m']
            f = getattr(self, m)
            return f()
        except Exception as e:
            return json.dumps({"Exception": str(e)}, ensure_ascii=False)

    @staticmethod
    def Login():
        user, pwd = request.args.get('user'), request.args.get('pwd')
        val = SysConfig.getItem('login', user).ItemValue
        success = (pwd == val)
        if success:
            session['user'] = user
        return json.dumps(success)

    @staticmethod
    def Logout():
        session.pop('user', None)
        return json.dumps(True)
