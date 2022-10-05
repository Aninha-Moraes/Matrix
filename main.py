from functools import partial
from os import system
import argparse
import threading
import sys
import functions.terminal as terminal
import functions.costumization as costumization
import functions.controllers as controllers
import signal
import functions.programConfig as programConfig
from classes.sharedValues import sharedValues

threadSharedValues = sharedValues
newTerminalSize = None
foregroundColor = 92
backgroundColor = 1
operatingSystemClearCommand = "cls" if sys.platform == "win32" else "clear"
stopFlag = [True]
stringSizes = {
    "max" : 12,
    "min" : 8
}


system(operatingSystemClearCommand)

parser = argparse.ArgumentParser(description="Matrix program")
parser.add_argument("-f", "--foreground-color", help="Set matrix string color", type=str)
parser.add_argument("-b", "--background-color", help="Set matrix background color", type=str)
parser.add_argument("-M", "--min-string-size", help="Set min matrix string size", type=int)
parser.add_argument("-m" , "--max-string-size", help="Set max matrix string size", type=int)

programArguments = parser.parse_args()

if(programArguments.foreground_color):
    resultOfColorChecking = costumization.checkIfForegroundColorIsAvailable(programArguments.foreground_color)

    if(resultOfColorChecking != -1):
        foregroundColor = resultOfColorChecking
    else:
        print("Not available foreground color")
        exit(1)

if(programArguments.background_color):
    resultOfColorChecking = costumization.checkIfBackgroundgroundColorIsAvailable(programArguments.background_color)

    if(resultOfColorChecking != -1):
        backgroundColor = resultOfColorChecking
    else:
        print("Not available background color")
        exit(1)

if(programArguments.max_string_size):
    stringSizes["max"] = programArguments.max_string_size

if(programArguments.min_string_size):
    stringSizes["min"] = programArguments.min_string_size

if(stringSizes["max"] < stringSizes["min"]):
    print("Max matrix string size lower than min matrix string size")
    exit(1)

if(stringSizes["max"] <= 0 or stringSizes["min"] <= 0):
    print("Matrix string sizes can't lower or equal than 0")
    exit(1)


signal.signal(signal.SIGINT, partial(programConfig.signalHandling, stopFlag))

threadSharedValues.terminalSizes = terminal.getTerminalSizes()
threadSharedValues.matrixArea = terminal.generateMatrixArea(threadSharedValues.terminalSizes.columns, threadSharedValues.terminalSizes.lines)
threadSharedValues.entryArea = terminal.generateEntryArea(threadSharedValues.terminalSizes.columns)

terminal.hideCursor()

matrixGeneratorThread = threading.Thread(target=controllers.matrixStringGenerator,args=(threadSharedValues,stopFlag, stringSizes))
matrixGeneratorThread.start()

controllers.matrixRenderer(foregroundColor, backgroundColor, threadSharedValues, stopFlag, operatingSystemClearCommand)

terminal.moveCursor(threadSharedValues.terminalSizes.lines, threadSharedValues.terminalSizes.columns)

system(operatingSystemClearCommand)

terminal.showCursor()
