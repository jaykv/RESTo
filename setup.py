from setuptools import find_packages, setup

setup(
    name='RESTo',
    version='0.1.0',
    description='REST API framework for the lazy',
    packages=find_packages(include=['resto', 'resto.*']),
    install_requires=[]
)