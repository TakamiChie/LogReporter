import logging
from pathlib import Path
import unittest

from logreporter.reporter import Reporter

class TestReporter(unittest.TestCase):
  """
  A test class that verifies the operation of `Reporter`.
  """

  #region prepare

  def tearDown(self):
    """
    Executed for each test method call.
    """
    r = Reporter()
    if r._handler._filename.exists():
      r._handler._filename.unlink()
    Reporter.reset()

  #endregion

  #region constructor test

  def test_constructor_default(self):
    """
    If you do not set any arguments in the constructor, make sure that the Reporter object is created by default.
    """
    reporter = Reporter()
    self.assertEqual(reporter._handler._filename.parent.parent, Path(__file__).parent.parent)
    self.assertEqual(reporter.enabled, True)

  def test_constructor_hasparam(self):
    """
    If you set an argument in the constructor, make sure that the value is set in the Reporter object.
    """
    path = Path(__file__).parent / "out" / "test.log"
    reporter = Reporter(filename=path, enabled=False)
    self.assertEqual(reporter._handler._filename, path)
    self.assertEqual(reporter.enabled, False)

  def test_constructor_twice(self):
    """
    After getting an instance of `Reporter`, make sure that its arguments are ignored when calling the` Reporter` constructor again.
    """
    reporter = Reporter()
    path = Path(__file__).parent / "out" / "test.log"
    reporter2 = Reporter(filename=path, enabled=False)
    self.assertEqual(reporter, reporter2)
    self.assertEqual(reporter2._handler._filename.parent.parent, Path(__file__).parent.parent)
    self.assertEqual(reporter2.enabled, True)

  #endregion

  #region setup test

  def test_setup(self):
    """
    When the log is output to the logger set by `Reporter # setup ()`, confirm that `ReportLogHandler` records the log.
    """
    logger = logging.getLogger("testlogger")
    reporter = Reporter()
    reporter.setup(logger)
    logger.warn("test message")
    self.assertFalse(reporter._handler.get_text() == "")

  #endregion
