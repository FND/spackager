#!/usr/bin/env python

"""
single-page app compiler

parses an HTML file for external resources (JavaScript, CSS and image files) and
assembles them into a stand-alone document

Usage:
  spa.py [options] <filename>

Options:
  -l, --no-legacy
    Drop support for legacy browsers (namely Internet Explorer <8).
    This significantly reduces file size by not duplicating image data, and
    also prevents breaking validity by not adding MHTML-specific data before
    the doctyle declaration.
"""

import sys
import os

from urllib2 import urlopen
from base64 import b64encode

from pyquery import PyQuery as pq


def main(args):
    args = [unicode(arg, 'utf-8') for arg in args]
    filename = args[1]

    # XXX: hacky?
    if os.sep in filename:
        cwd = os.path.dirname(filename)
        os.chdir(cwd)
        filename = os.path.basename(filename)

    original = _readfile(filename)
    doc = pq(original)

    doc.find('script').each(convert_script)
    doc.find('link[rel=stylesheet]').each(convert_stylesheet)
    doc.find('img').each(convert_image)

    filename = filename.replace('.html', '.spa.html')
    html = doc.__html__() # using __html__ rather than html method to avoid escaping -- XXX: ?
    f = open(filename, 'w')
    f.write(html)
    f.close()

    return True


def convert_script(node):
    node = pq(node)
    uri = node.attr('src')
    if uri:
        print 'converting', uri
        src = '/*<![CDATA[*/\n%s\n/*]]>*/' % _get_uri(uri)
        node.attr('src', None).text(src) # TODO: delete src attribute altogether?


def convert_stylesheet(node):
    node = pq(node)
    uri = node.attr('href')
    if uri:
        print 'converting', uri
        css = '<style>/*<![CDATA[*/\n%s\n/*]]>*/</style>' % _get_uri(uri) # TODO: XHTML/HTML4 compatibility
        pq(css).insertBefore(node)
        node.remove()


def convert_image(node):
    node = pq(node)
    uri = node.attr('src')
    if uri:
        print 'converting', uri
        img = _get_uri(uri, binary=True)
        ext = uri.rsplit('.', 1)[1]
        data = 'data:image/%s;base64,%s' % (ext, b64encode(img))
        node.attr('src', data)


def _get_uri(uri, binary=False):
    if uri.startswith('http://') or uri.startswith('https://'): # XXX: ignore HTTPS?
        return urlopen(uri).read()
    else:
        filepath = os.sep.join(uri.split('/'))
        return _readfile(filepath, binary)


def _readfile(filepath, binary=False):
    mode = 'rb' if binary else 'r'
    f = open(filepath, mode)
    content = f.read()
    f.close()
    return content


if __name__ == '__main__':
    status = not main(sys.argv)
    sys.exit(status)
