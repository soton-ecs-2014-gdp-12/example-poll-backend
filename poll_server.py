from functools import wraps
from flask import Flask, make_response, g, jsonify, request, abort
import sqlite3
import os
app = Flask(__name__)

db_name = "votes.db"

def add_cors(f):
    @wraps(f)
    def inner(*args, **kwargs):
        response = f(*args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return inner

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/cors_test')
@add_cors
def cors_test():
    resp = make_response()
    resp.data = 'cors response'
    return resp

@app.route('/setup')
@add_cors
def setup():
    print('setup time')
    resp = make_response()
    if os.path.isfile(db_name):
        resp.data = 'db already exists'
        return resp

    db = get_db()
    cur = db.cursor()
    cur.execute('''CREATE TABLE votes
             (questionID text, annotationID text, result text)''')
    db.commit()
    resp.data = 'db created'
    return resp

@app.route('/results')
@add_cors
def results():
    resp = make_response()
    resp.data = 'results'
    return resp

@app.route('/vote', methods=["POST"])
@add_cors
def vote():
    vote = request.get_json(force=True)

    if("questionResult" not in vote or "annotation" not in vote or "result" not in vote):
        abort(400)

    db = get_db()
    cur = db.cursor()

    if isinstance(vote["result"], list):
        for item in vote["result"]:
            cur.execute('INSERT INTO votes VALUES (?,?,?)', (vote["questionResult"],vote["annotation"],item))
    else:
            cur.execute('INSERT INTO votes VALUES (?,?,?)', (vote["questionResult"],vote["annotation"],vote["result"]))
    db.commit()
    
    resp = make_response()
    return resp

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
