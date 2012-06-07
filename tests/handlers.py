import logging

class ListHandler(logging.Handler):
    """A logging handler that stores everything it gets in a list."""
    
    def __init__(self, *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.log_list = []
    
    def emit(self, record):
        self.log_list.append(record.getMessage())
