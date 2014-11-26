import os
import poll_server
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        poll_server.app.config['TESTING'] = True
        self.app = poll_server.app.test_client()

    def tearDown(self):
        pass

    def test_test_page_exists(self):
        response = self.app.get('/cors_test')
        assert 'cors response' in response.data

    def test_cors_header(self):
        response = self.app.get('/cors_test', headers=dict(Origin='localhost'))
        print response.headers
        assert 'Access-Control-Allow-Origin' in response.headers

if __name__ == '__main__':
    unittest.main()
