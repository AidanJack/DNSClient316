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
    print(args.retries)
    print(args.mx)
    print(args.server)
    print(args.domain)


def addTerminalArgs():
    parser.add_argument("-t", "--timeout", default=5, help="Length of time in ms until request times out")
    parser.add_argument("-r", "--retries", default=3, help="Max Number of times the request will be attempted")
    parser.add_argument("-p", "--port", default=53, help="UDP port number of the server to connect to")
    parser.add_argument("-mx", "-nx", default="A", help="Specifies whether a mail server or a name server query will be sent."
                                           "IP querry sent if neither are provided.")
    parser.add_argument("server", help="IPv4 server address in the format a.b.c.d")
    parser.add_argument("domain", help="domain name to query for")


def initializeSocket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

#r_type: 1->IP 2->CNAME 3->MX 4->NS
def outputFormatting(response_received, r_type, responseIP, RTT, retries, n_answers):
    output = f"\nDNS Client sending request for\n{args.domain} Server: {responseIP}\nRequest type: {args.mx}\n\n"
    if response_received:
        output += f"Response received after {RTT} seconds ({retries} retries)\n\n***Answer Section ({n_answers} records)***\n\n"
        if r_type == 1:
            output += f"IP\t[ip address]\t[seconds can cache]\t[auth | nonauth]\n"
        elif r_type == 2:
            output += f"CNAME <tab> [alias] <tab> [seconds can cache] <tab> [auth | nonauth]\n"
    return output

def parseResponseData(received_packet):
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    addTerminalArgs()
    args = parser.parse_args()
    printArgs()
    packet = DNS.generateDNSHeader()
    packet.extend(DNS.generateDNSQuestions(args.domain))

    serverIP = args.server.replace("@", "").replace(" ", "") 

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# Initializes a socket object and connects to the server.
    
    response_time = 0
    num_retries = 0
    addr = (serverIP, args.port)
    retried_max = False
    
    print("Packet sent!", packet)

    for i in range(args.retries):
        sock.sendto(packet, addr) 
        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time > args.timeout:
                print ("Request timed out")
                num_retries = num_retries+1
                break
            received_packet, _ = sock.recvfrom(4096)
            print("Data received!: ", received_packet)
            #end_time = time.time()
            flag = True
            break
        if flag == True:
            break
        if i == args.retries - 1:
            retried_max = True

    if retried_max == True: #Case 1: Server never received
        pass #Do some printing
    else:                   # Case 2: Recevied response
        #parseResponseData()
        response_time = end_time-start_time
        print(outputFormatting(True, 1, "1.2.3.4", response_time, num_retries, 1)) # replace fillers with answers parsed from response


    for i in range(len(packet)):
        print(packet[i])

    print("-----------")
    for i in range(len(received_packet)):
        print(received_packet[i])

    """
    DNS Client sending request for 
    [name]Server: [server IP address] 
    Request type: [A | MX | NS]

    # Where the fields in square brackets are replaced by appropriate values. Then, subsequent lines should summarize the performance and content of the response. When a valid response is received, the firstline should read:

    Response received after [time] seconds ([num-retries] retries) # Print this if response is received

    # If the response contains records in the Answer section then print:

    ***Answer Section ([num-answers] records)***

    # Then, if the response contains A (IP address) records, each should be printed on a line of the form: 

    IP <tab> [ip address] <tab> [seconds can cache] <tab> [auth | nonauth]

    Where <tab> is replaced by a tab character. Similarly, if it receives CNAME, MX, or NS records, they should be printed on lines of the form:

    CNAME <tab> [alias] <tab> [seconds can cache] <tab> [auth | nonauth]

    MX <tab> [alias] <tab> [pref] <tab> [seconds can cache] <tab> [auth | nonauth] 

    NS <tab> [alias] <tab> [seconds can cache] <tab> [auth | nonauth]

    # If the response contains records in the Additional section then also print:

    ***Additional Section ([num-additional] records)***

    # along with appropriate lines for each additional record that matches one of the types A, CNAME, MX, or NS. You can ignore any records in the Authority section for this lab.
    # If no record is found then a line should simply be printed saying

    NOTFOUND

    # If any errors occur during execution then lines should be printed

    saying ERROR <tab> [description of error]

    # Be specific with your error messages. Some example of errors your DNS client may output are:

    21January2022 3 of 4
    ECSE316–Signals and Networks Winter2022

    ERROR <tab> Incorrect input syntax: [description of specific problem] 
    ERROR <tab> Maximum number of retries [max-retries] exceeded
    ERROR <tab> Unexpected response [description of unexpected response content]
    """










    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
