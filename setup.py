# -*- coding: UTF-8 -*-

import setuptools
from distutils.core import setup

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='summarify/__init__.py'
verstrline = open(VERSIONFILE, 'rt').read()
VSRE = r'^__version__\s+=\s+[\'"]([^\'"]+)[\'"]'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)

setup(
    name='summarify',
    version=verstr,
    author='Baptiste Fontaine',
    author_email='b@ptistefontaine.fr',
    packages=['summarify'],
    url='https://github.com/bfontaine/summarify',
    license=open('LICENSE', 'r').read(),
    description='Get title and description from a Web page',
    long_description="""\
Summarify takes a URL and parses its HTML to give you a title and description,
but also a picture URL, and a couple other attributes to summarize the page.
""",
    long_description_content_type='text/markdown',
    install_requires=[
        'beautifulsoup4>=4.6.0',
        'requests>=2.18.4',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)
