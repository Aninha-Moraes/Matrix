import os
import constants

def hideCursor():
    print(constants.HIDE_CURSOR_CODE, end="");

def showCursor():
    print(constants.SHOW_CURSOR_CODE, end="")

def getTerminalSizes():
    return os.get_terminal_size()

def generateMatrixArea(width, height):
    stringToGenerate = " " * width
    newMatrixLine = []
    matrixArea = []

    for i in range(height):
        for j in range(width):
            newMatrixLine.append(" ")
        matrixArea.append(newMatrixLine.copy())
        newMatrixLine.clear()

    return matrixArea

def generateEntryArea(width):
    entryArea = []

    for i in range(width):
        entryArea.append({
            "full": False,
            "currentNumberOfChars" : 0
        })

    return entryArea

def moveCursor (y, x):
    print("\033[%d;%dH" % (y, x))