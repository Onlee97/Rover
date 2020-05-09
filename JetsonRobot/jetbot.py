import serial

class jetbot:
    def __init__(self, _serialLink = "/dev/ttyACM0", _bandWidth = 9600):
        self.serialLink = serial.Serial(_serialLink, _bandWidth)

    def forward(self, speed = 1.0):
        speed = int(speed*255)


    def backward(self, speed = 1.0):
        speed = int(speed*255)

    def leftWheel(self, speed = 1.0):
        speed = int(speed*255)
        controlMsg = "L" + str(speed)
        self.serialLink.write(controlMsg.encode())


    def rightWheel(self, speed = 1.0):
        speed = int(speed*255)
        controlMsg = "R" + str(speed)
        self.serialLink.write(controlMsg.encode())



