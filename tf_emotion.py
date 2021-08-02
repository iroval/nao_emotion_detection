import tensorflow as tf
from deepface import DeepFace

def emotion_reco():
    obj = DeepFace.analyze(img_path = "image.png", actions = ['emotion']) #analyze emotion from image
    print("ran tf") #sanity check
    print(obj) #sanity check
    print("TF detected: " + obj["dominant_emotion"]) #sanity check
    return obj["dominant_emotion"] #return detected emotion

if __name__ == '__main__':
    emotion_reco()