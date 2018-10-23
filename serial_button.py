import serial
import time

try:
   arduino = serial.Serial('/dev/ttyACM', 9600)
except:
   print "Failed to connect on /dev/ttyACM0"


try:
   print arduino.readline()

   while True:
      if arduino.readline().strip() == 'E':
        print("Detected!\n")

except:
   print ("Failed to read!")
