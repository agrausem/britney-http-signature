# -*- coding: utf-8 -*-

"""
britney_http_signature
~~~~~~~~~~~~~~~~~~~~~~

Middlewares that bring several http signature authentication into britney spore client.
"""

from britney.middleware import ApiKey
from britney.middleware.base import add_header
from http_signature.sign import HeaderSigner


class HmacHttpSignature(ApiKey):
    """ Britney middleware that add to request an Authorization header containing an http signature,
    construct with an HMAC sign algorithm signature.
    """

    default_headers = ['Request-Line', 'Host', 'User-Agent', 'Date']

    def __init__(self, key_header, key_id, secret, hash_algorithm='sha256'):
        """
        :param key_header: the name of header containing the key id
        :param key_id: the key id
        :param secret: the secret shared with server
        :param hash_algorithm: a hash algorithm in sha1, sha256, sha512 (defaults to sha256)
        """
        super(HmacHttpSignature, self).__init__(key_header, key_id)
        headers = map(lambda h: h.lower(), self.default_headers + [self.key])
        algorithm = 'hmac-%s' % hash_algorithm
        self.header_signer = HeaderSigner(key_id=key_id, secret=secret, algorithm=algorithm,
                                          headers=headers)

    def process_request(self, environ):
        """
        :param environ: the environment of the request
        :type environ: dict
        """
        super(HmacHttpSignature, self).process_request(environ)
        signed_headers = self.header_signer.sign(environ.get('spore.headers'),
                                                 method=environ.get('REQUEST_METHOD'),
                                                 path=environ.get('PATH_INFO'))
        add_header(environ, 'Authorization', signed_headers['Authorization'])