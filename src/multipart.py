
from httplib import HTTP
from base64 import b64encode
from mimetypes import guess_type


# Original Source from <http://code.activestate.com/recipes/146306/>
# Adapted to support basic authentication


def post_multipart(host, selector, fields=[], files=[], basicAuth=None):
    """
    Post fields and files to an HTTP host as 'multipart/form-data'.
    `fields` is a sequence of (name, value) elements for regular form fields.
    `files` is a sequence of (name, filename, value) elements for data to be uploaded as files.
    Return the server's response page.
    """
    try:
        content_type, body = encode_multipart_formdata(fields, files)
        h = HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('Host', host)

        if basicAuth:
            # `basicAuth` should be a tuple (username, password)
            h.putheader('Authorization', 'Basic ' + b64encode('%s:%s' % basicAuth))

        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)

        errcode, errmsg, headers = h.getreply()

        return h.file.read()

    except:
        return None


def encode_multipart_formdata(fields, files):
    """
    `fields` is a sequence of (name, value) elements for regular form fields.
    `files` is a sequence of (name, filename, value) elements for data to be uploaded as files.
    Return (content_type, body) ready for `httplib.HTTP` instance
    """
    CRLF = '\r\n'
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    L = []

    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name=\"' + key + '\"')
        L.append('')
        L.append(value)

    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name=\"' + key + '\"; filename=\"' + filename + '\"')
        L.append('Content-Type: ' + guess_type(filename)[0] or 'application/octet-stream')
        L.append('')
        L.append(value)

    L.append('--' + BOUNDARY + '--')
    L.append('')

    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=' + BOUNDARY

    return content_type, body
