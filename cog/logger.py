import sys

class Logger(object):
    Debug, Info, Warn, Error = list(range(4))

    @classmethod
    def _write_log_message(cls, message, level):
        prefix = "COGCMD_"
        if level == Logger.Debug:
            prefix = prefix + "DEBUG"
        elif level == Logger.Info:
            prefix = prefix + "INFO"
        elif level == Logger.Warn:
            prefix = prefix + "WARN"
        else:
            prefix = prefix + "ERR"
        print("%s:%s" % (prefix, message), end="\n", file=sys.stdout)
        sys.stdout.flush()

    @classmethod
    def log(cls, message, level):
        Logger._write_log_message(message, level)

    @classmethod
    def debug(cls, message):
        Logger.log(message, Logger.Debug)

    @classmethod
    def info(cls, message):
        Logger.log(message, Logger.Info)

    @classmethod
    def warn(cls, message):
        Logger.log(message, Logger.Warn)

    @classmethod
    def error(cls, message):
        Logger.log(message, Logger.Error)
