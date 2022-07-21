import subprocess, json, sys
import glob
import os
import time
from utils import *
from download import Download

def rename(dirs, dest):
    dates = []
    for dir in dirs:
        dates.append(time.strptime(dir.split("/")[-1], "%Y_%m_%d"))
        for file in glob.glob(dest + time.strftime("%Y_%m_%d", min(dates)) + "/*"):
            cmd("mv " + file + " " + dest + time.strftime("%Y_%m_%d", time.localtime()))
    cmd("rmdir " + dest + time.strftime("%Y_%m_%d", min(dates)))

def sync(download: Download):
    dirs = []
    cmd("mkdir " + download.destination_path + time.strftime("%Y_%m_%d", time.localtime()), False, False)
    for x in os.walk(download.destination_path):
        if x[0] != download.destination_path:
            dirs.append(x[0])
    if len(dirs) > download.days:
        rename(dirs, download.destination_path)
    bashCommand = ["rsync", download.source_path, download.destination_path + time.strftime("%Y_%m_%d", time.localtime()) + "/"]
    i = 1
    for arg in download.flags:
        bashCommand.insert(i, arg)
        i += 1
    output, error = cmd(bashCommand)
    if error != b'':
        bashCommand = ["./signal/bin/signal-cli", "-a", "<SENDER>", "send", "-m", "Error: " + error.decode("utf-8"), "<RECEIVER>"]
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main(args):
    if (len(args) != 2 or args[0] != "-p"):
        print("Usage:\n python main.py -p <path_to_config_file>");
        return
    with open(args[1], 'r') as f:
        file = json.load(f)
    init_logging_path(file["logging_path"])
    for download in file["downloads"]:
        sync(Download(download))

if __name__ == "__main__":
    main(sys.argv[1:])
