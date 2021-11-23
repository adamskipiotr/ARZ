import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.models import Sequential, load_model
import numpy as np
import os
import random
import cv2
from sklearn.model_selection import train_test_split

class NeuralNetworkManager:



    def __init__(self) -> None:
        self.data = []

    def create_data(self):
        img_dir = "F:\\AnimalsDataset\\raw-img"

        categories = {"gallina": "chicken", "elefante": "elephant"}
        animals = ["chicken", "elephant"]

        img_size = 100

        for category, translate in categories.items():
            path = "F:\\AnimalsDataset\\raw-img\\" + category
            target = animals.index(translate)
            print("POBIERANIE ZWIERZAT Z:" + translate)
            for img in os.listdir(path):
                try:
                    img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                    new_img_array = cv2.resize(img_array, (img_size, img_size))
                    self.data.append([new_img_array, target])
                except Exception as e:
                    pass

    def create_neural_network(self):
        img_size = 100
        self.create_data()
        random.shuffle(self.data)
        x = []
        y = []
        for features, labels in self.data:
            x.append(features)
            y.append(labels)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,train_size=0.8)

        x_train = np.array(x_train).reshape(-1, img_size, img_size, 1)
        x_train = tf.keras.utils.normalize(x_train, axis=1)
        y_train = np.array(y_train)

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
        model.add(Dense(2, activation='softmax'))
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        model.fit(x_train, y_train, epochs=20, batch_size=256)
        model.save("recognizing-animals-network")

    def evaluate_image(self,image):
        try:
            model = load_model("recognizing-animals-network")
        except IOError as e:
            print(e)
            return
        gray_img = cv2.resize(image, (100, 100))
        predictions = model.predict(gray_img, verbose=0)
        print(np.argmax(predictions))
