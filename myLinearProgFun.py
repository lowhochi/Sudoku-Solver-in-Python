import math
import numpy as np
from numpy import linalg as la
import random
import matplotlib
import matplotlib.pyplot as plt
# import sympy

colorSet = ['blue', 'red', 'green', 'orange', 'yellow', 'cyan', \
            'purple', 'brown']
            
def switchRow(M, i, j):
    M0 = np.zeros(shape=M.shape)
    M0[:][:] = M[:][:]
    n = M0.shape[1]
    for k in range(0,n):
        temp1 = M0[i,k]
        temp2 = M0[j,k]
        M0[i, k] = temp2
        M0[j, k] = temp1
    return M0

# row_i' = row_i + k0*row_j
def sumRow(M, i, j, k0):
    M0 = np.zeros(shape=M.shape)
    M0[:][:] = M[:][:]
    n = M0.shape[1]
    for k in range(0,n):
        temp = M0[j,k]
        M0[i, k] = M0[i, k] + k0*temp
    return M0

# row_i' = k1*row_i
def prodRow(M, i, k1):
    M0 = np.zeros(shape=M.shape)
    M0[:][:] = M[:][:]
    n = M0.shape[1]
    for k in range(0,n):
        M0[i, k] = k1*M0[i, k]
    return M0

def arrayEqual(u, v):
    n = len(u)
    if (n!=len(v)):
        return False
    else:
        same = True
        for j in range(0,n):
            temp = u[j] - v[j]
            if (temp!=0):
                same = False
        return same

def check_rref(M):
    is_rref = True
    no_of_row = M.shape[0]
    no_of_column = M.shape[1]
    stair = -1
    row_break = False
    for j in range(0, no_of_row):
        if row_break==True:
            break
        for k in range(0, no_of_column):
            if (M[j,k]==0):
                continue
            elif ((M[j,k]!=0)and(k<=stair)):
                is_rref = False
                row_break = True
                break
            elif ((M[j,k]!=0) and (M[j,k]!=1)):
                is_rref = False
                row_break = True
                break
            else:                
                pivot_column = True
                for jj in range(0, no_of_row):
                    if (jj!=j) and (M[jj,k]!=0):
                        pivot_column = False
                        break
                if pivot_column==True:
                    stair = k
                    #print "stair: ", stair
                    break
                else:
                    is_rref = False
                    row_break = True
                    break
    # # # # #             
    return is_rref


def myRref(M):
    M0 = np.zeros(shape=M.shape)
    M0[:][:] = M[:][:]
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    is_rref = check_rref(M0)
    step = 0
    rowNum = 0
    while (is_rref==False) and (step<no_of_col):
        print("rowNum: ", rowNum)
        print("step: ", step)
        # work on column = step
        pivot_entry = M0[rowNum, step]
        if (pivot_entry==0):
            # switchRow
            is_zero_column = True
            for j in range(rowNum, no_of_row):
                if (M0[j, step]!=0):
                    is_zero_column = False
                    M0 = switchRow(M0, j, rowNum)
                    break
            if is_zero_column==True:
                step = step+1
                is_rref = check_rref(M0)
        else:
            # sumRow
            M0 = prodRow(M0, rowNum, 1/pivot_entry)
            for j in range(0, no_of_row):
                if (j!=rowNum):
                    M0 = sumRow(M0, j, rowNum, -M0[j,step])
            step = step+1
            rowNum = rowNum+1
            is_rref = check_rref(M0)
    # # # # #     
    return M0

def findPivot(M):
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    last_row = np.zeros(no_of_col-1)
    last_row[:] = M[(no_of_row-1), 0:(no_of_col-1)]
    pivot_row = 0
    pivot_col = 0
    pos = np.arange(0, no_of_col-1, 1)
    # sort the last row
    for j in range(0, (no_of_col-2)): # last_row[no_of_col-1] can be skipped
        for jj in range(j+1,  no_of_col-1):
            temp = last_row[j]
            if temp>last_row[jj]:
                last_row[j] = last_row[jj]
                last_row[jj] = temp
                pos[jj] = j
                pos[j] = jj
    pivot_col = pos[0]
    ratio = np.zeros(no_of_row-1)
    for k in range(0, no_of_row-1):
        if M[k, pivot_col]==0:
            ratio[k] = 1E6 # big number
            continue
        ratio[k] = float(M[k, (no_of_col-1)])/M[k, pivot_col]

    pos2 = np.arange(0, no_of_row-1,1)
    for k in range(0, no_of_row-2):
        for kk in range(k+1, no_of_row-1):
            temp2 = ratio[k]
            if (temp2>ratio[kk]):
                ratio[k] = ratio[kk]
                ratio[kk] = temp2
                pos2[kk] = k
                pos2[k] = kk

    for kkk in range(0, no_of_row-1):
        if ratio[kkk]>0:
            pivot_row= pos2[kkk]
            break
    return pivot_row, pivot_col

def check_lastRow(M):
    is_done = False
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    last_row = np.zeros(no_of_col-1)
    last_row[:] = M[(no_of_row-1), 0:(no_of_col-1)]
    minValue = np.amin(last_row)
    if (minValue>=0):
        is_done = True
    return is_done

def makeInequality(M, P, is_basic):
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    num_of_variable = 0
    for num in range(0,no_of_col-1):
        if is_basic[num]==True:
            num_of_variable = num_of_variable+1
    variableSet = []
    for num in range(0,num_of_variable):
        variableSet.append('x%d' %(num+1))

    print('max P = ', end='')
    count = 0
    for k in range(0, no_of_col-1):
        if is_basic[k]==True:
            if (count>0) and (P[k]>=0):
                print(' + ',end='')
            elif (count>0) and (P[k]<0):
                print(' - ',end='')
            print(('%.1f' %P[k]),'*',end='')
            print(variableSet[count],end='')
            count = count +1
    print('',end='\n')
    for j in range(0,no_of_row-1):
        count = 0
        for k in range(0, no_of_col-1):
            if is_basic[k]==True:
                if (count>0) and (M[j,k]>=0):
                    print(' + ',end='')
                elif (count>0) and (M[j,k]<0):
                    print(' - ',end='')
                print(('%.1f' %M[j,k]),'*',end='')
                print(variableSet[count],end='')
                count = count + 1
        print(' <= ', ('%.1f' %M[j, no_of_col-1]))   

def LPsolve01(M):
    M0 = np.zeros(M.shape)
    M0[:][:] = M[:][:]
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    is_done = check_lastRow(M0)
    count = 0
    while (is_done==False) and (count<=100): # implement a break here
        count = count+1
        pivot_row, pivot_col = findPivot(M0)
        if M0[pivot_row, pivot_col]==0:
            break
        M0 = prodRow(M0, pivot_row, 1.0/M0[pivot_row, pivot_col])
        for j in range(0, no_of_row):
            if (j!=pivot_row):
                M0 = sumRow(M0, j, pivot_row, -M0[j, pivot_col])

        is_done = check_lastRow(M0)
    return M0

def makeDomain(M, P, is_basic): #only when no of basic variables <= 2
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    temp = np.arange(0, no_of_col-1, 1)
    pos = [num for num in temp if is_basic[int(temp[num])]==True]
    bMax = 0.0
    aMax = 0.0
    for j in range(0, no_of_row-1):
        if (M[j, pos[0]]!=0) and (M[j,pos[1]]!=0):
            a = float(M[j, no_of_col-1])/M[j, pos[0]] # x1=a, x2=0
            b = float(M[j, no_of_col-1])/M[j, pos[1]] # x1= 0, x2=b
            if (a>aMax):
                aMax = a
            if (b>bMax):
                bMax = b
            if (j<6):
                plt.plot([0, a], [b, 0], linewidth=2, color=colorSet[j])
                plt.fill_between([0,a], [0,0], [b,0], color=colorSet[j], alpha=0.1)
            else:
                plt.plot([0, a], [b, 0], linewidth=2, color='cyan')
                plt.fill_between([0,a], [0,0], [b,0], color='cyan', alpha=0.1)
    pMax = max(P[pos[0]]*aMax, P[pos[1]]*bMax)
    h = float(pMax)/10.0
    pValue = np.arange(0.0, pMax+h, h)
    print(pValue)
    for p in pValue:
        a = p/P[pos[0]] #x1=a, x2=0
        b = p/P[pos[1]] #x1=0, x2=b
        plt.plot([0, a], [b, 0], linestyle='--', linewidth=1, color='black')
    plt.axis([-1, math.ceil(aMax)+1, -1, math.ceil(bMax)+1])
    plt.grid(True)
    plt.show()
    #return pos

def roundMatrix(M, r):
    Mrd = np.zeros(M.shape, dtype=float)
    for j in range(0, M.shape[0]):
        for k in range(0, M.shape[1]):
            Mrd[j, k] = round(M[j, k],r)
    return Mrd

def checkPivotColumn(colArray):
    colSum = sum(colArray)
    length = len(colArray)
    num_of_zeros = 0
    pos = 0
    for j in range(0, length):
        if colArray[j]==0:
            num_of_zeros+=1
        if colArray[j]==1:
            pos = j
    if (colSum==1)and (num_of_zeros==(length-1)):
        return True, pos
    else:
        return False, pos

def printSoln(M, P, is_basic):
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    num_of_variable = 0
    for num in range(0,no_of_col-1):
        if is_basic[num]==True:
            num_of_variable = num_of_variable+1
    variableSet = []
    for num in range(0,num_of_variable):
        variableSet.append('x%d' %(num+1))

    print("BFS to LP:")
    count = -1
    for k in range(0,no_of_col-1):
        if is_basic[k]==False:
            continue
        count+=1
        colArray = np.zeros(no_of_row-1)
        for j in range(0, no_of_row-1):
            colArray[j] = M[j,k]
        is_pivot, pos = checkPivotColumn(colArray)
        if is_pivot==False:
            print(variableSet[count]," = 0")
        else:
            print(variableSet[count]," = ", M[pos,-1])


def LPminimize(M):
    rowNum_in_M = M.shape[0]
    colNum_in_M = M.shape[1]
    # in the dual system
    num_of_equation = colNum_in_M -1
    num_of_basic_variable = rowNum_in_M -1
    num_of_slack_variable = colNum_in_M -1
    rowNum_in_Mtwo = colNum_in_M
    # colNum_in_Mtwo = num_of_basic_variable + num_of_slack_variable + 2
    colNum_in_Mtwo = rowNum_in_M + colNum_in_M
    Mtwo = np.zeros([rowNum_in_Mtwo, colNum_in_Mtwo])
    for j in range(0, rowNum_in_Mtwo-1):
        # Part 1: standard part
        for k in range(0, num_of_basic_variable):
            Mtwo[j,k] = M[k,j] # transpose
        #Part 2: last column of Mtwo
        Mtwo[j, num_of_basic_variable+j] = 1
        Mtwo[j,-1] = M[-1,j]
    # Part 3: last row of Mtwo
    P = np.zeros(colNum_in_Mtwo-1)
    for k in range(0, num_of_basic_variable):
        Mtwo[-1,k] = -M[k,-1]
        P[k] = M[k, -1]
    Mtwo[-1,-2] = 1
    is_basic = [True if num!=0 else False for num in P]
    # # # # #
    return Mtwo, P, is_basic

def printDualSoln(Mtwo, P, is_basic):
    num_of_variable = 0
    start = 0
    for k in range(0, len(P)-1): #ignore the P-column
        if is_basic[k]==False:
            num_of_variable+=1
        else:
            start+=1
    variableSet = []
    for num in range(0,num_of_variable):
        variableSet.append('y%d' %(num+1))
    tempList = [Mtwo[-1,kk] for kk in range(start, start+num_of_variable)]
    for pos, value in enumerate(tempList, 0):
        print(variableSet[pos]," = ", end="")
        print(value)
    print ("min value = ", Mtwo[-1][-1])

def checkPivotColumnnTwo(colArray):
    # ref: checkPivotColumn(colArray)
    length = len(colArray)
    colSum = sum(colArray)
    number_of_zeros = 0
    pos = 0
    for j in range(0, length):
        if colArray[j]==0:
            number_of_zeros+=1
        if (colArray[j]==1)or(colArray[j]==-1):
            pos = j
    if (abs(colSum)==1)and (number_of_zeros==(length-1)):
        return True, pos
    else:
        return False, pos


def currentSoln(M, is_basic):
    num_of_variable = sum(is_basic)
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    solnSet = np.zeros(no_of_col-1)
    for k in range(0, no_of_col-1):
        colArray = np.zeros(no_of_row-1)
        for j in range(0, no_of_row-1):
            colArray[j] = M[j,k]
        is_pivot, pos = checkPivotColumnnTwo(colArray)
        if is_pivot==True:
            solnSet[k]=M[pos, no_of_col-1]/M[pos,k]
    signSet = np.zeros(no_of_col-1)
    for k in range(0, no_of_col-1):
        if solnSet[k]>0:
            signSet[k] = 1
        if solnSet[k]<0:
            signSet[k]=-1
        if solnSet[k]==0:
            signSet[k]=0
    return solnSet, signSet


# LPsolve02 for mixed type problem
def LPsolve02(M, P, is_basic):
    M0 = np.zeros(M.shape)
    M0[:][:] = M[:][:]
    no_of_row = M.shape[0]
    no_of_col = M.shape[1]
    solnSet, signSet = currentSoln(M0, is_basic)
    is_done = check_lastRow(M0)and(-1 not in signSet)
    # start
    while (-1 in signSet):
        for k in range(0,no_of_col-1):
            if (signSet[k]==-1):
                is_pivot, pos = checkPivotColumnnTwo(M0[0:no_of_row-1,k])
                for kk in range(0,no_of_col-2):
                    if M0[pos,kk]>0:
                        column01 = kk
                ratio = np.zeros(no_of_row-1)
                posArray = np.arange(0, no_of_row-1,1)
                for j in range(0,no_of_row-1):
                    if M[j,column01]==0:
                        ratio[j]=1E6
                    else:
                        ratio[j]=float(M[j, no_of_col-1])/M[j,column01]
                        
                for m in range(0, no_of_row-2):
                    for n in range(m+1, no_of_row-1):
                        temp = ratio[m]
                        if (ratio[m]>ratio[n]):
                            ratio[m] = ratio[n]
                            ratio[n] = temp
                            posArray[n] = m
                            posArray[m] = n
                for m in range(0, no_of_row-1):
                    if ratio[m]>0: #smallest positive entry
                        row01 = posArray[m]
                        break
                M0 = prodRow(M0, row01, 1.0/M0[row01,column01])
                for j in range(0, no_of_row):
                    if (j!=row01):
                        M0 = sumRow(M0, j, row01, -M0[j, column01])
                solnSet, signSet = currentSoln(M0, is_basic)
                break
    is_done = check_lastRow(M0)      
    count = 0
    while (is_done==False) and (count<=200):
        count = count+1
        pivot_row, pivot_col = findPivot(M0)
        if M0[pivot_row, pivot_col]==0:
            break
        M0 = prodRow(M0, pivot_row, 1.0/M0[pivot_row, pivot_col])
        for j in range(0, no_of_row):
            if (j!=pivot_row):
                M0 = sumRow(M0, j, pivot_row, -M0[j, pivot_col])
        is_done = check_lastRow(M0)
    return M0







