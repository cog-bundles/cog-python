from __future__ import print_function
import json
import sys

def send_json(data, template=None):
    if template is not None:
        print("COG_TEMPLATE: %s" % (template), end="\n", file=sys.stdout)
    print("JSON", end="\n", file=sys.stdout)
    print(json.dumps(data), end="\n", file=sys.stdout)
    sys.stdout.flush()

def send_error(text):
    print(text, end="\n", file=sys.stderr)
    sys.stderr.flush()

def finish(error=False):
    if error:
        sys.exit(1)
    else:
        sys.exit(0)
