"""
Team: 57
Yixin Su (731067, yixins1@student.unimelb.edu.au)
Guoen Jin (935833, guoenj@student.unimelb.edu.au)
Tiantong Li (1037952, tiantongl1@student.unimelb.edu.au)
Haikuan Liu (1010887, haikuanl@student.unimelb.edu.au)
Haochen Qi (964325, hqq@student.unimelb.edu.au)
"""

import couchdb
import sys
import re
import string
from pyspark.mllib.feature import Word2Vec 
from pyspark import SparkContext
import pickle as pk
import argparse
import numpy as np
import csv

reload(sys)
sys.setdefaultencoding('utf-8')
sc = SparkContext() # remove it if executed from pyspark

# location la

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_address', nargs='?', default='http://45.113.235.228:5984',
                        help='database server address.')
    parser.add_argument('--db_user', nargs='?', default='admin',
                        help='database admin.')
    parser.add_argument('--db_pwd', nargs='?', default='admin',
                        help='database password.')
    parser.add_argument('--keyword', nargs='?', default='food',
                    help='The key word of data analysis.')
    parser.add_argument('--largest_syms_num', type=int, default=500,
                    help='expected largest number of similar synonyms of key word.')
    parser.add_argument('--syms_num', type=int, default=50,
                    help='top number of similar synonyms of key word. value should less than largest_syms_num')
    parser.add_argument('--wv_dbname', nargs='?', default='[\'exa\']',
                    help='all participated database for word2vec')
    parser.add_argument('--a_dbname', nargs='?', default='[\'melbourne\']',
                    help='all participated database for twitter analysis')
    parser.add_argument('--storedb', nargs='?', default='data_analysis',
                    help='all participated database')
    parser.add_argument('--word2vec', type=bool, default=True,
                    help='whether perform word2vec')
    
    return parser.parse_args()  


def preprocessing_tweet_db(dbn, analysis_db = True):
    punc_pattern = r'[{}]'.format(string.punctuation)
    tweet_info = []
    tweet_num = 0
    for item in dbn.view('docs/tweet'):
        [extended_tweet, short_tweet, pygon] = item.value
        if extended_tweet != None:
            tweet = extended_tweet['full_text']
        else:
            tweet = short_tweet
        # handle tweet sentences
        english_text = re.sub(r'https?://[^\s]+', '', tweet.strip()) # remove url 
        english_text = re.sub(r'[^\x00-\x7F]+',' ', english_text)  # remove all non ascii characters 
        english_text = re.sub(r'@[^\ ]+', '', english_text)    # remove all @ words because they are always names
        english_text = re.sub(r'#', '', english_text)          # remove all hastag symbol and keep hastag word
        english_text = re.sub(punc_pattern, '', english_text)          # remove all hastag symbol and keep hastag word
        
        #handle polygon location, average the boundary as the location
        try:
            avg_loc = [0,0]
            pygon = pygon['bounding_box']['coordinates'][0]
            for loc in pygon:
                avg_loc[0] += loc[0]
                avg_loc[1] += loc[1]
            
            avg_loc = [avg_loc[0]/len(pygon),avg_loc[1]/len(pygon)]
        except:
            avg_loc = [0,0]

        tweet_info.append([english_text.lower(), avg_loc])
        tweet_num += 1
    
    return tweet_info, tweet_num

def preprocessing_tweet(couch, args):
    wv_dbname = eval(args.wv_dbname)
    a_dbname = eval(args.a_dbname)
    
    wv_sentences = []
    a_sentences = []
    tweet_nums = []
    if args.word2vec:
        for dbn in wv_dbname:
            tweet_info, tweet_num = preprocessing_tweet_db(couch[dbn])
            wv_sentences.append(tweet_info)    # tweet_info = [sentence, location]
            tweet_nums.append(tweet_num)
    
    for dbn in a_dbname:
        tweet_info, tweet_num = preprocessing_tweet_db(couch[dbn])
        a_sentences.append(tweet_info)    # tweet_info = [sentence, location]
        tweet_nums.append(tweet_num)
 

    tweet_nums.append(sum(tweet_nums))

    print("number of tweets:")
    print(tweet_nums)
    return wv_sentences, a_sentences


def word_2_vector(tweet_info_db_list, args):
    w2v_sentences = []
    for tweet_info_list in tweet_info_db_list:
        for tweet_info in tweet_info_list:
            w2v_sentences.append(str(tweet_info[0])) 
    print("all sentence:", len(w2v_sentences))
    doc = sc.parallelize(w2v_sentences).map(lambda line: line.split(" "))
    model = Word2Vec().fit(doc)

    syms = model.findSynonyms(args.keyword, args.largest_syms_num)   # get enough sym words
    syms_word = [s[0] for s in syms]
    pk.dump(syms_word, open(args.keyword+'_syms.pkl', 'w'))
    print("synonyms of %s:" %(args.keyword))
    print syms_word[0:args.syms_num]

    return syms_word[0:args.syms_num]


def sins_analysis(syms_word, tweet_db_list, city_loc_list, args):

    def find_loc(loc, contain_keywords):
        result = np.array([0 for i in range(len(city_loc_list)*2)])
        for idx, city_bound in enumerate(city_loc_list):
            if is_in(city_bound, loc):
                result[idx*2] = 1
                if contain_keywords:
                    result[idx*2+1] = 1
                return result
        return result
        
    def is_in(bound, loc):
        loc_lo = loc[0]
        loc_la = loc[1]
        if loc_lo >= bound[0] and loc_lo <= bound[2] and loc_la >= bound[1] and loc_la <= bound[3]:
            return True
        else:
            return False
    
    def process_analysis(line):
        sentence = str(line[0])
        loc= list(line[1])
        contain_keywords = any([(word in syms_word) for word in sentence.split(' ')])
        return find_loc(loc, contain_keywords)
    
    merged_tweet_info_list = []
    for tweet_info_list in tweet_db_list:
        merged_tweet_info_list += tweet_info_list

    sentenceRDD = sc.parallelize(merged_tweet_info_list)
    #countRDD = sentenceRDD.map(lambda line: 1 if any([(word in syms_word) for word in line.split(' ')]) else 0).reduce(lambda a,b: a+b)
    countRDD = sentenceRDD.map(process_analysis).reduce(lambda a,b: a+b)
    
    return countRDD


def store_in_analysis_db(tweet_count_by_area, couch, cities, args):
    store_db = couch[args.storedb]
    doc_dict = {}
    for _id in store_db:
        doc = store_db[_id]
        doc_dict[doc['city']] = doc

    for i in range(len(cities)):
        try:
            doc = doc_dict[cities[i]]
            docid = doc.id
        except:
            doc = {'city': cities[i]}
            docid = cities[i]
        total = tweet_count_by_area[i*2]
        has_keywords = tweet_count_by_area[i*2+1]
        rate = float(has_keywords)/total
        # store information into database
        doc[args.keyword+'_'+str(args.syms_num)] = {'total_twitter': total ,'has_keywords': has_keywords }
        store_db[docid] = doc
        print '%s: total tweets: %d, contain keyword: %d, rate: %.3f' \
            %(cities[i], total, has_keywords, rate) 

def main():
    args = parse_args()
    city_loc_list = []
    cities = []
    with open('/root/location.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader, None)
        for row in csvreader:
            cities.append(row[0])
            city_loc_list.append([float(l) for l in row[1:5]])

    #SYDNEY_LOC = [150.6396, -34.1399, 151.3439, -33.5780]
    #MELBOURNE_LOC = [144.5532, -38.2250, 145.5498, -37.5401] 
    #BRISBANE_LOC = [152.6797, -27.7210, 153.2204, -27.1203]
    #ADELAIDE_LOC = [138.4421, -35.3490, 138.7832, -34.6481] 
    #city_loc_list = [ADELAIDE_LOC, BRISBANE_LOC, MELBOURNE_LOC, SYDNEY_LOC]
   
    couch = couchdb.Server(args.db_address)
    couch.resource.credentials = (args.db_user, args.db_pwd)

    wv_tweet_info_list, a_tweet_info_list = preprocessing_tweet(couch, args)

    if args.word2vec:
        syms_word = word_2_vector(wv_tweet_info_list + a_tweet_info_list, args)
    else:
        syms_word = pk.load(open(args.keyword+'_syms.pkl'))[0:args.syms_num]
        print(syms_word)

    tweet_count_by_area = sins_analysis(syms_word, a_tweet_info_list, city_loc_list, args)

    store_in_analysis_db(tweet_count_by_area, couch, cities, args)


main()