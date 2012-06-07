import datetime, logging, sys

class Transport(object):
    def __init__(self, level, handler=None, *args, **kwargs):
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
    
    COLORS = {"highlighted_red": "\033[41m", "bold_red": "\033[1m\033[31m", "red": "\033[31m",
        "yellow": "\033[33m", "green": "\033[32m", "blue": "\033[34m"}
    
    def __init__(self, format=None, colorize=False, timestamps=False, caller=False, stream=None, *args, **kwargs):
        self.stream = stream or sys.stdout
        if format:
            self.format = format
        else:
            self.format = ""
            if timestamps: self.format += "{time:%d %b %H:%M:%S} - "
            
            if caller: self.format += "[{name}] - "
            
            if colorize: self.format += "{start_color}{level}:{end_color} "
            else: self.format += "{level}: "
            
            self.format += "{msg}"
            
            self.format += "\n"
        
        Transport.__init__(self, *args, **kwargs)
    
    def log(self, name, level, all_levels, msg="", *args, **kwargs):
        if args:
            msg += " %s" % self.format_vals(args)
        if kwargs:
            msg += " %s" % self.format_kv(kwargs)
        
        msg = msg.strip()
        
        output = self.format.format(msg=msg, name=name, level=level, time=datetime.datetime.now(),
            start_color=self.color_for(level, all_levels), end_color="\033[0m")
        self.stream.write(output)
    
    def color_for(self, level, all_levels):
        color_levels = {
            "emergency": "highlighted_red",
            "alert": "highlighted_red",
            "critical": "bold_red",
            "error": "bold_red",
            "warning": "yellow",
            "notice": "yellow",
            "info": "green",
            "debug": "blue"
        }
        if level not in color_levels:
            return Console.COLORS["blue"]
        return Console.COLORS[color_levels[level]]
