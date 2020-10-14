import logging
from pathlib import Path

class ReporterLogHandler(logging.FileHandler):
  """
  Log handler for Reporter processing.
  """

  def __init__(self, filename=None):
    """
    Constructor.

    Parameters
    ----
    filename: Path or str
      Log file name. If omitted, it will be created in the same folder as the module file.
    """
    # Place the log file in the same folder as the application or directly under the user folder.
    self._filename = Path(__file__).parent / "reporter.log" if filename is None else filename
    super().__init__(self._filename, encoding="utf-8", delay=True)
    self.level == logging.WARNING
    self._enabled = True

  @property
  def enabled(self):
    """
    Whether to perform log collection processing. If False is set, log collection will be stopped and all accumulated logs will be deleted.
    """
    return self._enabled

  @enabled.setter
  def enabled(self, value):
    """
    Whether to perform log collection processing. If False is set, log collection will be stopped and all accumulated logs will be deleted.
    """
    self._enabled = value
    if not value:
      self.clear()

  def emit(self, record):
    """
    Override method.
    If the value of enabled is False, no processing is performed.
    """
    if self.enabled:
      super().emit(record)

  def clear(self):
    """
    Delete all the log text of the actual acquisition.
    """
    if self._filename.exists():
      self.close()
      self._filename.unlink()

  def get_text(self):
    """
    Get all the log strings written so far.

    Returns
    ----
    text: str
      Log string.
    """
    self.close()
    text = ""
    if self._filename.exists():
      with open(self._filename, mode="r", encoding="utf-8") as f:
        text = f.read()
      self.clear()
    return text
