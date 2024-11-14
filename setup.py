#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.

# Unauthorized copying of this file, via any medium is strictly prohibited,
# unless it was supplied under the terms of a license agreement or
# nondisclosure agreement with PAL Robotics SL. In this case it may not be
# copied or disclosed except in accordance with the terms of that agreement.

from pathlib import Path
from setuptools import find_packages, setup

import xml.etree.ElementTree as ET


def readme():
    with open('README.md') as f:
        return f.read()


NAME = "rpk"

# get the version from ROS' package.xml
DESCRIPTION = ET.parse("package.xml").find("description").text

TPLS = [
    ("share/%s/%s" % (NAME, t.parent), [str(t)])
    for t in Path("tpl").rglob("*")
    if t.is_file()
]

setup(
    name=NAME,
    version='4.2.0',
    description=DESCRIPTION,
    long_description=readme(),
    author="Séverin Lemaignan",
    author_email="severin.lemaignan@pal-robotics.com",
    license='Apache License 2.0',
    packages=find_packages(exclude=['test']),
    data_files=TPLS + [
        ('share/ament_index/resource_index/packages', ['resource/' + NAME]),
        ('share/' + NAME, ['package.xml'])
    ],
    install_requires=['setuptools', 'jinja2'],
    zip_safe=True,
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "rpk = " + NAME + ".rpk:main"
        ],
    },
)
