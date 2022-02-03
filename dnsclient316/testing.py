import socket
import threading
import time
import random
myBytes = bytearray(b'\xEF\xEF')
for i in range(2):
    r = random.randint(0, 255)
    print(r)
    myBytes.append(r)


myBytes.append(255)

myBytes.append(134)


for i in range(len(myBytes)):
    print(myBytes[i])





# Introducing fixed-length headers.
#msg = "welcome to the server"

