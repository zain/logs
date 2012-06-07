from .context import logs
import unittest

class DefaultLoggerTestSuite(unittest.TestCase):
    def setUp(self):
        self.logger = logs
    
    def test_version_is_set(self):
        self.assertTrue(hasattr(logs, "VERSION"))
    
    def test_logging_different_levels(self):
        self.logger.debug("This is a debug message.")
        self.logger.info("This is an info message.")
        self.logger.notice("This is a notice message.")
        self.logger.warning("This is a warning message.")
        self.logger.error("This is an error message.")
        self.logger.critical("This is a critical message.")
        self.logger.alert("This is an alert message.")
        self.logger.emergency("This is an emergency message.")

class CustomLoggerTestSuite(DefaultLoggerTestSuite):
    def setUp(self):
        self.logger = logs.Logger("Custom Logger")
    
    def test_invalid_level(self):
        with self.assertRaises(logs.exceptions.InvalidLogLevel):
            self.logger.invalid("This is an invalid message.")
