import socket
from PIL import Image
import sys
import io
import os
import pickle
import tf_emotion

binary_array = [] #Will store image data

HOST = '127.0.0.1'  # Standard loopback interface address (localhost). Change with current address
PORT = 6666        # Port to listen on (non-privileged ports are > 1023)

#Create socket
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
        final_data = b"" #Will be used to append the image data

        #Get buffer size
        size = conn.recv(1024)
        str_size = str(size, encoding = 'utf-8')
        int_size = int(size)
        print(int_size)

        #Get image data
        while True:
            try:
                img_data = conn.recv(4096)
            except:
                break
            binary_array = bytes(img_data)
            if(img_data.endswith(b'[END OF IMAGE]')):
                final_data += binary_array.replace(b'[END OF IMAGE]', b'')
                break
            else:
                final_data += binary_array

        #Save reconstructed image
        img = Image.frombytes('RGB', (640, 480), bytes(pickle.loads(final_data)))
        img.save('image.png')    
        print("Got image")

        #Get emotion
        detected_emotion = tf_emotion.emotion_reco()
        print("TF returned: " + detected_emotion)

        #Send data to NAO
        conn.send(bytes(detected_emotion, encoding='utf8'))
        
    except Exception as e:
        print(e)
        
    finally:
        conn.close()

s.close()
