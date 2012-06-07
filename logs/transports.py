import logging

class Transport(object):
    def __init__(self, handler, level):
        self.handler = handler
        self.level = level
    
    def log(self, name, level, all_levels, msg="", *args, **kwargs):
        if args:
            msg += " %s" % self.format_vals(args)
        if kwargs:
            msg += " %s" % self.format_kv(kwargs)
        
        logger = self.get_logger(name, all_levels)
        level_num = logging._levelNames[level]
        logger.log(level_num, msg)
    
    def get_logger(self, logger_name, level_list):
        levels = list(enumerate(reversed(level_list), start=1))
        logging._levelNames = dict(levels + [(name, num) for num, name in levels])
        logger = logging.getLogger(logger_name)
        logger.handlers = [self.handler]
        
        return logger
    
    def format_vals(self, l):
        """Format a list of positional values that were logged"""
        return " ".join(l)
    
    def format_kv(self, pairs):
        """Format a dictionary with key/value pairs that were logged"""
        return " ".join("%s=%s" % (key, val) for key, val in pairs.items())


class Console(Transport):
    def __init__(self, level=-1, format=None, colorize=False, timestamps=False):
        if not format:
            format = "%(levelname)-10s %(message)s"
