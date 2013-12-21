#!/usr/bin/python

from setuptools import setup

with open('README.rst') as fd:
    readme = fd.read()

with open('requirements.txt') as fd:
    requirements = fd.readlines()
    install_requires = [line for line in requirements if not line.startswith('#')]

with open('requirements-testing.txt') as fd:
    test_reqs = fd.readlines()
    tests_require = [line for line in test_reqs if not line.startswith('#')]

setup(
    name = 'email-utils',
    version = '0.1',
    description = 'Email Utils',
    long_description = readme,
    author = 'Serge Domkowski',
    author_email = 'sergedomk@gmail.com',
    include_package_data = True,
    install_requires = install_requires,
    tests_require = tests_require,
    platforms = ['any'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
)
