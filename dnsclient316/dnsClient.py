import socket
import time
import sys
import threading
import argparse
parser = argparse.ArgumentParser()


def printArgs():
    print(args.timeout)
    print(args.port)
    print(args.server)
    print(args.domain)


def addTerminalArgs():
    parser.add_argument("-t", "--timeout", help="Length of time in ms until request times out")
    parser.add_argument("-r", "--max-retries", help="Max Number of times the request will be attempted")
    parser.add_argument("-p", "--port", default=53, help="UDP port number of the server to connect to")
    parser.add_argument("-mx", "-nx", default="ip", help="Specifies whether a mail server or a name server query will be sent."
                                           "IP querry sent if neither are provided.")
    parser.add_argument("server", help="IPv4 server address in the format a.b.c.d")
    parser.add_argument("domain", help="domain nam eto query for")


def initializeSocket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s
# Generates  and returns a formatted DNS request Header.
def generateDNSHeader():
    header = ""
    return header

def sendDNSRequest():
    print("Sent")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    addTerminalArgs()
    args = parser.parse_args()
    printArgs()

    serverIP = args.server.replace("@", "")
    sock = initializeSocket(serverIP, args.port)  # Initializes a socket object and connects to the server.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
