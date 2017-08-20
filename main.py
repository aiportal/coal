from flask import Flask, Blueprint, redirect
import os
from service import bp_service


# set working directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

bp_static = Blueprint('static', __name__, static_folder='./static', static_url_path='', url_prefix='')

app = Flask(__name__)
app.register_blueprint(bp_static)
app.register_blueprint(bp_service)


@app.route('/')
def hello_world():
    return redirect('/main.htm')
    # return 'Hello World!'


if __name__ == '__main__':
    app.run(port=8090)
