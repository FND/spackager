#!/usr/bin/env python

import os

from urllib2 import urlopen
from base64 import b64encode

from pyquery import PyQuery as pq

from spackager.mhtml import generate_mhtml


def compile(filename, legacy_mode=False):
    original = _readfile(filename)
    doc = pq(original)

    doc.find('script').each(convert_script)
    doc.find('link[rel=stylesheet]').each(convert_stylesheet)
    doc.find('img').each(convert_image)
    html = doc.__html__() # __html__ method avoids escaping -- TODO: retain doctype

    if legacy_mode:
        mhtml = generate_mhtml(doc) # XXX: rename variable
        html = '%s%s' % (mhtml, html) # TODO: MHTML data can also be appended after HTML (retaining validity)!?

    filename = filename.replace('.html', '.spa.html') # TODO: configurable
    f = open(filename, 'w')
    f.write(html)
    f.close()


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
        uri = 'data:image/%s;base64,%s' % (ext, b64encode(img))
        node.attr('src', uri)


def _get_uri(uri, binary=False):
    if uri.startswith('http://') or uri.startswith('https://'): # XXX: ignore HTTPS?
        return urlopen(uri).read() # TODO: should be optional
    else:
        filepath = os.sep.join(uri.split('/'))
        return _readfile(filepath, binary)


def _readfile(filepath, binary=False):
    mode = 'rb' if binary else 'r'
    f = open(filepath, mode)
    content = f.read()
    f.close()
    return content
