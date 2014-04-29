import unittest

from britney.utils import get_http_date, get_user_agent
from britney_http_signature import HmacHttpSignature
from Crypto.Hash import HMAC, SHA256
import base64
from six import b


class TestHmacHttpSignature(unittest.TestCase):

    def setUp(self):
        self.hmac_http_signature = HmacHttpSignature(key_id='my_key_id', key_header='X-Api-Key-Id',
                                                     secret='cdvbdfsibvqklscb')

    def test_instantiate(self):
        self.assertEqual(self.hmac_http_signature.key, 'X-Api-Key-Id')
        self.assertEqual(self.hmac_http_signature.value, 'my_key_id')
        signer_headers = sorted(self.hmac_http_signature.header_signer.headers)
        self.assertListEqual(signer_headers, ['date', 'host', 'request-line', 'user-agent',
                                              'x-api-key-id'])

    def test_signature(self):
        today = get_http_date()
        user_agent = get_user_agent()
        environ = {
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': 80,
            'PATH_INFO': '/users/89.json',
            'REQUEST_METHOD': 'PATCH',
            'spore.headers': {
                'Date': today,
                'Host': 'localhost:80',
                'User-Agent': user_agent,
                'X-Api-Key-Id': 'my_key_id'
            }
        }
        self.hmac_http_signature.process_request(environ)
        signature = environ.get('spore.headers').get('Authorization', '')
        introduction, _, signature = signature.partition(' ')
        exploded_sign = signature.split(',')

        to_sign = ['PATCH /users/89.json HTTP/1.1']
        to_sign.append('host: localhost:80')
        to_sign.append('user-agent: %s' % user_agent)
        to_sign.append('date: %s' % today)
        to_sign.append('x-api-key-id: my_key_id')
        to_sign = '\n'.join(to_sign)
        hmac = HMAC.new(b'cdvbdfsibvqklscb', digestmod=SHA256)
        hmac.update(b(to_sign))
        digest = hmac.digest()
        sign = base64.b64encode(digest)

        self.assertIn('keyId="my_key_id"', exploded_sign)
        self.assertIn('algorithm="hmac-sha256"', exploded_sign)
        headers = map(lambda h: h.lower(), HmacHttpSignature.default_headers + ['X-Api-Key-Id'])
        header_string = ' '.join(headers)
        self.assertIn('headers="%s"' % header_string, exploded_sign)
        self.assertIn('signature="%s"' % sign, exploded_sign)
