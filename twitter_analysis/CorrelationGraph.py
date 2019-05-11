'''# test pearson correlation
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
