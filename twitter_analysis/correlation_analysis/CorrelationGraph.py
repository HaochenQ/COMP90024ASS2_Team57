"""
Team: 57
Yixin Su (731067, yixins1@student.unimelb.edu.au)
Guoen Jin (935833, guoenj@student.unimelb.edu.au)
Tiantong Li (1037952, tiantongl1@student.unimelb.edu.au)
Haikuan Liu (1010887, haikuanl@student.unimelb.edu.au)
Haochen Qi (964325, hqq@student.unimelb.edu.au)
"""

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

objects = ('overweight','obesity','chronic disease risk',
       'high blood pressure','mental depression','no/low exercise')
y_pos = np.arange(len(objects))
performance = [0.669, 0.506, 0.625, 0.695, 0.638, 0.515]

plt.barh( y_pos, performance, height= 0.5, align='center', alpha=0.5, color='#000080')
plt.yticks(y_pos, objects,size=11)
plt.xlabel('Correlation coefficient',size=11)
plt.title('Correlation coefficients between \n glutton tweets(100 words) and health problems',size=13)

plt.show()
