import logging
from logreporter.reporterloghandler import ReporterLogHandler
from pathlib import Path
import unittest

from logreporter.reporter import Reporter

class TestReporter(unittest.TestCase):
  """
  A test class that verifies the operation of `Reporter`.
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
    Reporter.reset()

  #endregion

  #region constructor test

  def test_constructor_twice(self):
    """
    After getting an instance of `Reporter`, make sure that when you call the` Reporter` constructor again, you get the same instance.
    """
    reporter = Reporter()
    reporter2 = Reporter()
    self.assertEqual(reporter, reporter2)

  #endregion

  #region setup test

  def test_setup_default(self):
    """
    If you do not set the optional parameters in `Reporter#setup()`, make sure that the log file is set with the default settings.
    """
    reporter = Reporter()
    logger = logging.getLogger("testlogger")
    reporter.setup(logger, None)
    self.assertEqual(reporter._handler._filename.parent.parent, Path(__file__).parent.parent)
    self.assertEqual(reporter.enabled, True)

  def test_setup_hasparam(self):
    """
    If you set the optional parameters in `Reporter#setup()`, make sure that the value is set in the Reporter object.
    """
    path = Path(__file__).parent / "out" / "test.log"
    reporter = Reporter()
    logger = logging.getLogger("testlogger")
    reporter.setup(logger, None, filename=path, enabled=False)
    self.assertEqual(reporter._handler._filename, path)
    self.assertEqual(reporter.enabled, False)

  def test_setup_logging(self):
    """
    When the log is output to the logger set by `Reporter # setup ()`, confirm that `ReportLogHandler` records the log.
    """
    logger = logging.getLogger("testlogger")
    reporter = Reporter()
    reporter.setup(logger, None)
    logger.warn("test message")
    self.assertFalse(reporter._handler.get_text() == "")

  #endregion
