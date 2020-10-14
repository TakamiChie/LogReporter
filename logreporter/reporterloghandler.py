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

  def get_text(self, max_length=-1):
    """
    Get all the log strings written so far.

    Parameters
    ----
    max_length: int
      Maximum number of characters requested.
      If this value is set, get the text with the number of lines closest to this number of characters and return it.
      Also, in this case, the unacquired text is saved in the internal log file.

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
      if max_length != -1:
        lines = text.splitlines()
        result = []
        while max_length > 0 and len(lines) > 0:
          t = lines[0]
          max_length -= len(t)
          if max_length >= 0:
            result.append(t)
            lines.pop(0)
            max_length -= len("\n") # Newline character.
        with open(self._filename, mode="w", encoding="utf-8") as f:
          f.write("\n".join(lines))
        text = "\n".join(result)
      else:
        self.clear()
    return text
