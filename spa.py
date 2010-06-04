#!/usr/bin/env python

"""
single-page app compiler

parses an HTML file for external resources (JavaScript, CSS and image files) and
bakes them into a stand-alone document

Usage:
  spa.py [options] <filename>

Options:
  -l, --no-legacy
    Drop support for legacy browsers (namely Internet Explorer <8).
    This significantly reduced file sizes and prevents breaking validity.
"""

import sys
import os
import re

from urllib import urlopen
from base64 import b64encode


def main(args):
	args = [unicode(arg, "utf-8") for arg in args]
	filename = args[1]

	patterns = {
		"js": re.compile(r'<script[^>]*src=[\'"](.*?)[\'"][^>]*></script>'),
		"css": re.compile(r'<link[^>]*rel=[\'"]stylesheet[\'"][^>]*href="(.*?)[\'"][^>]*>'),
		"img": re.compile(r'<img[^>]*src=[\'"](.*?)[\'"][^>]*>')
	}
	original = _readfile(filename)

	references = []
	for type in patterns.keys():
		refs = patterns[type].findall(original)
		references.extend(refs)

	resources = {}
	for uri in references:
		if uri.startswith("http://") or uri.startswith("https://"): # XXX: ignore HTTPS?
			resources[uri] = urlopen(uri).read()
		else:
			filepath = os.sep.join(uri.split("/"))
			binary = not (uri.endswith(".js") or uri.endswith(".css")) # XXX: special-casing
			resources[uri] = _readfile(filepath, binary)

	spa = []
	for line in original.splitlines():
		for uri, src in resources.items():
			if uri in line:
				if uri.endswith(".js"):
					template = "<script>\n%s\n</script>"
				elif uri.endswith(".css"):
					template = "<style>\n%s\n</style>"
				else: # image
					ext = uri.rsplit(".", 1)[1]
					template = '<img src="data:image/%s;base64,%s">' % (ext, "%s")
					src = b64encode(src)
				line = template % src
		spa.append(line)

	filename = filename.replace(".html", ".spa.html")
	f = open(filename, "w")
	f.write("\n".join(spa))
	f.close()

	print "converted %s resources: %s" % (len(resources), filename)

	return True


def _readfile(filepath, binary=False):
	mode = "rb" if binary else "r"
	f = open(filepath, mode)
	content = f.read()
	f.close()
	return content


if __name__ == "__main__":
	status = not main(sys.argv)
	sys.exit(status)
