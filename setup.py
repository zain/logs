# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='logs',
    version='0.0.3',
    description='Logging for humans.',
    long_description=readme,
    author='Zain Memon',
    author_email='zain@inzain.net',
    url='https://github.com/zain/logs',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
