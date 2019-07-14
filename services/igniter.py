import serial
import time

ser = None
try:
    ser = serial.Serial("/dev/ttyACM0",9600)
except:
    print("Unable to connect to serial")

def ignite(channel):
    if(ser):
      ser.write(bytes("N" + channel, "UTF-8"))
      ser.flush()
      time.sleep(2)
      ser.write(bytes("F" + channel, "UTF-8"))
      ser.flush()
    else:
      print("No serial attached")
