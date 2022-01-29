import tensorflow as tf
from keras.datasets import mnist
from keras.utils import np_utils
from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.models import Sequential, load_model
import numpy as np
import os
import random
import cv2
from sklearn.model_selection import train_test_split


class NeuralNetworkManager:

    def __init__(self) -> None:
        self.animals = ["butterfly", "elephant", "cat"]
        self.image_size = 100

    def create_data(self):
        data = []
        categories = {"gallina": "butterfly", "elefante": "elephant", "gatto": "cat"}
        animals = ["chicken", "elephant", "cat"]
        for category, translate in categories.items():
            path = "F:\\AnimalsDataset\\raw-img\\" + category
            target = animals.index(translate)
            for img in os.listdir(path):
                try:
                    img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                    new_img_array = cv2.resize(img_array, (self.image_size, self.image_size))
                    data.append([new_img_array, target])
                except Exception as e:
                    pass
        return data

    def create_neural_network(self):
        data = self.create_data()

        random.shuffle(data)
        x = []
        y = []
        for features, labels in data:
            x.append(features)
            y.append(labels)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

        x_train = np.array(x_train).reshape(-1, self.image_size, self.image_size, 1)
        x_train = tf.keras.utils.normalize(x_train, axis=1)
        y_train = np.array(y_train)

        try:
            model = load_model('recognizing-animals-network')
        except IOError as e:
            model = Sequential()
            model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=x_train.shape[1:]))
            model.add(Conv2D(32, kernel_size=3, activation='relu'))
            model.add(Conv2D(32, kernel_size=3, strides=2, padding='same', activation='relu'))
            model.add(Dropout(0.2))
            model.add(Conv2D(64, kernel_size=5, strides=2, padding='same', activation='relu'))
            model.add(Dropout(0.2))
            model.add(Conv2D(256, kernel_size=3, activation='relu'))
            model.add(Flatten())
            model.add(Dropout(0.2))
            model.add(Dense(64, activation='relu'))
            model.add(Dense(3, activation='softmax'))
            model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
            model.fit(x_train, y_train, epochs=20, batch_size=256)
            model.save("recognizing-animals-network")
        x_test = np.array(x_test).reshape(-1, self.image_size, self.image_size, 1)
        y_test = np.array(y_test)
        scores = model.evaluate(x_test, y_test)

    def evaluate_image(self, image):
        try:
            model = load_model("recognizing-animals-network")
        except IOError as e:
            return
        gray_img = cv2.imread(os.path.join('static/uploads', image.filename))
        gray_img = cv2.resize(gray_img, (100, 100))
        gray_img = gray_img.reshape(-1, 100, 100, 1)
        predictions = model.predict(gray_img, verbose=0)
        predicted_animal_name = self.animals[np.argmax(predictions)]
        return predicted_animal_name
