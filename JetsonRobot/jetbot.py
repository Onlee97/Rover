import serial
import image_processing.lane_detection as ld
import cv2
import time

class Rover:
    def __init__(self, _serialLink = "/dev/ttyACM0", _bandWidth = 9600):
        self.serialLink = serial.Serial(_serialLink, _bandWidth)
        self.video_capture = None
        
        #Instance use to keep track of time loop
        self.old_distance = 0
        self.prev_time = 0

    def stop(self):
        self.left(0)
        self.right(0)

    def left(self, speed = 1.0):
        speed = min(1.0, speed)
        speed = max(-1.0, speed)
        speed = int(speed*255)
        controlMsg = 'L' + str(speed) + '\n'
        self.serialLink.write(controlMsg.encode())
#        self.displaySerial()

    def right(self, speed = 1.0):
        speed = min(1.0, speed)
        speed = max(-1.0, speed)
        speed = int(speed*255)
        controlMsg = 'R' + str(speed) + '\n'
        self.serialLink.write(controlMsg.encode())
#        self.displaySerial()

    def displaySerial(self):
        data = self.serialLink.readline()
        print(data)
    
    
    def startVideoCapture(self):
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
        self.video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
        print("Camera is ready to read")

    def control_motor(self, distance = 0, offset = -5):
        distance = distance - offset
        threshold = 20
        speed = 0.5
        s = 0.4
        p = 1
        speedDif = 1 + 2*abs(distance)/320
        left_speed = s
        right_speed = s
        if (distance < -threshold):  #turn right
            left_speed = speed*speedDif
            right_speed = speed
        elif (distance > threshold): #turn Left
            right_speed = speed*speedDif
            left_speed = speed

        self.left(left_speed)
        self.right(right_speed)
        print("Distance: ", distance, "left: ", left_speed, "right: ", right_speed)


    def follow_lane(self):
        if self.video_capture == None:
            self.startVideoCapture()
        while self.video_capture.isOpened():
            return_key, frame = self.video_capture.read()
            if not return_key:
                break
            try:
                #Apply lane detection, return the processed image and the distance 
                #between the robot direction and center of lane
                frame, distance = ld.detect_lane(frame)

                #Sending control signal to MotorDriver in a constant rate loop
                cur_time = time.time()
                if (distance != self.old_distance and cur_time-self.prev_time >= 0.1):
                    self.prev_time = cur_time
                    self.control_motor(distance)
                    self.old_distance = distance
            except ValueError:
                print("No lane Detected")
                #break
            cv2.imshow('lane', frame)
            key = cv2.waitKey(30) & 0xff
            if key == 27:
                print("stop")
                break
        self.stop()
        cv2.destroyAllWindows()
        self.video_capture.release()






























