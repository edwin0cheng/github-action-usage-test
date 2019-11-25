import sys
import os
import json

# simple json tool
key = sys.argv[1]
o = json.loads(os.environ["JSON"])
if key in o:
    print(o[key],end='')
else:
    print('', end='')