import cv2
import time
import threading
from flask import Response, Flask
import sys
import image_processing.lane_detection as ld
from jetbot import Rover
import curses

# Image frame sent to the Flask object
global video_frame
video_frame = None

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock 
thread_lock = threading.Lock()


# Create the Flask object for the application
app = Flask(__name__)

global old_distance, prev_time
old_distance = 0
prev_time = 0
def captureFrames():
    global video_frame, thread_lock, old_distance, prev_time, stop_thread
    
    # Create global robot object
    robot = Rover()
    robot.startVideoCapture()

    # Video capturing from robot
    video_capture = robot.video_capture 
    while True and video_capture.isOpened():
        return_key, frame = video_capture.read()
        if not return_key:
            break
        try:
            #Apply lane detection, return the processed image and the distance 
            #between the robot direction and center of lane
            frame, distance = ld.detect_lane(frame)

            #Sending control signal to MotorDriver in a constant rate loop
            cur_time = time.time()
            if (distance != old_distance and cur_time-prev_time >= 0.1):
                prev_time = cur_time
                robot.control_motor(distance)
                old_distance = distance
        except ValueError:
            print("No lane Detected")
            #break
        # Create a copy of the frame and store it in the global variable,
        # with thread safe access
        with thread_lock:
            video_frame = frame.copy()
        cv2.imshow('lane', frame)
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            print("stop")
            break
    robot.stop()
    cv2.destroyAllWindows()
    video_capture.release()
        
def encodeFrame():
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

        # Output image as a byte array
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encoded_image) + b'\r\n')

def captureKeyboard():
    global stop_thread
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    try:
        while True:
            char = screen.getch()
            if char == 27:
                stop_thread = True
                break
    finally:
        #Close down curses properly, inc turn echo back on!
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()

@app.route("/")
def streamFrames():
    return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':

    # Create a thread and attach the method that captures the image frames, to it
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True

    #keycap_thread = threading.Thread(target=captureKeyboard)
    #keycap_thread.daemon = True
    
    # Start the thread
    process_thread.start()
    #keycap_thread.start()

    # start the Flask Web Application
    # While it can be run on any feasible IP, IP = 0.0.0.0 renders the web app on
    # the host machine's localhost and is discoverable by other machines on the same network 
    app.run("0.0.0.0", port="8000")

