#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

dynamic_requires = []

version = 1.3

setup(
    name='decora_wifi',
    version=1.3,
    author='Tim Lyakhovetskiy',
    author_email='tlyakhov@gmail.com',
    url='http://github.com/tlyakhov/python-decora_wifi',
    packages=find_packages(),
    scripts=[],
    description='Python API for controlling Leviton Decora Smart WiFi switches',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=['requests', 'inflect'],
    include_package_data=True,
    zip_safe=False,
)
