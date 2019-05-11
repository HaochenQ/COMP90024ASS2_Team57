import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json
import couchdb


# extract and merge relevant data from aurin datasets
f1 = open('sydney.json',encoding='utf8')
f2 = open('melbourne.json',encoding='utf8')
f3 = open('adelaide.json',encoding='utf8')
f4 = open('brisbane.json',encoding='utf8')


sydn = json.load(f1)
melb = json.load(f2)
adel = json.load(f3)
bris = json.load(f4)


overweight = []
obseity = []
chronic_disease_risk = []
hi_blood_pressure_risk = []
psy_distress = []
lo_exercise = []

def dataGathering(file,region):
    num1 = 0
    num4 = 0
    num2 = 0
    num3 = 0
    num5 = 0
    num6 = 0
    for i in file['features']:
        if i['properties']['phn_code'] in region:
            num1=(num1+i['properties']['est_ppl_18yrs_plus_obese_2014_15_asr_100'])/2
            num2=(num2+i['properties']['est_ppl_18yrs_plus_ovrwht_2014_15_asr_100'])/2
            num3=(num3+i['properties']['est_ppl_18yrs_plus_wst_meas_ind_rsk_dis_2014_15_asr_100'] )/2
            num4=(num4+i['properties']['est_ppl_18yrs_plus_hi_blood_pressure_2014_15_asr_100'])/2
            num5=(num5+i['properties']['est_ppl_18yrs_plus_hi_psyc_strs_k10_scal_2014_15_asr_100'])/2
            num6=(num6+i['properties']['est_ppl_18yrs_plus_lo_exc_prev_wk_2014_15_asr_100'])/2
    obseity.append(round(num1,3))
    overweight.append(round(num2,3))
    chronic_disease_risk.append(round(num3,3))
    hi_blood_pressure_risk.append(round(num4,3))
    psy_distress.append(round(num5,3))
    lo_exercise.append(round(num6,3))


dataGathering(sydn, ['PHN101', 'PHN102','PHN103', 'PHN105'])
dataGathering(melb, ['PHN201', 'PHN202','PHN203'])
dataGathering(adel, ['PHN401'])
dataGathering(bris, ['PHN301', 'PHN302'])


def printt(list):
    location=['Sydney','Melbourne','Adelaide','Brisbane']
    dic={}
    for each in range(len(list)):
        dic[location[each]]=list[each]
    return dic



print("overWeight:", printt(overweight))
print("obesity:",printt(obseity))
print("chronic_disease", printt(chronic_disease_risk))
print("high blood pressure risk",  printt(hi_blood_pressure_risk))
print("mental depression",  printt(psy_distress))
print("low exercise", printt(lo_exercise))

user = 'admin'
passwd = 'admin'
couchserver = couchdb.Server('http://%s:%s@45.113.235.228:5984/'%(user,passwd))
db_twitter = couchserver['data_analysis']
db_aurin = couchserver['aurin']

# upload aurin data into couchdb

'''try:
    db_aurin['ratio of overWeight'] = printt(overweight)
    db_aurin['ratio obesity'] = printt(obseity)
    db_aurin['ratio of chronic_disease_risk'] = printt(chronic_disease_risk)
    db_aurin['ratio of high_blood_pressure_risk'] = printt(hi_blood_pressure_risk)
    db_aurin['ratio of mental_depression'] = printt(psy_distress)
    db_aurin['ratio of low_exercise'] = printt(lo_exercise)
except:
    print("fail to upload")'''

# retrieve data from couchdb
food20={}
food50={}
food100={}
food200={}

food_20=[]
food_50=[]
food_100=[]
food_200=[]

def getData(city):
    for each in db_twitter:
        try:
            doc = db_twitter[each]
            if doc['city']==city:
                twenty=round(doc['food_20']['has_keywords']/(doc['food_20']['total_twitter']),3)
                food20[city] = twenty
                food_20.append(twenty)
                fifty=round(doc['food_50']['has_keywords']/(doc['food_50']['total_twitter']),3)
                food50[city] = fifty
                food_50.append(fifty)
                oneHundred = round(doc['food_100']['has_keywords']/(doc['food_100']['total_twitter']),3)
                food100[city] = oneHundred
                food_100.append(oneHundred)
                tweHundred = round(doc['food_200']['has_keywords']/(doc['food_20']['total_twitter']),3)
                food200[city] = tweHundred
                food_200.append(tweHundred)
        except:
            print('database error')
getData('sydney')
getData('melbourne')
getData('adelaide')
getData('bristane')
print('\n')
print('food_20:',food20)
print('food_50:',food50)
print('food_100:',food100)
print('food_200:',food200)

# analysis of correlation
def calculateCorr(list):
    dic = {}
    overweightCor = round(np.corrcoef(overweight,list)[0,1],3)
    obseityCor = round(np.corrcoef(obseity,list)[0,1],3)
    chronic_disease_riskCor = round(np.corrcoef(chronic_disease_risk,list)[0,1],3)
    hi_blood_pressure_riskCor = round(np.corrcoef(hi_blood_pressure_risk,list)[0,1],3)
    psy_distressCor = round(np.corrcoef(psy_distress,list)[0,1],3)
    lo_exerciseCor = round(np.corrcoef(lo_exercise,list)[0,1],3)
    dic['overweight'] = overweightCor
    dic['obesity'] = obseityCor
    dic['chronic disease risk'] = chronic_disease_riskCor
    dic['high blood pressure risk'] = hi_blood_pressure_riskCor
    dic['mental depression'] = psy_distressCor
    dic['low exerise'] = lo_exerciseCor

    print('overweight:', overweightCor)
    print('obesity:', obseityCor)
    print('chronic risk:', chronic_disease_riskCor)
    print('high blood pressure risk:', hi_blood_pressure_riskCor)
    print('mental depression:',psy_distressCor)
    print('low exercise:', lo_exerciseCor)
    return dic

print('\nfood_20:')
calculateCorr(food_20)
print('\nfood_50:')
corr50 = calculateCorr(food_50)
print('\nfood_100:')
corr100 =calculateCorr(food_100)
print('\nfood_200:')
calculateCorr(food_200)

# upload correlation result
db_result = couchserver['analysis_result']
try:
    db_result['correlation_food20'] = calculateCorr(food_20)
    db_result['correlation_food50'] = calculateCorr(food_50)
    db_result['correlation_food100'] = calculateCorr(food_100)
    db_result['correlation_food200'] = calculateCorr(food_200)
except:
    print("already exists")
