# import curses and GPIO
import curses
import time
import serial

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

#Initialize
ser = serial.Serial("/dev/ttyACM0", 9600)
delaytime = 0.2
while True:   
	char = screen.getch()
	if char == 27:
		break
	elif char == ord('w'):
		print("w")
		ser.write(b'w')
		time.sleep(delaytime) 

	elif char == ord('s'):
		print("s")
		ser.write(b's')
		time.sleep(delaytime) 

	elif char == ord('d'):
		print("d")
		ser.write(b'd')
		time.sleep(delaytime) 

	elif char == ord('a'):
		print("a")
		ser.write(b'a')
		time.sleep(delaytime) 

	elif char == ord('q'): 
		print("STOP")
		ser.write(b'q')
		time.sleep(delaytime) 
			 
#Close down curses properly, inc turn echo back on!
curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
