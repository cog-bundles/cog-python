from __future__ import print_function
import json
import os
import re
import string
import sys

from cog.logger import Logger

class Request(object):
    def __init__(self):
        self.load_args_()
        self.load_options_()
        self.load_requestor_()

    def name_to_option_var_(self, name):
        return "COG_OPT_%s" % (string.upper(name))

    def index_to_arg_var_(self, index):
        return "COG_ARGV_" + str(index)

    def load_requestor_(self):
        self.requestor_ = os.getenv("COG_CHAT_HANDLE")

    def load_args_(self):
        self.args_ = []
        cog_argc = int(os.getenv("COG_ARGC", 0))
        for i in range(cog_argc):
            self.args_.append(os.getenv(self.index_to_arg_var_(i)))

    def load_options_(self):
        self.option_names_ = []
        self.options_ = {}
        names = os.getenv("COG_OPTS")
        if names is None:
            return
        names = re.sub(r'(^"|"$)', r'', names)
        self.option_names_ = names.split(",")
        for name in self.option_names_:
            self.options_[name] = os.getenv(self.name_to_option_var_(name))

    def pipeline(self):
        return os.getenv("COG_PIPELINE_ID")

    def requestor(self):
        return self.requestor_

    def option_names(self):
        return list(self.option_names_)

    def option(self, name, default=None):
        if self.options_.has_key(name):
            return self.options_[name]
        else:
            return default

    def options(self):
        return dict(self.options_)

    def arg_count(self):
        return len(self.args_)

    def arg(self, index):
        if index >= len(self.args_):
            return None
        return self.args_[index]

    def args(self):
        return list(self.args_)

    def config(self, name, default = None):
        config_value = os.getenv(string.upper(name))
        if config_value is None:
            return default
        else:
            return config_value

class Response(object):
    def __init__(self):
        self.output_ = []
        self.error_ = None
        self.committed_ = False

    def append_body(self, data, template=None):
        if self.committed_ == True:
            raise IOError("Response has been committed.")
        self.output_.append({"template": template,
                             "json": data})

    def send_error(self, message):
        self.error_ = message
        self.commit()

    def reset(self):
        if self.committed_ == True:
            raise IOError("Response has been committed.")
        self.output_ = []
        self.error_ = None

    def commit(self, error=False):
        if self.committed_ == True:
            raise IOError("Response has been committed.")
        if self.error_ is not None:
            error = True
            print(self.error_, end="\n", file=sys.stderr)
            sys.stderr.flush()
        else:
            for entry in self.output_:
                template = entry["template"]
                content = entry["json"]
                if template is not None:
                    print("COG_TEMPLATE: %s" % (template), end="\n", file=sys.stdout)
                print("JSON", end="\n", file=sys.stdout)
                print(json.dumps(content), end="\n", file=sys.stdout)
        sys.stdout.flush()
        self.committed_ = True
        sys.exit(int(error))

class Command(object):
    def __init__(self):
        self.req = Request()
        self.resp = Response()
        self.handlers = {}

    def handle_action(self, action, callback):
        self.handlers[action] = callback

    def run(self):
        self.prepare()
        self.invoke()

    def invoke(self):
        default = self.usage_error
        if self.handlers.has_key("default"):
            default = self.handlers["default"]
        if self.req.arg_count() == 0:
            default()
        else:
            handler = None
            action = self.req.arg(0)
            if self.handlers.has_key(action):
                handler = self.handlers[action]
            else:
                handler_name = "handle_%s" % (action)
                try:
                    handler = getattr(self, handler_name)
                except AttributeError:
                    handler = default
            handler()
        self.resp.commit()

    def prepare(self):
        pass

    def usage_error(self):
        self.resp.send_error("Guru meditation: PEBKAC")
