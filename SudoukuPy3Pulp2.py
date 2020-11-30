import math
import os
import sys
import numpy as np
from numpy import linalg as la
import pulp

import matplotlib
import matplotlib.pyplot as plt
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##game = np.array([[9, 0, 0, 6, 4, 0, 0, 0, 3],
##                 [2, 7, 0, 0, 9, 0, 5, 8, 0],
##                 [0, 1, 0, 5, 8, 0, 0, 0, 0],
##                 [0, 9, 0, 0, 0, 0, 7, 0, 0],
##                 [0, 0, 7, 9, 6, 5, 8, 0, 0],
##                 [0, 0, 2, 0, 0, 0, 0, 4, 0],
##                 [0, 0, 0, 0, 5, 3, 0, 6, 0],
##                 [0, 5, 1, 0, 7, 0, 0, 2, 8],
##                 [4, 0, 0, 0, 1, 6, 0, 0, 5]])

game = np.array([[0, 6, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 5, 3, 0, 8, 0, 6, 0],
                 [0, 0, 0, 0, 6, 0, 0, 7, 4],
                 [0, 0, 7, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 4, 5, 0, 1, 8],
                 [0, 8, 0, 0, 0, 0, 0, 0, 3],
                 [5, 0, 0, 0, 0, 3, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 6, 4, 0],
                 [0, 0, 0, 9, 0, 0, 0, 0, 0]])

# create 729 unknowns
# xVar[m] = x_[ijk]
# row: ii = m//81
# column: jj = (m - 81*ii)//9
# value: kk = m - 81*ii - 9*jj
xVar = []
for m in range(729):
    ii = m//81
    jj = (m - 81*ii)//9
    kk = m - 81*ii - 9*jj
    temp = "x"+str(ii+1)+str(jj+1)+str(kk+1)
    xVar.append(temp)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

sudokuProblem = pulp.LpProblem("sudoku9", pulp.LpMaximize)
for m in range(729):
    temp = xVar[m]+"=pulp.LpVariable('"+xVar[m]\
           +"', lowBound=0, upBound=1, cat='Integer')"
    exec(temp)
#objective function    
sudokuProblem += 0, "P"

# \sum_{col} x[row][col][v] = 1
# On every row, every number appears once
for row in range(9):
    for v in range(9):
        temp = ""
        for p in range(9):
            xtemp = xVar[81*row +9*p +v]
            if (p!=8):
                temp = temp+xtemp+"+"
            else:
                temp = temp+xtemp
        temp = temp+"==1"
        exec("sudokuProblem+= "+temp)

# \sum_{row} x[row][col][v] = 1
# On every column, every number appears once
for col in range(9):
    for v in range(9):
        temp = ""
        for p in range(9):
            xtemp = xVar[81*p +9*col +v]
            if (p!=8):
                temp = temp+xtemp+"+"
            else:
                temp = temp+xtemp
        temp = temp+"==1"
        exec("sudokuProblem+= "+temp)

# \sum_{v} x[row][col][v] = 1
# Every position (row, col) is filled by a number 1/2/3/4/5/6/7/8/9
for row in range(9):
    for col in range(9):
        temp = ""
        for p in range(9):
            xtemp = xVar[81*row +9*col +p]
            if (p!=8):
                temp = temp+xtemp+"+"
            else:
                temp = temp+xtemp
        temp = temp+"==1"
        exec("sudokuProblem+= "+temp)


# \sum_{r,c in block} x[r][c][v] = 1
# In every block, every number appears once
# block[num, k]:
#   9 blocks are labelled from left to right, top to bottom
#       num = block number = 0,1,2,3,4,5,6,7,8
#   each block has 9 entries, labelled from left to right, top to bottom
#       k = position index in a block = 0,1,2,3,4,5,6,7,8
#   block[num, k] = m value at x_(row)(column)(1) 
block = np.zeros([9, 9]) 
for num in range(9):
    # block 0,1,2: first entry of xVar is on row=0 (m0=0)
    # block 3,4,5: first entry of xVar is on row=3 (m0=3)
    # block 6,7,8: first entry of xVar is on row=6 (m0=6)
    m0 = 3*(num//3)
    # block 0,3,6, first entry of xVar is on col=0 (n0=0)
    # block 1,4,7, first entry of xVar is on col=3 (n0=3)
    # block 2,5,8, first entry of xVar is on col=6 (n0=6)
    n0 = 3*(num - m0)
    block[num,0] = 81*m0 + 9*n0 #first entry
    block[num,1] = 81*m0 + 9*(n0+1)
    block[num,2] = 81*m0 + 9*(n0+2)
    block[num,3] = 81*(m0+1) + 9*n0
    block[num,4] = 81*(m0+1) + 9*(n0+1)
    block[num,5] = 81*(m0+1) + 9*(n0+2)
    block[num,6] = 81*(m0+2) + 9*n0
    block[num,7] = 81*(m0+2) + 9*(n0+1)
    block[num,8] = 81*(m0+2) + 9*(n0+2)
for v in range(9):
    for num in range(9):
        temp = ""
        for p in range(9):
            xtemp = xVar[int(block[num,p]+v)]
            if (p!=8):
                temp = temp+xtemp+"+"
            else:
                temp = temp+xtemp
        temp = temp+"==1"
        exec("sudokuProblem+= "+temp)

# known values
for row in range(9):
    for col in range(9):
        fillValue = game[row, col]
        if fillValue!=0:
            fillValue-=1
            xtemp0 = xVar[81*row+9*col+fillValue]
            temp = xtemp0+"==1"
            exec("sudokuProblem+= "+temp)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

sudokuProblem.solve()
##pulp.LpStatus[sudokuProblem.status]
##for variable in sudokuProblem.variables():
##    print("{} = {}".format(variable.name, variable.varValue))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
fig = plt.figure()
ax = plt.gca()
ax.set_aspect('equal')    
ax.axis('off')
ax.set_xlim([0, 9])
ax.set_ylim([0, 9])

for p in range(0,10):
    ax.plot([0, 9], [p, p], color='blue', linestyle='--')
    ax.plot([p, p], [0, 9], color='blue', linestyle='--')
for row in range(0, 3):
    for col in range(0,3):
        ax.fill_between([col, col+1], row, row+1, \
                        facecolor='green', alpha=0.5)
        ax.fill_between([col+3, col+4], row, row+1, \
                        facecolor='lime', alpha=0.5)
        ax.fill_between([col+6, col+7], row, row+1, \
                        facecolor='lemonchiffon', alpha=0.5)
for row in range(3,6):
    for col in range(0,3):
        ax.fill_between([col, col+1], row, row+1, \
                        facecolor='cyan', alpha=0.5)
        ax.fill_between([col+3, col+4], row, row+1, \
                        facecolor='violet', alpha=0.5)
        ax.fill_between([col+6, col+7], row, row+1, \
                        facecolor='pink', alpha=0.5)

for row in range(6,9):
    for col in range(0,3):
        ax.fill_between([col, col+1], row, row+1, \
                        facecolor='yellow', alpha=0.5)
        ax.fill_between([col+3, col+4], row, row+1, \
                        facecolor='orange', alpha=0.5)
        ax.fill_between([col+6, col+7], row, row+1, \
                        facecolor='gold', alpha=0.5)
        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
originalBlock = np.zeros([9,9], dtype=np.int32)
for row in range(0,9):
    for col in range(0,9):
        value = game[row, col]
        if value!=0:
            originalBlock[row, col] = 1
            ax.text(col+0.25, 8.25-row, str(value), size=20, color='black')

for row in range(0,9):
    for col in range(0,9):
        if originalBlock[row, col]==1:
            continue
        pos = 0
        for v in range(0,9):
            temp = 0
            xtemp = xVar[81*row + 9*col+ v]
            exec("temp=int("+xtemp+".value())")
            if temp==1:
                pos = v
                break
        ax.text(col+0.25, 8.25-row, str(pos+1), size=20, color='red')

plt.show()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

