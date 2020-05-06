import cv2
import numpy as np
import sys
from jetbot import Robot
import time



def detect_edges(lane_image):
	gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
	blur = cv2.GaussianBlur(gray,(5, 5),0)
	canny = cv2.Canny(blur, 200, 240)
	return canny

def region_of_interest(canny):
	height, width = canny.shape
	mask = np.zeros_like(canny)
	polygon = np.array([[
		(0, height*1/2),
		(width, height*1/2),
		(width, height),
		(0, height),
		]], np.int32)
	cv2.fillPoly(mask, polygon, 255)
	cropped_edges = cv2.bitwise_and(canny, mask)
	return cropped_edges

def detect_line_segments(cropped_edges):
    rho = 2
    angle = np.pi / 180
    min_threshold = 50
    line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, np.array([]),minLineLength=50, maxLineGap=25)
    return line_segments


#x = 640
#y = 360
x = 0
y = 0
center_point = []
center_point.append([[x,y]])

def average_slope_intercept(frame, line_segments):
    lane_lines = []
    center_line = []
    # center_point = []
    global center_point
    distance_line = []
    if line_segments is None:
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)
    right_region_boundary = width * boundary 

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)

    center_line.append(center_lineMake(frame))

    if len(left_fit) > 0 and len(right_fit) > 0:
    	center_point = []
    	lane_lines.append(make_points(frame, left_fit_average))
    	lane_lines.append(make_points(frame, right_fit_average))
    	center_point.append(midpoints(lane_lines))
    
    if len(left_fit) > 0 and len(right_fit) <= 0:
    	center_point = []
    	lane_lines.append(make_points(frame, left_fit_average))
    	lane_lines.append(right_line(frame, left_fit_average))
    	center_point.append(midpoints(lane_lines))
    
    if len(right_fit) > 0 and len(left_fit) <= 0:
    	center_point = []
    	lane_lines.append(make_points(frame, right_fit_average))
    	lane_lines.append(left_line(frame, right_fit_average))
    	center_point.append(midpoints(lane_lines))
    # else:
    # 	center_point = []
    # 	center_point.append([[int(width*1/2),int(height*1/2)]])

    distance_line.append(distance_lineMake(frame, center_point))
    return lane_lines, center_point, center_line, distance_line

distance = 0
def distance_lineMake(frame, center_point):
    height, width, _ = frame.shape
    circle1 = center_point[0]
    circle2 = circle1[0]
    y2 = circle2[1]
    y1 = circle2[1]
    x1 = circle2[0]
    x2 = int(width*1/2)
    global distance
    distance = x2 - x1
    #print(distance)
    return [[x1, y1, x2, y2]]

def center_lineMake(frame):
	height, width, _ = frame.shape
	y1 = 0
	y2 = height
	x1 = int(width*1/2)
	x2 = int(width*1/2)
	return [[x1, y1, x2, y2]]

def left_line(frame, opposite_line):
	height, width, _ = frame.shape
	slope, intercept = opposite_line
	y1 = height
	y2 = int(y1 * 1 / 2)
	x1 = 0
	x2 = 0
	return [[x1, y1, x2, y2]]

def right_line(frame, opposite_line):
	height, width, _ = frame.shape
	slope, intercept = opposite_line
	y1 = height
	y2 = int(y1 * 1 / 2)
	x1 = width-1
	x2 = width-1
	return [[x1, y1, x2, y2]]

def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height
    y2 = int(y1 * 1 / 2)
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def midpoints(lane_lines):
	lane_lines = lane_lines
	leftcoords = lane_lines[0]
	leftcoords1 = leftcoords[0]
	Lx = leftcoords1[2]
	Ly = leftcoords1[3]
	rightcoords = lane_lines[1]
	rightcoords1 = rightcoords[0]
	Rx = rightcoords1[2]
	Ry = rightcoords1[3]
	Cx = int((Lx + Rx)/2)
	Cy = int((Ly + Ry)/2)
	global filtered_x
	filtered_x = exponential_filter(filtered_x, Cx, 0.1)
	Cx = int(filtered_x)
	return [[Cx, Cy]]

filtered_x = 0

def exponential_filter(filtered_x, x, alpha):
	filtered_x = alpha*x + (1-alpha)*filtered_x
	return filtered_x

def detect_lane(frame):
	global distance
	edges = detect_edges(frame)
	cropped_edges = region_of_interest(edges)
	line_segments = detect_line_segments(cropped_edges)
	lane_lines, center_point, center_line, distance_line = average_slope_intercept(frame, line_segments)
	lane_lines_image = display_lines(frame, lane_lines, center_point, center_line, distance_line)
	return lane_lines_image, distance

def display_lines(frame, lines, points, center_line, distance_line, distance_color = (255, 0, 0), center_color = (0, 255, 0), line_color=(0, 255, 0), point_color = (0, 0, 255), line_width=2):
    line_image = np.zeros_like(frame)
    for point in points:
        for Cx, Cy in point:
        	cv2.circle(line_image, (Cx, Cy), 10, point_color, line_width)
    for line in center_line:
        for x1, y1, x2, y2 in line:
        	cv2.line(line_image, (x1, y1), (x2, y2), line_color, 1)
    for line in distance_line:
    	for x1, y1, x2, y2 in line:
    		cv2.line(line_image, (x1, y1), (x2, y2), distance_color, 1)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.9, line_image, 1, 1)
    return line_image

def show_video():
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("output4.mp4")
    while(True):
        _, frame = cap.read()
        detected = detect_lane(frame)
        cv2.imshow('result', detected)
        #cv2.imshow('result', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;

    cap.release()
    cv2.destroyAllWindows()

w=320
h=180
def gstreamer_pipeline(
    #capture_width=1280,
    #capture_height=720,
    #display_width=1280,
    #display_height=720,
    framerate=15,
    capture_width=w,
    capture_height=h,
    display_width=w,
    display_height=h,
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

robot = Robot()
def control_motor(distance):
    threshold = 30
    speed = 0.1
    speedDif = speed*((2*abs(distance))/w)
    print(distance)
    if (distance < -threshold):  #turn right
        robot.left_motor.value = speed+speedDif
        robot.right_motor.value = speed
    elif (distance > threshold): #turn Left
        robot.right_motor.value = speed+speedDif
        robot.left_motor.value = speed
    else:
        robot.set_motors(speed*1.5, speed*1.5)

def show_camera():
	print(gstreamer_pipeline(flip_method=0))
	cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
	if cap.isOpened():
		window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
		# Window
		while cv2.getWindowProperty("CSI Camera", 0) >= 0:
			ret_val, img = cap.read()

			try:
				img, distance = detect_lane(img)
				control_motor(distance)
			except:
				print("Error")

			cv2.imshow("CSI Camera", img)
			# This also acts as
			keyCode = cv2.waitKey(30) & 0xFF
			# Stop the program on the ESC key
			if keyCode == 27:
				break
		cap.release()
		cv2.destroyAllWindows()
	else:
		print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
    #show_video()

