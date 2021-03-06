#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# setup.py
# Description: zipwatch setup file
# -----------------------------------------------------------------------------
#
# Login   <carlos.linares@uc3m.es>
#

"""
zipwatch setup file
"""

import setuptools

# import the version file
import sys
sys.path.insert(1, 'zipwatch/')
import zwcversion

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zipwatch",
    version=zwcversion.__version__,
    author="Carlos Linares Lopez",
    author_email="carlos.linares@uc3m.es",
    description="examines the contents of zip files and triggers actions according to their contents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phovox/zipwatch",
    packages=setuptools.find_packages(),
    scripts = ['zipwatch/zipdog.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# Local Variables:
# mode:python
# fill-column:80
# End:
