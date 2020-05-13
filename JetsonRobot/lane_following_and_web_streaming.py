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

# threadkill flag
global stop_thread
stop_thread = False


# Create global robot object
global robot
robot = Rover()

# Create the Flask object for the application
app = Flask(__name__)

def gstreamer_pipeline(
    #capture_width=1280,
    #capture_height=720,
    #display_width=1280,
    #display_height=720,
    #framerate=60,
    #flip_method=0,

    capture_width=320,
    capture_height=180,
    display_width=320,
    display_height=180,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def control_motor(distance = 0):
    #print("control2")
    global robot
    threshold = 30
    speed = 0.3
    speedDif = speed*((2*abs(distance))/320)
    left_speed = speed*1.5
    right_speed = speed*1.5
    if (distance < -threshold):  #turn right
        left_speed = speed + speedDif
        right_speed = speed
    elif (distance > threshold): #turn Left
        left_speed = speed
        right_speed = speed + speedDif
    robot.left(left_speed)
    robot.right(right_speed)
    #robot.right(0.5)
    print("Distance: ", distance, "left: ", left_speed, "right: ", right_speed)

global old_distance, prev_time
old_distance = 0
prev_time = 0
def captureFrames():
    global video_frame, thread_lock, old_distance, prev_time, stop_thread
    stop_thread = False 
    print(gstreamer_pipeline(flip_method=0))
    
    # Video capturing from OpenCV
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
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
                control_motor(distance)
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
        if stop_thread:
            print("Stop video capture")
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

