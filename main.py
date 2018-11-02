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

    #color section where min and max HSV values are set, general BGR values, and empty color coordinate list
    minimumVal = {'red':(166, 84, 141), 'blue':(97, 100, 117), 'green':(66, 122, 129), 'yellow':(20, 100, 10), 'pink': (125,100,30), 'white': (0,0,100)} 
    maximumVal = {'red':(186,255,255), 'blue':(117,255,255), 'green':(86,255,255), 'yellow':(30,255,255), 'pink':(255,255,255), 'white':(0,0,255)}

    colors = {'red':(0,0,255), 'blue':(255,0,0), 'green':(0,255,0), 'yellow':(0,255,255), 'pink':(255,0,255), 'white':(255,255,255)}

    colorCoord = {
        'red':[0,0],
        'blue':[0,0],
        'green':[0,0],
        'yellow':[0,0],
        'pink': [0,0],
        'white': [0,0],
        }

    #taking maximum values and isolating them within the frame, creating "mask", and returning the coordinates within the colorCoord dictionary
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

    return colorCoord

def creating_circles(radius, x, y, colors, key, frame):
    # find in contours then creating the circle
        # draw the circle and centroid on the frame, updates position
    if radius > 0.5:
        cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
        cv2.putText(frame,key + " ball", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)

def calculating_distances(colorCoord):
    #calculates the distances between finger points 
    calculations = {
    'thumbIndex_x':colorCoord['blue'][0] - colorCoord['yellow'][0],
    'thumbIndex_y' : colorCoord['blue'][1] - colorCoord['yellow'][1],
    'indexMiddle_x' : colorCoord['yellow'][0] - colorCoord['white'][0],
    'indexMiddle_y' : colorCoord['yellow'][1] - colorCoord['white'][1],
    'middleRing_x' : colorCoord['white'][0] - colorCoord['green'][0],
    'middleRing_y' : colorCoord['white'][1] - colorCoord['green'][1],
    'ringPinky_x' : colorCoord['green'][0] - colorCoord['pink'][0],
    'ringPinky_y' : colorCoord['green'][1] - colorCoord['pink'][1],
    'pinkyThumb_x' : colorCoord['pink'][0] - colorCoord['blue'][0],
    'pinkyThumb_y'  : colorCoord['pink'][1] - colorCoord['blue'][1],
    }
    
    return calculations
    

def translate_to_letter(colorCoord, calculations):
    #letter dictionary with minimum and maximum possible values 

    minCoordVals = {
        'A': {'indexMiddle_x': 22, 'indexMiddle_y':13, 'middleRing_x':25, 'middleRing_y':-1, 'ringPink_x':25, 'ringPinky_y':-21},
        'D': {'thumbIndex_x': 10, 'thumbIndex_y': -192, 'indexMiddle_x': -14, 'indexMiddle_y': 138, 'middleRing_x':23, 'middleRing_y':-7, 'ringPinky_x': 22, 'ringPinky_y' :-5, 'pinkyThumb_x': -121, 'pinkyThumb_y': -56},
        'R': {'thumbIndex_x': -21, 'thumbIndex_y': -124, 'indexMiddle_x': -31, 'indexMiddle_y': -43, 'middleRing_x': -12, 'middleRing_y': 128, 'ringPinky_x': 16, 'ringPinky_y' : 2, 'pinkyThumb_x': -54, 'pinkyThumb_y': -73},
        }

    maxCoordVals = {
        'A': {'indexMiddle_x': 46, 'indexMiddle_y':26, 'middleRing_x':51, 'middleRing_y':17, 'ringPink_x':37, 'ringPinky_y':-4},
        'D': {'thumbIndex_x': 35, 'thumbIndex_y': -141, 'indexMiddle_x' : 9, 'indexMiddle_y': 175, 'middleRing_x':45, 'middleRing_y':31, 'ringPinky_x':41, 'ringPinky_y':11, 'pinkyThumb_x': -57, 'pinkyThumb_y' : 24},
        'R': {'thumbIndex_x': 30, 'thumbIndex_y': -81, 'indexMiddle_x': 10, 'indexMiddle_y': 27, 'middleRing_x': 32, 'middleRing_y': 237, 'ringPinky_x': 33, 'ringPinky_y' : 22, 'pinkyThumb_x': -3, 'pinkyThumb_y': -58},
        }
    
    for max_item in maxCoordVals.items():
        if minCoordVals.items() <= calculations.items() <= maxCoordVals.items():
            #print(max_item)
            #letter = max_item
            #return letter
            print("working")
        else:
            print("something wrong")
            
"""   
def text_to_audio(translatedletter):
    
    text = tts.init()
    text.say("Your letter is", translatedLetter)
    text.runAndWait()
"""

#Running program until broken by using escape key
while(1):

    # Take each frame
    _, frame = video.read(0)
    frame = resize(frame)
    frame = cv2.flip(frame, 1)
    colorCoord = find_centers(frame)
    
    
    cv2.imshow('frame',frame)     
            
    #escape
    k = cv2.waitKey(1) & 0xFF
    if k == 27:#escape key
        print("Quit")
        video.release()
        cv2.destroyAllWindows()

        #future button prompt that will start the calculations and translation
        question = input("enter")
        if question == "go":
            calculated_distances = calculating_distances(colorCoord)
            letter = translate_to_letter(colorCoord, calculated_distances)

            #audibleLetter = text_to_audio(letter)
            
        else:
            print("wrong input")
            
        break
    
