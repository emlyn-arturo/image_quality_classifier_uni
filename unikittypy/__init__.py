import os
import random

from werkzeug.exceptions import NotFound, BadRequest

from image_preprocessing import ImagePreprocessing, ImageData
from neural_network import Network
from database import Database
from sklearn.externals import joblib


class UnikittyPy:
    database = None
    network = None

    def __init__(self, net_fitted):
        self.database = Database()
        if net_fitted:
            self.network = joblib.load(
                os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'fitted_network_IDS6.pkl'))
        else:
            self.network = Network()

    def run(self, file):
        """
        Runs the evaluation of an input image file
        :param file: Raw input image.
        :type file: ImageData
        :return: Result of evaluation
        """
        if not isinstance(file, ImageData):
            file = ImageData(file=file)
        processed_image = self.process_image(file)
        return self.network.evaluate(processed_image).network_result

    def process_image(self, file):
        """
        Runs the preprocessing of an input image file
        :param file: Raw input image.
        :return: Result of preprocessing
        """
        processed_image = ImagePreprocessing(file).feature_extract()
        return processed_image

    @staticmethod
    def shuffle_array(list):
        """
        :param list: List which items should be shuffled.
        :param list: Shuffled list
        :return:
        """
        random.shuffle(list)
        return list

    def shuffle_list(self, list):
        """
        Alias for shuffle_array.
        :param list: List which items should be shuffled.
        :return: Shuffled list.
        """
        return self.shuffle_array(list)

    def train(self, train_data_slice=0.7):
        """
        Loads all training data and starts network training.
        :return: Result of network learning success rate.
        """
        all_training_data = self.database.get_images()
        shuffled_data = self.shuffle_array(all_training_data)
        if train_data_slice < 1.0:
            upper_bound = int(train_data_slice * len(shuffled_data))
        else:
            upper_bound = train_data_slice
        for i in range(0, upper_bound):
            if isinstance(shuffled_data[i], ImageData):
                shuffled_data[i] = self.process_image(shuffled_data[i])
            else:
                raise IOError("Expected ImageData.")
        result = self.network.train(shuffled_data[:upper_bound])
        return result

    def register_feedback(self, file, path, feedback):
        """
        Registers feedback and saves it to the database
        :param file: The former input file for labelling target.
        :param feedback: Feedback from the user
        :type file: file
        :type feedback: bool
        :return: Status of database action.
        """
        if not file:
            raise NotFound("No file uploaded.")
        import web
        allowed = web.allowed_file(file.name)
        if not allowed:
            raise BadRequest("File type not allowed: " + str(allowed))
        return self.database.feedback(file, path, feedback)
