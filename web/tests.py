import os
import unittest

from flask import json

from web import app
from werkzeug.datastructures import FileStorage
from mock import patch

ALLOWED_EXTENSIONS = ('jpeg', 'jpg', 'gif', 'png')


class ApiTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['UPLOAD_FOLDER'] = \
            os.path.join(os.path.dirname(__file__), 'test_uploads')

        try:
            os.stat(app.config['UPLOAD_FOLDER'])
        except:
            os.mkdir(app.config['UPLOAD_FOLDER'])

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER'],
                                         topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(app.config['UPLOAD_FOLDER'])

    @staticmethod
    def get_headers():
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @patch("unikittypy.UnikittyPy.train")
    def test_train_triggering(self, unikikitty_train):
        unikikitty_train.return_value = 0.4
        headers = self.get_headers()
        response = self.app.get("/api/train",
                                headers=headers,
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertIn("result", json_response)

    def test_allowed_filetypes(self):
        import web
        self.assertIsNone(web.allowed_file('bladatei'))
        self.assertEqual(web.allowed_file('bladatei.bla'), 'bla')
        self.assertIs(web.allowed_file('bladatei.png'), True)

    @patch('unikittypy.UnikittyPy.run')
    def test_image_upload(self, unikitty_run):
        headers = self.get_headers()
        unikitty_run.return_value = 0.5
        with open(os.path.join(os.path.dirname(__file__),
                               "1351470314823095095.jpg"), 'rb') as fp:
            file = FileStorage(fp)
            response = self.app.post("/api/evaluate",
                                     data={"image": file},
                                     headers=headers,
                                     content_type="multipart/form-data",
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_image_upload_with_invalid_filetype(self):
        headers = self.get_headers()
        with open(os.path.join(os.path.dirname(__file__),
                               "test_image.exe"), 'rb') as fp:
            file = FileStorage(fp)
            response = self.app.post("/api/evaluate",
                                     data={"image": file},
                                     headers=headers,
                                     content_type="multipart/form-data",
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 400)

    def test_image_upload_with_invalid_file(self):
        headers = self.get_headers()
        response = self.app.post("/api/evaluate",
                                 data={"image": "blakeks"},
                                 headers=headers,
                                 content_type="multipart/form-data",
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_image_upload_with_missing_file(self):
        headers = self.get_headers()
        response = self.app.post("/api/evaluate",
                                 data={"blakeks": "nusskuchen"},
                                 headers=headers,
                                 content_type="multipart/form-data",
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
