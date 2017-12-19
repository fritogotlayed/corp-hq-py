#!/usr/bin/env python
"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = [
    str(ir.req)
    for ir in parse_requirements('requirements.txt', session=PipSession())
]

setup(
    name='Corp-HQ-job-runner',
    author='fritogotlayed',
    description='',
    url='https://github.com/fritogotlayed/corp-hq/job-runner',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    package_data={'runner': ['config.yml']},
    package_dir={'runner': 'runner'},
    install_requires=install_reqs,
    entry_points={
        'console_scripts':
        ['corp-hq-api-server = developer:build_and_start_server']
    })