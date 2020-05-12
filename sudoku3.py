from sympy import *
import math
import numpy as np
import sys
import os
import time
import sudoku3Fun
import sudokuBank
from sudokuBank import sudoku

def main():
    # # # # # # # # # # get Sudoku # # # # # # # # # #
    myNum = raw_input("Type the puzzle number: ")
    sdk01 = sudoku(myNum)
    A= sdk01.puzzle
    number_of_blank = sudoku3Fun.countBlank(A)
    AfillMatrix = sudoku3Fun.fillBlank(A)
    total = sudoku3Fun.countCombination(AfillMatrix)
    Avalid = sudoku3Fun.checkConsistent(A, AfillMatrix)
    # # # # # # # # # # Printing # # # # # # # # # #
    startPuzzle(A, Avalid, number_of_blank, total)
    myExit = False
    while myExit==False:
        # # # # # # # # # # Perform # # # # # # # # # #
        print "Option 1: myBootstrap"
        print "Option 2: myExhaustFill"
        print "Option 3: mySolveEngine"
        print "Option 4: NDBsolveEngine"
        print "Option 0: QUIT\n"
        choice = raw_input("Choose Option: ")
        if int(choice)==0:
            myExit=True
        if int(choice)==1:
            B,BfillMatrix,Bvalid=sudoku3Fun.myBootstrap(A, AfillMatrix)
        if int(choice)==2:
            B,BfillMatrix,Bvalid=sudoku3Fun.myExhaustFill(A, AfillMatrix)
        if int(choice)==3:
            B,BfillMatrix,Bvalid=sudoku3Fun.mySolveEngine(A, AfillMatrix, Avalid, total)
        if int(choice)==4:
            B,BfillMatrix,Bvalid=sudoku3Fun.NDBsolveEngine(A, AfillMatrix, Avalid, total)

        if myExit==True:
            print "-"*30, "END", "-"*30
            break
        B2 = sudoku3Fun.copyPuzzle(B)
        endPuzzle(B2, Bvalid)
        save_sudoku = raw_input("Save Answer(Y/N)?")
        if str(save_sudoku)=="Y":
            sudokuBank.answerIn(int(myNum), B2) #myNum is a string
            print "-"*30, "SAVED", "-"*30
        else:
            print "-"*30, "END", "-"*30
        del B, BfillMatrix, B2, Bvalid        
        
def startPuzzle(A, valid, number_of_blank, total):    
    print "-"*30, "START", "-"*30
    print "The puzzle is:"
    print A
    print "\nNumber of blank:", str(number_of_blank)
    print "Total number of combination:", str(total)
    print "The original consistency is T/F:", str(valid)
    print "\n"

def endPuzzle(B, valid):
    print "\n\n The solution is"
    print B
    print "\nThe answer is T/F:",
    print valid

# # # # # # # # # # # # # # # # # # # #  RUN # # # # # # # # # # # # # # # # # # # #
if (__name__=="__main__"):
    main()



