#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2023 PAL Robotics S.L. All rights reserved.

# Unauthorized copying of this file, via any medium is strictly prohibited,
# unless it was supplied under the terms of a license agreement or
# nondisclosure agreement with PAL Robotics SL. In this case it may not be
# copied or disclosed except in accordance with the terms of that agreement.

from pathlib import Path
from distutils.core import setup

import xml.etree.ElementTree as ET

NAME = "pal_app"

# get the version from ROS' package.xml
VERSION = ET.parse("package.xml").find("version").text
DESCRIPTION = ET.parse("package.xml").find("description").text

TPLS = [
    ("share/%s/%s" % (NAME, t.parent), [str(t)])
    for t in Path("tpl").rglob("*")
    if t.is_file()
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author="Séverin Lemaignan",
    author_email="severin.lemaignan@pal-robotics.com",
    license="PAL Robotics S.L.",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    requires=["jinja2"],
    scripts=["scripts/pal_app"],
    package_dir={"": "src"},
    packages=["pal_app"],
    data_files=TPLS + [("share/doc/pal_app", ["README.md"])],
)
