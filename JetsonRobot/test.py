import time
from jetbot import Rover
import serial

if __name__ == "__main__":
    bot = Rover()
    old_time = 0
    ser = serial.Serial("/dev/ttyACM0", 9600)
    while True:
        bot.left(0.5)
        bot.right(0.5)
#        ser.write("L255".encode())        
        print(time.time() - old_time)
        time.sleep(0.2)
        old_time = time.time()
