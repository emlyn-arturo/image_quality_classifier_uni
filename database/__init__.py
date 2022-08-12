import glob
import os
import hashlib

from flask import json
from PIL import Image
from shutil import copyfile


class Database:
    def feedback(self, file, path, feedback):

        file_type = ".%s" % path.rsplit(".", 1)[1]
        file_check = Image.open(path)
        filename = hashlib.md5(file_check.tobytes()).hexdigest()

        filename = filename + file_type

        with open(os.path.join(os.path.dirname(__file__), 'labels',
                               '%s.json' % filename), 'w') as f:
            json.dump({"label": feedback}, f)

        copyfile(path,
                 os.path.join(os.path.dirname(__file__), 'images', filename))
        return True

    def get_images(self, debug=False):
        from image_preprocessing import ImageData
        dataset = []
        for file in glob.glob(os.path.join(os.path.dirname(__file__),
                                           "images/*")):
            filename = os.path.basename(file)
            if not os.path.isfile(file):
                continue
            im = Image.open(file)
            with open(os.path.join(os.path.dirname(__file__), "labels",
                                   filename + ".json"), "r") as label_file:
                file_content = label_file.read()
                if debug:
                    print(filename, file_content)
                file_content = json.loads(file_content)
                label = file_content["label"]
                dataset.append(ImageData(file=im, label=label))
        return dataset


if __name__ == "__main__":
    database = Database()
    database.get_images(debug=True)

    """file_path = os.path.join(os.path.dirname(__file__), 'test_image2.png')
    with open(file_path, 'rb') as input_file:
        database.feedback(input_file, file_path, {"label": 234})"""
