import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json
import couchdb
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
plt.xlabel('location')                 # plt.xlabel 设置x轴标签
plt.ylabel('population)')
plt.scatter(x, y)
plt.show()'''
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
heart_disease_risk = []
hi_blood_pressure = []
psy_distress = []
lo_exercise = []

def dataGathering(file,region):
    num1=0
    num4 = 0
    num2 = 0
    num3 = 0
    num5 = 0
    num6 = 0
    for i in file['features']:
        if i['properties']['phn_code'] in region:
            num1+=i['properties']['est_ppl_18yrs_plus_obese_2014_15_num']
            num2+=i['properties']['est_ppl_18yrs_plus_ovrwht_2014_15_num']
            num3+=i['properties']['est_ppl_18yrs_plus_wst_meas_ind_rsk_dis_2014_15_num']
            num4+=i['properties']['est_ppl_18yrs_plus_hi_blood_pressure_2014_15_num']
            num5+=i['properties']['est_ppl_18yrs_plus_hi_psyc_strs_k10_scal_2014_15_num']
            num6+=i['properties']['est_ppl_18yrs_plus_lo_exc_prev_wk_2014_15_num']
    obseity.append(num1)
    overweight.append(num2)
    heart_disease_risk.append(num3)
    hi_blood_pressure.append(num4)
    psy_distress.append(num5)
    lo_exercise.append(num6)


dataGathering(sydn, ['PHN101', 'PHN102','PHN103', 'PHN105'])
dataGathering(melb, ['PHN201', 'PHN202','PHN203'])
dataGathering(adel, ['PHN401'])
dataGathering(bris,['PHN301', 'PHN302'])

print("overWeight:",overweight)
print("obesity:",obseity)
print("heart_disease",heart_disease_risk)
print("high blood pressure", hi_blood_pressure)
print("mental depression", psy_distress)
print("low exercise",lo_exercise)


