import time
from jetbot import Rover
import serial
import threading
import curses

global stop_threads, time_elapse
def run():
    while True:
        #print("running", flush=True)
        time.sleep(1)
        global stop_threads, time_elapse
        time_elapse += 1
        if stop_threads:
            break
    #print("thread safely stop", flush=True)

if __name__ == "__main__":
    global time_elapse, stop_threads
    stop_threads = False
    time_elapse = 0
    thread = threading.Thread(target=run)
    thread.daemon = True

    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    try:
        while True:
            char = screen.getch()
            if char == 27:
                stop_threads = True
                break
        print("stop main")
        print(time_elapse)
    finally: 
        #Close down curses properly, inc turn echo back on!
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()


