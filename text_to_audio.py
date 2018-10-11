import cv2
import pyttsx3 as tts

user_input = input("What should I say: ")
text = tts.init()
rate = text.getProperty('rate')
text.setProperty('rate', rate-25)
text.say(user_input)
text.runAndWait()

