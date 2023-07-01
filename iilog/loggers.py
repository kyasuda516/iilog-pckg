# Copyright (c) 2023 Kanta Yasuda (GitHub: @kyasuda516)
# This software is released under the MIT License, see LICENSE.

class __BaseLogger():
  from iilog.__c import StrPath as __StrPath
  from iilog.__c import _FormatStyle as __FormatStyle
  from iilog.__c import _Level as __Level
  from iilog.__c import SupportsWrite as __SupportsWrite
  from typing import Iterable as __Iterable
  from logging import Handler as __Handler

  __id = 0
  __doc__ = """
    Base class for loggers.
    Not meant to be instantiated directly.  Instead, use Logger
    or WarningsLogger.
  """

  def __new__(
    cls, 
    name: str | None = None,
    *,
    filename: __StrPath | None = ...,
    filemode: str = ...,
    format: str = ...,
    datefmt: str | None = ...,
    style: __FormatStyle = ...,
    level: __Level | None = ...,
    stream: __SupportsWrite[str] | None = ...,
    handlers: __Iterable[__Handler] | None = ...,
    # force: bool | None = ...,
    encoding: str | None = ...,
    errors: str | None = ...
  ):
    # validate meeting some conditions about parameters 
    if filename != ... and stream != ...:
      raise ValueError("'stream' and 'filename' should not be specified together")
    if (filename != ... or stream != ...) and handlers != ...:
      raise ValueError("'stream' or 'filename' should not be specified together with 'handlers'")

    # The following statements are for Singleton when using getLogger.
    if name is not None and hasattr(cls, "_instance"):
      # if not force:
      #   return cls._instance
      # else:
      #   cls._instance.handlers.clear()
      return cls._instance

    # create a formatter
    formatter = None
    if format != ...:
      from logging import Formatter
      formatter = Formatter(
        fmt=format,
        datefmt=datefmt if datefmt != ... else None,
        style=style if style != ... else '%',
        validate=True,
        defaults=None
      )
    
    from iilog.__c import NILS

    # create some handlers
    handlers = handlers if handlers != ... else []
    if filename not in NILS:
      from logging import FileHandler
      handler = FileHandler(
        filename=filename, 
        mode=filemode if filemode != ... else 'a',
        encoding=encoding if encoding != ... else None,
        delay=False,
        errors=errors if errors != ... else None
      )
      handler.setFormatter(formatter)
      handlers.append(handler)
    elif stream not in NILS:
      from logging import StreamHandler
      handler = StreamHandler(
        stream=stream
      )
      handler.setFormatter(formatter)
      handlers.append(handler)
    
    # create or get a logger
    logger = None
    if name is not None:
      from logging import getLogger
      logger = getLogger(name)
    else:
      from logging import Logger as _Logger
      logger = _Logger(
        name=f'{__name__}.Logger.i{cls.__id}',
        level=level if level != ... else 0
      )
      cls.__id += 1
    
    # add the handlers to the logger
    if handlers not in NILS:
      for handler in handlers:
        logger.addHandler(handler)

    # The following statements are for Singleton when using getLogger.
    if name is not None:
      cls._instance = logger
    
    return logger

class Logger(__BaseLogger):
  from iilog.__c import StrPath as __StrPath
  from iilog.__c import _FormatStyle as __FormatStyle
  from iilog.__c import _Level as __Level
  from iilog.__c import SupportsWrite as __SupportsWrite
  from typing import Iterable as __Iterable
  from logging import Handler as __Handler

  __doc__ = """
    Creates a logger with a unique name.
    You can create a Logger instance with roughly the same 
    feeling as the "logging.basicConfig" function.
  """

  def __new__(
    cls, 
    *,
    filename: __StrPath | None = ...,
    filemode: str = ...,
    format: str = ...,
    datefmt: str | None = ...,
    style: __FormatStyle = ...,
    level: __Level | None = ...,
    stream: __SupportsWrite[str] | None = ...,
    handlers: __Iterable[__Handler] | None = ...,
    # force: bool | None = ...,
    encoding: str | None = ...,
    errors: str | None = ...
  ):
    return super().__new__(
      cls,
      None,
      filename=filename,
      filemode=filemode,
      format=format,
      datefmt=datefmt,
      style=style,
      level=level,
      stream=stream,
      handlers=handlers,
      # force=force,
      encoding=encoding,
      errors=errors
    )

class WarningsLogger(__BaseLogger):
  from iilog.__c import StrPath as __StrPath
  from iilog.__c import _FormatStyle as __FormatStyle
  from iilog.__c import _Level as __Level
  from iilog.__c import SupportsWrite as __SupportsWrite
  from typing import Iterable as __Iterable
  from logging import Handler as __Handler

  __doc__ = """
    Special logger that logs warnings issued by the warnings
    module.
    You can get the instance with roughly the same feeling as
    the "logging.basicConfig" function. From the moment the
    instance is created, start to redirect all warnings to
    this package.
    If neither filename, stream nor handlers are specified
    after that, stop the redirect.
  """

  def __new__(
    cls, 
    *, 
    filename: __StrPath | None = ...,
    filemode: str = ...,
    format: str = ...,
    datefmt: str | None = ...,
    style: __FormatStyle = ...,
    level: __Level | None = ...,
    stream: __SupportsWrite[str] | None = ...,
    handlers: __Iterable[__Handler] | None = ...,
    # force: bool | None = ...,
    encoding: str | None = ...,
    errors: str | None = ...
  ):
    from logging import captureWarnings
    from iilog.__c import NILS
    # if all([filename in NILS, stream in NILS, handlers in NILS, force]):
    if all([filename in NILS, stream in NILS, handlers in NILS]):
      captureWarnings(False)
    else:
      captureWarnings(True)
    
    return super().__new__(
      cls,
      'py.warnings',
      filename=filename,
      filemode=filemode,
      format=format,
      datefmt=datefmt,
      style=style,
      level=level,
      stream=stream,
      handlers=handlers,
      # force=force,
      encoding=encoding,
      errors=errors
    )

from iilog.__c import Env as __Env
get_env_logger = __Env().get_logger
