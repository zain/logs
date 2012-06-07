from .exceptions import InvalidLogLevel

SYSLOG_LEVELS = ["debug", "info", "notice", "warning", "error", "critical", "alert", "emergency"]

class Logger(object):
    def __init__(self, name="root", levels=None, *args, **kwargs):
        if not levels:
            self.levels = SYSLOG_LEVELS
    
    def log(self, level, msg, *args, **kwargs):
        if level not in self.levels:
            raise InvalidLogLevel("%s is not a valid log level. Valid log levels are: %s" % 
                (level, ",".join(self.levels)))
    
    def __getattr__(self, method_name):
        return lambda msg, *args, **kwargs: self.log(*args, level=method_name, msg=msg, **kwargs)
