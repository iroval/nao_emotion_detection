import socket
from PIL import Image
import sys
import io
import os
import pickle

binary_array = []


HOST = '83.212.67.183'
#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
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
    conn.settimeout(0.25)
    print('Got connection from', addr)

    try:
        final_data = b""

        #Get buffer size
        size = conn.recv(1024)
        str_size = str(size, encoding = 'utf-8')
        int_size = int(size)
        print('str_size: ' + str_size)
        print(int_size)
        #Get all of the image data
        # while True:
        #     img_data = conn.recv(4096)
        #     binary_array = bytes(img_data)
        #     final_data += binary_array
        #     if not img_data: 
        #         break
        



        number_of_bytes_received = 0

        # while True:
        #     img_data = conn.recv(4096)
        #     binary_array = bytes(img_data)
        #     final_data += binary_array
        #     int_size = int_size - 4096
        #     number_of_bytes_received += sys.getsizeof(binary_array)
        #     print(number_of_bytes_received)
        #     if (int_size - 4096) <= 0:
        #         img_data = conn.recv(4096)
        #         binary_array = bytes(img_data)
        #         final_data += binary_array
        #         int_size = int_size - 4096
        #         break

        while True:
            try:
                img_data = conn.recv(4096)
            except:
                break
            binary_array = bytes(img_data)
            final_data += binary_array

        # f = open("pickle_data.bin", "wb")
        # f.write(final_data)
        # f.close()


        #Save reconstructed image
        img = Image.frombytes('RGB', (640, 480), bytes(pickle.loads(final_data)))
        img.save('image.png')    
        print("Got image")

        conn.send(bytes('neutral', encoding='utf8'))
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
        
    finally:
        conn.close()

s.close()