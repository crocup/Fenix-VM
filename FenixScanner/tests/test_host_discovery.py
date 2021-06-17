import unittest
import requests


class TestHostDiscovery(unittest.TestCase):

    def test_read_root_none(self):
        response = requests.post('http://localhost:8000/api/v1/fenix/hostdiscovery', json={})
        assert response.status_code == 422

    def test_read_root_ok(self):
        response = requests.post('http://localhost:8000/api/v1/fenix/hostdiscovery', json={"host": "192.168.1.1"})
        assert response.status_code == 200

    def test_read_root_text(self):
        response = requests.post('http://localhost:8000/api/v1/fenix/hostdiscovery', json={"host": "text"})
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
