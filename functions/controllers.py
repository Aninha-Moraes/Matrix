import time
import random
import constants
from os import get_terminal_size, system
import functions.terminal as terminal

def matrixStringGenerator(threadSharedValues, stopFlag, availableStringSizes):
    while(stopFlag[0]):
        indexesOfEmptyEntryStrings = []
        sortedIndexToBeFilled = None


        for i in range(len(threadSharedValues.entryArea)):
            if(threadSharedValues.entryArea[i]["full"] == False):
                indexesOfEmptyEntryStrings.append(i)

        if(len(indexesOfEmptyEntryStrings) > 0):

            sortedIndexToBeFilled = indexesOfEmptyEntryStrings[random.randint(0, len(indexesOfEmptyEntryStrings) - 1)]

            threadSharedValues.entryArea[sortedIndexToBeFilled]["full"] = True
            threadSharedValues.entryArea[sortedIndexToBeFilled]["currentNumberOfChars"] = random.randint(availableStringSizes["min"], availableStringSizes["max"])
            

        time.sleep(constants.MATRIX_STRING_GENERATOR_INTERVAL)


def matrixRenderer(theForegroundColor, theBackgroundColor, threadSharedValues, stopFlag, operatingSystemClearCommand):
    theSwap = None
    j = None
    while(stopFlag[0]):
        newTerminalSize = get_terminal_size()
        terminal.moveCursor(0,0)

        if(threadSharedValues.terminalSizes.columns != newTerminalSize.columns or threadSharedValues.terminalSizes.lines != newTerminalSize.lines):
            system(operatingSystemClearCommand)
            threadSharedValues.terminalSizes = newTerminalSize
            threadSharedValues.matrixArea = terminal.generateMatrixArea(threadSharedValues.terminalSizes.columns, threadSharedValues.terminalSizes.lines)
            threadSharedValues.entryArea = terminal.generateEntryArea(threadSharedValues.terminalSizes.columns)

        for i in range(threadSharedValues.terminalSizes.columns):
            threadSharedValues.matrixArea[threadSharedValues.terminalSizes.lines - 1][i] = " "

        for i in range(threadSharedValues.terminalSizes.columns):
            j = threadSharedValues.terminalSizes.lines - 1

            while(j > 0):
                theSwap = threadSharedValues.matrixArea[j - 1][i]
                threadSharedValues.matrixArea[j - 1][i] = threadSharedValues.matrixArea[j][i]
                threadSharedValues.matrixArea[j][i] = theSwap
                
                j -= 1

        for i in range(threadSharedValues.terminalSizes.columns):
            if(threadSharedValues.entryArea[i]["full"] == True):
                if(threadSharedValues.entryArea[i]["currentNumberOfChars"] <= 0):
                    threadSharedValues.entryArea[i]["full"] = False
                else:
                    threadSharedValues.matrixArea[0][i] = constants.POSSIBLE_MATRIX_STRING_CHARACTERS[random.randint(0, len(constants.POSSIBLE_MATRIX_STRING_CHARACTERS) - 1)]
                    threadSharedValues.entryArea[i]["currentNumberOfChars"] -= 1

        for f in range(len(threadSharedValues.matrixArea) - 1):
            finalString = ""
            for character in threadSharedValues.matrixArea[f]:
                finalString += character
        
            print(f"\033[{theForegroundColor};{theBackgroundColor}m{finalString}\033[0m", end="")

        time.sleep(constants.MATRIX_RENDERER_RATE)
