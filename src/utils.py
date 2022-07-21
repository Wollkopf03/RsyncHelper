import subprocess
from inspect import currentframe, getframeinfo
import logging as log
import time

def init_logging_path(logging_path):
    log.basicConfig(filename=logging_path, level=log.DEBUG)

def cmd(bashCommand, output = True, logging = True):
    if type(bashCommand) == list:
        process = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.stdout, process.stderr
    if output:
        print("------------Begin-Command------------\n" + str(bashCommand))
        print("Output: " + output.decode("utf-8") + "\nError: " + error.decode("utf-8"))
        print("-------------End-Command-------------")
    if logging:
        log.info("------------Begin-Command------------")
        log.info("Timestamp: " + time.strftime("%H:%M:%S %z", time.localtime()))
        log.info("Command: " + str(bashCommand))
        if error == b'':
            log.info(output.decode("utf-8"))
        else:
            log.error(error.decode("utf-8"))
        log.info("-------------End-Command-------------")
    return (output, error)

def debug(dbgMsg):
    frameinfo = getframeinfo(currentframe().f_back)
    print(frameinfo.filename + "(" + str(frameinfo.lineno) + ")" + ": " + dbgMsg)
