from flask import Flask, Blueprint, redirect
import os
from service import bp_login, bp_service


# set working directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

bp_static = Blueprint('static', __name__, static_folder='./static', static_url_path='', url_prefix='')

app = Flask(__name__)
app.secret_key = 'www.ultragis.com'
app.register_blueprint(bp_static)
app.register_blueprint(bp_login)
app.register_blueprint(bp_service)


@app.route('/')
def hello_world():
    return redirect('/login.htm')


if __name__ == '__main__':
    app.run(port=8090)
