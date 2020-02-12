# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import time
import picamera

#set GPIO numbering mode and define output pins
forward = 31
backward = 33
left = 37
right = 35

GPIO.setmode(GPIO.BOARD)
GPIO.setup(forward,GPIO.OUT)
GPIO.setup(backward,GPIO.OUT)
GPIO.setup(left,GPIO.OUT)
GPIO.setup(right,GPIO.OUT)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)
#Initialize
GPIO.output(forward,False)
GPIO.output(left,False)
GPIO.output(backward,False)
GPIO.output(right,False)
delaytime = 0.2
while True:   
    char = screen.getch()
    if char == ord('q'):
        break
    elif char == ord('w'):
        print("w")
        GPIO.output(forward,True)
        GPIO.output(left,False)
        GPIO.output(backward,False)
        GPIO.output(right,False)
        time.sleep(delaytime) 

    elif char == ord('s'):
        print("s")
        GPIO.output(forward,False)
        GPIO.output(left,False)
        GPIO.output(backward,True)
        GPIO.output(right,False)
        time.sleep(delaytime) 

    elif char == ord('d'):
        print("d")
        GPIO.output(forward,False)
        GPIO.output(left,False)
        GPIO.output(backward,False)
        GPIO.output(right,True)
        time.sleep(delaytime) 

    elif char == ord('a'):
        print("a")
        GPIO.output(forward,False)
        GPIO.output(left,True)
        GPIO.output(backward,False)
        GPIO.output(right,False)
        time.sleep(delaytime) 

    elif char == ord("e"): #Backspace
        print("STOP")
        GPIO.output(forward,False)
        GPIO.output(left,False)
        GPIO.output(backward,False)
        GPIO.output(right,False)
        time.sleep(delaytime) 
         
#Close down curses properly, inc turn echo back on!
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()
GPIO.cleanup()
