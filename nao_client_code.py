class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        import socket
        import pickle
        import sys

        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 6666       # The port used by the server

        #Establish connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        #Call ALVideoDevice service
        session = self.session()
        camSession = session.service("ALVideoDevice")
        resolution = 2 #VGA
        colorSpace = 11 #RGB
        fps = 5

        nameId = camSession.subscribeCamera("cameratest",0,resolution,colorSpace,fps)

        #Get camera image
        naoImage = camSession.getImageRemote(nameId)
        camSession.releaseImage(nameId)
        camSession.unsubscribe(nameId)

        try:
            #Send buffer size
            size = sys.getsizeof(pickle.dumps(naoImage[6]))
            s.send(str(size))

            #Send image to server
            s.sendall(pickle.dumps(naoImage[6]))

            #Get emotion response from server
            emotion=b""
            emotion = s.recv(1024)
            voice_emotion = s.recv(1024)
            self.logger.info(emotion)
            self.logger.info(voice_emotion)

        except Exception as e:
            pass
        finally:
            s.close()
            self.output_emotion(emotion)
            self.onStopped()
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box