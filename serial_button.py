import serial

arduino = serial.Serial('/dev/tty.usbserial-DN01DY7O', 9600, timeout = 1)
"""
except:
   print("Failed to connect on /dev/ttyACM0")
"""

commands = arduino.readline()

while True:
   if commands == 'analyze':
            #call analyze
      print("analyzed")
   elif commands == 'finish':
            #call finish
      print("fished")
            
            
    

#except:
 #  print ("Failed to read!")
