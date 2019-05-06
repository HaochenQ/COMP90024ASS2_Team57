"""
from pyspark import SparkConf, SparkContext
from pyspark.ml.feature import HashingTF, IDF, Tokenizer,Word2Vec
import re

words= re.split('\W+', open("/root/wc.txt").read())
wordsRDD= sc.parallelize(words)
countsRDD = wordsRDD.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)

wc = countsRDD.collect()
print(wc)    
"""

import couchdb
import sys
import re
import string
from pyspark.mllib.feature import Word2Vec
import pickle as pk

reload(sys)
sys.setdefaultencoding('utf-8')

dbname = ['exa', 'melbourne']
couch = couchdb.Server('http://45.113.235.228:5984')
couch.resource.credentials = ('admin', 'admin')
db = [couch[dbn] for dbn in dbname]

KEY_WORD = 'food'
SYM_NUM = 100

punc_pattern = r'[{}]'.format(string.punctuation)

def preprocessing_tweet_db(dbn):
    sentence = []
    tweet_num = 0
    for item in dbn.view('docs/tweet'):
        english_text = re.sub(r'https?://[^\s]+', '', item.value) # remove url 
        english_text = re.sub(r'[^\x00-\x7F]+',' ', english_text)  # remove all non ascii characters 
        english_text = re.sub(r'@[^\ ]+', '', english_text)    # remove all @ words because they are always names
        english_text = re.sub(r'#', '', english_text)          # remove all hastag symbol and keep hastag word
        english_text = re.sub(punc_pattern, '', english_text)          # remove all hastag symbol and keep hastag word

        sentence.append(english_text.lower())
        tweet_num += 1
    
    return sentence, tweet_num


sentences = []
tweet_nums = []
for dbn in db:
    sentence, tweet_num = preprocessing_tweet_db(dbn)
    sentences += sentence
    tweet_nums.append(tweet_num)

tweet_nums.append(sum(tweet_nums))

print("number of tweets:")
print(tweet_nums)

doc = sc.parallelize(sentences).map(lambda line: line.split(" "))
model = Word2Vec().fit(doc)
syms = model.findSynonyms(KEY_WORD, SYM_NUM)

syms_word = [s[0] for s in syms]
print("synonyms of %s:" %(KEY_WORD))
print syms_word

pk.dump(syms_word, open('food_syms.pkl', 'w'))

keys = model.getVectors().keys()
with open('keys.txt', 'w') as f:
    f.writelines(keys)


#pk.dump(keys, open('keys.pkl', 'wb'))
#values = model.getVectors().values()
"""
for i in range(len(keys))[100:300]:
    print(keys[i])
    syms = model.findSynonyms(keys[i], 5)
    print [s[0] for s in syms]
"""
#for i in len(keys):
#    print(keys[i], values[i])
