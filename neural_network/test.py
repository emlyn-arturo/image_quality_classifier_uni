""" Neural network testmodule

Tests for the Network class
"""
import os
import unittest
import random
from sklearn.externals import joblib

from image_preprocessing import ImageData, \
    IMAGE_DATA_SIZE
from neural_network import Network


class NeuralNetworkTest(unittest.TestCase):
    """ Neural network test

    test to ensure that the neural network work as wished
    """

    def test_evaluation_output(self):
        """
        Test for the output of the evaluation method from the neural network
        """

        # load the fitted network for evaluation
        network = joblib.load(os.path.join(os.path.dirname(__file__),
                                           'network_test_fit.pkl'))

        # what does this code?
        # Our fitted model uses no ImageProcess.entropy
        test_data = [0.5] * (IMAGE_DATA_SIZE - 1)
        test_data_obj = ImageData(data=test_data)

        # evaluates the network with a given object
        result = network.evaluate(test_data_obj)

        # the result of the evaluation should be 1
        self.assertEqual(result.network_result, 1)

    def test_train(self):
        """
        Test for the fitting function of the neural network
        """
        network = Network()

        # get training_data
        # all_training_data = database.get_images()

        # feature1 für IMAGE_DATA_SIZE=6
        feature1 = [
            [619.45769904237625, 17.0, 23.0, 10.0, 21.342992798766346,
             1227523],
            [9.0315458377137645, 12.0, 14.0, 5.0, 24.465762491463394, 1032850],
            [255.86475805066434, 11.0, 15.0, 7.0, 21.262116227338076, 1986071],
            [3.2307624319154358, 4.0, 5.0, 2.0, 23.23160914285489, 1842465],
            [838.19058539547007, 27.0, 38.0, 14.0, 25.29086712272825, 1724504],
            [5134.6823768549502, 44.0, 54.0, 22.0, 32.33841867809606, 1373847],
            [5341.0571008897332, 49.0, 62.0, 22.0, 54.90147965544296, 1590652],
            [18601.855627056808, 82.0, 106.0, 34.0, 111.1941778272843,
             1835792],
            [18814.013419186071, 84.0, 109.0, 35.0, 92.64333649976118,
             1267926],
            [2801.9413014780471, 36.0, 42.0, 20.0, 29.58324852722407, 1398340],
            [30.052843922102412, 4.0, 2.0, 3.0, 64.24290198487556, 1435682],
            [265.54499401294015, 11.0, 11.0, 9.0, 34.95460807776531, 1078238],
            [24.55965163387333, 3.0, 2.0, 3.0, 58.95401737264215, 1006358],
            [918.14050144668363, 24.0, 27.0, 17.0, 34.07711738991745, 1367485],
            [7.5258242024315694, 1.0, 0.0, 1.0, 28.890006893483015, 2005861]]

        # feature2 für Image_Data_Size=5
        feature2 = [
            [619.45769904237625, 17.0, 23.0, 10.0, 21.342992798766346],
            [9.0315458377137645, 12.0, 14.0, 5.0, 24.465762491463394],
            [255.86475805066434, 11.0, 15.0, 7.0, 21.262116227338076],
            [3.2307624319154358, 4.0, 5.0, 2.0, 23.23160914285489],
            [838.19058539547007, 27.0, 38.0, 14.0, 25.29086712272825],
            [5134.6823768549502, 44.0, 54.0, 22.0, 32.33841867809606],
            [5341.0571008897332, 49.0, 62.0, 22.0, 54.90147965544296],
            [18601.855627056808, 82.0, 106.0, 34.0, 111.1941778272843],
            [18814.013419186071, 84.0, 109.0, 35.0, 92.64333649976118],
            [2801.9413014780471, 36.0, 42.0, 20.0, 29.58324852722407],
            [30.052843922102412, 4.0, 2.0, 3.0, 64.24290198487556],
            [265.54499401294015, 11.0, 11.0, 9.0, 34.95460807776531],
            [24.55965163387333, 3.0, 2.0, 3.0, 58.95401737264215],
            [918.14050144668363, 24.0, 27.0, 17.0, 34.07711738991745],
            [7.5258242024315694, 1.0, 0.0, 1.0, 28.890006893483015]]

        i1 = ImageData()
        i2 = ImageData()
        i3 = ImageData()
        i4 = ImageData()
        i5 = ImageData()
        i6 = ImageData()
        i7 = ImageData()
        i8 = ImageData()
        i9 = ImageData()
        i10 = ImageData()
        i11 = ImageData()
        i12 = ImageData()
        i13 = ImageData()
        i14 = ImageData()
        i15 = ImageData()

        training_data = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12,
                         i13, i14, i15]

        for i, item in enumerate(training_data):
            item.data = feature1[i]
            item.label = int(bool(random.getrandbits(1)))

        # fits the model
        result = network.train(training_data)

        if (result == False):
            raise IOError("Fitting doesn't work")

        # save the network to a file
        joblib.dump(network, (os.path.join(os.path.dirname(__file__),
                                           'fitted_network_for_nosetest.pkl')))

        # tests if the file with the network exists
        path = os.path.join(os.path.dirname(__file__),
                            'fitted_network_for_nosetest.pkl')
        self.assertTrue(os.path.exists(path))
