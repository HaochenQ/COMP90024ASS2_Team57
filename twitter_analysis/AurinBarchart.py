"""
Team: 57
Yixin Su (731067, yixins1@student.unimelb.edu.au)
Guoen Jin (935833, guoenj@student.unimelb.edu.au)
Tiantong Li (1037952, tiantongl1@student.unimelb.edu.au)
Haikuan Liu (1010887, haikuanl@student.unimelb.edu.au)
Haochen Qi (964325, hqq@student.unimelb.edu.au)
"""

import numpy as np
import matplotlib.pyplot as plt

'''data = [[33.781,33.288,18.0,26.275],
        [25.15,21.6,14.05,20.675],
        [56.275,52.013,30.3,47.375],
        [27.719,21.012,12.1,18.55],
        [10.944,10.575,7.05,9.1],
        [65.088,55.787,33.45,51.0]]

X = np.arange(5)
plt.bar(X + 0.00, data[0], color = 'b', width = 0.25)
plt.bar(X + 0.25, data[1], color = 'g', width = 0.25)
plt.bar(X + 0.50, data[2], color = 'r', width = 0.25)
plt.bar(X + 0.75, data[3], color = 'r', width = 0.25)
plt.bar(X + 1, data[4], color = 'r', width = 0.25)
plt.bar(X + 1.25, data[5], color = 'r', width = 0.25)
plt.show()'''
N = 6
sydney = (33.781,25.15, 56.725, 21.719, 10.944,65.088)
melbourne = (33.288,21.6,52.013,21.012,10.575,55.787)
adelaide = (18.0,14.05,30.3,12.1,7.05,33.45)
brisbane = (26.275,20.675,47.375,18.55,9.1,51.0)
ind = np.arange(N)
width = 0.20
plt.bar(ind, sydney, width, label='sydney')
plt.bar(ind + width, melbourne, width, label='melbourne')
plt.bar(ind + 2*width, adelaide, width, label='adelaide')
plt.bar(ind + 3*width, brisbane, width, label='brisbane')


plt.ylabel('ratio of people',size=12)
plt.title('Health Condition in Four Cities',size=18)

plt.xticks(ind + width*1.5 , ('overweight','obesity','chronic disease risk',
       'high blood pressure','mental depression','low exercise'),rotation=-30,size = 12)
plt.legend(loc='best')
plt.show()
