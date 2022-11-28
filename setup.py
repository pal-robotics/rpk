#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from distutils.core import setup


def readme():
    with open("README.md") as f:
        return f.read()


NAME = "pal_create_app"

TPLS = [
    ("share/%s/%s" % (NAME, t.parent), [str(t)])
    for t in Path("tpl").rglob("*")
    if t.is_file()
]

setup(
    name=NAME,
    version="0.1.0",
    license="Proprietary",
    description="A tool to create application controller skeletons for interactive robots",
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    requires=["jinja2"],
    author="Séverin Lemaignan",
    author_email="severin.lemaignan@pal-robotics.com",
    scripts=["scripts/pal_create_app"],
    data_files=TPLS,
)
