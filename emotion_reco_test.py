import tensorflow as tf
import numpy as np

from tensorflow import keras
from keras import Sequential
from keras.layers import LSTM as KERAS_LSTM, Dense, Dropout, Conv2D, Flatten, \
    BatchNormalization, Activation, MaxPooling2D

from speechemotionrecognition.utilities import get_feature_vector_from_mfcc
from speechemotionrecognition.utilities import get_data, \
    get_feature_vector_from_mfcc

def predict_one(self, sample):
        sample = sample.reshape(198,39,1)
        return np.argmax(self.predict(np.array([sample])))

model = Sequential()

model.add(Conv2D(8, (13, 13),input_shape=(198, 39, 1)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(8, (13, 13)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Conv2D(8, (13, 13)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(8, (2, 2)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Flatten())
model.add(Dense(64))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.2))

model.add(Dense(4, activation='softmax'))

model.load_weights("speech-emotion-recognition/models/best_model_CNN.h5")

model.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy'])

print(model.summary())

to_flatten= False
filename = "03-01-03-02-01-01-10.wav"
print('prediction', predict_one(model, get_feature_vector_from_mfcc(filename, flatten=to_flatten)),'Actual 3')