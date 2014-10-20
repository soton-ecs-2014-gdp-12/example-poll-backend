from functools import wraps
from flask import Flask, make_response
app = Flask(__name__)


def add_cors(f):
    @wraps(f)
    def inner(*args, **kwargs):
        response = f(*args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return inner

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/cors_test')
@add_cors
def cors_test():
    resp = make_response()
    resp.data = 'cors response'
    return resp

if __name__ == '__main__':
    app.run()
