# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import time
import picamera

#set GPIO numbering mode and define output pins
l_foward = 31
l_backward = 33
r_forward = 37
r_backward = 35

GPIO.setmode(GPIO.BOARD)
GPIO.setup(l_foward,GPIO.OUT)
GPIO.setup(l_backward,GPIO.OUT)
GPIO.setup(r_forward,GPIO.OUT)
GPIO.setup(r_backward,GPIO.OUT)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)
#Initialize
GPIO.output(l_foward,False)
GPIO.output(r_forward,False)
GPIO.output(l_backward,False)
GPIO.output(r_backward,False)
delaytime = 0.2
while True:   
    char = screen.getch()
    if char == ord('q'):
        break
    elif char == ord('w'):
        print("w")
        GPIO.output(l_foward,False)
        GPIO.output(r_forward,False)
        GPIO.output(l_backward,False)
        GPIO.output(r_backward,False)
        time.sleep(delaytime) 
        GPIO.output(l_foward,True)
        GPIO.output(r_forward,True)
        GPIO.output(l_backward,False)
        GPIO.output(r_backward,False)

    elif char == ord('s'):
        print("s")
        GPIO.output(l_foward,False)
        GPIO.output(r_forward,False)
        GPIO.output(l_backward,False)
        GPIO.output(r_backward,False)
        time.sleep(delaytime) 
        GPIO.output(l_foward,False)
        GPIO.output(r_forward,False)
        GPIO.output(l_backward,True)
        GPIO.output(r_backward,True)

    elif char == ord('d'):
        print("d")
        GPIO.output(l_foward,False)
        GPIO.output(r_forward,False)
        GPIO.output(l_backward,False)
        GPIO.output(r_backward,False)
        time.sleep(delaytime) 
        GPIO.output(l_foward,True)
        GPIO.output(r_forward,False)
        GPIO.output(l_backward,False)
        #GPIO.output(r_backward,True)

    elif char == ord('a'):
        print("a")
        GPIO.output(l_foward,False)
        GPIO.output(r_forward,False)
        GPIO.output(l_backward,False)
        GPIO.output(r_backward,False)
        time.sleep(delaytime) 
        GPIO.output(l_foward,False)
        GPIO.output(r_forward,True)
        #GPIO.output(l_backward,True)
        GPIO.output(r_backward,False)

    elif char == ord("e"): #Backspace
        print("STOP")
        GPIO.output(l_foward,False)
        GPIO.output(r_forward,False)
        GPIO.output(l_backward,False)
        GPIO.output(r_backward,False)
         
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
