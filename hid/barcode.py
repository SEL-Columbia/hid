
import os
import tempfile
import StringIO
import base64
import uuid

from elaphe import barcode
from django.conf import settings

''' IDs & QRCode for them

    IDs are URL containing three parameter:
        - base_url (the namespace, defined in settings.IDGEN_BASE_URI)
        - uid, a random uuid hexadecimal
        - sid, a short representation of the UUID (collision possible)
    Format of the ID (URL) is defined in settings.IDGEN_FORMAT.
    Defaults: %(base_url)s/teachers/%(uuid)s?short=%(shortid)s

    QRCodes are generated from the full ID. '''


def generate_qrcodefile(message, filename=None):
    ''' Generate a QRCode Image into a file, defaulting to a tempfile '''

    if not filename:
        fileh, filename = tempfile.mkstemp(suffix='.png')
        os.close(fileh)

    code = generate_qrcode(message, stream=filename)

    return code


def generate_qrcode(message, stream=None,
                    eclevel='M', margin=10,
                    data_mode='8bits', format='PNG', scale=1.0):
    ''' Generate a QRCode, settings options and output '''

    if stream is None:
        stream = StringIO.StringIO()

    img = barcode('qrcode', message,
                  options=dict(version=9, eclevel=eclevel),
                  margin=margin, data_mode=data_mode, scale=scale)

    if isinstance(stream, basestring):
        for ext in ('jpg', 'png', 'gif', 'bmp', 'xcf', 'pdf'):
            if stream.lower().endswith('.%s' % ext):
                img.save(stream)
                return stream

    img.save(stream, format)

    return stream


def b64_random_qrcode(as_tuple=False, as_url=False):
    ''' base64 encoded PNG image representing a QRCode of a random ID '''

    if as_url:
        qr_id, uid, sid = get_random_urlid(as_tuple=True)
    else:
        qr_id = get_random_id()
        sid = short_id_from(qr_id)
    b64_data = b64_qrcode(qr_id)

    if as_tuple:
        return (qr_id, b64_data, sid)

    return b64_data


def b64_qrcode(urlid, scale=1.0):
    ''' base64 encoded PNG image representing urlid '''
    return base64.b64encode(generate_qrcode(urlid, scale=scale).getvalue())
