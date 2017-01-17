#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io

import setuptools

with io.open('README.md', encoding='utf-8') as readme:
    long_description = readme.read()

name = 'x2dhf.py'
description = 'A module wrapper for x2dhf fortran code'

setup_params = dict(
    name=name,
    version='v0.1.0',
    author="Lukasz Mentel",
    author_email="lmmentel@gmail.com",
    description=description or name,
    long_description=long_description,
    url="https://github.com/lmmentel/x2dhf" + name,
    py_modules=['x2dhf'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    entry_points={
        'console_scripts': [
            'xhf.py = x2dhf:xhf',
        ]
    },
)


if __name__ == '__main__':
    setuptools.setup(**setup_params)
