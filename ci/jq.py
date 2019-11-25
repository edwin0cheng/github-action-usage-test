import sys
import json

# simple json tool

json_str = sys.argv[1]
key = sys.argv[2]
o = json.loads(json_str)
if key in o:
    print(o[key],end='')
else:
    print('', end='')