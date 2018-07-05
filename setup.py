#!/usr/bin/env python

from distutils.core import setup
import sys

if sys.version_info[0] == 2:
    from commands import getoutput
elif sys.version_info[0] == 3:
    from subprocess import getoutput


setup(
    name='unifi',
    version='1.0.0',
    description='API Ubiquity UniFi Controller',
    author='Felipe Barros',
    author_email='felipe.barros@gmail.com',
    url='https://github.com/fgbs/unifi',
    packages=['unifi'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Networking'
    ]
)