import os
import sys
import math
import numpy as np
from numpy import linalg as la
from scipy.linalg import lu
from fractions import Fraction
os.chdir('C:\\Users\\Tony Low\\Desktop\\Python3File')
cwd = os.getcwd()
#######################################################################
def array01():
    a = np.array([1,2,3,4,5])
    b = np.arange(0.0, 1.1, 0.1)
    clist = [3,4,5,6,7]
    c = np.array(clist)
    d = np.array([[1,2,3],
                  [4,5,6],
                  [7,8,9]])
    print("{:*^50s}".format("np.array"))
    print('a = ', a)
    print('a.shape = ', a.shape)
    print('b= ', end=' ')
    print(b)
    print('\nb = [', end=' ')
    for num in b:
        print('%.1f'%num, end='')
        if (num==b[-1]):
            print(']')
        else:
            print(' ', end='')
    print('c = ', c)
    print('d = [', end='')
    for j in range(0,d.shape[0]):
        if j==0:
            print('[',end='')
        else:
            print('{0:5}['.format(' '),end='')
        for k in range(0,d.shape[1]):
            print(d[j][k],end='')
            if (k==(d.shape[1]-1))and(j!=(d.shape[0]-1)):
                print(']',end='\n')
            elif (k==(d.shape[1]-1))and(j==(d.shape[0]-1)):
                print(']',end='')
            else:
                print(' ',end='')
    print(']')
    print("{:*^50s}".format("close: np.array"))
#######################################################################
def basic_operation():
    a = 2.345678
    print("a = ",a)
    print("round(a)= ", round(a))
    print("a up to 2 decimal places= %.2f"%a)
    print("ceil(a)= ", math.ceil(a))
    print("floor(a)= ",math.floor(a))
    A = 12345678
    B = 9876
    print("A/B = ", A/B)
    print("type A/B = ", type(A/B))
    print("A//B = ", A//B)
    print("type A//B = ", type(A//B))
    print("A mod B = ", A%B)
    print("int(A/B) = ", int(A/B))
    b = 0.25
    b2 = Fraction(b)
    print("%.5f is represented by %s" %(b,str(b2)))
          
#######################################################################
def array02():
    a = np.array([1,-6,3])
    b = np.array([-1,-1,1])
    N = np.cross(a,b)
    print("vecor a: ", a)
    print("vector b: ", b)
    print("a cross b: ", N)
    a2 = np.array([1,2,3,4,5,6,7,8])
    print("original array: ",a2)
    b2 = a2.reshape(2,4)
    print("a2.reshape(2,4):")
    print("[",end='')
    print(*b2[0,:], sep=" ", end='') # or print(*b2[0,:])
    print("]\n[", end='')
    print(*b2[1,:], sep=" ", end='')
    print("]")
#######################################################################






