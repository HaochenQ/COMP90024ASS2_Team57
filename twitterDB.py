"""
Team: 57
Yixin Su (731067, yixins1@student.unimelb.edu.au)
Guoen Jin (935833, guoenj@student.unimelb.edu.au)
Tiantong Li (1037952, tiantongl1@student.unimelb.edu.au)
Haikuan Liu (1010887, haikuanl@student.unimelb.edu.au)
Haochen Qi (964325, hqq@student.unimelb.edu.au)
"""

#Author: Guoen Jin 935833

import tweepy
import json
import hashlib
import re
import couchdb
from tweepy.utils import import_simplejson

#Define Database connection creds
server = "localhost:5984"
admin_username = "admin"
admin_password = "admin"

#Twitter auth stuff
#Get yours by registering an app at dev.twitter.com
access_token_key = "1118325454031601664-Gu6XlEc8F9G12Oh7hvcgGSCQqo01zH"
access_token_secret = "oBXXKzvNRNnjChBG8EdVSQt0YxPs6NfIfdhWkrIMvkJrp"
consumer_key = "gKXNjLGKoh9D2mNxOVTHHBdWI"
consumer_secret = "CAQ0534UcpjUV9tZmr3vSEANgkEokkQUw3VylReNZHGhZVgcUg"

#Define filter terms
filterTerms = ["food"]

json = import_simplejson()
try:
    couchclient = couchdb.Server()
except:
    print ("Cannot find CouchDB Server ... Exiting\n")
    print ("----_Stack Trace_-----\n")
    raise

#Try to use the twitter bucket or else switch to use default bucket
try:
    db = couchclient['exa']
    print ("Using exa bucket")
except:
    db = couchclient['default']
    print ("Using default bucket")

#OAuth
auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)

class StreamListener(tweepy.StreamListener):
    json = import_simplejson()

    def on_status(self, tweet):
        print ('Ran on_status')

    def on_error(self, status_code):
        print(status_code)
        return False

    def on_data(self, data):
        if data[0].isdigit():
            pass
        else:
            jdata = json.loads(data)
            db.save(jdata)

l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l)
streamer.filter(track=filterTerms)
