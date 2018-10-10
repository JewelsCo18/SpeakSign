import time
import pyttsx3 as tts
import cv2
import numpy 

video = cv2.VideoCapture('testvideo.avi')

#template matching with video: https://stackoverflow.com/questions/42559985/python-opencv-template-matching-using-the-live-camera-feed-frame-as-input

while(1):

    # Take each frame
    _, frame = video.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    blue_min = np.array([110,50,50])
    blue_max = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, blue_min, blue_max)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

#understand what this is attempting to do 
    """
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    """
    
video.release()
cv2.destroyAllWindows()


#Text to audio
"""
text = tts.init()
text.say("I will speak this text")
text.runAndWait()
"""
