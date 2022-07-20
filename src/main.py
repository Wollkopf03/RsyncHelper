import subprocess, json, sys

def sync(download):
    bashCommand = "rsync -azP --exclude=" + download["filters"]["exclude_pattern"] +  " --include=" + download["filters"]["include_pattern"] + " " + download["source_path"] + " " + download["destination_path"]
    process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout
    error = process.stderr
    if error == b'':
        print(output.decode("utf-8") + "\n---------------------------------------------------------\n")
    else:
        print("Error:\n" + error.decode("utf-8") + "\n---------------------------------------------------------\n")
        bashCommand = ["./signal/bin/signal-cli", "-a", "<SENDER>", "send", "-m", "Error: " + error.decode("utf-8"), "<RECEIVER>"]
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main(args):
    if (len(args) != 2 or args[0] != "-p"):
        print("Usage:\n python main.py -p <path_to_config_file>");
        return
    with open(args[1], 'r') as f:
        downloads = json.load(f)["downloads"]
    for download in downloads:
        sync(download)

if __name__ == "__main__":
    main(sys.argv[1:])
