"""
Refer to this guide about writing a setup.py
https://docs.python.org/3/distutils/setupscript.html
"""

#!/usr/bin/env python

from distutils.core import setup

setup(
    name='package-name',
    version='1.0',
    description='Short Project/Package Description',
    author='Project Author(s)',
    author_email='project.author@email.com',
    url='BitBucket/GitHub repo URL',
    packages=['foo', 'foo.bar'],
    install_requires=[
        'foo.bar==2.20.0',
        'something.else==1.10.2'
    ]
)
