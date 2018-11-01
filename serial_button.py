import serial

try:
   arduino = serial.Serial('/dev/ttyACM', 9600)
except:
   print "Failed to connect on /dev/ttyACM0"


try:
   commands = print arduino.readline()

    while True:
        if commands == 'analyze':
            #call analyze
           print("analyzed")
        elif commands == 'space':
            #call space
           print("spaced")
        elif commands == 'finish':
            #call finish
           print("fiished")
            
            
    

except:
   print ("Failed to read!")
