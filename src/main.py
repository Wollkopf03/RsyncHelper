import json, sys, glob, os, time as tm
from utils import *
from download import Download
from datetime import datetime, timedelta

def rename(dirs, dest):
    dates = []
    for dir in dirs:
        dates.append(tm.strptime(dir.split("/")[-1], "%Y_%m_%d"))
        for file in glob.glob(dest + time(min(dates)) + "/*"):
            cmd("mv " + file + " " + dest + time())
    cmd("rmdir " + dest + time(min(dates)))

def sync(download: Download, signal_home: str, sender: str, recipients: list):
    dirs = []
    cmd("mkdir " + download.destination_path, False, False)
    cmd("mkdir " + download.destination_path + time(), False, False)
    for x in os.walk(download.destination_path):
        if x[0] != download.destination_path:
            dirs.append(x[0])
    if len(dirs) > download.days:
        rename(dirs, download.destination_path)
    elif len(dirs) > 1:
        cmd(["cp", download.destination_path + datetime.strftime(datetime.now() - timedelta(1), "%Y_%m_%d") + "/" + download.destination_path.split("/")[-2], download.destination_path + time() + "/" + download.destination_path.split("/")[-2]])
    rsyncCommand = ["rsync", download.source_path, download.destination_path + time() + "/"]
    i = 1
    for arg in download.flags:
        rsyncCommand.insert(i, arg)
        i += 1
    output, error = cmd(rsyncCommand)
    if not os.path.exists(download.destination_path + time() + "/" + download.destination_path.split("/")[-2]):
        for recipient in recipients:
            cmd([signal_home, "-a", sender, "send", "-m", "Error: Missing file:" + download.destination_path + time() + "/" + download.destination_path.split("/")[-2], recipient])
    if error != b'':
        for recipient in recipients:
            cmd([signal_home, "-a", sender, "send", "-m", "Error: " + error.decode("utf-8"), recipient])

def main(args):
    if (len(args) != 2 or args[0] != "-p"):
        print("Usage:\n python main.py -p <path_to_config_file>");
        return
    with open(args[1], 'r') as f:
        file = json.load(f)
    init_logging_path(file["logging_path"] + "rsync_" + time() + ".log")
    for download in file["downloads"]:
        sync(Download(download), file["signal_home"], file["sender"], file["recipients"])
    dates = []
    for dir in os.listdir(file["logging_path"]):
        if dir.endswith(".log") and dir.startswith("rsync_"):
            dates.append(tm.strptime(dir.replace("rsync_", "").replace(".log", ""), "%Y_%m_%d"))
    if len(dates) > 3:
        cmd("rm " + file["logging_path"] + "rsync_" + time(min(dates)) + ".log")
    with open(file["logging_path"] + "rsync_" + time() + ".log", "a") as f:
        f.write("Done!\n")

if __name__ == "__main__":
    main(sys.argv[1:])
