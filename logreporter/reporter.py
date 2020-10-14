
from logreporter.reporterloghandler import ReporterLogHandler

class Reporter(object):
  """
  The main class that reports logs.
  This object has a singleton implementation. Therefore, the same object can always be obtained on one application.
  """
  _instance = None

  def __init__(self, *args, **kwargs):
    pass

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance.__initialize(*args, **kwargs)
    return cls._instance

  def __initialize(self, filename=None, enabled=True):
    """
    A method that behaves as a constructor.
    This method is only executed when there is no instance of this class in the process.

    Parameters
    ----
    filename: Path or str
      Log file name. If omitted, it will be created in the same folder as the module file.
    enabled: bool
      A flag that indicates whether to enable log collection. No logs are collected when set to False.
    """
    self._handler = ReporterLogHandler(filename=filename)
    self.enabled = enabled
    self.logger = None

  def setup(self, logger):
    """
    Set up the Reporter object.

    Parameters
    ----
    logger: logging.Logger
      Logger object.
    """
    self.logger = logger
    logger.addHandler(self._handler)

  #region properties

  @property
  def enabled(self):
    """
    Whether to perform log collection processing. If False is set, log collection will be stopped and all accumulated logs will be deleted.
    """
    return self._handler.enabled

  @enabled.setter
  def enabled(self, value):
    """
    Whether to perform log collection processing. If False is set, log collection will be stopped and all accumulated logs will be deleted.
    """
    self._handler.enabled = value

  #endregion

  #region for testing

  @staticmethod
  def reset():
    """
    Destroy an instance of the class and reset all states.
    This method is only used for unit tests.
    """
    Reporter._instance = None

  #endregion
