# Copyright (c) 2023 Kanta Yasuda (GitHub: @kyasuda516)
# This software is released under the MIT License, see LICENSE.

from setuptools import setup, find_packages
from iilog.__version__ import __version__

with open('README.md', encoding='utf-8') as f:
  readme = f.read()

setup(
  name="iilog-pckg",
  version=__version__,
  packages=find_packages(),
  description="iilog: alternative library to logging",
  long_description=readme,
  long_description_content_type='text/markdown',
  author="Kanta Yasuda",
  # author_email="",
  url="https://github.com/kyasuda516/iilog-pckg",
  download_url="https://github.com/kyasuda516/iilog-pckg",
  # project_urls = ,
  keywords=["iilog", "iilog-pckg", "logging", "logger", "log"],
  license="MIT license",
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Topic :: System :: Logging',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3 :: Only',
  ],
  install_requires=[
    "PyYAML>=6.0",
  ],
  # extras_require={},
  include_package_data=True,
  python_requires=">=3.8",
)
