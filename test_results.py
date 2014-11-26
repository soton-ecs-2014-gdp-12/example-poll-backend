import poll_server
import unittest
import json
import uuid
import time


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        poll_server.app.config['TESTING'] = True
        self.app = poll_server.app.test_client()

    def tearDown(self):
        pass

    def test_get_results(self):
        random_id = uuid.uuid4().hex
        cur_time = int(time.time())
        poll_response = self.app.post('/vote', data=json.dumps(dict(questionResult=cur_time, annotation=random_id,  result=cur_time)))
        result_response = self.app.get('/results/' + random_id + '/' + str(cur_time))
        json_response = json.loads(result_response.data)

        self.assertTrue(str(cur_time) in json_response)
        self.assertEqual(json_response[str(cur_time)], 1)

    def test_get_multiple_results(self):
        random_id = uuid.uuid4().hex
        cur_time = int(time.time())
        poll_response = self.app.post('/vote', data=json.dumps(dict(questionResult=cur_time, annotation=random_id,  result=[cur_time, cur_time - 1, cur_time - 2])))
        result_response = self.app.get('/results/' + random_id + '/' + str(cur_time))
        json_response = json.loads(result_response.data)

        self.assertTrue(str(cur_time) in json_response)
        self.assertEqual(json_response[str(cur_time)], 1)
        self.assertTrue(str(cur_time - 1) in json_response)
        self.assertEqual(json_response[str(cur_time - 1)], 1)
        self.assertTrue(str(cur_time - 2) in json_response)
        self.assertEqual(json_response[str(cur_time - 2)], 1)


if __name__ == '__main__':
    unittest.main()
