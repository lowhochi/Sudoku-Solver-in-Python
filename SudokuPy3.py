from sympy import *
import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
import SudokuPy3Fun
import SudokuPy3Bank
from SudokuPy3Bank import sudoku
import SudokuPy3PulpSolver

def main():
    # # # # # # # # # # get Sudoku # # # # # # # # # #
    myNum = input("Type the puzzle number: ")
    sdk01 = sudoku(myNum)
    A= sdk01.puzzle
    number_of_blank = SudokuPy3Fun.countBlank(A)
    AfillMatrix = SudokuPy3Fun.fillBlank(A)
    total = SudokuPy3Fun.countCombination(AfillMatrix)
    Avalid = SudokuPy3Fun.checkConsistent(A, AfillMatrix)
    # # # # # # # # # # Printing # # # # # # # # # #
    startPuzzle(A, Avalid, number_of_blank, total)
    myExit = False
    while myExit==False:
        # # # # # # # # # # Perform # # # # # # # # # #
        print("Option 1: myBootstrap")
        print("Option 2: myExhaustFill")
        print("Option 3: mySolveEngine")
        print("Option 4: NDBsolveEngine")
        print("Option 5: PulpSolver")
        print("Option 0: QUIT\n")
        choice = input("Choose Option: ")
        if int(choice)==0:
            myExit=True
        if int(choice)==1:
            B,BfillMatrix,Bvalid=SudokuPy3Fun.myBootstrap(A, AfillMatrix)
        if int(choice)==2:
            B,BfillMatrix,Bvalid=SudokuPy3Fun.myExhaustFill(A, AfillMatrix)
        if int(choice)==3:
            B,BfillMatrix,Bvalid=SudokuPy3Fun.mySolveEngine(A, AfillMatrix, Avalid, total)
        if int(choice)==4:
            B,BfillMatrix,Bvalid=SudokuPy3Fun.NDBsolveEngine(A, AfillMatrix, Avalid, total)
        if int(choice)==5:
            B = SudokuPy3PulpSolver.pulpSolver(A)
            BfillMatrix = SudokuPy3Fun.fillBlank(B)
            Bvalid = SudokuPy3Fun.checkConsistent(B, BfillMatrix)

        if myExit==True:
            print("-"*30, "END", "-"*30)
            break
        
        showPuzzleAnswer(A, B)
        B2 = SudokuPy3Fun.copyPuzzle(B)
        endPuzzle(B2, Bvalid)
        save_sudoku = input("Save Answer(Y/N)?")
        if str(save_sudoku)=="Y":
            SudokuPy3Bank.answerIn(int(myNum),B2)#myNum is a string
            print("-"*30, "SAVED", "-"*30)
        else:
            print("-"*30, "END", "-"*30)
        del B, BfillMatrix, B2, Bvalid      

        
def startPuzzle(A, valid, number_of_blank, total):    
    print("-"*30, "START", "-"*30)
    print("The puzzle is:")
    print(A)
    print("\nNumber of blank:", str(number_of_blank))
    print("Total number of combination:", str(total))
    print("The original consistency is T/F:", str(valid))
    print("\n")

def endPuzzle(B, valid):
    print("\n\n The solution is")
    print(B)
    print("\nThe answer is T/F:", end='')
    print(valid)

def showPuzzleAnswer(A, B):
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
    # # # # #
    for row in range(0,9):
        for col in range(0,9):
            originalValue = int(A[row, col])
            value = int(B[row, col])
            if originalValue!=0:
                ax.text(col+0.25, 8.25-row, str(originalValue), \
                        size=20, color='black')
            else:
                ax.text(col+0.25, 8.25-row, str(value), \
                        size=20, color='red')
    plt.show()


# # # # # # # # # # RUN # # # # # # # # # #
if (__name__=="__main__"):
    main()

# # # # # # # # # # # # # # # # # # # # # #


    
