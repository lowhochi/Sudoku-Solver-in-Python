import os
import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
################################################################### 
# Bubble sort: low performance data
# x = size/1000
x0 = np.array([1.0, 2.0, 4.0, 8.0, 10.0, 20.0])
# y = second*100
y0 = np.array([1.5, 1.6, 4.6, 15.6, 36.0, 132.8])
################################################################### 
# x = size/10000
x = np.array([1.0, 2.0, 4.0, 8.0, 10.0])
# y = second
yB = np.array([0.36, 1.328, 4.203, 13.344, 35.047])
yM = np.array([0.015, 0.015, 0.015, 0.015, 0.031])

plt.plot(x,yB,linewidth=2,color='blue')
plt.plot(x,yM,linewidth=2, linestyle='--',color='red')
plt.axis([0,12,0,40])
plt.grid(True)
plt.show()
