from uuid import uuid4 as uuid


SECTION_TEMPLATE = """/*
Content-Type: multipart/related; boundary="_EOT"

%s
*/
"""

BLOCK_TEMPLATE = """--_EOT
Content-Location:%s
Content-Transfer-Encoding:base64

%s
"""


def generate_mhtml(doc): # XXX: rename?
    """
    adds a unique class to base64-encoded images in a document (PyQuery object)
    returns a string of MHTML data
    """
    separator = ';base64,'
    mdata = []
    def augment(node): # XXX: rename
        uri = node.attr('src')
        if separator in uri:
            data = uri.split(separator)[1] # XXX: unsafe?
            data_id = 'mhtml_%s' % uuid().hex
            node.addClass(data_id)
            mdata.append(BLOCK_TEMPLATE % (data_id, data))
    doc.find('img').each(augment)
    return SECTION_TEMPLATE % ''.join(mdata)
