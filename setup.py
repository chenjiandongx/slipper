#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

# RELEASE STEPS
# $ python setup.py bdist_wheel
# $ python twine upload dist/VX.Y.Z.whl
# $ git tag -a VX.Y.Z -m "release version VX.Y.Z"
# $ git push origin VX.Y.Z

NAME = "slipper"
VERSION = "0.4.1"
URL = "https://github.com/chenjiandongx/slipper"
AUTHOR = "chenjiandongx"
AUTHOR_EMAIL = "chenjiandongx@qq.com"
LICENSE = "MIT"
REQUIRES = ["aiohttp"]
MODULES = ["slipper"]
DESC = "Async HTTP Requests-like library based on Aiohttp"
PYTHON_REQUIRES = ">=3.5.3"
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Development Status :: 3 - Alpha",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Topic :: Internet :: WWW/HTTP",
    "Framework :: AsyncIO",
]

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    name=NAME,
    version=VERSION,
    license=LICENSE,
    install_requires=REQUIRES,
    url=URL,
    py_modules=MODULES,
    description=DESC,
    python_requires=PYTHON_REQUIRES,
    classifiers=CLASSIFIERS,
)
