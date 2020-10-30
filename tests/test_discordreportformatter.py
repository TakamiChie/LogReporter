import logging
from os import name
import unittest

from logreporter.formatter import DiscordReportFormatter

class TestDiscordReportFormatter(unittest.TestCase):

  def record(self, loglevel=logging.WARNING, text="test", exc_info=None, sinfo=None):
    return logging.LogRecord(
      name="test",
      level=loglevel,
      pathname="pathname",
      lineno=0,
      msg=text,
      args=[],
      exc_info=exc_info,
      func=None,
      sinfo=sinfo)

  def test_level_debug(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, check that the emoji is added to the beginning of the line.
    * LogLevel: Debug
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(loglevel=logging.DEBUG)), ":detective: **test**")

  def test_level_info(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, check that the emoji is added to the beginning of the line.
    * LogLevel: Info
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(loglevel=logging.INFO)), ":speech_balloon: **test**")

  def test_level_warning(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, check that the emoji is added to the beginning of the line.
    * LogLevel: Warning
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(loglevel=logging.WARNING)), ":warning: **test**")

  def test_level_error(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, check that the emoji is added to the beginning of the line.
    * LogLevel: Error
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(loglevel=logging.ERROR)), ":exclamation: **test**")

  def test_level_critical(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, check that the emoji is added to the beginning of the line.
    * LogLevel: Critical
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(loglevel=logging.CRITICAL)), ":bangbang: **test**")

  def test_level_unknown(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, Make sure that no error occurs.
    * LogLevel: Unknown
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(loglevel=999)), "**test**")

  def test_text_multiline(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, check that the emoji is added to the beginning of the line.
    * LogLevel: WARNING
    * Multi-line text
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(text="abc\ndef")), ":warning: **abc**\ndef")

  def test_exc_info(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, check that the emoji is added to the beginning of the line.
    * LogLevel: WARNING
    * There is exception information.
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(exc_info=(None, None, None))), ":warning: **test**\n" + \
      "**exc**\n" + \
      "```\n" + \
      "NoneType: None\n" + \
      "```")

  def test_stack_info(self):
    """
    If you call `DiscordReportFormatter#format ()` with the following log specified, check that the emoji is added to the beginning of the line.
    * LogLevel: WARNING
    * There is stack information.
    """
    self.assertEqual(DiscordReportFormatter().format(self.record(sinfo="stack")), ":warning: **test**\n" + \
      "**stack**\n" + \
      "```\n" + \
      "stack\n" + \
      "```")
