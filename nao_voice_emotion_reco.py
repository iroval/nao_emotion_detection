from keras.models import model_from_json
import numpy as np
import librosa
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import keras

emotion_list = [
    'female_angry',
    'female_calm',
    'female_fearful',
    'female_happy',
    'female_sad',
    'male_angry',
    'male_calm',
    'male_fearful',
    'male_happy',
    'male_sad'
]

def voice_emotion():
    opt = keras.optimizers.RMSprop(lr=0.00001, decay=1e-6)
    lb = LabelEncoder()

    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("Emotion_Voice_Detection_Model.h5")
    print("Loaded model from disk")
    
    # evaluate loaded model on test data
    loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

    X, sample_rate = librosa.load('output10.wav', res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
    featurelive = mfccs
    livedf2 = featurelive
    livedf2= pd.DataFrame(data=livedf2)
    livedf2 = livedf2.stack().to_frame().T
    twodim= np.expand_dims(livedf2, axis=2)
    livepreds = loaded_model.predict(twodim, 
                            batch_size=32, 
                            verbose=1)

    livepreds1=livepreds.argmax(axis=1)
    liveabc = livepreds1.astype(int).flatten()
    #livepredictions = (lb.inverse_transform((liveabc)))
    print(liveabc)
    final_emotion = str(liveabc)
    return emotion_list[int(final_emotion[1:-1])]

if __name__ == '__main__':
    voice_emotion()