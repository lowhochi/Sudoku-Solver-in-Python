import math
import os
import sys
import numpy as np
from numpy import linalg as la
import pulp
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##A = np.array([[9, 0, 0, 6, 4, 0, 0, 0, 3],
##                 [2, 7, 0, 0, 9, 0, 5, 8, 0],
##                 [0, 1, 0, 5, 8, 0, 0, 0, 0],
##                 [0, 9, 0, 0, 0, 0, 7, 0, 0],
##                 [0, 0, 7, 9, 6, 5, 8, 0, 0],
##                 [0, 0, 2, 0, 0, 0, 0, 4, 0],
##                 [0, 0, 0, 0, 5, 3, 0, 6, 0],
##                 [0, 5, 1, 0, 7, 0, 0, 2, 8],
##                 [4, 0, 0, 0, 1, 6, 0, 0, 5]])

def pulpSolver(A):
    game = np.zeros([9, 9])
    game[:][:] = A[:][:]
    xVar = []
    for m in range(729):
        ii = m//81
        jj = (m - 81*ii)//9
        kk = m - 81*ii - 9*jj
        temp = "x"+str(ii+1)+str(jj+1)+str(kk+1)
        xVar.append(temp)

    sudokuProblem = pulp.LpProblem("sudoku", pulp.LpMaximize)
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
                xtemp0 = xVar[int(81*row+9*col+fillValue)]
                temp = xtemp0+"==1"
                exec("sudokuProblem+= "+temp)

    sudokuProblem.solve()
    B = np.zeros([9,9])
    for row in range(9):
        for col in range(9):
            pos = 0
            for v in range(9):
                number = 0
                xtemp = xVar[81*row + 9*col+ v]
                number = eval("int("+xtemp+".value())")
                if number==1:
                    pos = v
                    break
            B[row][col] = int(pos+1)

    return B

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
