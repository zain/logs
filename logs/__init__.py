VERSION = (0, 0, 1)

from .logger import Logger

root_logger = Logger()
debug = lambda *args, **kwargs: root_logger.debug(*args, **kwargs)
info = lambda *args, **kwargs: root_logger.info(*args, **kwargs)
notice = lambda *args, **kwargs: root_logger.notice(*args, **kwargs)
warning = lambda *args, **kwargs: root_logger.warning(*args, **kwargs)
error = lambda *args, **kwargs: root_logger.error(*args, **kwargs)
critical = lambda *args, **kwargs: root_logger.critical(*args, **kwargs)
alert = lambda *args, **kwargs: root_logger.alert(*args, **kwargs)
emergency = lambda *args, **kwargs: root_logger.emergency(*args, **kwargs)
