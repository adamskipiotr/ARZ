from flask import Flask, flash, request, redirect, url_for, Blueprint, jsonify
import json
import os
from werkzeug.utils import secure_filename

from service.images_neural_network import NeuralNetworkManager
from service.images_service import ImagesService

images = Blueprint('images', __name__)
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'

images_service = ImagesService()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@images.route('/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}
    file = request.files['file']
    if file.filename == '':
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads', filename))
        neural_network_manager = NeuralNetworkManager()
        prediction = neural_network_manager.evaluate_image(file)
        data = {'prediction': str(prediction)}
        return jsonify(data), 200
    else:
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}


@images.route('/train-neural-network')
def train_neural_network():
    neural_network_manager = NeuralNetworkManager()
    neural_network_manager.create_neural_network()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'},

@images.route('/<animalName>/<isCorrect>')
def evaluate_animal(animalName, isCorrect):
    images_service.update_animal_category_rating(animalName, isCorrect)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@images.route('/get-animals-stats')
def get_animals_stats():
    animals_rating = images_service.get_animals_category_rating()
    json_string = json.dumps([animal_rating.__dict__ for animal_rating in animals_rating])
    return json_string, 200
