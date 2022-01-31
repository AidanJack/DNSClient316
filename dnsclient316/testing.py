import socket
import threading
import time

# Introducing fixed-length headers.
msg = "welcome to the server"


'''#Server sided things...
#AF.INET corresponds to IPv4, SOCK_STREAM corresponds to TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket is just an endpoint to send and receives data. sits at an IP address and port.
s.bind((socket.gethostname(), 5050))

while True:
    clientSocket, address = s.accept()
    print(f"Connected")
    clientSocket.send(bytes("Welcome to the server!", "utf-8"))
#Client sided things...

x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
x.connect(("132.0.0.132", 1234))

while True:
    # Doing it with small num of bytes and buffering this is good
    # so that you make sure that you receive everything
    # This can be done because this is incoming on a open stream of data.
    msg = x.recv(8) #takes in how many bytes you are willing to receive.
    print(msg.decode("utf-8")) #must pass the decode the type fo bytes used so that it knows how to decode them.
#Questions:
# what are utf-8 bytes??'''
