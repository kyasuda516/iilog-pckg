# Copyright (c) 2023 Kanta Yasuda (GitHub: @kyasuda516)
# This software is released under the MIT License, see LICENSE.

from typing import TypeAlias, Literal, TypeVar
import typing
from abc import abstractmethod

runtime_checkable = typing.runtime_checkable     # Python 3.8+ required
AnyStr_co = TypeVar("AnyStr_co", str, bytes, covariant=True)
Protocol = typing.Protocol                       # Python 3.8+ required
_T_contra = TypeVar("_T_contra", contravariant=True)

@runtime_checkable
class PathLike(Protocol[AnyStr_co]):
  @abstractmethod
  def __fspath__(self) -> AnyStr_co: ...

StrPath: TypeAlias = str | PathLike[str]
_FormatStyle: TypeAlias = Literal["%", "{", "$"]
_Level: TypeAlias = int | str

class SupportsWrite(Protocol[_T_contra]):
  def write(self, __s: _T_contra) -> object: ...

# The followings are original.

NILS = (None, ...)
ConfigFileFormat: TypeAlias = Literal["yaml", "json"]

class Env():
  from typing import Any as __Any
  from logging import Logger as __Logger

  __doc__ = """
    Class with the environmental state.
    Although designed with the singleton pattern, this class 
    is not expected to instantiate again.
  """

  def __new__(cls):
    if not hasattr(cls, "_instance"):
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
    self.__set_levels()
    self.__config = dict()
  
  def __set_levels(self):
    from logging import CRITICAL
    from logging import DEBUG
    from logging import FATAL
    from logging import ERROR
    from logging import INFO
    from logging import NOTSET
    from logging import WARN
    from logging import WARNING
    self.CRITICAL = CRITICAL
    self.DEBUG = DEBUG
    self.FATAL = FATAL
    self.ERROR = ERROR
    self.INFO = INFO
    self.NOTSET = NOTSET
    self.WARN = WARN
    self.WARNING = WARNING

  def set_config(
      self,
      *,
      filename: StrPath | None = ...,
      fileformat: ConfigFileFormat = ...,
      encoding: str = ..., 
      config: dict[str, __Any] | None = ...,
    ) -> None:
    # validate meeting some conditions about parameters 
    if filename != ... and config != ...:
      raise ValueError("'filename' and 'dict' should not be specified together")

    if filename != ...:
      from pathlib import Path
      filename = Path(filename)
      with open(filename, 'rt', encoding=encoding) as f:
        if fileformat == "yaml" or (fileformat == ... and filename.suffix in ("yaml", "yml")):
          import yaml
          self.__config = yaml.safe_load(f)
        elif fileformat == "json" or (fileformat == ... and filename.suffix in ("json", )):
          import json
          self.__config = json.load(f)
        else:
          raise ValueError("Unable to determine the file format. Please specify the 'fileformat' argument.")

    if config != ...:
      self.__config = config
    
    from logging.config import dictConfig
    dictConfig(self.__config, )
    
  @property
  def config(self):
    return self.__config
  
  def get_logger(self, name: str) -> __Logger:
    from logging import getLogger
    return getLogger(name)
