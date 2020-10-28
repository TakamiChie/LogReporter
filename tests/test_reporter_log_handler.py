from logging import Logger
from pathlib import Path
import unittest
import logging

from logreporter.reporterloghandler import ReporterLogHandler

class TestReporterLogHandler(unittest.TestCase):
  """
  A test class that verifies the operation of `ReporterLogHandler`.
  """

  #region prepare

  def setUp(self):
    """
    Executed for each test method call.
    """
    logger = logging.getLogger("testlogger")
    logger.handlers.clear()
    f = ReporterLogHandler.get_defaultfilename()
    if f.exists(): f.unlink()

  #endregion

  #region constructor test

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
    self.assertFalse(rlh.has_text )

  #endregion

  #region get_text() test

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
    self.assertFalse(rlh.has_text)

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

  #endregion

  #region get_text(max_length) test

  def test_get_text_max_length(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions, confirm that the log of the specified number of characters is output.
    Also, check that the log that exceeds the specified number of characters remains in the file.
    * Specify the value of max_length as a value less than the number of characters in the log.
    * The value of max_length is equal to the number of characters in one line of the log.
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing" * 30)
    logger.warn("message" * 30)
    self.assertEqual(rlh.get_text(max_length=210), "testing" * 30)
    self.assertEqual(rlh.get_text(), "message" * 30)

  def test_get_text_max_length_2line(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions, confirm that the log of the specified number of characters is output.
    Also, check that the log that exceeds the specified number of characters remains in the file.
    * Specify the value of max_length as a value less than the number of characters in the log.
    * The value of max_length is greater than the number of characters per line in the log.
    * The value of max_length is equal to the number of characters in two line of the log.
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing" * 20)
    logger.warn("message" * 30)
    logger.warn("abcdefg" * 30)
    self.assertEqual(rlh.get_text(max_length=351), "{}\n{}".format("testing" * 20, "message" * 30))
    self.assertEqual(rlh.get_text(), "abcdefg" * 30)

  def test_get_text_max_length_2line_little_after(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions, confirm that the log of the specified number of characters is output.
    Also, check that the log that exceeds the specified number of characters remains in the file.
    * Specify the value of max_length as a value less than the number of characters in the log.
    * The value of max_length is greater than the number of characters per line in the log.
    * The value of max_length is greater than the number of characters in two lines of the log and less than the number of characters in three lines.
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing" * 20)
    logger.warn("message" * 30)
    logger.warn("abcdefg" * 30)
    self.assertEqual(rlh.get_text(max_length=360), "{}\n{}".format("testing" * 20, "message" * 30))
    self.assertEqual(rlh.get_text(), "abcdefg" * 30)

  def test_get_text_max_length_large_value(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions, confirm that the log of the specified number of characters is output.
    Also, make sure that the log file is empty.
    * Specify the value of max_length as a value grater than the number of characters in the log.
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing" * 20)
    logger.warn("message" * 30)
    logger.warn("abcdefg" * 30)
    self.assertNotEqual(len(rlh.get_text(max_length=1000)), 0)
    self.assertEqual(rlh.get_text(), "")

  def test_get_text_max_length_overtext(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions, confirm that the log of the specified number of characters is output.
    Also, check that the log that exceeds the specified number of characters remains in the file.
    * Specify the value of max_length as a value greater than the number of characters in the log.
    * The value of max_length is greater than the number of characters first line in the log.
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("1" * 20 + "2" * 10)
    self.assertEqual(rlh.get_text(max_length=20), "1" * 20)
    self.assertEqual(rlh.get_text(), "2" * 10)

  #endregion

  #region get_text(report) test

  def test_get_text_report_commited(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions,
    The text is passed to the function, and the return value of the function determines whether or not to commit.
    * `max_length` parameter: not specified
    * `report` parameter: specified
    * Return value of the function specified by the `report` parameter: True
    """
    def test(text):
      self.assertEqual(text, "testing\n")
      return True
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing")
    rlh.get_text(report=test)
    self.assertEqual(rlh.get_text(), "")

  def test_get_text_report_cancelled(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions,
    The text is passed to the function, and the return value of the function determines whether or not to commit.
    * `max_length` parameter: not specified
    * `report` parameter: specified
    * Return value of the function specified by the `report` parameter: False
    """
    def test(text):
      self.assertEqual(text, "testing\n")
      return False
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing")
    rlh.get_text(report=test)
    self.assertEqual(rlh.get_text().strip(), "testing")

  def test_get_text_report_max_length_commited(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions,
    The text is passed to the function, and the return value of the function determines whether or not to commit.
    * `max_length` parameter: specified
    * `report` parameter: specified
    * Return value of the function specified by the `report` parameter: True
    """
    def test(text):
      self.assertEqual(text, "testing")
      return True
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing")
    logger.warn("message")
    rlh.get_text(max_length=7,report=test)
    self.assertEqual(rlh.get_text().strip(), "message")

  def test_get_text_report_max_length_cancelled(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions,
    The text is passed to the function, and the return value of the function determines whether or not to commit.
    * `max_length` parameter: specified
    * `report` parameter: specified
    * Return value of the function specified by the `report` parameter: False
    """
    def test(text):
      self.assertEqual(text, "testing")
      return False
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing")
    logger.warn("message")
    rlh.get_text(max_length=7,report=test)
    self.assertEqual(rlh.get_text().strip(), "testing\nmessage")

  def test_get_text_report_max_length_2line(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions,
    The text is passed to the function, and the return value of the function determines whether or not to commit.
    * `max_length` parameter: specified
    * `report` parameter: specified
    * Return value of the function specified by the `report` parameter: True
    * Number of characters specified for `max_length`: 2 lines of text
    """
    def test(text):
      self.assertEqual(text, "testing\nmessage")
      return True
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing")
    logger.warn("message")
    logger.warn("abcdefg")
    rlh.get_text(max_length=20,report=test)
    self.assertEqual(rlh.get_text().strip(), "abcdefg")

  #endregion

  #region clear() test

  def test_clear(self):
    """
    Confirm that the existing log is deleted when `ReportLogHandler#clear()` is executed without calling `ReportLogHandler#get_text()` after outputting some log.
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("test message")
    logger.warn("test message")
    rlh.clear()
    self.assertFalse(rlh.has_text)

  #endregion

  #region enabled test

  def test_enabled_false(self):
    """
    Make sure that all logs are deleted when `ReporterLogHandler#enabled` is set to False.
    Also, make sure that log collection starts again when set to True.
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("test message")
    logger.warn("test message")
    rlh.enabled = False
    logger.warn("test message")
    self.assertFalse(rlh.has_text)
    rlh.enabled = True
    logger.warn("test message")
    self.assertTrue(rlh.has_text)

  #endregion

  #region has_text test

  def test_hastext_there_text(self):
    """
    When you refer to `ReporterLogHandler#has_text` under the following conditions, check that the value is True.
    * Log file: Exists
    * Log data: Not empty
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("test message")
    self.assertTrue(rlh.has_text)

  def test_hastext_empty_text(self):
    """
    When you refer to `ReporterLogHandler#has_text` under the following conditions, check that the value is False.
    * Log file: Exists
    * Log data: Empty
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("test message")
    rlh.get_text(max_length=12)
    self.assertFalse(rlh.has_text)

  def test_hastext_empty_text(self):
    """
    When you refer to `ReporterLogHandler#has_text` under the following conditions, check that the value is False.
    * Log file: Not exist
    * Log data: N/A
    """
    rlh = ReporterLogHandler()
    self.assertFalse(rlh.has_text)

  #endregion

  #region Anomaly test.

  def test_get_text_max_length_valueerror(self):
    """
    When `ReporterLogHandler#get_text()` is called under the following conditions, Confirm that ValueError occurs.
    * max_length=1 or 0
    """
    rlh = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.warn("testing" * 30)
    with self.assertRaises(ValueError):
      rlh.get_text(max_length=1)
    with self.assertRaises(ValueError):
      rlh.get_text(max_length=0)

  def test_handler_multiple_registration(self):
    """
    Confirm that `ReporterLogHandler#clear()` works normally with `ReporterLogHandler` registered in two loggers.
    """
    rlh = ReporterLogHandler()
    rlh2 = ReporterLogHandler()
    logger = logging.getLogger("testlogger")
    logger.addHandler(rlh)
    logger.addHandler(rlh2)
    logger.warn("test message")
    rlh.clear()

  #endregion
