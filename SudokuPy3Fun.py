from sympy import *
import math
import numpy as np
import sys
import os
import time
reference = [9,8,7,6,5,4,3,2,1]
ref_tuple = tuple(reference)

#count no. of blanks on M
def countBlank(M):
    number_of_blank = 0
    for i in range(0,9):
        for j in range(0,9):
            if (M[i,j]==0):
                number_of_blank+=1
    return number_of_blank

def myBlockIndex(k): #k = location in myArray[]
    block00 = [0,1,2,9,10,11,18,19,20]
    block03 = [i+3 for i in block00]
    block06 = [i+6 for i in block00]
    block30 = [i+27 for i in block00]
    block33 = [i+30 for i in block00]
    block36 = [i+33 for i in block00]
    block60 = [i+54 for i in block00]
    block63 = [i+57 for i in block00]
    block66 = [i+60 for i in block00]
    if (k in block00):
        return block00   
    if (k in block03):
        return block03
    if (k in block06):
        return block06
    if (k in block30):
        return block30
    if (k in block33):
        return block33
    if (k in block36):
        return block36
    if (k in block60):
        return block60
    if (k in block63):
        return block63
    if (k in block66):
        return block66

# create fillMatrix of the puzzle M
def fillBlank(M):
    fillMatrix = np.zeros([81, 9])
    for i in range(0,81):
        for j in range(0,9):
            fillMatrix[i,j] = j+1
    # take away impossible numbers
    for i in range(0,9):
        for j in range(0,9):
            myBlock = myBlockIndex(9*i+j)
            if M[i,j]!=0:
                fixNum = M[i,j]
                for k in range(0,9):
                    # fix-number at position (i,j)
                    if (k!=(M[i,j]-1)):
                        fillMatrix[9*i+j,k]=0
                    # row-check and column-check
                    if k!=j:
                        fillMatrix[9*i+k,int(M[i,j]-1)]=0
                    if k!=i:
                        fillMatrix[9*k+j,int(M[i,j]-1)]=0
                # block-check
                for m in myBlock:
                    if (m!=(9*i+j)):
                        fillMatrix[m,int(M[i,j]-1)]=0
    return fillMatrix

# myArray = a np-array of shape = (1,81)
def myRowCheck(myArray):
    valid = True
    for myRow in range(0,9):
        for i in range(0,9):
            for j in range(i+1,9):
                if (myArray[0,i+9*myRow]!=0)and(myArray[0,i+9*myRow]==myArray[0,j+9*myRow]):
                    valid = False
    return valid

def myColumnCheck(myArray):
    valid = True
    for myColumn in range(0,9):
        for i in range(0,9):
            for j in range(i+1,9):
                if (myArray[0,9*i+myColumn]!=0)and(myArray[0,9*i+myColumn]==myArray[0,9*j+myColumn]):
                    valid = False
    return valid

def myBlockCheck(myArray):
    valid = True
    for myNum in [0,3,6,27,30,33,54,57,60]:
        myBlock = myBlockIndex(myNum)
        for i in range(0,9):
            N1 = myBlock[i]
            for j in range(i+1,9):           
                N2 = myBlock[j]
                if (myArray[0,N1]!=0)and(myArray[0,N1]==myArray[0,N2]):
                    valid=False                   
    return valid

def checkConsistent(M, fMatrix):
    # fillMatrix = fillBlank(M)
    tempArray = np.zeros([1,81])
    for i in range(0,9):
        for j in range(0,9):
            tempArray[0,9*i+j]=M[i,j]
    rowValid = myRowCheck(tempArray)
    columnValid = myColumnCheck(tempArray)
    blockValid = myBlockCheck(tempArray)
    if (rowValid==False)or(columnValid==False)or(blockValid==False):
        return False
    else:
        for j in range(0,81):
            mySum = sum(fMatrix[j,:])
            if mySum==0:
                return False
    return True

def countCombination(fMatrix):
    shape_of_fMatrix = fMatrix.shape
    no_of_Row = shape_of_fMatrix[0]
    no_of_Column = shape_of_fMatrix[1]
    no_of_combination = 1
    for i in range(0,no_of_Row):
        myCount = 0
        for j in range(0,no_of_Column):
            if fMatrix[i,j]!=0:
                myCount = myCount+1
        no_of_combination = no_of_combination*myCount
    return no_of_combination

# insert sudoku2 here for efficiency
def firstFill(M, fillMatrix):
    M01 = np.zeros([9,9])
    fillMatrix01 = np.zeros([81,9])
    for i in range(0,9):
        for j in range(0,9):
            M01[i][j]=M[i][j]
    for i in range(0,81):
        for j in range(0,9):
            fillMatrix01[i][j] = fillMatrix[i][j]

    number_of_blank = countBlank(M)
    valid = checkConsistent(M, fillMatrix)
    if valid==False:
        return M, fillMatrix, False

    myDoneList = []
    for i in range(0,81):
        if M[i/9,i%9]!=0:
            myDoneList.append(i)
           
    while (number_of_blank>0):
        safe = number_of_blank
        for rowNum in range(0,81):
            number_of_zero = 0
            for j in range(0,9):
                if fillMatrix01[rowNum,j]==0:
                    number_of_zero += 1
            if number_of_zero==8:
                Num1 = rowNum//9 #Python3
                Num2 = rowNum%9
                if (rowNum not in myDoneList):
                    myDoneList.append(rowNum)
                    number_of_blank =number_of_blank-1
                    M01[Num1,Num2] = int(sum(fillMatrix01[rowNum,:]))
                    fillMatrix01 = fillBlank(M01)
                    break
 
        if (safe==number_of_blank):
            break

    valid01 =  checkConsistent(M01,fillMatrix01) 
    return M01, fillMatrix01, valid01

# bootstrapping
def myBootstrap(M,fillMatrix):
    M01 = np.zeros([9,9])
    M01[:][:]= M[:][:]
    fillMatrix01 = np.zeros([81,9])
    fillMatrix01[:][:] = fillMatrix[:][:]
    print("\nRunning: myBootstrap(M,fillMatrix)") #Python3
    # start_time = time.time()
    total = countCombination(fillMatrix)
    tempNum = total
    divisor = []
    # make sure divisor is well defined
    valid01 = checkConsistent(M, fillMatrix)
    if valid01==False:
        print("Inconsistent input") #Python3
        return M01, fillMatrix01, False
    for rowNum in range(0,81):
        if rowNum==80:
            divisor.append(1)
            break
        myCount = 0
        for j in range(0,9):
            if fillMatrix[rowNum,j]!=0:
                myCount+=1
        tempNum = tempNum//myCount #Python3
        divisor.append(tempNum)

    position = np.zeros([1,81])
    step = total//long(1E6) #Python3
    print("total = ", str(total)) #Python3
    print("step = ", str(step)) #Python3
    if step==0:
        for Num in range(0,total):
            if (Num%1000==0):
                print("Num =", str(Num)) #Python3
            for k in range(0,81):
                position[0,k] = int(Num//divisor[k]) #Python3
                Num = Num - divisor[k]*position[0,k]
                # return a filled M at this step Num
                myRow = [i for i in fillMatrix[k,:] if (i!=0)]
                fillValue = myRow[position[0,k]]
                M01[k/9,k%9] = int(fillValue)
            # check valid
            fillMatrix01 = fillBlank(M01)
            valid01 = checkConsistent(M01,fillMatrix01)
            if valid01==True:
                break

    else:
        bPoint=False
        for stepNum in range(0,step+1):
            print("stepNum =", str(stepNum)) #Python3
            if (stepNum<step):
                listTemp = [j for j in range(stepNum*long(1E6), (stepNum+1)*long(1E6))]
            else:
                listTemp = [j for j in range(step*long(1E6),total)]

            for Num in listTemp:
                for k in range(0,81):
                    position[0,k] = int(Num//divisor[k]) #Python3
                    Num = Num - divisor[k]*position[0,k]
                    # return a filled M at this step Num
                    myRow = [i for i in fillMatrix[k,:] if (i!=0)]
                    fillValue = myRow[int(position[0,k])]
                    M01[k/9,k%9] = int(fillValue)
                # check valid
                fillMatrix01 = fillBlank(M01)
                valid01 = checkConsistent(M01, fillMatrix01)
                if valid01==True:
                    bPoint=True
                    break
                
            if bPoint==True:
                break

    # elapsed_time = time.time()-start_time
    # print "Elapsed Time =", str(elapsed_time), " seconds"
    return M01, fillMatrix01, valid01

# count number of dual-blanks in M and list out the position
def listDB(fillMatrix):
    list_of_dualBlank = []
    for i in range(0,81):
        myCount=0
        for j in range(0,9):
            if (fillMatrix[i,j]!=0):
                myCount+=1
        if myCount==2:
            list_of_dualBlank.append(i)
    number_of_dualBlank = len(list_of_dualBlank)
    return list_of_dualBlank, number_of_dualBlank

def makeCase(M, fillMatrix, list_of_dualBlank, numDB):
    numDB = min(numDB,15)
    if numDB>15:
        list_of_dualBlank = list_of_dualBlank[0:15]

    choice_of_dualBlank = np.zeros([numDB,2])
    #choice_of_dualBlank[i,0],choice_of_dualBlank[i,1],
    # = dual choices on the row represented by list_of_dualBlank[i]
    for i in range(0,numDB):
        rowNum = list_of_dualBlank[i]
        myCount = 0
        for j in range(0,9):
            if fillMatrix[rowNum,j]!=0:
                choice_of_dualBlank[i,myCount]=fillMatrix[rowNum,j]
                myCount += 1
    # caseArray stores all possible case by the choice_of_dualBlank
    # caseArray[0,myNum][0,k] = the i-th possible filling at location k.
    #   k-th position of list_of_dualBlank[j]: y,
    #   The M[y/9,y%9] should be filled by caseArray[0,myNum][0,k]
    caseArray = np.empty([1,pow(2,numDB)], dtype=object)
    posArray = np.zeros([pow(2,numDB),numDB])
    for myNum in range(0,pow(2,numDB)):
        temp = myNum
        for j in range(0,numDB):
            posArray[myNum,j] = int(temp//pow(2,numDB-1-j)) #Python3
            temp = temp - int(posArray[myNum,j]*pow(2,numDB-1-j))
    # Careful! pow returns a float, instead of int   
    for myNum in range(0,pow(2,numDB)):
        caseArray[0,myNum]=np.zeros([1,numDB])
        for k in range(0,numDB):
            caseArray[0,myNum][0,k] = int(choice_of_dualBlank[k,posArray[myNum,k]])

    return caseArray 

def myFinish(M):
    stop = 0
    for i in range(0,9):
        for j in range(0,9):
            if M[i,j]==0:
                stop=1
                break
        if stop==1:
            break
    if stop==0:
        return True
    else:
        return False

# PreSolveEngine: similar to mySolveEngine but without self-recursion. 
# AfillMatrix = fillBlank(A3)
# myValid = checkConsistent(A3, AfillMatrix)
# A, AfillMatrix, myValid = PreSolveEngine(A3,AfillMatrix, myValid)
def PreSolveEngine(M,fillMatrix, valid):
    no_of_blank = countBlank(M)
    print("number of blank =", no_of_blank) #Python3
    if valid==False:
        return M, fillMatrix, False
    elif no_of_blank<10:
        print("number of blanks<10") #Python3
        print(M)
        print("T/F value:", valid)
        return M, fillMatrix, valid

    else:    
        list_of_dualBlank, numDB = listDB(fillMatrix)
        Mcopy = np.zeros([9,9])
        for m1 in range(0,9):
            for m2 in range(0,9):
                Mcopy[m1][m2] = M[m1][m2]
        if numDB==0:
            return M, fillMatrix, True
        else:
            print("Make Case") #Python3
            caseArray = makeCase(M, fillMatrix, list_of_dualBlank, numDB)
            numDB = min(numDB,15)
            bPoint = False
            # Useful: print caseArray

            for i in range(0,pow(2,numDB)):
                for n1 in range(0,9):
                    for n2 in range(0,9):
                        M[n1,n2]=Mcopy[n1][n2]

                for j in range(0,numDB):
                    Num1 = int(list_of_dualBlank[j]//9) #Python3
                    Num2 = int(list_of_dualBlank[j]%9)
                    M[Num1,Num2] = caseArray[0,i][0,j]

                fillMatrix01 = fillBlank(M)
                valid01 = checkConsistent(M, fillMatrix01)
                if (i==(pow(2,numDB)-1)):
                    print("End at last term")
                    return M, fillMatrix01, valid01
                elif valid01==False:
                    continue
                
                print("\n") #Python3
                print(M)
                print("\n")
                print("\nT/F value:", valid01)
                # Caution about side effect here
                M02, fillMatrix02, valid02 = PreSolveEngine(M[:][:] ,fillMatrix01, True)
                if valid02==True:
                    return M02, fillMatrix02, valid02

# copy the puzzle.
def copyPuzzle(M):
    N = np.zeros([9,9],dtype=int)
    for i in range(0,9):
        for j in range(0,9):
            N[i,j]=int(M[i][j])
    return N

# fill by exhaustion in (1,2,3,4,5,6,7,8,9)
def myExhaustFill(M, fillMatrix):
    M01 = np.zeros([9,9])
    M01[:][:] = M[:][:]
    fillMatrix01 = np.zeros([81,9])
    fillMatrix01[:][:] = fillMatrix[:][:]
    print("\nRunning: myExhaustFill(M, fillMatrix)") #Python3
    number_of_blank = countBlank(M)
    valid = checkConsistent(M, fillMatrix)
    if valid==False:
        print("Inconsistent input")
        return M01, fillMatrix01, False

    while (number_of_blank>0):
        safe = number_of_blank
        bPoint = False
        for i in reference:
            for rowNum in range(0,9):
                appearance = 0
                fillpos = 0
                for j in range(0,9):
                    if (i in fillMatrix01[9*rowNum+j,:]):
                        fillpos = j
                        appearance += 1
                if (appearance==1)and(M01[rowNum,fillpos]==0):
                    M01[rowNum, fillpos]=i
                    fillMatrix01 = fillBlank(M01)
                    number_of_blank = number_of_blank-1
                    bPoint = True
                    break

            for colNum in range(0,9):
                appearance = 0
                fillpos = 0
                for j in range(0,9):
                    if (i in fillMatrix01[9*j+colNum,:]):
                        fillpos = j
                        appearance += 1
                if (appearance==1)and(M01[fillpos,colNum]==0):
                    M01[fillpos, colNum]=i
                    fillMatrix01 = fillBlank(M01)
                    number_of_blank = number_of_blank-1
                    bPoint = True
                    break

            for myNum in [0,3,6,27,30,33,54,57,60]:
                myBlock = myBlockIndex(myNum)
                # block00 = [0,1,2,9,10,11,18,19,20]
                appearance = 0
                fillpos = 0
                for j in myBlock:
                    if (i in fillMatrix01[j,:]):
                        fillpos = j
                        appearance +=1
                if (appearance==1)and (M01[int(fillpos/9), int(fillpos%9)]==0):
                    M01[int(fillpos//9), int(fillpos%9)]=i #Python3
                    fillMatrix01 = fillBlank(M01)
                    number_of_blank = number_of_blank-1
                    bPoint = True
                    break

            if bPoint==True:
                break

        if (safe==number_of_blank):
            print("Run ends") #Python3
            break       
    valid01 = checkConsistent(M01, fillMatrix01)
    blankLeft = countBlank(M01)
    print("Number of blanks left =", str(blankLeft)) #Python3
    return M01, fillMatrix01, valid01

def mySolveEngine(M, fillMatrix, valid, total):
    total01 = total
    M01 = np.zeros([9,9])
    M01[:][:] = M[:][:]
    fillMatrix01 = np.zeros([81,9])
    fillMatrix01[:][:] = fillMatrix[:][:]
    print("\nRunning: mySolveEngine(M, fillMatrix, valid, total)") #Python3
    # start_time = time.time()
    if valid==False:
        print("Inconsistent input") #Python3
        return M01, fillMatrix01, False
    elif (total<1E6): # total< maximum number is required here.
        print("Start Bootstrapping") #Python3
        M02, fillMatrix02, valid02 = myBootstrap(M, fillMatrix)
        if valid02==True:
            return M02, fillMatrix02, True
        else:
            print("Inconsistent input") #Python3
            return M01, fillMatrix01, False

    else: # total>1E6
        print("Start exhaust Fill") #Python3
        M05, fillMatrix05, valid05 = myExhaustFill(M01, fillMatrix01)
        finish05 = myFinish(M05)
        if valid05==False:
            print("Inconsistent input") #Python3
            return M01, fillMatrix01, False
        elif (valid05==True)and(finish05==True):
            return M05, fillMatrix05, True
        else:
            list_of_dualBlank, numDB = listDB(fillMatrix01)
            if (numDB==0):
                print("Hard Puzzle Warning") #Python3
                M03, fillMatrix03, valid03 = myBootstrap(M01, fillMatrix01)
                if valid03==True:
                    return M03, fillMatrix03, True
                else:
                    print("Inconsistent input") #Python3
                    return M01, fillMatrix01, False
            else:
                M01[:][:]=M05[:][:]
                fillMatrix01[:][:] = fillMatrix05[:][:]
                Mtup = tuple(M01)
                print("Make Case. Number of DB(<=15) :", str(min(numDB,15))) #Python3
                caseArray = makeCase(M01, fillMatrix01, list_of_dualBlank, numDB)
                numDB = min(numDB,15)
                for i in range(0,pow(2,numDB)):
                    #print ("i = "+str(i))
                    for n1 in range(0,9):
                        for n2 in range(0,9):
                            M01[n1,n2]=Mtup[n1][n2]
            
                    for j in range(0,numDB):
                        Num1 = int(list_of_dualBlank[j]//9) #Python3
                        Num2 = int(list_of_dualBlank[j]%9)
                        M01[Num1,Num2] = caseArray[0,i][0,j]

                    fillMatrix01 = fillBlank(M01)
                    valid01 = checkConsistent(M01, fillMatrix01)
                    total01 = countCombination(fillMatrix01)
                    if i==(pow(2,numDB)-1):
                        # elasped_time = time.time()-start_time
                        # print "Elasped time =", str(elasped_time)
                        return M01, fillMatrix01, valid01
                    elif valid01==False:
                        continue
                    else:
                        # Recursion
                        print("Recursion in. Current puzzle is:") #Python3
                        print(M01) #Python3
                        M04, fillMatrix04, valid04 = mySolveEngine(M01, fillMatrix01, valid01, total01)
                        print("Recursion out") #Python3
                        if valid04==True:
                        # elapsed_time = time.time()-start_time
                        # print "Elasped time =", str(elapsed_time), "in seconds"
                            return M04, fillMatrix04, True


# On Progress: the non-dual blank engine
def makeCaseNDB(M, fMatrix):
    countVec = np.zeros([2,81])
    countVec[0,:] = np.arange(0,81,1)
    for i in range(0,81):
        myRow = [num for num in fMatrix[i,:] if (num!=0)]
        countVec[1][i] = len(myRow)
    # sort
    tempNum = 0
    tempPos = 0
    for i in range(0,81):
        for j in range(i+1,81):
            if countVec[1][i]>countVec[1][j]:
                tempNum = countVec[1][i]
                tempPos = countVec[0][i]
                countVec[1][i] = countVec[1][j]
                countVec[1][j] = tempNum
                countVec[0][i] = countVec[0][j]
                countVec[0][j] = tempPos
    posVec =[]
    start = 0
    for Num in range(0,5):
        for i in range(start,81):
            if (countVec[1][i]!=1):
                posVec.append(int(countVec[0][i]))
                start = i+1
                break
    choice_of_blanks = np.empty([1,5],dtype=object)
    for Num in range(0,5):
        myRow = [int(j) for j in fMatrix[posVec[Num],:] if (j!=0)]
        choice_of_blanks[0][Num] = myRow

    caseTotal = 1
    for Num in range(0,5):
        caseTotal = caseTotal*len(choice_of_blanks[0][Num])
    caseTotal = int(caseTotal)

    caseArray = np.empty([1,caseTotal],dtype=object)
    posArray = np.zeros([caseTotal, 5])
    for myNum in range(0,caseTotal):
        tempNum2 = myNum
        divisor = caseTotal
        for j in range(0,5):
            divisor = divisor//len(choice_of_blanks[0][j]) #Python3
            posArray[myNum][j] = int(tempNum2//divisor) #Python3
            tempNum2 = tempNum2 - divisor*posArray[myNum][j]

    for myNum in range(0,caseTotal):
        caseArray[0,myNum] = np.zeros([1,5])
        for j in range(0,5):
            tempArray = choice_of_blanks[0][j]
            caseArray[0,int(myNum)][0,j] = tempArray[int(posArray[myNum][j])]
    
    return posVec, caseArray, caseTotal


def NDBsolveEngine(M, fillMatrix, valid, total):
    M01 = np.zeros([9,9])
    M01[:][:] = M[:][:]
    fillMatrix01 = np.zeros([81,9])
    fillMatrix01[:][:] = fillMatrix[:][:]
    total01=total
    valid01 = valid
    if valid==False:
        return M, fillMatrix, False
    
    elif (total01<1E6): # total< maximum number is required here.
        M02,fillMatrix02,valid02 = myBootstrap(M01, fillMatrix01)
        if valid02==True:
            return M02, fillMatrix02, True
        else:
            return M01, fillMatrix01, False

    else:
        M03, fillMatrix03, valid03 = myExhaustFill(M01, fillMatrix01)
        finish03 = myFinish(M03)
        if valid03==False:
            return M01, fillMatrix01, False
        elif (valid03==True)and(finish03==True):
            return M03, fillMatrix03, True
        else:
            M01[:][:] = M03[:][:]
            fillMatrix01[:][:] = fillMatrix03[:][:]
            valid01 = valid03        
            Mtup = tuple(M01)
            posVec, caseArray, caseTotal = makeCaseNDB(M01, fillMatrix01)
            for i in range(0,caseTotal):
                for n1 in range(0,9):
                    for n2 in range(0,9):
                        M01[n1,n2]=Mtup[n1][n2]
            
                for j in range(0,5):
                    Num1 = int(posVec[j]//9) #Python3
                    Num2 = int(posVec[j]%9)
                    M01[Num1,Num2] = caseArray[0,i][0,j]

                fillMatrix01 = fillBlank(M01)
                valid01 = checkConsistent(M01, fillMatrix01)
                total01 = countCombination(fillMatrix01)
                if (i==caseTotal-1):
                    return M01, fillMatrix01, valid01
                elif valid01==False:
                    continue
                else:
                    M04, fillMatrix04, valid04 = NDBsolveEngine(M01, fillMatrix01, valid01, total01)
                    if valid04==True:
                        return M04, fillMatrix04, True

# # # # # # # # # # # # # # # OTHER FUNCTION # # # # # # # # # # # # # # # 


