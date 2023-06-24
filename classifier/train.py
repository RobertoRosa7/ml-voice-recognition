import os
import json
import numpy as np
import tensorflow.keras as keras
from sklearn.model_selection import train_test_split

DATA_PATH = os.path.join("data.json")
SAVED_MODEL_PATH = os.path.join("../flask/model.h5")

LEARNING_RATE = 0.0001
EPOCHS = 40
BATCH_SIZE = 32
NUM_KEYWORDS = 10


def load_dataset(data_path):
    with open(data_path, 'r') as fp:
        data = json.load(fp)

    # extract inputs and targets
    x = data["MFCCs"]
    y = data["labels"]

    return x, y


def get_data_splits(data_path, test_size=0.1, test_validation=0.1):
    # load dataset
    x, y = load_dataset(data_path)

    # create train/validation/test splits
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
    x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size=test_validation)

    # convert inputs in array shape
    x_train = np.array(x_train)  # (segments, 44, 13, 1)
    x_validation = np.array(x_validation)
    x_test = np.array(x_test)

    # convert input 3d in 4d
    x_train = x_train[..., np.newaxis]
    x_validation = x_validation[..., np.newaxis]
    x_test = x_test[..., np.newaxis]

    return x_train, x_validation, x_test, y_train, y_validation, y_test


def build_model(input_shape, learning_rate, error="sparse_categorical_crossentropy"):
    # build network
    model = keras.Sequential()

    # conv layer 1
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=input_shape,
                                  kernel_regularizer=keras.regularizers.l2(0.001)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))

    # conv layer 2
    model.add(keras.layers.Conv2D(32, (3, 3), activation='relu',
                                  kernel_regularizer=keras.regularizers.l2(0.001)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))

    # conv layer 3
    model.add(keras.layers.Conv2D(32, (2, 2), activation='relu',
                                  kernel_regularizer=keras.regularizers.l2(0.001)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPool2D((2, 2), strides=(2, 2), padding="same"))

    # flatten the output feed it into dense layer
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64, activation="relu"))
    model.add(keras.layers.Dropout(0.3))

    # softmax classifier
    model.add(keras.layers.Dense(NUM_KEYWORDS, activation="softmax"))  # [0.1, 0.7, 0.2]

    # compile the model
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss=error, metrics=["accuracy"])
    model.summary()

    return model


def main():
    # load train/validate/test data split
    x_train, x_validation, x_test, y_train, y_validation, y_test = get_data_splits(DATA_PATH)

    # build the CNN model
    input_shape = (x_train.shape[1], x_train.shape[2], x_train.shape[3])  # (segments, coefficients 13, 1)
    model = build_model(input_shape, LEARNING_RATE)

    # train the model
    model.fit(np.array(x_train), np.array(y_train), epochs=EPOCHS, batch_size=BATCH_SIZE,
              validation_data=(np.array(x_validation), np.array(y_validation)))

    # evaluate the model
    test_error, test_accuracy = model.evaluate(np.array(x_test), np.array(y_test))
    print(f'Test error: {test_error}, test accuracy: {test_accuracy}')

    # save the model
    model.save(SAVED_MODEL_PATH)


if __name__ == "__main__":
    main()
