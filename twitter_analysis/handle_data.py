import couchdb

#HTTP = 'https://'
#auth = 'admin:admin@'
#host = 'localhost'
dbname = 'melbourne'

couch = couchdb.Server()
couch.resource.credentials = ('admin', 'admin')
#couch = couchdb.Server(HTTP+auth+host+':5984/')


#db = couch.create('exampledb') # newly created
db = couch[dbname] # existing

#doc = {'foo': 'bar'}
#db.save(doc)
#print(doc)

rows = db.view('_all_docs', include_docs=True)
data = [row['doc'] for row in rows]

print(data[0])
