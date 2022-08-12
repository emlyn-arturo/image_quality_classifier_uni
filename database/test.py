import unittest
import os
import json

from database import Database
from image_preprocessing import ImageData
from PIL import Image


class DatabaseTest(unittest.TestCase):
    def test_feedback(self):
        # Check if uploaded testfile was saved
        testimage = Image.open(
            os.path.join(os.path.dirname(__file__), 'images',
                         '98c12cda3bc801cbbc140b849418cd21.png'))
        self.assertTrue(testimage)

        # Check if correct label for testimage was saved
        with open(os.path.join(os.path.dirname(__file__), 'labels',
                               '98c12cda3bc801cbbc140b849418cd21.png.json')) \
                as label:
            testlabel = json.loads(label.read())
            self.assertEqual(testlabel, {'label': 234})

    def test_get_images(self):
        database = Database()
        images = database.get_images()

        self.assertIsInstance(images, list)
        self.assertGreater(len(images), 0)

        if isinstance(images, list) and isinstance(images[0], ImageData):
            self.assertIn(images[0].label, (0, 1))


if __name__ == '__main__':
    unittest.main()
