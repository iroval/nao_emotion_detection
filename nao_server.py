import socket
from PIL import Image
import sys
import io
import os
import pickle

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
        while True:
            img_data = conn.recv(4096)
            binary_array = bytes(img_data)
            final_data += binary_array
            if not img_data: 
                break

        img = Image.frombytes('RGB', (640, 480), bytes(pickle.loads(final_data)))
        img.save('image.png')    
        print("Got image")
        
    except Exception as e:
        print(e)
        
    finally:
        conn.close()
        continue

s.close()