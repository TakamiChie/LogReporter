from pathlib import Path
import unittest
import logging

from logreporter.reporterloghandler import ReporterLogHandler

class TestReporterLogHandler(unittest.TestCase):
  """
  A test class that verifies the operation of `ReporterLogHandler`.
  """

  def setUp(self):
    """
    Executed for each test method call.
    """
    pass

  def tearDown(self):
    """
    Executed for each test method call.
    """
    pass

  @classmethod
  def setUpClass(self):
    """
    Called only once when running a test case.
    """

  @classmethod
  def teardownClass(self):
    """
    Called only once when running a test case.
    """
    pass

  def test_get_text_warning(self):
    """
    After outputting the following log, when using the `ReportLogHandler#get_text()` method, get the log contents and check that the file has been deleted.
    * Log level = WARING
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("test message")
    self.assertFalse(rlh.get_text() == "")
    self.assertFalse(rlh._filename.exists())

  def test_get_text_debug(self):
    """
    After outputting the following log, when using the `ReportLogHandler#get_text()` method, check that the string is empty and that the file has been deleted.
    * Log level = DEBUG
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.debug("test message")
    self.assertTrue(rlh.get_text() == "")
    self.assertFalse(rlh._filename.exists())

  def test_get_text_twice(self):
    """
    If you use the `ReportLogHandler#get_text()` method after outputting the following log, check that the log contents include line breaks.
    * Log level of the log to be output the first time = WARING
    * Log level of the log to be output the second time = WARING
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("test message")
    logger.warn("test message")
    self.assertIn("\n", rlh.get_text())

  def test_get_text_morethanonce(self):
    """
    After outputting the following log, if you use the `ReportLogHandler#get_text ()` method, check that you can get the contents of the log.
    * Log level of the log to be output the first time = WARING
    * Log level of the log to be output the second time = DEBUG
    * Log level of the log to be output the third time = WARNING
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("test message")
    self.assertFalse(rlh.get_text() == "")
    logger.debug("test message")
    self.assertTrue(rlh.get_text() == "")
    logger.warn("test message")
    self.assertFalse(rlh.get_text() == "")

  def test_original_path(self):
    """
    If you specify your own file path as an argument of the constructor, check that the file is created in the specified folder.
    """
    path = Path(__file__).parent / "out" / "test.log"
    rlh = ReporterLogHandler(path)
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("test message")
    self.assertTrue(path.exists())
    rlh.get_text()
    self.assertFalse(path.exists())
