#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2022 PAL Robotics S.L. All rights reserved.

from pathlib import Path
from distutils.core import setup

NAME = "pal_app"

TPLS = [
    ("share/%s/%s" % (NAME, t.parent), [str(t)])
    for t in Path("tpl").rglob("*")
    if t.is_file()
]

setup(
    name=NAME,
    version="0.1.9",
    license="GPLv3",
    description="A tool to create application controller skeletons for interactive robots",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    requires=["jinja2"],
    author="Séverin Lemaignan",
    author_email="severin.lemaignan@pal-robotics.com",
    scripts=["scripts/pal_app"],
    package_dir={"": "src"},
    packages=["pal_app"],
    data_files=TPLS + [("share/doc/pal_app", ["README.md", "LICENSE"])],
)
