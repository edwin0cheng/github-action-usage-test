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
    ref_len = len("raa+ a1d631da")
    if len(arg) < ref_len:
        print("Invalid format")
        return False
    arg = arg[len("raa+ "):ref_len]
    try:
        int(arg, 16)
    except ValueError:
        print("Not valid sha format")
        return False
    
    open('target_sha.txt', "w").write(arg)
    return True

def do_valid(arg):
    result = subprocess.run(['git', 'cat-file', '-t', arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.decode('utf-8').strip() == "commit":
        return True
    else:
        print("No this commit")
        return False

def do_exists(arg):
    j = json.load(open("./data/commits.json", "r"))
    if arg in j["commits"]:
        print("Target sha already exists in commits.json")
        return False
    else:
        print("Target not exists in commits.json")
        return True

if len(sys.argv) < 3:
    print("Not valid command line args")
    exit(-1)

def fail_return(msg):
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w') as file:
            file.write(msg)
    else:
        exit(-1)

mode = sys.argv[1]

# Check if error.txt exists and not empty
if len(sys.argv) > 3:
    try:
        with open(sys.argv[3], 'r') as file:
            if file.read() != "":
                exit(-1)
    except:
        pass

if mode == "check":
    if not do_check(sys.argv[2]):
        fail_return("Your request is not valid.")
elif mode == "exists":
    if not do_exists(sys.argv[2]):
        fail_return("Your request is already in the page.")
elif mode == "valid":
    if not do_valid(sys.argv[2]):
        fail_return("Your request is not a RA Commit.")
else:
    print("No this command")
    exit(-1)
