# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='dress',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'dress',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
