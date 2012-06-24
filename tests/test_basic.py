import unittest, StringIO

from .context import logs
from .handlers import ListHandler


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
        self.assert_msg_logged("This is an emergency message. with other=stuff")

    def test_logging_property_with_a_space(self):
        self.logger.emergency("Message", has="a big property")
        self.assert_msg_logged('Message has="a big property"')

    def test_exception_logging(self):
        try:
            raise Exception("This is the exception message")
        except Exception, e:
            self.logger.error(exception=e)

        self.assert_msg_logged("Traceback (most recent call last):")
        self.assert_msg_logged("raise Exception")
        self.assert_msg_logged("Exception: This is the exception message")

    # can't actually test these for the default logger, but children can
    def assert_num_logged(self, num_expected):
        pass
    
    def assert_msg_logged(self, expected_msg):
        pass


class CustomLoggerTestSuite(DefaultLoggerTestSuite):
    def setUp(self):
        self.logger = logs.Logger("Custom Logger")
    
    def test_invalid_level(self):
        try:
            self.logger.log("invalid", "This is an invalid message.")
            assert False
        except logs.exceptions.InvalidLogLevel:
            pass
        
        try:
            self.logger.invalid("This is an invalid message.")
            assert False
        except AttributeError:
            pass


class CustomTransportTestSuite(CustomLoggerTestSuite):
    def setUp(self):
        list_transport = logs.transports.Transport(handler=ListHandler(), level="debug")
        self.logger = logs.Logger(transports=[list_transport])
    
    def test_adding_a_new_log_level(self):
        self.logger.levels.append("super_debug")
        self.logger.super_debug("This should be below the log level and should be ignored.")
        self.assert_num_logged(0)
        self.logger.debug("This should still be logged though.")
        self.assert_num_logged(1)
    
    def assert_num_logged(self, num_expected):
        num_logged = len(self.logger.transports[0].handler.log_list)
        self.assertEquals(num_logged, num_expected)
    
    def assert_msg_logged(self, expected_msg):
        logged_msg = self.logger.transports[0].handler.log_list[-1]
        self.assertTrue(expected_msg in logged_msg)


class ConsoleTransportTestSuite(CustomTransportTestSuite):
    def setUp(self):
        self.stream = StringIO.StringIO()
        transport = logs.transports.Console(level="debug", timestamps=True, stream=self.stream)
        self.logger = logs.Logger(transports=[transport])
    
    def tearDown(self):
        self.stream.close()
    
    def assert_num_logged(self, num_expected):
        # this is not perfect; it assumes that no messages logged have newlines in them
        num_logged = len(self.stream.getvalue().split('\n')) - 1  # trailing newline
        self.assertEquals(num_logged, num_expected)
    
    def assert_msg_logged(self, expected_msg):
        self.assertTrue(expected_msg in self.stream.getvalue())
