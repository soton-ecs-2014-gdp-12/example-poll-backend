from functools import wraps
from flask import Flask, make_response, g, jsonify, request, abort
import sqlite3
import os
app = Flask(__name__)

db_name = "votes.db"

# CORS from http://coalkids.github.io/flask-cors.html

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']


    return resp

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/cors_test')
def cors_test():
    resp = make_response()
    resp.data = 'cors response'
    return resp

@app.route('/setup')
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

@app.route('/results/<annotationId>/<questionId>', methods=["GET"])
def results(annotationId, questionId):

    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT result, count(*) FROM votes WHERE questionID = ? AND annotationID = ? GROUP BY result', (questionId, annotationId))
    return jsonify(cur.fetchall());

@app.route('/vote', methods=["POST"])
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
