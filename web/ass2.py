from flask import Flask, render_template, url_for, jsonify, abort, request, make_response
import couchdb
import requests
import json
app = Flask(__name__)

server_url = "http://45.113.235.228:5984/"
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
    couch = couchdb.Server(server_url)
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

aurin = couch['aurin']
aurin_rows = aurin.view('_all_docs', include_docs=True)
aurin_raw_data = [row['doc'] for row in aurin_rows]
def data_plot(aurin_raw_data):
    dic = {}
    data_list = []
    city_list = ['Sydney', 'Melbourne', 'Brisbane', 'Adelaide']
    for data in aurin_raw_data:
        for city in city_list:
            data_list.append(data[city])
        dic[data['_id']] = data_list
    return dic
plot_aurin_plot = data_plot(aurin_raw_data)
print(aurin_raw_data)


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
