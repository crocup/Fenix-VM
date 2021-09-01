import unittest
import requests


class TestWeb(unittest.TestCase):

    def test_index_page(self):
        response = requests.get('http://192.168.1.111:8000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.headers, {'User-Agent': 'python-requests/2.26.0',
                                                    'Accept-Encoding':'gzip, deflate',
                                                    'Accept': '*/*', 'Connection': 'keep-alive'})
