#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='unifi-api',
    version='1.0.2',
    author='Felipe Barros',
    author_email='felipe.barros@gmail.com',
    description='API Ubiquity UniFi Controller',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fgbs/unifi',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'requests-toolbelt'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Networking'
    ]
)