import sys

from .exceptions import InvalidLogLevel
from .transports import Console

SYSLOG_LEVELS = ["emergency", "alert", "critical", "error", "warning", "notice", "info", "debug"]
DEFAULT_TRANSPORTS = []#[Console(level="info", colorize=True, timestamps=True)]

class Logger(object):
    def __init__(self, name=None, levels=None, transports=None, *args, **kwargs):
        self.name = name
        self.levels = levels or SYSLOG_LEVELS
        self.transports = transports or DEFAULT_TRANSPORTS
    
    def log(self, level, msg="", *args, **kwargs):
        if level not in self.levels:
            raise InvalidLogLevel("%s is not a valid log level. Valid log levels are: %s" % 
                (level, ", ".join(self.levels)))
        
        if not self.name:
            # populate the name with the caller
            name = sys._getframe(2).f_globals['__name__']
        
        for transport in self.transports:
            if self.levels.index(level) <= self.levels.index(transport.level):
                transport.log(name, level, self.levels, msg, *args, **kwargs)
    
    def __getattr__(self, method_name):
        if method_name not in self.levels:
            raise AttributeError(
                "'%s' object has no attribute '%s'. " % (self.__class__.__name__, method_name) +
                "To log something, use a valid log level: %s" % ", ".join(self.levels)
            )
        return lambda msg="", *args, **kwargs: self.log(method_name, msg, *args, **kwargs)
