import time
import pyttsx3 as tts
import cv2
import numpy as np

video = cv2.VideoCapture(0)

#colours
while(1):

    # Take each frame
    _, frame = video.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # range of blue 
    blue_min = np.array([121,91,39])
    blue_mid = np.array([173,134,66])
    blue_max = np.array([232,199,141])

    #range of orange
    orange_min = np.array([51,92,205])
    orange_mid = np.array([67,115,251])
    orange_max = np.array([115,152,255])

    #range of red
    red_min = np.array([32,36,98])
    red_mid = np.array([53,59,154])
    red_max = np.array([121,125,197])

    #range of purple
    purp_min = np.array([63,29,64])
    purp_mid = np.array([105,53,107])
    purp_max = np.array([181,114,184])

    # Threshold the HSV image to get only blue colors
    blue = cv2.inRange(hsv, blue_min, blue_max)
    orange = cv2.inRange(hsv, orange_min, orange_max)
    red = cv2.inRange(hsv, red_min, red_max)
    purple = cv2.inRange(hsv, purp_min, purp_max)

    # Bitwise-AND mask and original image
    res_blue = cv2.bitwise_and(frame,frame, mask= blue)
    res_orange = cv2.bitwise_and(frame,frame, mask= orange)
    res_red = cv2.bitwise_and(frame,frame, mask= red)
    res_purple = cv2.bitwise_and(frame,frame, mask= purple)

#understand what this is attempting to do 

    cv2.imshow('frame',frame)
    cv2.imshow('mask',blue)
    cv2.imshow('mask',orange)
    cv2.imshow('mask',red)
    cv2.imshow('mask',purple)
    cv2.imshow('res',res_blue)
    cv2.imshow('res',res_orange)
    cv2.imshow('res',res_red)
    cv2.imshow('res',res_purple)

    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        print("Quit")
        video.release()
        cv2.destroyAllWindows()
        break



# When everything done, release the capture
video.release()
cv2.destroyAllWindows()


#Text to audio
"""
text = tts.init()
text.say("I will speak this text")
text.runAndWait()
"""

