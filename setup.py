#!/usr/bin/env python
import os
import sys
import io

from setuptools import setup, find_packages


requires = [
    'jmespath>=0.4.1,<=1.0.0',
    'Pygments>=1.6,<=2.0',
    'urwid==1.2.2'
]


setup(
    name='jmespath-terminal',
    version='0.1.0',
    description='JMESPath Terminal',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    author='James Saryerwinnie',
    author_email='js@jamesls.com',
    url='https://github.com/jmespath/jmespath.terminal',
    scripts=['bin/jpterm'],
    py_modules=['jpterm'],
    install_requires=requires,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ),
)
