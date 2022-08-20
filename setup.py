from setuptools import find_packages, setup

from resto import __VERSION__

setup(
    name='resto',
    version=__VERSION__,
    description='REST API framework for the lazy',
    author='Jay',
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha', 'License :: OSI Approved :: MIT License'],
    packages=find_packages(include=['resto', 'resto.*']),
    python_requires='>=3.9',
    install_requires=['pydantic >= 1.9.1', 'spectree >= 0.10.0'],
    extras_require={'testing': ['flask', 'mongoframes', 'pymongo']},
)
