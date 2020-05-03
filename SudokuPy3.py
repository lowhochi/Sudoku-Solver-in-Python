from sympy import *
import math
import numpy as np
import sys
import os
import time
import SudokuPy3Fun
import SudokuPy3Bank
from SudokuPy3Bank import sudoku

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

        if myExit==True:
            print("-"*30, "END", "-"*30)
            break
        B2 = SudokuPy3Fun.copyPuzzle(B)
        endPuzzle(B2, Bvalid)
        print("-"*30, "END", "-"*30)
        del B, BfillMatrix, B2, Bvalid        
##        mySave= raw_input("Save(Y/N):")
##        if str(mySave)=='Y':
##            SudokuPy3Bank.answerIn(myNum, B2)
##        else:
##            print "-"*30, "END", "-"*30
##        del B, BfillMatrix, B2, Bvalid

        
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

# # # # # # # # # # RUN # # # # # # # # # #
if (__name__=="__main__"):
    main()
