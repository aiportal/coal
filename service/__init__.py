from flask import Blueprint
from .check import CheckService
from .store import StoreService
from .consume import ConsumeService


bp_service = Blueprint('svc', __name__, url_prefix='')
bp_service.add_url_rule('/CheckService.svc', view_func=CheckService.as_view('check'))
bp_service.add_url_rule('/StoreService.svc', view_func=StoreService.as_view('store'))
bp_service.add_url_rule('/ConsumeService.svc', view_func=ConsumeService.as_view('consume'))


# @bp_service.before_request
# def open_db():
#     pass
#
#
# @bp_service.after_request
# def close_db():
#     pass
