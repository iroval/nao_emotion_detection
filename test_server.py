import socket
from PIL import Image
import sys
import io
import os
import pickle
import tf_emotion
import nao_voice_emotion_reco

def server_func():
    binary_array = []

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 6666        # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT))
    print("Socket bind complete")
    s.listen(10)
    print("Socket now listening")

    while True:
        #Establish connection with client
        conn, addr = s.accept()
        print('Got connection from', addr)

        try:
            final_data = b""
            #Get buffer size
            size = conn.recv(1024)

            #Get all image data
            img_data = conn.recv(int(size))
            final_data = bytes(img_data)
                    
            #Save reconstructed image
            img = Image.frombytes('RGB', (640, 480), bytes(pickle.loads(final_data)))
            img.save('image.png')    
            print("Got image")

            #Get emotion
            detected_emotion = tf_emotion.emotion_reco()
            print("TF returned: " + detected_emotion)

            #Get voice emotion
            detected_voice_emotion = nao_voice_emotion_reco.voice_emotion()
            print("Detected on voice: " + detected_voice_emotion)

            #Send data to NAO
            conn.send(bytes(detected_emotion, encoding='utf8'))
            conn.send(bytes(detected_voice_emotion, encoding='utf-8'))

        except Exception as e:
            print(e)
            
        finally:
            conn.close()

    s.close()

if __name__ == '__main__':
    server_func()