import subprocess
from inspect import currentframe, getframeinfo
import logging
import time

logging.basicConfig(filename='rsync.log', level=logging.DEBUG)

def cmd(bashCommand):
    if type(bashCommand) == list:
        process = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.stdout, process.stderr
    print("------------Begin-Command------------\n" + str(bashCommand))
    print("Output: " + output.decode("utf-8") + "\nError: " + error.decode("utf-8"))
    print("-------------End-Command-------------")
    logging.info("------------Begin-Command------------")
    logging.info("Timestamp: " + time.strftime("%H:%M:%S %z", time.localtime()))
    logging.info("Command: " + str(bashCommand))
    if error == b'':
        logging.info(output.decode("utf-8"))
    else:
        logging.error(error.decode("utf-8"))
    logging.info("-------------End-Command-------------")
    return (output, error)

def debug(dbgMsg):
    frameinfo = getframeinfo(currentframe().f_back)
    print(frameinfo.filename + "(" + str(frameinfo.lineno) + ")" + ": " + dbgMsg)
