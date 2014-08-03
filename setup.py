#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = ["httpretty==0.8.3",
                    "requests==2.2.0",
                    "dropbox==2.1.0",
                    "django==1.6.1"]

import sys

setup(
    name='dropboxmock',
    version='0.0.1',
    description='dropboxmock is a simple library '
    'that allow you to mock dropbox library '
    'in your code',
    author='Elastic Coders - Davide Scatto',
    author_email='davidescatto@gmail.com',
    url='https://github.com/elastic-coders/dropboxmock.git',
    packages=find_packages(),
    install_requires=install_requires,
)
