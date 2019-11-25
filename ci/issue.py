import os
import sys
import subprocess
import json

def do_check(arg):
    # check whether arg contains raa+
    pos = arg.find("raa+")
    if pos == -1:
        print("Normal comment, skip")
        return False
    arg = arg[pos:]

    args = arg.split()
    if len(args) < 2:
        print("Invalid format")
        return False        
    arg = args[1]
    try:
        int(arg, 16)
    except ValueError:
        print("Not valid sha format")
        return False
    
    open('target_sha.txt', "w").write(arg)
    return True

def do_valid(arg_file):
    arg = ""
    with open(arg_file, 'r') as file:
        arg = file.read().strip()
    result = subprocess.run(['git', 'cat-file', '-t', arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.decode('utf-8').strip() != "commit":
        print("No this commit")
        return False
    # normalize the sha to len => 8
    result = subprocess.run(['git', 'rev-parse', arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = result.stdout.decode('utf-8').strip()
    try:
        int(result, 16)
    except ValueError:
        print("Not valid sha format")
        return False
    print(result[0:8])
    arg = result[0:8]
    open(arg_file, "w").write(arg)
    return True

def do_exists(arg_file):
    arg = ""
    with open(arg_file, 'r') as file:
        arg = file.read().strip()

    j = json.load(open("./data/commits.json", "r"))
    if arg in j["commits"]:
        print("Target sha already exists in commits.json")
        return False
    else:
        print("Target not exists in commits.json")
        return True

def fail_return(msg):
    with open(sys.argv[3], 'w') as file:
        file.write(msg)

if len(sys.argv) != 4:
    print("Not valid command line args")
    exit(0)

# Check if error.txt exists and not empty
with open(sys.argv[3], 'r') as file:
    if file.read() != "":
        exit(0)

mode = sys.argv[1]
if mode == "check":
    if not do_check(sys.argv[2]):
        fail_return("NO_MSG")
elif mode == "exists":
    if not do_exists(sys.argv[2]):
        sha = ""
        with open(sys.argv[2], 'r') as file:
            sha = file.read().strip()
        url = os.environ["HOMEPAGE"] + "#" + sha
        reply = "Your request is already in the page. ({})".format(url)
        fail_return(reply)
elif mode == "valid":
    if not do_valid(sys.argv[2]):
        fail_return("Your request is not a RA Commit.")
else:
    print("No this command")
    exit(0)
