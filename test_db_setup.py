import os
import poll_server
import unittest
import shutil

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        poll_server.app.config['TESTING'] = True
        self.app = poll_server.app.test_client()

    def tearDown(self):
        pass

    def move_save_db_file(self):
        if os.path.exists(poll_server.db_name):
            shutil.move(poll_server.db_name, poll_server.db_name + ".bak")

    def move_save_db_file_back(self):
        if os.path.exists(poll_server.db_name + ".bak"):
            shutil.move(poll_server.db_name + ".bak", poll_server.db_name)

    def test_db_created(self):
        self.move_save_db_file()

        response = self.app.get('/setup')
        self.assertIn('db created', response.data)
        self.assertTrue(os.path.isfile(poll_server.db_name))

        os.remove(poll_server.db_name)
        self.move_save_db_file_back()


    def test_db_created_already(self):
        self.move_save_db_file()

        response = self.app.get('/setup')
        self.assertIn('db created', response.data)
        self.assertTrue(os.path.isfile(poll_server.db_name))

        response = self.app.get('/setup')
        self.assertIn('db already exists', response.data)
        self.assertTrue(os.path.isfile(poll_server.db_name))

        os.remove(poll_server.db_name)
        self.move_save_db_file_back()

if __name__ == '__main__':
    unittest.main()
