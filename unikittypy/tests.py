import os
import unittest

from PIL import Image
from sklearn.externals import joblib

from image_preprocessing import ImageData, IMAGE_DATA_SIZE
from unikittypy import UnikittyPy
from mock import patch


class UnikittyPyTests(unittest.TestCase):
    def setUp(self):
        if not os.path.isfile(os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'fitted_network_IDS6.pkl')):
            unikittypy = UnikittyPy(net_fitted=False)
            unikittypy.train()

    @patch('image_preprocessing.ImagePreprocessing.feature_extract')
    def test_run_return_value(self, process):
        self.unikittypy = UnikittyPy(net_fitted=True)
        self.unikittypy.network = joblib.load(
            os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'fitted_network_IDS6.pkl'))
        with Image.open(os.path.join(os.path.dirname(__file__),
                                     "1351470314823095095.jpg")) as file:
            process.return_value = ImageData(
                file=file, data=[0.5] * IMAGE_DATA_SIZE)
            result = self.unikittypy.run(ImageData(file=file))
            self.assertIn(result, (0, 1))

    @patch('image_preprocessing.ImagePreprocessing.feature_extract')
    def test_run_return_value_with_real_net(self, process):
        self.unikittypy = UnikittyPy(net_fitted=True)
        with Image.open(os.path.join(os.path.dirname(__file__),
                                     "1351470314823095095.jpg")) as file:
            process.return_value = ImageData(
                file=file, data=[0.5] * IMAGE_DATA_SIZE)
            result = self.unikittypy.run(ImageData(file=file))
            self.assertIn(result, (0, 1))

    def test_run_return_value_with_real_net_real(self):
        self.unikittypy = UnikittyPy(net_fitted=True)
        with Image.open(os.path.join(os.path.dirname(__file__),
                                     "1351470314823095095.jpg")) as file:
            result = self.unikittypy.run(file=file)
            self.assertIn(result, (0, 1))

    @patch('database.Database.feedback')
    def test_feedback_return_value(self, feedback):
        feedback.return_value = True
        self.unikittypy = UnikittyPy(net_fitted=False)
        path = os.path.join(os.path.dirname(__file__),
                            "1351470314823095095.jpg")
        with open(path, 'rb') as file:
            result = self.unikittypy.register_feedback(file, path, True)
            self.assertIs(True, result)

    def test_feedback_return_value_real(self):
        self.unikittypy = UnikittyPy(net_fitted=False)
        path = os.path.join(os.path.dirname(__file__),
                            "1351470314823095095.jpg")
        with open(path, 'rb') as file:
            result = self.unikittypy.register_feedback(file, path, True)
            self.assertIs(True, result)

    def test_train_return_value_real(self):
        self.unikittypy = UnikittyPy(net_fitted=False)
        result = self.unikittypy.train(5)
        self.assertIsInstance(result, bool)
        self.assertIs(result, True)

    def test_array_shuffling(self):
        self.unikittypy = UnikittyPy(net_fitted=False)
        former_array = [1, 2, 3, 4]
        array = [1, 2, 3, 4]
        array = self.unikittypy.shuffle_array(array)
        self.assertIsInstance(array, list)
        self.assertEqual(4, len(array))
        self.assertNotEqual(array, former_array)


if __name__ == "__main__":
    unittest.main()
