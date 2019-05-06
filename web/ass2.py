from flask import Flask, render_template, url_for, jsonify, abort, request, make_response
# from flask_httpauth import HTTPBasicAuth
import couchdb
import requests
import json
app = Flask(__name__)

server_url = "http://127.0.0.1:5984/"


def getDataFromCouchDB(data):
    # this function will convert a list of dictionaries obtained from couchDB into a dictionary
    # which contains all required information for analysis
	dic = {}

    # iterate all documents
    for i in data:
        try:
            temp = {}
            temp["twitter_result"] = i['twitter_result']
            temp["obesity"] = i['obesity']
            temp["heart_disease"] = i['heart_disease']
            dic[i['city']] = temp
		except:
			continue
	return dic

try:
    couch = couchdb.Server(server_url)
except:
    print "Cannot find CouchDB Server ... Exiting\n"
    print "----_Stack Trace_-----\n"
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

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

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

if __name__ == '__main__':
	app.run(debug=True)
