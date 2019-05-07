import sys
import couchdb
import json

'''DB_STRING = "http://45.113.235.228:5984"


def main(json_file,
         db_name,
         couchdb_address):
    # 1. Create the database.. No error checking here because we want to get exception if db exists
    couch = couchdb.Server(couchdb_address)
    db = couch.create(db_name)
    # 2 Read the json line by line and put into the db
    with open(json_file) as jsonfile:
        for row in jsonfile:
            db_entry = json.loads(row)
            db.save(db_entry)


if __name__ == '__main__':
    print ("Call as <jsondb.json> <new_db> <optional db string>")
    args = sys.argv[1:]
    json_file = args[0]
    try:
        db_name = args[1]
    except:
        db_name = json_file.split(".")[0]
    try:
        db_str = args[2]
    except:
        db_str = DB_STRING
    main(json_file,
         db_name,
         db_str)'''


'''# pearson correlation
list1=[500,800,380,270]
list2=[200,300,100,80]
print(np.corrcoef(list1, list2)[0,1])
#matplotlib inline
#matplotlib.style.use('ggplot')
#plt.scatter(list1, list2)
#plt.show()

x=(list)(np.random.randint(0,50,1000))
y=(list)(x+np.random.randint(0,50,1000))
np.corrcoef(x, y)
print(np.corrcoef(x, y)[0,1])
#matplotlib inline
matplotlib.style.use('ggplot')
plt.xlabel('location')                 # plt.xlabel x axis
plt.ylabel('population)')
plt.scatter(x, y)
plt.show()'''
