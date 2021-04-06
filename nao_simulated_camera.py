import cv2
from naoqi import ALProxy
import vision_definitions
import time
import numpy as np

print("Default IP: 127.0.0.1")
print("Default Port= 9559")
print("******")

camProxy = ALProxy("ALVideoDevice", "localhost", 9559)
print(camProxy)
resolution = 2
colorSpace = 11
fps = 15

nameId = camProxy.subscribeCamera("cameraTest", 0, resolution, colorSpace, fps)

vc = cv2.VideoCapture(0)

#print current camera configuration to set parameters 
print(camProxy.getExpectedImageParameters(0))
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while vc.isOpened():
    rval, frame = vc.read()
	
    frame=cv2.resize(frame, (640, 480))
    time.sleep(0.15)
    b,g,r = cv2.split(frame)       # get b,g,r
    rgb_img = cv2.merge([r,g,b])     # switch it to rgb
	#important: image sent to the robot upper camera is rgb 640x480 

    set=camProxy.putImage(0,640,480,rgb_img.tobytes())

    image_raw = camProxy.getImageRemote(nameId)

    #print(set)
    #if key == 27: # exit on ESC
        #break
camProxy.unsubscribe(nameId)
cv2.destroyWindow("preview")