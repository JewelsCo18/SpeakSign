import serial
import time

try:
   arduino = serial.Serial('/dev/tty.usbserial-DN01DY7O', 9600)
except:
   print("Failed to connect on /dev/tty.usbserial-DN01DY7O")


try:
   msg=arduino.readline()
   print(msg.decode('utf-8'))
   
   while True:
      msg=arduino.readline()
      print(msg.decode('utf-8'))
      
      if arduino.readline().strip().decode('utf-8') == 'A':
        print("Anazlying!\n")
        
      if arduino.readline().strip().decode('utf-8') == 'F':
        print("Finished!\n")
        
      if arduino.readline().strip().decode('utf-8') == 'S':
        print("Space!\n")

except:
   print ("Failed to read!")
