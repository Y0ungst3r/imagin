#import sht85
import time
import datetime
import math
import serial
import socket

s = socket.socket()
TCP_IP = '192.168.0.216'
TCP_PORT = 12401
BUFFER_SIZE = 1024
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    c,addr = s.accept()

    string = c.recv(1024).decode()
    print(string)



