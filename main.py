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
    minimumVal = {'blue':(97, 100, 117), 'green':(60,50,50), 'yellow':(20, 100, 10), 'pink': (125,100,30), 'white': (0,0,100)} 
    maximumVal = {'blue':(117,255,255), 'green':(86,255,255), 'yellow':(30,255,255), 'pink':(255,255,255), 'white':(0,0,255)}

    colors = {'blue':(255,0,0), 'green':(0,255,0), 'yellow':(0,255,255), 'pink':(255,0,255), 'white':(255,255,255)}

    #removal of red due to mix up with pink but just in case:
    """
    'red':(166, 84, 141)
    'red':(186,255,255)
    'red':(0,0,255)
    """

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
    
    """
    list order[
    thumbIndex_x,
    thumbIndex_y,
    indexMiddle_x,
    indexMiddle_y,
    middleRing_x,
    middleRing_y,
    ringPinky_x
    ringPinky_y
    pinkyThumb_x
    pinkyThumb_y
    ]
    """
    
    calculations = [
    colorCoord['yellow'][0] - colorCoord['blue'][0],
    colorCoord['yellow'][1] - colorCoord['blue'][1],
    colorCoord['white'][0] - colorCoord['yellow'][0],
    colorCoord['white'][1] - colorCoord['yellow'][1],
    colorCoord['green'][0] - colorCoord['white'][0],
    colorCoord['green'][1] - colorCoord['white'][1],
    colorCoord['pink'][0] - colorCoord['green'][0],
    colorCoord['pink'][1] - colorCoord['green'][1],
    colorCoord['blue'][0] - colorCoord['pink'][0],
    colorCoord['blue'][1] - colorCoord['pink'][1],
    ]
    
    print(calculations)
    return calculations
    
    

def translate_to_letter(colorCoord, calculations):
    #letter list with minimum and maximum possible values

    """
    list order[
    thumbIndex_x,
    thumbIndex_y,
    indexMiddle_x,
    indexMiddle_y,
    middleRing_x,
    middleRing_y,
    ringPinky_x
    ringPinky_y
    pinkyThumb_x
    pinkyThumb_y
    ]
    """

    minCoordVals = {
        'A': [0,0,22,13,25,-1,0,21,0,0],
        'D': [10,-192,-14, 138, 23, -7, 22, -5, -121, -56],
        'R': [-21, -124, -31, -43, -12, 128, 16, 2, -54, -73],
        }

    maxCoordVals = {
        'A': [0,0,61,26,51, 17, 68, -4,0,0],
        'D': [35, -141, 9, 175, 45, 31, 41, 11, -57, 24],
        'R': [30, -81, 10, 27, 32, 237, 33, 22, -3, -58],
        }

    for key in maxCoordVals:
        matchCount = 0
        for i in range(10):
            if minCoordVals[key][i] < calculations[i] < maxCoordVals[key][i]:
                matchCount += 1
                print("letterfound!")
                print(key)
            else:
                print("invalid")
        if matchCount == 10:
            return key
                
   
def text_to_audio(translatedLetter):
    
    text = tts.init()
    voices = engine.getProperty('voices')
    rate = text.getProperty('rate')
    text.setProperty('voice',voices[7].id)
    text.setProperty('rate', rate-25)
    
    print("Your letter is", translatedLetter) 
    text.say(translatedLetter)
    text.runAndWait()


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
            audibleLetter = text_to_audio(letter)
            
        else:
            print("wrong input")
            
        break
    
