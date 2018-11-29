
import time
import pyttsx3 as tts
import cv2
import numpy as np
import serial 

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
    #for refernence to calculations
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
    
    #letter list with minimum and maximum possible values
    minCoordVals = {
        'A': [0,0,22,13,25,-1,0,21,0,0],
        'B': [-80,-150,38,-35,20,0,40,55,-65,90],
        #Jules'C': [
        'D': [0,-192,0, 176, 23, 8, 17, -5, -88, -120],
        #Jules'E': [
        #Jules'F': [
        'G': [-80, -60, 370, -240, 0,0,0,0, -390, -150],
        'H': [-125,-150,-30, 40,-200,-250,0,0,260,-130],
        'I':[-7,50,20,14,30,-15,50,-190,-140,100],
        'K': [377, 77, 36, -20, -37, 204, 18, -10, -567, -338],
        'L': [81, -209, 12, 147, 29, -5, 16, -21, -283, -71], 
        'M': [380, 170, -400, -200, 220, -160, -10,0, -461, -240],
        'N': [275, 175, 5, -20, 40, 30,30,10, -520,-310],
        #'O': [
        #'P': [
        #'Q': [
        'R': [-21, -124, -31, -43, -12, 128, 16, 2, -54, -73],
        #'S': [
        'T': [-4, 68, 24, 16, 27, -19, 23, -52, -98, -64],
        'U': [-73, -197, 30, -24, -46, 70, 18, 2, -15, -126],
        #'V': [
        #'W': [
        #'X': [
        'Y': [55, 103, 21, 12, 43, -23, 57, -220, -337, 49],
        'I Love You': [48, -169, 20, 172, 13, -1.5, 30, -172,-224, 56],
        }

    maxCoordVals = {
        'A': [0,0,61,26,51, 17, 68, -4,0,0],
        'B': [-50,-140,50,-15,35,20,55,65,-50,105],
        #'C':[
        'D': [35, -120, 20, 230, 42, 31, 41, 10, 5, -80],
        #'E': 
        #'F': [
        'G': [-60, -30, 400, -165, 0, 0, 0, 0, -280, -100],
        'H': [-70,-100,-4,80,150,70,0,0,350,7],
        'I':[14,73,30,30,40,-6,70,-150,-105, 120],
        'K': [465, 116, 72, 10, 13, 240, 29, 12, -420, -271],
        'L': [149, -134, 56, 278, 48, 19, 40, 18, -159, -8],
        'M': [415,200,-170, 200, 430,200, 10, 30, 430, -200],
        'N': [400, 260,78,20,80,89, 70, 40, -335, -275],
        'O': [ 380, 165, -60, 56, 413, 439, 387, 60, -386, -102],
        #'P': [
        #'Q': [
        'R': [30, -81, 10, 27, 32, 237, 33, 22, -3, -58],
        #'S': [
        'T': [-4, 91, 39, 25, 46, -3, 45, -17, -71, -53], 
        'U': [-46, -136, 75, 167, -2, 289, 35, 25, 6, -92],
        #'V': [
        #'W': [
        #'X': [
                'Y': [117, 134, 41, 50, 52, 9, 133, -179 , -190, 108],
        'I Love You': [101, -97, 61, 212, 34, 20, 52, -134, -146, 134],
        }

    #checks if calculations are in between the minimum and maximum values for letters and returns the most frequent letter 
    alphaCompile = []
    for key in maxCoordVals:
        for i in range(10):
            if minCoordVals[key][i] < calculations[i] < maxCoordVals[key][i]:  
                alphaCompile.append(key)
            
    frequentLetter = max(alphaCompile, key=alphaCompile.count)

    print(frequentLetter)
    return frequentLetter

#compiles a list of all the letters that are found
letterCompile = []
def compile_letters(letter):
    
    letterCompile.append(letter)

    print(letterCompile)
    return letterCompile

#function for creating spaces for sentences
def created_space(letterList):

    letterList.append(" ")
    
    print(letterList)
    return letterList

#function for deleting characters (safety measure)
def delete_letter(letterList):

    letterList.pop(len(letterList)-1)

    print(letterList)
    return letterList

#takes the list of compiled characters and creates the sentence or word
def letters_to_words(letterList):

    word = ""
    for elem in letterList:
        word += elem
    return word
      
        
def text_to_audio(translatedWord):
    
    text = tts.init()
    #voices = text.getProperty('voices')
    rate = text.getProperty('rate')
    #text.setProperty('voice',voices[7].id)
    text.setProperty('rate', rate-25)
    print("Your word is :", translatedWord)
    text.say(translatedWord)
    text.runAndWait()

#Running program until broken by using escape or key command functions
while(1):

    # Take each frame
    _, frame = video.read(0)
    frame = resize(frame)
    frame = cv2.flip(frame, 1)
    colorCoord = find_centers(frame)
    
    cv2.imshow('frame',frame)

    #Pyserial Arduino Function
    try:
       arduino = serial.Serial('/dev/tty.usbserial-DN01DY7O', 9600)
    except:
        print("Failed to connect on /dev/tty.usbserial-DN01DY7O")

    k = cv2.waitKey(1) & 0xFF

    #Arduino button component commands 
    try:
        msg=arduino.readline()
        print(msg.decode('utf-8'))
   
        while True:
            msg=arduino.readline()
            print(msg.decode('utf-8'))

            if arduino.readline().strip().decode('utf-8') == 'A':
                print("Anazlying!\n")
                calculated_distances = calculating_distances(colorCoord)
                letterFound = translate_to_letter(colorCoord, calculated_distances)
                listOfLetters = compile_letters(letterFound)
                
            if arduino.readline().strip().decode('utf-8') == 'F':
                print("Finished!\n")
                wordCreated = letters_to_words(listOfLetters)
                audibleLetter = text_to_audio(wordCreated)
        
            if arduino.readline().strip().decode('utf-8') == 'S':
                print("Space!\n")
                spaceAdded = created_space(listOfLetters)

    except:
        print ("Failed to read!")

    #delete function
    if k == ord("d"):
        deletedLetter = delete_letter(listOfLetters)

    #Old key commands
    """
    #key command for "Analyse"
    if k == ord("a"):
        calculated_distances = calculating_distances(colorCoord)
        letterFound = translate_to_letter(colorCoord, calculated_distances)
        listOfLetters = compile_letters(letterFound)

    #space function
    if k == ord("s"):

    #key command for "Finish" 
    if k == ord("f"):
        wordCreated = letters_to_words(listOfLetters)
        audibleLetter = text_to_audio(wordCreated)
    """

    #escape
    if k == 27:#escape key
        print("Quit")
        video.release()
        cv2.destroyAllWindows()
        break
    
