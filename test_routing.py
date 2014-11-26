import poll_server
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        poll_server.app.config['TESTING'] = True
        self.app = poll_server.app.test_client()

    def tearDown(self):
        pass

    def test_routing_maintest_page_exists(self):
        response = self.app.get('/')
        assert 'Hello World!' in response.data


if __name__ == '__main__':
    unittest.main()
