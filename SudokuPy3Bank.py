from sympy import *
import math
import numpy as np
import sys
import os
from datetime import datetime

class sudoku:
    def __init__(self, Number):
        self.puzzle = getSudoku(Number)
        self.number = Number
        self.change = []

    def setEntry(self, row, column, entry):
        self.puzzle[row][column] = entry
        self.change.append(9*row+column)

    def restore(self):
        temp = self.change[-1]
        row = int(temp/9)
        column = int(temp%9)
        self.puzzle[row][column] = 0
    
    def show(self):
        for i in range(0,9):
            print("[",end='')
            for j in range(0,9):
                print(int(self.puzzle[i][j]),end='')
                if (j!=8):
                    print(" ",end=''),
            print("]")

    def record(self,M):
        myString = 'pz'+str(self.number)+'.txt'
        if os.path.exists(myString):
            f = open(myString,"a")
            currentTime = datetime.now()
            f.write("\nRecord:"+ str(currentTime)+"\n")
            for i in range(0,9):
                for j in range(0,9):
                    temp = int(M[i][j])
                    if (j!=8):
                        f.write(str(temp)+" ")
                    else:
                        f.write(str(temp)+"\n")
            f.close()
        else:
            f = open(myString,"w+")
            currentTime = datetime.now()
            f.write("Record: "+ str(currentTime)+"\n")
            for i in range(0,9):
                for j in range(0,9):
                    if (j!=8):
                        f.write(str(temp)+" ")
                    else:
                        f.write(str(temp)+"\n")
            f.close()
            
def createBank():
    f = open("mySudokuBank.txt","w+")
    f.write("This is my sudoku bank.")
    f.close()
    g = open("sudokuAnswer.txt","w+")
    g.write("This is the answer bank.")
    g.close()

def sudokuIn():
    puzzleNo = int(input('Set the puzzle number:'))
    puzzleRow1 = input('1st Row:').split(',')
    puzzleRow2 = input('2nd Row:').split(',')
    puzzleRow3 = input('3rd Row:').split(',')
    puzzleRow4 = input('4th Row:').split(',')
    puzzleRow5 = input('5th Row:').split(',')
    puzzleRow6 = input('6th Row:').split(',')
    puzzleRow7 = input('7th Row:').split(',')
    puzzleRow8 = input('8th Row:').split(',')
    puzzleRow9 = input('9th Row:').split(',')

    with open("mySudokuBank.txt","a") as f:
        f.write("\nPuzzleNo%d\n" %puzzleNo)
        for rowNum in range(0,9):
            tempRow = eval('puzzleRow'+str(rowNum+1))
            puzzle = [int(num) for num in tempRow]
            for i in range(0,9):
                f.write(str(puzzle[i])+" ")
            f.write("\n")
##    f = open("mySudokuBank.txt","a")
##    f.write("\nPuzzleNo%d\n" %puzzleNo)
##    for rowNum in range(0,9):
##        tempRow = eval('puzzleRow'+str(rowNum+1))
##        puzzle = [int(num) for num in tempRow]
##        for i in range(0,9):
##            f.write(str(puzzle[i])+" ")
##        f.write("\n")
##    f.close()
    
# M = getSudoku(1001)
def getSudoku(puzzleNumber):
    M = np.zeros([9,9],dtype=int)
    f0 = open("mySudokuBank.txt","r")
    fread = f0.readlines()
    searchKey = 'PuzzleNo'+str(puzzleNumber)
    for lineNum, line in enumerate(fread,1):
        line = line.rstrip()
        if line==searchKey:
            for i in range(0,9):
                temp = (fread[lineNum+i].split(' '))[0:9]
                tempRow = [int(num) for num in temp]
                for j in range(0,9):
                    M[i][j] = int(tempRow[j])
    f0.close()
    return M
 
def answerIn(puzzleNumber, M):
    g = open("sudokuAnswer.txt","a")
    g.write("\nPuzzleNo%d\n" %puzzleNumber)
    for i in range(0,9):
        for j in range(0,9):
            if (j!=8):
                g.write(str(M[i][j])+" ")
            else:
                g.write(str(M[i][8])+"\n")
    g.close()

def getAnswer(puzzleNumber):
    Ans = np.zeros([9,9])
    g0 = open("sudokuAnswer.txt","r")
    gread = g0.readlines()
    searchKey = 'PuzzleNo'+str(puzzleNumber)
    for lineNum, line in enumerate(gread,1):
        line = line.rstrip()
        if line==searchKey:
            for i in range(0,9):
                temp = (gread[lineNum+i].split(' '))[0:9]
                tempRow = [int(num) for num in temp]
                for j in range(0,9):
                    Ans[i][j] = int(tempRow[j])
    g0.close()
    #print(searchKey,end='')
    #print(" -Answer-")
    #print(Ans)
    return Ans
