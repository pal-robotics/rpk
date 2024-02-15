#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2023 PAL Robotics S.L. All rights reserved.

# Unauthorized copying of this file, via any medium is strictly prohibited,
# unless it was supplied under the terms of a license agreement or
# nondisclosure agreement with PAL Robotics SL. In this case it may not be
# copied or disclosed except in accordance with the terms of that agreement.

from pathlib import Path
from setuptools import find_packages, setup

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
    license="Proprietary",
    packages=find_packages(exclude=['test']),
    data_files=TPLS + [
        ('share/ament_index/resource_index/packages', ['resource/' + NAME]),
        ('share/' + NAME, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "pal_app = " + NAME +".pal_app:main"
        ],
    },
)
