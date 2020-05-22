# import curses and GPIO
import curses
import time
from jetbot import Rover

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

#Initialize
delaytime = 0.2
speed = 0.7
robot = Rover()
while True:   
    char = screen.getch()
    if char == 27:
            break
    elif char == ord('w'):
            print("w")
            robot.left(speed)
            robot.right(speed)
            time.sleep(delaytime) 

    elif char == ord('s'):
            print("s")
            robot.left(-speed)
            robot.right(-speed)
            time.sleep(delaytime) 

    elif char == ord('d'):
            print("d")
            robot.left(speed)
            robot.right(-speed)
            time.sleep(delaytime) 

    elif char == ord('a'):
            print("a")
            robot.left(-speed)
            robot.right(speed)
            time.sleep(delaytime) 

    elif char == ord('q'): 
            print("STOP")
            robot.stop()
            time.sleep(delaytime) 
			 
#Close down curses properly, inc turn echo back on!
curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
