AUTHOR = 'FND'
AUTHOR_EMAIL = 'FNDo@gmx.net'
NAME = 'spackager'
DESCRIPTION = 'compiler for creating single-page applications'


import os

from setuptools import setup, find_packages

from spackager import __version__


try:
	long_desc = open(os.path.join(os.path.dirname(__file__), 'DESC')).read()
except IOError: # XXX: hacky way to avoid including DESC in distribution
	long_desc = None


setup(
    name = NAME,
    version = __version__,
    description = DESCRIPTION,
    long_description = long_desc,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = 'http://pypi.python.org/pypi/%s' % NAME,
    platforms = 'Posix; MacOS X; Windows',
    packages = find_packages(exclude=['test']),
    scripts = ['spac'],
    #package_data = { '': ['DESC'] },
    install_requires = ['pyquery'],
    #include_package_data = True,
    #zip_safe = False
)
