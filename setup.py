#!/usr/bin/env python
""" TO DO"""
import os
from setuptools import setup
import metrics

REQUIREMENTS = [
    line.strip() for line in open(os.path.join(os.path.dirname(__file__),
                                               'requirements.txt')).readlines()]

version = {}
with open("metrics/metric/version.py") as fp:
    exec(fp.read(), version)


setup(
    name='metric',
    version=version['__version__'],
    packages=['crypto', 'crypto.actor', 'crypto.domain', 'crypto.rest', 'crypto.rest.cryptocompare', 'crypto.db', 'crypto.util', 'crypto.stub'],
    description='CryptoAlgo python implementation',
    author='Marcin Gorzynski',
    license='MIT',
    author_email='marcin.gorzynski@gmail.com',
    install_requires=REQUIREMENTS,
    include_package_data=True,
    keywords='cryptoalgo exchange rest api bitcoin ethereum btc eth',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
