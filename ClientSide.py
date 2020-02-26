import socket
import sys
import time

import cv2
import numpy

server_address = "127.0.0.1"
server_port = 9568

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((server_address, server_port))
imagesize = 0
frame = bytearray()
currentreceived = 0


def showImage(by):
    print("SHOWING IMAGE")
    nparr = numpy.frombuffer(bytes(by), numpy.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow("Heh", image)
    frame.clear()
    currentreceived = 0
    cv2.waitKey(0)


while True:
    buffer, address = soc.recvfrom(1024)
    if (len(buffer) == 10):
        if (currentreceived > imagesize):
            showImage(frame)
        else:
            imagesize = int.from_bytes(buffer, byteorder="little")  ## Recieve image size
    else:
        if (currentreceived < imagesize):
            if (currentreceived + len(buffer) + 1 > imagesize):
                dif = imagesize - currentreceived
                currentreceived += dif
                for x in buffer[imagesize - dif:imagesize]:
                    frame.append(x)
            else:
                currentreceived += len(buffer) + 1
                if (len(buffer) > 0):
                    for x in buffer:
                        frame.append(x)
