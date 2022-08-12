""" Neural network module

Network class for training and classifying image
features with Support Vector Machine principle
"""

import os
import numpy as np
from sklearn import svm
from sklearn.externals import joblib


class Network(object):
    """ Neural network for image classification

    Support Vector Machine based on scikit-learn module
    to classify extracted features from images
    """

    def __init__(self):
        """ Initializes object of C-Support Vector Classificator from
        scikit-learn module
        """
        self.support_vector_machine = svm.SVC()

    def train(self, training_dataset):
        """
        Trains the network by the use of the given training data set.
        :param training_dataset: Dataset used for training.
        This must be a list of ImageData objects.
        :type training_dataset: list(ImageData)
        :return: Success rate
        """
        if len(training_dataset) == 0:
            raise IOError("Training dataset empty.")

        # extract attributes from training_dataset object list
        feature_list = [o.data for o in training_dataset]
        label_list = [o.label for o in training_dataset]

        # train support vector machine
        self.support_vector_machine.fit(feature_list, label_list)

        # save the fitted model
        joblib.dump(self.support_vector_machine, (
            os.path.join(os.path.dirname(__file__), 'fitted_network.pkl')))

        return True

    def evaluate(self, image_data):
        """
        Evaluates support vector machine output on the given image data.
        :param image_data: ImageData object containing all relevant data
            for the network evaluation.
        :type image_data: ImageData
        :return: Raw network output.
        """

        # evaluate class of given features (image_date) through SVM
        features_np = np.array([image_data.data])
        classification = self.support_vector_machine.predict(features_np)
        # convert classification from numpy.ndarray to int
        image_data.network_result = np.asscalar(classification)
        return image_data
