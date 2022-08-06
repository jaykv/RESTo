from setuptools import find_packages, setup
from resto import __VERSION__

setup(
    name='resto',
    version=__VERSION__,
    description='REST API framework for the lazy',
    packages=find_packages(include=['resto', 'resto.*']),
    install_requires=[
        "pydantic >= 1.9.1",
        "spectree >= 0.10.0"
    ],
)
