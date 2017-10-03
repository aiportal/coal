from flask import request, session, make_response
from flask.views import View
import json
from database.config import Account
import urllib.parse


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
        q = Account.select().where(Account.Name == user).where(Account.Password == pwd)
        success = q.exists()
        resp = make_response(json.dumps(success))
        if success:
            session['user'] = user
            r = q[0]    # type:Account
            resp.set_cookie('username', value=urllib.parse.quote(r.Alias))
            resp.set_cookie('userrole', value=urllib.parse.quote(r.Role))
        return resp

    @staticmethod
    def Logout():
        session.pop('user', None)
        return json.dumps(True)
