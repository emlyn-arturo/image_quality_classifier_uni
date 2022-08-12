import os
import unittest

from PIL import Image
from image_preprocessing import ImagePreprocessing, ImageData


class ImageProcessTest(unittest.TestCase):
    def setUp(self):
        # self.image_processing = ImagePreprocessing('JPEG1.jpeg')
        pass

    def test_inputfile(self):
        """ throw error if input-file is wrong (jpg)"""
        file = Image.open(os.path.join(os.path.dirname(__file__),
                                       "JPEG1.jpeg"))
        imdata = ImageData(file=file)
        image_processing = ImagePreprocessing(imdata)
        self.assertIsInstance(image_processing.image, ImageData)

    def test_output_vector(self):
        """ throw error if any output-value is smaller than zero (jpg)"""
        with Image.open(os.path.join(os.path.dirname(__file__),
                                     "JPEG1.jpeg")) as file:
            imdata = ImageData(file=file)
            features = ImagePreprocessing(imdata)
            for feature in features.feature_extract().data:
                self.assertGreaterEqual(feature, 0)


"""
hab es rauskommentiert, wir können keine PNGs bearbeiten
da es Probleme gibt PNG's aufzuteilen.
JPEGS spannen den RGB Raum auf, PNGS für
grayscale sind anders, Farben sind RGBA

    def test_inputfile_png(self):
        # throw error if input-file is wrong (png)
        file = Image.open(os.path.join(os.path.dirname(__file__),
                                       "PNG1.png"))
        imdata = ImageData(file=file)
        image_processing = ImagePreprocessing(imdata)
        self.assertIsInstance(image_processing.image, ImageData)

    def test_output_vector_png(self):
        # throw error if any output-value is smaller than zero (png)
        with Image.open(os.path.join(os.path.dirname(__file__),
                                     "PNG1.png")) as file:
            imdata = ImageData(file=file)
            features = ImagePreprocessing(imdata)
            for feature in features.feature_extract().data:
                self.assertGreaterEqual(feature, 0)

"""

if __name__ == '__main__':
    unittest.main()
