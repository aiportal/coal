from flask import Blueprint, session
from .login import LoginService
from .config import ConfigService
from .check import CheckService
from .store import StoreService
from .consume import ConsumeService
import json


bp_login = Blueprint('login', __name__ + '/login', url_prefix='')
bp_login.add_url_rule('/Login.svc', view_func=LoginService.as_view('login'))

bp_service = Blueprint('svc', __name__, url_prefix='')
bp_service.add_url_rule('/Config.svc', view_func=ConfigService.as_view('config'))
bp_service.add_url_rule('/CheckService.svc', view_func=CheckService.as_view('check'))
bp_service.add_url_rule('/StoreService.svc', view_func=StoreService.as_view('store'))
bp_service.add_url_rule('/ConsumeService.svc', view_func=ConsumeService.as_view('consume'))


@bp_service.before_request
def check_login():
    user = session.get('user', None)
    if not user:
        js = json.dumps({'Exception': '未登录'}, ensure_ascii=False)
        return js
