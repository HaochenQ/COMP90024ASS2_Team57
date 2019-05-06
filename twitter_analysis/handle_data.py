import couchdb
import sys
import re
#from pyspark.ml.feature import Word2Vec
import pickle as pk

reload(sys)
sys.setdefaultencoding('utf-8')

dbname = 'data_analysis'
couch = couchdb.Server('http://45.113.235.228:5984')
#couch = couchdb.Server()
couch.resource.credentials = ('admin', 'admin')

db = couch[dbname] # existing

for _id in db:
    print db[_id]



#sentence = []
#index = 0
#tid_set = set()
#print 'start checking...'
"""
for _id in db:
    index += 1
    tid = db[_id].id
    tid_set.add(tid)
    if index%1000 == 0:
        print(index, len(tid_set))
"""

"""
for item in db.view('docs/new-view'):
    print item
    print item.value
    break
    #english_text = re.sub(r'[^\x00-\x7F]+',' ', item.value)  # remove all non ascii characters 
    #english_text = re.sub(r'@[^\ ]+', '', english_text)    # remove all @ words because they are always names
    #english_text = re.sub(r'#', '', english_text)          # remove all hastag symbol and keep hastag word
    #english_text = re.sub(r'https?://[^\s]+', '', english_text) # remove url 
    
    #sentence.append(english_text.lower())
    index += 1

print index
"""

