"""
Spackager
single-page app compiler

parses an HTML file for external resources (JavaScript, CSS and image files) and
assembles them into a stand-alone document

http://github.com/FND/spackager
http://pypi.python.org/pypi/spackager

Usage:
  spac [options] <filename>

Options:
  -l, --no-legacy
    Drop support for legacy browsers (namely Internet Explorer <8).
    This significantly reduces file size by not duplicating image data, and
    also prevents breaking validity by not adding MHTML-specific data before
    the doctyle declaration.
"""

__version__ = '0.5.0'
