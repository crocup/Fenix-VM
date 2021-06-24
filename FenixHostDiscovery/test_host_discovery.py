import unittest
import requests
from host_discovery import DistributionDB
import datetime


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

    def test_delete_misc_data(self):
        result = {
            "host": "10.10.10.10",
            "stats": "test",
            "runtime": "test"
        }
        self.assertEqual(DistributionDB(host="10.10.10.10").delete_misc_data(result=result), {"host": "10.10.10.10"})

    def test_delete_misc_data_not_data(self):
        result = {
            "stats": "test"
        }
        self.assertEqual(DistributionDB(host="10.10.10.10").delete_misc_data(result=result), {})

    def test_delete_misc_data_not_stats(self):
        self.assertEqual(DistributionDB(host="10.10.10.10").delete_misc_data(result={}), {})

    def test_edit_data_result(self):
        result = {
            "10.10.10.10": {
                "hostname": [],
                "macaddress": {
                    "mac": "test"
                }
            }
        }
        data = [{
            "host": "10.10.10.10",
            "hostname": [],
            "macaddress": {
                "mac": "test"
            },
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }]
        self.assertEqual(DistributionDB(host="10.10.10.10").edit_data_result(result=result), data)

    def test_edit_data_result_not_data(self):
        result = {
            "10.10.10.10": {
            }
        }
        data = [{
            "host": "10.10.10.10",
            "hostname": "",
            "macaddress": "",
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }]
        self.assertEqual(DistributionDB(host="10.10.10.10").edit_data_result(result=result), data)


if __name__ == '__main__':
    unittest.main()
