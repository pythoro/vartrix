# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 15:02:12 2019

@author: Reuben
"""

import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="vartrix",
    version="0.0.9",
    author="Reuben Rusk",
    description="Easily manange and automate variables and parameters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pythoro/vartrix.git",
    project_urls={
        'Documentation': 'https://vartrix.readthedocs.io/en/latest/',
        'Source': 'https://github.com/pythoro/vartrix.git',
        'Tracker': 'https://github.com/pythoro/vartrix/issues',
    },
    download_url="https://github.com/pythoro/vartrix/archive/v0.0.9.zip",
    packages=['vartrix'],
    keywords=['PARAMETERS', 'VARIABLES', 'PARAMETRIC', 'AUTOMATION', 'AUTOMATE'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[],
)