
# https://www.coin-or.org/PuLP/CaseStudies/a_sudoku_problem.html
import math
import os
import sys
import numpy as np
from numpy import linalg as la
import pulp
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
game = np.array([[2,0,0,0],
                 [0,1,0,2],
                 [0,0,3,0],
                 [0,0,0,4]])
# create 64 unknowns 
# xVar[m] = x_[ijk]
# row: ii = m//16
# column: jj = (m - 16*i)//4
# value: kk = m - 16*i - 4*j
xVar = []
for m in range(0, 64):
    ii = m//16
    jj = (m - 16*ii)//4
    kk = m - 16*ii - 4*jj
    temp = "x"+str(ii+1)+str(jj+1)+str(kk+1)
    xVar.append(temp)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
sudokuProblem = pulp.LpProblem("sudoku4", pulp.LpMaximize)
for m in range(0, 64):
    temp = xVar[m]+"=pulp.LpVariable('"+xVar[m]\
           +"', lowBound=0, upBound=1, cat='Integer')"
    exec(temp)
    
#objective function    
sudokuProblem += 0, "P"

# \sum_{col} x[row][col][v] = 1
# On every row, every number appears once
for row in range(4):
    for v in range(4):
        xtemp0 = xVar[16*row +4*0 +v]
        xtemp1 = xVar[16*row +4*1 +v]
        xtemp2 = xVar[16*row +4*2 +v]
        xtemp3 = xVar[16*row +4*3 +v]
        temp = xtemp0+"+"+xtemp1+"+"+xtemp2+"+"+xtemp3
        temp = temp+"==1"
        exec("sudokuProblem+= "+temp)
        
# \sum_{row} x[row][col][v] = 1
# On every column, every number appears once
for col in range(4):
    for v in range(4):
        xtemp0 = xVar[16*0 +4*col +v]
        xtemp1 = xVar[16*1 +4*col +v]
        xtemp2 = xVar[16*2 +4*col +v]
        xtemp3 = xVar[16*3 +4*col +v]
        temp = xtemp0+"+"+xtemp1+"+"+xtemp2+"+"+xtemp3
        temp = temp+"==1"
        exec("sudokuProblem+= "+temp)

# \sum_{v} x[row][col][v] = 1
# Every position (row, col) is filled by a number 1/2/3/4
for row in range(0,4):
    for col in range(0,4):
        xtemp0 = xVar[16*row +4*col +0]
        xtemp1 = xVar[16*row +4*col +1]
        xtemp2 = xVar[16*row +4*col +2]
        xtemp3 = xVar[16*row +4*col +3]
        temp = xtemp0+"+"+xtemp1+"+"+xtemp2+"+"+xtemp3
        temp = temp+"==1"
        exec("sudokuProblem+= "+temp)

# \sum_{r,c in block} x[r][c][v] = 1
# In every block, every number appears once
# block[num, k]:
#   num = block number = 0,1,2,3
#   k = position index in a block = 0,1,2,3
# block[num, k] = m value at x_(row)(column)(1) 
block = np.zeros([4, 4]) 
for num in range(0,4):
    m0 = 2*(num//2)
    n0 = 2*(num-2*(num//2))
    block[num,0] = int(16*m0 +4*n0)
    block[num,1] = int(16*m0 +4*n0 +4)
    block[num,2] = int(16*(m0+1) +4*n0)
    block[num,3] = int(16*(m0+1) +4*n0 +4)        
for v in range(4):
    for num in range(4):
        xtemp0 = xVar[int(block[num,0]+v)]
        xtemp1 = xVar[int(block[num,1]+v)]
        xtemp2 = xVar[int(block[num,2]+v)]
        xtemp3 = xVar[int(block[num,3]+v)]
        temp = xtemp0+"+"+xtemp1+"+"+xtemp2+"+"+xtemp3
        temp = temp+"==1"
        exec("sudokuProblem+= "+temp)

# known values
for row in range(4):
    for col in range(4):
        fillValue = game[row, col]
        if fillValue!=0:
            fillValue-=1
            xtemp0 = xVar[16*row+4*col+fillValue]
            temp = xtemp0+"==1"
            exec("sudokuProblem+= "+temp)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
sudokuProblem.solve()
pulp.LpStatus[sudokuProblem.status]
for variable in sudokuProblem.variables():
    print("{} = {}".format(variable.name, variable.varValue))
# print(pulp.value(sudokuProblem.objective))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    

