import poll_server
import unittest
import json
import time

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        poll_server.app.config['TESTING'] = True
        self.app = poll_server.app.test_client()

    def tearDown(self):
        pass

    def test_empty_vote(self):
        response = self.app.post('/vote')
        self.assertEqual(response.status_code, 400)

    def test_empty_dict_vote(self):
        response = self.app.post('/vote', data=json.dumps(dict()))
        self.assertEqual(response.status_code, 400)

    def test_missing_question_result_vote(self):
        response = self.app.post('/vote', data=json.dumps(dict(annotation='yes', result='yes')))
        self.assertEqual(response.status_code, 400)

    def test_missing_result_vote(self):
        response = self.app.post('/vote', data=json.dumps(dict(questionResult='yes', result='yes')))
        self.assertEqual(response.status_code, 400)

    def test_missing_annotation_vote(self):
        response = self.app.post('/vote', data=json.dumps(dict(questionResult='yes', annotation='yes')))
        self.assertEqual(response.status_code, 400)

    def test_valid_vote(self):
        response = self.app.post('/vote', data=json.dumps(dict(questionResult='yes', annotation='yes',  result='yes')))
        self.assertEqual(response.status_code, 200)

    def test_valid_vote(self):
        response = self.app.post('/vote', data=json.dumps(dict(questionResult='yes', annotation='yes',  result='yes')))
        self.assertEqual(response.status_code, 200)

    def test_valid_vote_data_not_in_db_already(self):
        cur_time = int(time.time())
        response = self.app.post('/vote', data=json.dumps(dict(questionResult=cur_time, annotation=cur_time,  result=cur_time)))
        self.assertEqual(response.status_code, 200)

    def test_valid_vote_data_in_db_already(self):
        cur_time = int(time.time())
        response = self.app.post('/vote', data=json.dumps(dict(questionResult=cur_time, annotation=cur_time,  result=cur_time)))
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/vote', data=json.dumps(dict(questionResult=cur_time, annotation=cur_time,  result=cur_time)))
        self.assertEqual(response.status_code, 200)

    def test_valid_vote_multiple(self):
        cur_time = int(time.time())
        response = self.app.post('/vote', data=json.dumps(dict(questionResult=cur_time, annotation=cur_time,  result=[cur_time, cur_time -1, cur_time - 2])))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
