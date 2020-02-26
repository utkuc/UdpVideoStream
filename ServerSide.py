import socket
import cv2

server_address = "127.0.0.1"
server_port = 9568
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
capture = cv2.VideoCapture(0)


def sendImageSize(size):
    if (soc):
        buf = size.to_bytes(10, byteorder='little')
        soc.sendto(buf, (server_address, server_port))


x = 1
while (1):  # Each loop is 1 frame
    ret, frame = capture.read()
    data = cv2.imencode(".jpg", frame)[1].tostring()
    imagelength = len(data)  ## Size of 1 frame
    bufferSize: int = 1024
    buffer = bytearray()
    count = 0
    if (imagelength > 0):
        sendImageSize(imagelength)  # Send size of video image for 1 frame.
        lowbound = 0
        highbound = bufferSize - 1
        while (imagelength > 0):
            imagelength -= bufferSize
            buffer = data[lowbound:highbound]
            soc.sendto(buffer, (server_address, server_port))
            lowbound += bufferSize
            if (highbound + bufferSize > len(data)):
                highbound += imagelength
            else:
                highbound += bufferSize
        x = 0
