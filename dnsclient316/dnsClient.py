import socket
import time
import sys
import threading
import argparse
import random
from dns import DNS
parser = argparse.ArgumentParser()


def printArgs():
    print(args.timeout)
    print(args.port)
    print(args.mx)
    print(args.server)
    print(args.domain)


def addTerminalArgs():
    parser.add_argument("-t", "--timeout", help="Length of time in ms until request times out")
    parser.add_argument("-r", "--max-retries", help="Max Number of times the request will be attempted")
    parser.add_argument("-p", "--port", default=53, help="UDP port number of the server to connect to")
    parser.add_argument("-mx", "-nx", default="ip", help="Specifies whether a mail server or a name server query will be sent."
                                           "IP querry sent if neither are provided.")
    parser.add_argument("server", help="IPv4 server address in the format a.b.c.d")
    parser.add_argument("domain", help="domain name to query for")


def initializeSocket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    addTerminalArgs()
    args = parser.parse_args()
    printArgs()
    packet = DNS.generateDNSHeader()
    packet.extend(DNS.generateDNSQuestions(args.domain))

    serverIP = args.server.replace("@", "").replace(" ", "")  # Initializes a socket object and connects to the server.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    try:
        sock.connect((serverIP, args.port))
    except RuntimeError:
        print("Could not connect to ", serverIP)
    else:
        print("Connection Established with ", serverIP)
    try:
        sock.send(packet)
    except socket.error:
        print("Query not sent")
    print("Packet sent!", packet)
    while True:
        received_packet = sock.recv(1024)
        print("Data: ", received_packet)
        if len(received_packet) <= 0:
            break
    sock.close()










# See PyCharm help at https://www.jetbrains.com/help/pycharm/
