#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    lines = requirements.readlines()
    libraries = [lib for lib in lines if not lib.startswith('-')]
    dependency_links = [link.split()[1] for link in lines if 
            link.startswith('-f')]

setup(
    name='britney-http-signature',
    version='0.1',
    author='Arnaud Grausem',
    author_email='arnaud.grausem@gmail.com',
    maintainer='Arnaud Grausem',
    maintainer_email='arnaud.grausem@gmail.com',
    url='https://github.com/agrausem/britney-http-signature',
    license='PSF',
    description='Http Signature authenticatio middleware for britney',
    long_description=long_description,
    py_modules=['britney_http_signature'],
    download_url='http://pypi.python.org/pypi/britney-http-signature',
    install_requires=libraries,
    dependency_links=dependency_links,
    keywords=['SPORE', 'REST Api', 'authentication', 'britney', 'http signature'],
    entry_points={
        'britney.plugins.middleware': [
            'HmacHttpSignature = britney_http_signature:HmacHttpSignature'
        ]
    },
    classifiers = (
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    )
)
