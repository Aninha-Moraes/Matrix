from concurrent.futures import thread
from os import get_terminal_size, system
import random
import sys
import time
import threading
import functions.terminal as terminal
import constants

terminalSizes = None
matrixArea = None
entryArea = None
newTerminalSize = None

def matrixStringGenerator():
    while(True):
        indexesOfEmptyEntryStrings = []
        sortedIndexToBeFilled = None


        for i in range(len(entryArea)):
            if(entryArea[i]["full"] == False):
                indexesOfEmptyEntryStrings.append(i)

        if(len(indexesOfEmptyEntryStrings) > 0):

            sortedIndexToBeFilled = indexesOfEmptyEntryStrings[random.randint(0, len(indexesOfEmptyEntryStrings) - 1)]

            entryArea[sortedIndexToBeFilled]["full"] = True
            entryArea[sortedIndexToBeFilled]["currentNumberOfChars"] = random.randint(constants.MIN_MATRIX_STRING_SIZE, constants.MAX_MATRIX_STRING_SIZE)
            

        time.sleep(constants.MATRIX_STRING_GENERATOR_INTERVAL)


def matrixRenderer():
    theSwap = None
    j = None
    global terminalSizes
    global matrixArea
    global entryArea
    while(True):
        newTerminalSize = get_terminal_size()
        terminal.moveCursor(0,0)

        if(terminalSizes.columns != newTerminalSize.columns or terminalSizes.lines != newTerminalSize.lines):
            system("clear")
            terminalSizes = newTerminalSize
            matrixArea = terminal.generateMatrixArea(terminalSizes.columns, terminalSizes.lines)
            entryArea = terminal.generateEntryArea(terminalSizes.columns)

        for i in range(terminalSizes.columns):
            matrixArea[terminalSizes.lines - 1][i] = " "

        for i in range(terminalSizes.columns):
            j = terminalSizes.lines - 1

            while(j > 0):
                theSwap = matrixArea[j - 1][i]
                matrixArea[j - 1][i] = matrixArea[j][i]
                matrixArea[j][i] = theSwap
                
                j -= 1

        for i in range(terminalSizes.columns):
            if(entryArea[i]["full"] == True):
                if(entryArea[i]["currentNumberOfChars"] <= 0):
                    entryArea[i]["full"] = False
                else:
                    matrixArea[0][i] = constants.POSSIBLE_MATRIX_STRING_CHARACTERS[random.randint(0, len(constants.POSSIBLE_MATRIX_STRING_CHARACTERS) - 1)]
                    entryArea[i]["currentNumberOfChars"] -= 1

        for f in range(len(matrixArea) - 1):
            finalString = ""
            for character in matrixArea[f]:
                finalString += character
        
            print(f"\033[92;1m{finalString}\033[0m", end="")

        time.sleep(constants.MATRIX_RENDERER_RATE)

def showMatrixEntryArea():
    while(True):
        time.sleep(1)
        system("clear")
        print(entryArea)

system("clear")

terminalSizes = terminal.getTerminalSizes()
matrixArea = terminal.generateMatrixArea(terminalSizes.columns, terminalSizes.lines)
#entryArea = terminal.generateEntryArea(terminalSizes.columns)
entryArea = terminal.generateEntryArea(terminalSizes.columns)

thr = threading.Thread(target=matrixStringGenerator)
thr.start()

matrixRenderer()





