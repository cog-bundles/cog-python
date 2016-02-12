import json
import sys

def send_json(data):
    print "JSON\n"
    print "%s\n" % (json.dumps(data))
    sys.stdout.flush()

def send_error(text):
    send_json({"error": text})

def finish(error=False):
    if error:
        sys.exit(1)
    else:
        sys.exit(0)
