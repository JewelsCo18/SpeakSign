import time
import pyttsx3 as tts
import cv2
import numpy as np
import serial as serialkiller

video = cv2.VideoCapture(0)

def resize(frame, width=680, height=440):
    return cv2.resize(frame, (width, height))

def find_centers(frame):

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    minimumVal = {'red':(166, 84, 141), 'light-blue':(97, 100, 117), 'green':(66, 122, 129), 'yellow':(20, 100, 10), 'pink': (125,100,30), 'white': (0,0,0)} 
    maximumVal = {'red':(186,255,255), 'light-blue':(117,255,255), 'green':(86,255,255), 'yellow':(30,255,255), 'pink':(255,255,255), 'white':(0,0,255)}

    colors = {'red':(0,0,255), 'light-blue':(255,0,0), 'green':(0,255,0), 'yellow':(0,255,255), 'pink':(255,0,255), 'white':(255,255,255)}

    colorCoord = {}
    
    for key in maximumVal.keys():

        mask = cv2.inRange(hsv, minimumVal[key], maximumVal[key])

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            centroid = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(centroid)

            colorCoord[key] = [x,y]

            creating_circles(radius, x, y, colors, key, frame)
            
    print(colorCoord)
    return colorCoord

def creating_circles(radius, x, y, colors, key, frame):
    # find in contours then creating the circle
        # draw the circle and centroid on the frame, updates position
    if radius > 0.5:
        cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
        cv2.putText(frame,key + " ball", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)

#Running program until broken by using escape key
while(1):

    # Take each frame
    _, frame = video.read(0)
    frame = resize(frame)
    colorCoord = find_centers(frame)

    cv2.imshow('frame',frame)     
            

    #escape
    k = cv2.waitKey(1) & 0xFF
    if k == 27:#escape key
        print("Quit")
        video.release()
        cv2.destroyAllWindows()
        question = input("Enter")
        if question == "go":
            check = colorCoord['light-blue'][0] - colorCoord['yellow'][0]
            if 102 <= check <= 128:
                print("done")
        break


#Text to audio
"""
text = tts.init()
text.say("I will speak this text")
text.runAndWait()
"""
