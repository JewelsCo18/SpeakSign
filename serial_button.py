import serial
import time

try:
   arduino = serial.Serial('/dev/tty.usbserial-DN01DY7O', 9600)
except:
   print("Failed to connect on /dev/tty.usbserial-DN01DY7O")

while True:
   if arduino.readline().strip() == 'A':
     print("Detected! Analyzing !\n")
