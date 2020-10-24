import json
import logging
import unittest

from logreporter.reporter import Reporter
from logreporter.report.discordwhreporter import DiscordWHReporter

class TestDiscordWHReporter(unittest.TestCase):
  """
  A test class that verifies the operation of `DiscordWHReporter`.
  """

  #region prepare

  def setUp(self):
    """
    Executed for each test method call.
    """
    with open("tests/test.json") as f:
      data = json.load(f)
      self.reporter = DiscordWHReporter(data["discordwh"]["url"])

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

  def test_sendtext(self):
    """
    When you send the following log using `DiscordWHReporter`, check that it can be sent.
    * Number of characters: 1,000 characters
    """
    logger = logging.getLogger("testlogger")
    reporter = Reporter()
    reporter.setup(logger, self.reporter)
    logger.warn("1234567890" * 100)
    reporter.upload_report()
    self.assertFalse(reporter.log_remaining)

  def test_sendtext_hasmessage(self):
    """
    When you send the following log using `DiscordWHReporter`, check that it can be sent.
    * Number of characters: 1,000 characters
    * There is a value in the argument message of `Reporter#upload_report()`.
    """
    logger = logging.getLogger("testlogger")
    reporter = Reporter()
    reporter.setup(logger, self.reporter)
    logger.warn("1234567890" * 100)
    reporter.upload_report(message="test message")
    self.assertFalse(reporter.log_remaining)

  def test_sendtext_2record(self):
    """
    When you send the following log using `DiscordWHReporter`, check that it can be sent.
    * Number of characters: 3,000 characters
    """
    logger = logging.getLogger("testlogger")
    reporter = Reporter()
    reporter.setup(logger, self.reporter)
    logger.warn("1234567890" * 100)
    logger.warn("1234567890" * 100)
    logger.warn("1234567890" * 100)
    reporter.upload_report()
    self.assertFalse(reporter.log_remaining)

  #endregion
