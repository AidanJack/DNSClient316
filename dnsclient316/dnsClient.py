import socket
import time
import sys
import threading
import argparse
import random
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

def generatePacketID():
    headerID = bytearray()
    for i in range(2):
        r = random.randint(0, 255)
        headerID.append(r)
    return headerID

def generateQueryFlags():
    flags = bytearray()
    flags.append(1)
    flags.append(0)
    return flags

def generateQDCount():
    qCount = bytearray()
    qCount.append(0)
    qCount.append(1)
    return qCount

def generateANCount():
    aCount = bytearray()
    aCount.append(0)
    aCount.append(0)
    return aCount

def generateNSCount():
    nCount = bytearray()
    nCount.append(0)
    nCount.append(0)
    return nCount

def generateARCount():
    aCount = bytearray()
    aCount.append(0)
    aCount.append(0)
    return aCount

def generateNRCount():
    nrCount = bytearray()
    nrCount.append(0)
    nrCount.append(0)
    return nrCount

# Generates  and returns a formatted DNS request Header.
def generateDNSHeader():
    header = bytearray()
    header.append(generatePacketID())
    header.extend(generateQueryFlags()) # For us it should always be 1, and 0
    header.extend(generateQDCount()) # QDCount is always 1 for us
    header.extend(generateANCount()) # Default 0, only regarded in response packets
    header.extend(generateNSCount())
    header.extend(generateNRCount())
    return header

def generateQName(name):
    qName = bytearray()
    tokens = name.split('.')
    for token in tokens:
        token = token.replace(" ", "")
        qName.append(len(token))
        for char in token:
            qName.append(char)
    qName.append(0)
    return qName

def generateQType():
    qType = bytearray() #needs to choose between 1, 2, and 3. for now use 1 since default ip type.
    qType.append(0)
    qType.append(1)
    return qType

def generateQClass():
    qClass = bytearray()
    qClass.append(0)
    qClass.append(1)
    return qClass

def generateDNSQuestions(name):
    questions = bytearray()
    questions.extend(generateQName(name))
    return questions

def sendDNSRequest():
    print("Sent")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    addTerminalArgs()
    args = parser.parse_args()
    printArgs()

    serverIP = args.server.replace("@", "")
    sock = initializeSocket(serverIP, args.port)  # Initializes a socket object and connects to the server.

    packet = generateDNSHeader()
    packet.extend(generateDNSQuestions(args.domain))
    packet.extend(generateQType())
    packet.extend(generateQClass())





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
