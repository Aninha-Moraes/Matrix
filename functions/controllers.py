import time
import random
import constants
from os import get_terminal_size, system
import functions.terminal as terminal

def matrixStringGenerator(entryArea, stopFlag, availableStringSizes):
    while(stopFlag[0]):
        indexesOfEmptyEntryStrings = []
        sortedIndexToBeFilled = None


        for i in range(len(entryArea)):
            if(entryArea[i]["full"] == False):
                indexesOfEmptyEntryStrings.append(i)

        if(len(indexesOfEmptyEntryStrings) > 0):

            sortedIndexToBeFilled = indexesOfEmptyEntryStrings[random.randint(0, len(indexesOfEmptyEntryStrings) - 1)]

            entryArea[sortedIndexToBeFilled]["full"] = True
            entryArea[sortedIndexToBeFilled]["currentNumberOfChars"] = random.randint(availableStringSizes.min, availableStringSizes.max)
            

        time.sleep(constants.MATRIX_STRING_GENERATOR_INTERVAL)


def matrixRenderer(theForegroundColor, theBackgroundColor, terminalSizes, matrixArea, entryArea, stopFlag):
    theSwap = None
    j = None
    while(stopFlag[0]):
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
        
            #print(f"\033[92;1m{finalString}\033[0m", end="")
            print(f"\033[{theForegroundColor};{theBackgroundColor}m{finalString}\033[0m", end="")

        time.sleep(constants.MATRIX_RENDERER_RATE)
