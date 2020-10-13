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
    super().__init__(self._filename, encoding="utf-8")
    self.level == logging.WARNING

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
      self._filename.unlink()
    return text
