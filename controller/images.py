from flask import Flask, flash, request, redirect, url_for, Blueprint
import json
import os
from werkzeug.utils import secure_filename

from service.images_neural_network import NeuralNetworkManager

images = Blueprint('images', __name__)
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@images.route('/image', methods=['POST'])
def upload_image():
    aaa = request
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads', filename))
        neural_network_manager = NeuralNetworkManager()
        #TODO Przetestowac bo moze sie tu rypnac
        neural_network_manager.evaluate_image(file)
        print('Image successfully uploaded and displayed below')
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'},
    else:
        print('Allowed image types are - png, jpg, jpeg, gif')
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}


@images.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@images.route('/train-neural-network')
def train_neural_network():
    neural_network_manager = NeuralNetworkManager()
    neural_network_manager.create_neural_network()
