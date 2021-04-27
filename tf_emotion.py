import tensorflow as tf
from deepface import DeepFace

def emotion_reco():
    #print(tf.version.VERSION)
    #print(tf.config.list_physical_devices('GPU'))

    #DeepFace.stream()
    obj = DeepFace.analyze(img_path = "image.png", actions = ['emotion'])
    print("ran tf")
    print(obj)
    print("TF detected: " + obj["dominant_emotion"])
    return obj["dominant_emotion"]

if __name__ == '__main__':
    emotion_reco()