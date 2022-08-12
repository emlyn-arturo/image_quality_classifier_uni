#!/usr/bin/python

import os

import time

from werkzeug.exceptions import BadRequest, NotFound
from unikittypy import UnikittyPy
from flask import Flask, request, send_from_directory, json
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = ('jpeg', 'jpg', 'gif', 'png')

app = Flask(__name__, static_folder='dist')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

try:
    os.stat(UPLOAD_FOLDER)
except:
    os.mkdir(UPLOAD_FOLDER)


def allowed_file(filename):
    if '.' in filename:
        filetype = filename.rsplit(".", 1)[1].lower()
        if filetype in ALLOWED_EXTENSIONS:
            return True
        return filetype
    return None


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
@app.route('/upload', defaults={'path': ''})
@app.route('/', defaults={'path': ''})
def index(path):
    root_dir = os.path.dirname(os.getcwd())
    print(os.path.join(root_dir, 'dist', 'index.html'))
    return app.send_static_file('index.html')


@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('dist/static/js', path)


@app.route('/uploads/<path:path>')
def send_uploaded_file(path):
    return send_from_directory('uploads', path)


@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('dist/static/css', path)


class ImageUpload(Resource):
    def post(self):
        """
        Uploads an image and saves it to the preset upload directory.
        :return: Response JSON of this action containing file and
            classification result
        """
        if len(request.files) == 0 or 'image' not in request.files:
            raise NotFound("No file uploaded.")
        response = []
        for file in request.files.getlist('image'):
            allowed = allowed_file(file.filename)
            if allowed is not True:
                raise BadRequest("File type not allowed: " + str(allowed))
            filename = str(int(time.time())) + "_" \
                + secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            image_obj = Image.open(path)

            unikittypy = UnikittyPy(net_fitted=True)
            response.append({
                "file": filename,  # For feedback later
                "result": unikittypy.run(image_obj),
            })
        return response


class TriggerTraining(Resource):
    def get(self):
        """
        Trigger the network's training cycle.
        :return: JSON containing success rate of training cycle
        """
        unikittypy = UnikittyPy(net_fitted=False)
        result = unikittypy.train()
        response = {
            "result": result
        }
        return response


class AddFeedback(Resource):
    def post(self):
        """
        Adds feedback to prior image classification requests.
        :param filename: The former filename returned by the classification.
        :return: The new status of this classified labelling.
        """
        data = json.loads(request.data)

        print(data)

        unikittypy = UnikittyPy(net_fitted=False)

        path = os.path.join(os.path.dirname(__file__),
                            "uploads", data["image"])
        with open(path) as file:
            response = {
                "file": data["image"],
                "status": unikittypy.register_feedback(
                    file, path, bool(data['feedback']))
            }
            return response


api.add_resource(ImageUpload, "/api/evaluate")
api.add_resource(TriggerTraining, "/api/train")
api.add_resource(AddFeedback, "/api/feedback")
