<div align="center">

![iilog_logo](https://github.com/kyasuda516/iilog-pckg/assets/127583471/a16a4431-83fb-479a-8609-785c2c66d7a1)

[![Python](https://img.shields.io/pypi/pyversions/iilog-pckg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/iilog-pckg?color=blue)](https://pypi.org/project/iilog-pckg/)
[![LICENSE](https://img.shields.io/pypi/l/iilog-pckg?color=blue)](https://github.com/kyasuda516/iilog/blob/master/LICENSE)

</div>

<div align="center">

## iilog is an alternative library to `logging`

</div>

iilog provides a little more comfortable logging experience.
It is my ([@kyasuda516](https://github.com/kyasuda516)) own reconfiguration of Python's stdlib [`logging`](https://docs.python.org/3/library/logging.html).

<br>

# Features

- A solution for those who feel slightly dissatisfied with the usability of the built-in logging library.
- Logger instances can be created in a way that is very similar to using the [`logging.basicConfig`](https://docs.python.org/3/library/logging.html#logging.basicConfig) function.
- The usage of accessing the root logger is designed to be as invisible as possible.

<br>

# Installation

You can install iilog with

```shell
python -m pip install iilog-pckg
```

Otherwise, you can install directly from the github repo using

```shell
python -m pip install git+https://github.com/kyasuda516/iilog-pckg.git
```

<br>

# Example Usage

## Simple example

sample.py:
```python
from iilog.loggers import Logger
import iilog

# define loggers
logger1 = Logger(
    filename='myapp.log', filemode='w', encoding='UTF-8')

import sys
logger2 = Logger(
    format=r'%(asctime)s %(levelname)-8s %(name)-15s %(message)s', 
    datefmt=r'%Y-%m-%d %H:%M:%S',
    stream=sys.stdout, level=iilog.env.WARNING)

formatter = iilog.formatters.Formatter(iilog.formatters.BASIC_FORMAT)
handler = iilog.handlers.RotatingFileHandler(
    filename='dev.log', maxBytes=256, backupCount=3)
handler.setFormatter(formatter)
logger3 = Logger(handlers=[handler])

# logging
logger1.warning('Watch out!')
logger1.info('I told you so')

logger2.warning('Watch out!')
logger2.info('I told you so')

logger3.error('An unknown error occured.')
logger3.error('An unknown error occured.')
logger3.error('An unknown error occured.')
logger3.error('An unknown error occured.')
logger3.error('An unknown error occured.')
```

The results are as follows:
```shell
$ python sample.py
2023-07-01 02:03:04 WARNING  iilog.loggers.Logger.i1 Watch out!

$ cat myapp.log
Watch out!
I told you so

$ cat dev.log
ERROR:iilog.loggers.Logger.i2:An unknown error occured.

$ cat dev.log.1
ERROR:iilog.loggers.Logger.i2:An unknown error occured.
ERROR:iilog.loggers.Logger.i2:An unknown error occured.
ERROR:iilog.loggers.Logger.i2:An unknown error occured.
ERROR:iilog.loggers.Logger.i2:An unknown error occured.

```

<details>
<summary>For more details</summary>

The `iilog.loggers.Logger` constructor works in much the same way as the [`logging`](https://docs.python.org/3/library/logging.html) library's [`basicConfig`](https://docs.python.org/3/library/logging.html#logging.basicConfig) function. The following is the description of [`logging.basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig)'s parameters taken from the official documentation and added with strikethrough decoration according to the unique specification:

- *filename* – Specifies that a [`FileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler) be created, using the specified filename, rather than a [`StreamHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.StreamHandler).
- *filemode* – If *filename* is specified, open the file in this [mode](https://docs.python.org/3/library/functions.html#filemodes). Defaults to `'a'`.
- *format* – Use the specified format string for the handler. Defaults to attributes `levelname`, `name` and `message` separated by colons.
- *datefmt* – Use the specified date/time format, as accepted by [`time.strftime()`](https://docs.python.org/3/library/time.html#time.strftime).
- *style* – If *format* is specified, use this style for the format string. One of `'%'`, `'{'` or `'$'` for [printf-style](https://docs.python.org/3/library/stdtypes.html#old-string-formatting), [`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format) or [`string.Template`](https://docs.python.org/3/library/string.html#string.Template) respectively. Defaults to `'%'`.
- *level* – Set the ~~root~~ logger level to the specified [level](https://docs.python.org/3/library/logging.html#levels).
- *stream* – Use the specified stream to initialize the [`StreamHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.StreamHandler). Note that this argument is incompatible with *filename* - if both are present, a `ValueError` is raised.
- *handlers* – If specified, this should be an iterable of already created handlers to add to the ~~root~~ logger. Any handlers which don’t already have a formatter set will be assigned the default formatter created in this function. Note that this argument is incompatible with *filename* or *stream* - if both are present, a `ValueError` is raised.
- ~~*force* – If this keyword argument is specified as true, any existing handlers attached to the root logger are removed and closed, before carrying out the configuration as specified by the other arguments.~~
- *encoding* – If this keyword argument is specified along with *filename*, its value is used when the [`FileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler) is created, and thus used when opening the output file.
- *errors* – If this keyword argument is specified along with *filename*, its value is used when the [`FileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler) is created, and thus used when opening the output file. If not specified, the value ‘backslashreplace’ is used. Note that if `None` is specified, it will be passed as such to [`open()`](https://docs.python.org/3/library/functions.html#open), which means that it will be treated the same as passing ‘errors’.

Also, the `iilog.formatters.Formatter`, `iilog.filters.Filter`, `iilog.handlers.FileHandler`, `iilog.handlers.StreamHandler` classes and so on, which you should use when specifying *handlers*, are exactly the same as defined in the [`logging`](https://docs.python.org/3/library/logging.html) library.
</details>

<br>

## Example for loading a configuration file

config.yml:
```YAML
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
loggers:
  foobarExample:
    level: DEBUG
    handlers: 
      - console
    propagate: no
```

sample2.py:
```python
import iilog
iilog.env.set_config(filename='config.yml', encoding='UTF-8')
logger = iilog.env.get_logger('foobarExample')
logger.info('I told you so')
```

The results are as follows:
```shell
$ python test.py
2023-07-01 02:03:04,005 - foobarExample - INFO - I told you so

```

<details>
<summary>For more details</summary>

Takes the logging configuration from a file or dictionary. The parameters are as follows:

- *filename* – Use the specified filename to read the logging configuration from the file.
- *fileformat* – If *filename* is specified, read it as a file written in this format. Accepts either `'yaml'` or `'json'`. If not specified, it will be determined based on *filename*'s extension.
- *encoding* – If this keyword argument is specified along with *filename*, its value is used when opening the file.
- *config* – Takes the logging configuration from the specified dictionary, as accepted by the [`logging.config`](https://docs.python.org/3/library/logging.config.html) module's [`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig). Note that this argument is incompatible with *filename* or *config* - if both are present, a `ValueError` is raised.

</details>

<br>

For any grammar or examples not listed here, please refer to the documentation (sorry, currently under construction).

<br>

# License

This software is released under the MIT License, see LICENSE.
