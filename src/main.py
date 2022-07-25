import json, sys, glob, os, time as tm
from utils import *
from download import Download

def rename(dirs, dest):
    dates = []
    for dir in dirs:
        dates.append(tm.strptime(dir.split("/")[-1], "%Y_%m_%d"))
        for file in glob.glob(dest + time(min(dates)) + "/*"):
            cmd("mv " + file + " " + dest + time())
    cmd("rmdir " + dest + time(min(dates)))

def sync(download: Download):
    dirs = []
    cmd("mkdir " + download.destination_path + time(), False, False)
    for x in os.walk(download.destination_path):
        if x[0] != download.destination_path:
            dirs.append(x[0])
    if len(dirs) > download.days:
        rename(dirs, download.destination_path)
    rsyncCommand = ["rsync", download.source_path, download.destination_path + time() + "/"]
    i = 1
    for arg in download.flags:
        rsyncCommand.insert(i, arg)
        i += 1
    output, error = cmd(rsyncCommand)
    if error != b'':
        cmd(["./signal/bin/signal-cli", "-a", "<SENDER>", "send", "-m", "Error: " + error.decode("utf-8"), "<RECEIVER>"])

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
