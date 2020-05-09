import serial

class jetbot:
    def __init__(self, _serialLink = "/dev/ttyACM0", _bandWidth = 9600):
        self.serialLink = serial.Serial(_serialLink, _bandWidth)

    def forward(self, speed = 1.0):
        speed = int(speed*255)


    def backward(self, speed = 1.0):
        speed = int(speed*255)

    def left(self, speed = 1.0):
        speed = int(speed*255)
        controlMsg = 'L' + str(speed) + '\n'
        self.serialLink.write(controlMsg.encode())
#        self.displaySerial()

    def right(self, speed = 1.0):
        speed = int(speed*255)
        controlMsg = 'R' + str(speed) + '\n'
        self.serialLink.write(controlMsg.encode())
#        self.displaySerial()

    def displaySerial(self):
        data = self.serialLink.readline()
        print(data)

