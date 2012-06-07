from .context import logs
from .handlers import ListHandler
import unittest

class DefaultLoggerTestSuite(unittest.TestCase):
    def setUp(self):
        self.logger = logs
    
    def test_version_is_set(self):
        self.assertTrue(hasattr(logs, "VERSION"))
    
    def test_no_msg(self):
        self.logger.alert(foo="bar", gah="gurk")
        self.assert_num_logged(1)
        self.assert_msg_logged("foo=bar")
        self.assert_msg_logged("gah=gurk")
    
    def test_logging_different_levels(self):
        self.logger.debug("This is a debug message.", "with", other="stuff")
        self.logger.info("This is an info message.", "with", other="stuff")
        self.logger.notice("This is a notice message.", "with", other="stuff")
        self.logger.warning("This is a warning message.", "with", other="stuff")
        self.logger.error("This is an error message.", "with", other="stuff")
        self.logger.critical("This is a critical message.", "with", other="stuff")
        self.logger.alert("This is an alert message.", "with", other="stuff")
        self.logger.emergency("This is an emergency message.", "with", other="stuff")
        
        self.assert_num_logged(8)
    
    # can't actually test these for the default logger, but children can
    def assert_num_logged(self, num_expected):
        pass
    
    def assert_msg_logged(self, expected_msg):
        pass


class CustomLoggerTestSuite(DefaultLoggerTestSuite):
    def setUp(self):
        self.logger = logs.Logger("Custom Logger")
    
    def test_invalid_level(self):
        with self.assertRaises(logs.exceptions.InvalidLogLevel):
            self.logger.log("invalid", "This is an invalid message.")
        with self.assertRaises(AttributeError):
            self.logger.invalid("This is an invalid message.")


class CustomTransportTestSuite(CustomLoggerTestSuite):
    def setUp(self):
        list_transport = logs.transports.Transport(handler=ListHandler(), level="debug")
        self.logger = logs.Logger(transports=[list_transport])
    
    def assert_num_logged(self, num_expected):
        num_logged = len(self.logger.transports[0].handler.log_list)
        self.assertEquals(num_logged, num_expected)
    
    def assert_msg_logged(self, expected_msg):
        logged_msg = self.logger.transports[0].handler.log_list[-1]
        self.assertTrue(expected_msg in logged_msg)


class MultipleTransportTestSuite(CustomLoggerTestSuite):
    pass
