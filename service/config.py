from flask import request
from flask.views import View
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

