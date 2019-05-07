from flask import Flask, render_template, url_for, jsonify, abort, request, make_response
import couchdb
import requests
import json
import matplotlib.pyplot as plt
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
user = 'admin'
passwd = 'admin'

def getDataFromCouchDB(data):
    # this function will convert a list of dictionaries obtained from couchDB into a dictionary
    # which contains all required information for analysis
    dic = {}

    # iterate all documents
    for i in data:
        try:
            if i['city'] == 'brisbane':
                continue
            temp={}
            temp["total_twitter"] = i['food_100']['total_twitter']
            dic[i['city']] = temp
        except:
            continue
    return dic

try:
    couch = couchdb.Server('http://%s:%s@45.113.235.228:5984/'%(user,passwd))
except:
    print("Cannot find CouchDB Server ... Exiting")
    print("----_Stack Trace_-----")
    raise
    
# couchdb username and password
couch.resource.credentials = ('admin', 'admin')

# locate to certain database
db = couch['data_analysis']

# all docs including views
rows = db.view('_all_docs', include_docs=True)

# transfer couchdb object to a list, each list contains a dictionary
raw_data = [row['doc'] for row in rows]

# collect all required data into one dictionary
data = getDataFromCouchDB(raw_data)

# so can access home page though two paths
@app.route("/")
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/twitter")
def twitter():
    return render_template('twitter.html', data = json.dumps(data))

@app.route("/about")
def about():
    return render_template('about.html', title = "About")

# --------------------- Restful API ------------------------
@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'admin'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


tasks = []
for doc in data:
    doc['url'] = "http://127.0.0.1:5984/twitter/api/tasks/" + doc['city']
    tasks.append(doc)

# get all twitters
@app.route('/twitter/api/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/twitter/api/tasks/<string:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = -1
    for i in range(len(tasks)):
        if task_id == tasks[i]['city']:
            task = i
            break
    if task == -1:
        abort(404)
    return jsonify({'task': tasks[task]})


@app.route('/twitter/api/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'city' in request.json:
        abort(400)
    task = {
        'city': request.json['city'],
        'total_twitter': request.json.get('total_twitter', ""),
    }
    tasks.append(task)
    # db.save(task)
    return jsonify({'task': tasks}), 201


@app.route('/twitter/api/tasks/<string:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = -1
    for i in range(len(tasks)):
        if task_id == tasks[i]['key']:
            task = i
            break
    if task == -1:
        abort(404)
    if not request.json:
        abort(400)
    if 'city' in request.json and type(request.json['city']) != unicode:
        abort(400)
    if 'total_twitter' in request.json and type(request.json['total_twitter']) is not unicode:
        abort(400)
    tasks[task]['city'] = request.json.get('city', tasks[task]['city'])
    tasks[task]['total_twitter'] = request.json.get(
        'total_twitter', tasks[task]['total_twitter'])
    return jsonify({'task': tasks[task]})


@app.route('/twitter/api/tasks/<string:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = -1
    for i in range(len(tasks)):
        if task_id == tasks[i]['city']:
            task = i
            break
    if task == -1:
        abort(404)
    tasks.remove(tasks[task])
    # db.delete(tasks[task])
    return jsonify({'result': True})


if __name__ == '__main__':
	app.run(debug=True)
