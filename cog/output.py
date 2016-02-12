from __future__ import print_function
import json
import sys

def log(message, error=False):
    fd = sys.stdout
    if error:
        fd = sys.stderr
    print("LOG: %s" % (message), end="\n", file=fd)
    fd.flush()

def send_json(data, fd=sys.stdout):
    print("JSON", end="\n", file=fd)
    print(json.dumps(data), end="\n", file=fd)
    fd.flush()

def send_error(text):
    print(text, end="\n", file=sys.stderr)
    sys.stderr.flush()

def finish(error=False):
    if error:
        sys.exit(1)
    else:
        sys.exit(0)
