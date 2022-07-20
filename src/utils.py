import subprocess
from inspect import currentframe, getframeinfo


def cmd(bashCommand):
    process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.stdout, process.stderr
    print("------------Begin-Command------------\n" + bashCommand)
    print("Output: " + output.decode("utf-8") + "\nError: " + error.decode("utf-8"))
    print("-------------End-Command-------------")
    return (output, error)

def debug(dbgMsg):
    frameinfo = getframeinfo(currentframe().f_back)
    print(frameinfo.filename + "(" + str(frameinfo.lineno) + ")" + ": " + dbgMsg)
