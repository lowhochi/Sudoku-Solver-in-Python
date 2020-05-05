import math
import numpy as np
from numpy import linalg as la
import pulp
import matplotlib
import matplotlib.pyplot as plt
from myLinearProgFun import *
import sympy
import sys
import os

# find rref of a matrix
def example1():
    M = np.array([[1,2,3], [2,4,5], [7,9,10]])
    M1 = np.array([[1,2,3,4], [5,8,10,12], [7, 9, 11, 28]])
    M2 = np.array([[1,0,5,0,3],
               [0,1,3,0,4],
               [0,0,0,1,0]])
    M3 = np.array([[0,1,4,6,0],
               [1,0,3,5,0],
               [0,0,0,0,1]])
    M4 = np.array([[1,2,3,4,5,6,7,8,9,10],
               [2,3,5,7,11,13,17,19,23,29],
               [1,5,10,10,5,1,1,5,10,2]])
    M5 =sympy.Matrix([[1,2,3,4,5,6,7,8,9,10],
               [2,3,5,7,11,13,17,19,23,29],
               [1,5,10,10,5,1,1,5,10,2]])
    M4rref = myRref(M4)
    print(M4rref)
    M5rref = M5.rref()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LP: example2
# max P = 40*x1 + 30*x2
# constraint
# x1+2*x2 <= 16 
# x1+x2 <= 9 
# 3*x1 +2*x2 <= 24 
# x1, x2 >= 0 
def example2():
    P = np.array([40, 30, 0, 0, 0, 0])
    M = np.array([[1, 2, 1, 0, 0, 0, 16],
                  [1, 1, 0, 1, 0, 0, 9],
                  [3, 2, 0, 0, 1, 0, 24],
                  [-40, -30, 0, 0, 0, 1, 0]])
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    is_basic = [True, True, False, False, False, False]
    makeInequality(M, P, is_basic)
    makeDomain(M, P, is_basic)
    Msoln = LPsolve01(M)
    Mrd = roundMatrix(Msoln,2)    
    print(Mrd)
    printSoln(Msoln, P, is_basic)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LP: example3
def example3():
    P = np.array([3, 2, 1, 0, 0, 0, 0])
    M = np.array([[2, 1, 1, 1, 0, 0, 0, 150],
                  [2, 2, 8, 0, 1, 0, 0, 200],
                  [2, 3, 1, 0, 0, 1, 0, 320],
                  [-3, -2, -1, 0, 0, 0, 1, 0]])
    is_basic = [True, True, True, False, False, False, False]
    makeInequality(M, P, is_basic)
    Msoln = LPsolve01(M)
    Mrd = roundMatrix(Msoln,2)    
    print(Mrd)
    printSoln(Msoln, P, is_basic)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LP: example4, minimizing problem
# min P = 8*x1 + 16*x2
# constraint
# x1 + 5*x2 >= 9
# 2*x1 + 2*x2 >= 10
# x1, x2 >= 0
def example4():
    Q = np.array([8, 16])
    M = np.array([[1, 5, 9],
                  [2, 2, 10],
                  [8, 16, 0]])
    Mtwo, P, is_basic = LPminimize(M)
    M2soln = LPsolve01(Mtwo)
    Mrd = roundMatrix(M2soln,2)    
    print(Mrd)
    printDualSoln(Mrd, P, is_basic)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LP: example5, minimizing problem
def example5():
    Q = np.array([1, 3, 7])
    M = np.array([[3, 6, 9, -5],
                  [1, 3, 9, 15],
                  [1, 3, 7, 0]])
    Mtwo, P, is_basic = LPminimize(M)
    M2soln = LPsolve01(Mtwo)
    Mrd = roundMatrix(M2soln,2)    
    print(Mrd)
    printDualSoln(Mrd, P, is_basic)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# pulp to solve example3()
def examplePulp():
    my_problem = pulp.LpProblem("my_LP_Problem", pulp.LpMaximize)
    x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
    x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')
    x3 = pulp.LpVariable('x3', lowBound=0, cat='Continuous')
    # objective function (Z)
    my_problem += 3*x1 + 2*x2 + x3, "Z"
    # constraints
    my_problem += 2*x1+x2+x3<=150
    my_problem += 2*x1+2*x2+8*x3<=200
    my_problem += 2*x1+3*x2+x3<=320
    print(my_problem)
    print("")
    # print solution
    my_problem.solve()
    pulp.LpStatus[my_problem.status]
    for variable in my_problem.variables():
        print("{} = {}".format(variable.name, variable.varValue))
    print(pulp.value(my_problem.objective))

# # # # # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # #
def examplePulp2(): # same question as example5
    # Q = np.array([1, 3, 7])
    # M = np.array([[3, 6, 9, -5],
    #               [1, 3, 9, 15],
    #               [1, 3, 7, 0]])
    my_problem = pulp.LpProblem("my_LP_Problem", pulp.LpMinimize)
    x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
    x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')
    x3 = pulp.LpVariable('x3', lowBound=0, cat='Continuous')
    my_problem += x1+3*x2+7*x3, "Z"
    my_problem += 3*x1+6*x2+9*x3>=-5
    my_problem += 1*x1+3*x2+9*x3>=15
    print(my_problem)
    print("")
    my_problem.solve()
    pulp.LpStatus[my_problem.status]
    for variable in my_problem.variables():
        print("{} = {}".format(variable.name, variable.varValue))
    print(pulp.value(my_problem.objective))
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # #
# LP: example6, non-standard problem
# max P = 120*x1+ 40*x2 + 60*x3
# constraint
# x1 + x2 + x3 <= 100
# 10*x1 + 4*x2 + 7*x3 <= 500
# x1 + x2 + x3 >= 60
# x1, x2, x3 >= 0
def example6():
    P = np.array([120, 40, 60, 0, 0, 0, 0])
    M = np.array([[1, 1, 1, 1, 0 ,0 ,0, 100],
                 [10, 4, 7, 0, 1, 0, 0, 500],
                 [1, 1, 1, 0, 0, -1, 0, 60],
                 [-120, -40, -60, 0, 0, 0, 1, 0]])
    is_basic = [True, True, True, False, False, False, False]
    Mtwo = LPsolve02(M, P, is_basic)
    for j in range(0,M.shape[0]):
        print('[', end='')
        for k in range(0,M.shape[1]):
            print('%8.2f'%Mtwo[j,k] ,end='')
        print(']')

def example6_Pulp():
    eg6Problem = pulp.LpProblem("example6", pulp.LpMaximize)
    x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
    x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')
    x3 = pulp.LpVariable('x3', lowBound=0, cat='Continuous')
    eg6Problem += 120*x1+40*x2+60*x3, "Z"
    eg6Problem += x1 + x2 + x3 <= 100
    eg6Problem += 10*x1 + 4*x2 + 7*x3 <= 500
    eg6Problem += x1 + x2 + x3 >= 60
    print(eg6Problem)
    print("")
    eg6Problem.solve()
    pulp.LpStatus[eg6Problem.status]
    for variable in eg6Problem.variables():
        print("{} = {}".format(variable.name, variable.varValue))
    print(pulp.value(eg6Problem.objective))
# # # # # # # # # # # # # # # # # # # # MAIN # # # # # # # # # # # # # # # # # # # #
example6()








# # #
