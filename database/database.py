import peewee
from peewee import SqliteDatabase
from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.signals import Model
import json
import os
from datetime import datetime

# set working directory
os.chdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


db_main = SqliteDatabase('./main.db')


def datetime_now():
    return '{0:%Y-%m-%d %H:%M}'.format(datetime.now())


class MainModel(Model):
    class Meta:
        database = db_main
    TimeStamp = peewee.DateTimeField(default=datetime_now, help_text='时间戳')

    def __str__(self):
        return json.dumps(model_to_dict(self), ensure_ascii=False)

    @classmethod
    def new(cls, form) -> Model:
        return dict_to_model(cls, form, ignore_unknown=True)


