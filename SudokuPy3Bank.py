from sympy import *
import math
import numpy as np
import sys
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
# sample
Mtest = np.array([[9, 0, 4, 0, 0, 0, 0, 0, 5],
                  [0, 0, 0, 0, 4, 0, 2, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 2, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 7, 0, 0, 0, 2, 0],
                  [1, 0, 0, 0, 0, 2, 0, 0, 0],
                  [0, 5, 0, 0, 0, 0, 0, 8, 1],
                  [0, 0, 6, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 3, 0, 0, 0, 0]])
Mzero = np.zeros([9, 9])
# # # # # # # # # # # # # # # CLASS SUDOKU # # # # # # # # # # # # # # #
class sudoku:
    puzzle = Mzero
    number = 1000
    change = np.empty([9,9], dtype=object)
    def __init__(self, Number=None):
        self.puzzle = getSudoku(Number)
        if Number!=None:
            self.number = Number
        else:
            self.number = int(input('Set the sudoku id: (10xx) '))
        # self.change = np.empty([9, 9], dtype=object)
        for row in range(0,9):
            for col in range(0,9):
                self.change[row][col] = [int(self.puzzle[row][col])]
        file_create = "puzzleNo%s.txt"%(self.number)
        if os.path.exists(file_create)==False:
            f = open(file_create,"w+")
            f.write("PuzzleNo%s\n"%Number)
            f.write("save original\n")
            for row in range(0,9):
                for col in range(0,9):
                    f.write("%d"%self.puzzle[row][col])
                    if col!=8:
                        f.write(" ")
                    else:
                        f.write("\n")
            f.close()
        self.filename = file_create


    def setEntry(self, row, col, entry):
        self.puzzle[row][col] = entry
        self.change[row][col].append(entry)
    
    def show(self):
        for i in range(0,9):
            print("[",end='')
            for j in range(0,9):
                print(int(self.puzzle[i][j]),end='')
                if (j!=8):
                    print(" ",end='')
            print("]")

    def pop(self, row, col):
        if len(self.change[row][col])>1:
            self.change[row][col].pop()
            temp = self.change[row][col]
            self.puzzle[row][col] = temp[-1]

    def restore(self):
        for row in range(0,9):
            for col in range(0,9):
                temp = self.change[row][col]
                self.puzzle[row][col] = temp[0]
                self.change[row][col] = temp[0:1]
    
    def save(self, M=None):
        with open(self.filename, "a") as f:
            current_time = datetime.now()
            f.write("save "+str(current_time)+"\n")
            if M==None:
                print("save self.puzzle")
                for row in range(0,9):
                    for col in range(0,9):
                        f.write("%d"%self.puzzle[row][col])
                        if col!=8:
                            f.write(" ")
                        else:
                            f.write("\n")
            else:
                print("save input matrix")
                for row in range(0,9):
                    for col in range(0,9):
                        f.write("%d"%M[row][col])
                        if col!=8:
                            f.write(" ")
                        else:
                            f.write("\n")

    def read(self):
        record = []
        with open(self.filename, "r") as f:
            f01 = f.readlines()
            for row, line in enumerate(f01, 0):
                find_save = line[0:line.find(' ')]
                if find_save=="save":
                    record.append(row)
            for j in range(0, len(record)):
                print("[%d] "%j,end='')
                print(f01[record[j]], end='\n')
            choice = input("which record [x] are you reading? x = ")
            choice_number = int(choice)
            start_row = record[choice_number]+1
            M01 = np.zeros([9,9])
            for j in range(0,9):
                rowString = f01[start_row+j].split(' ')
                rowNumber = [int(string) for string in rowString]
                for k in range(0,9):
                    M01[j][k] = rowNumber[k]
        self.puzzle = M01
        for row in range(0,9):
            for col in range(0,9):
                self.change[row][col] = [int(self.puzzle[row][col])]

    def showImage(self):
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

        for row in range(0,9):
            for col in range(0,9):
                value = int(self.puzzle[row, col])
                if value!=0:
                    ax.text(col+0.25, 8.25-row, str(value), size=20, color='black')
        plt.show()
        
# # # # # # # # # # # # # # # OTHER FUNCTION # # # # # # # # # # # # # # #            
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











