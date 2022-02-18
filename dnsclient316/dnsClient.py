from distutils.log import error
import socket
import time
import sys
import random
import re
from dns import DNS
from argumentparser import Parser


def main():
    # Initializes Terminal Arguments Parser
    args = Parser(sys.argv)
    serverIP = args.server.replace("@", "").replace(" ", "") 

    # Generates the query packet
    packet = DNS.generateDNSHeader()
    packet.extend(DNS.generateDNSQuestions(args.domain, args.queryType))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    
    response_time = 0
    num_retries = 0
    addr = (serverIP, args.port)
    retried_max = False
    flag = False
    names = []
    pattern_domain = "([0-9a-zA-Z]*.)*([0-9a-zA-Z]*)+.[0-9a-zA-Z]*"
    names.append(args.domain)
    print(f"\nDNS Client sending request for\n{args.domain} Server: {serverIP}\nRequest type: {args.queryType}\n\n")

    for i in range(args.retries):
        sock.sendto(packet, addr) # Send packet and start timer for timeout
        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time > args.timeout: # If time from send to receive exceeds timeout resend and retry
                num_retries = num_retries+1
                break
            try:
                received_packet, _ = sock.recvfrom(4096)
            except:
                continue
            flag = True
            break
        if flag == True:
            break
        if i == args.retries - 1:
            retried_max = True
    
    if retried_max == True: #Case 1: Did not receive response
        print(f"ERROR\tMaximum number of retries {args.retries} exceeded")
    
    else:                   # Case 2: Recevied response
        response_time = end_time-start_time
        num_answers = DNS.parseAnsCount(received_packet)
        output = f"Response received after {round(response_time, 3)} seconds ({num_retries} retries)\n\n***Answer Section ({num_answers} records)***\n\n"
        temp_i = None
        try:
            if DNS.raParser(received_packet):
                raise RuntimeError(f"Error: \t server does not support recursive query")
        except Exception as e:
            print(e)
            sys.exit()
        for i in range(num_answers):
            try:
                #response_fields = (r_type, r_class, r_ttl, rdlength, record, pref, record, start_index of next record)
                response_fields = answerParser(packet, received_packet, names, temp_i)
            except Exception as e:
                print(e)
                sys.exit()
            if re.search(pattern_domain, response_fields[6]):
                names.append(response_fields[6])
            output += outputFormatting(True, response_fields[0], response_fields[4], response_fields[2], 
            num_retries, DNS.responseCodeParser(received_packet), DNS.parseAuthoritative(received_packet),
            response_fields[5], response_fields[6])
            temp_i = response_fields[7]
        print(output)

"""
Replaces output string placeholders with values

:param response_received_bool: True if a response was recevied, else False, bool
:param r_type: Type of response record, 1->IP 2->CNAME 3->MX 4->NS, int
:param responseIP: IP address of the query domain name, string
:param TTL: Allowed time in seconds to cache to IP, int
:param RTT: Response time from sent query to response received, int
:param retries: Number of times to resend query, int
:param n_answers: Number of response records received, int
:param error_code: Error code provided by the server response, int
:param auth: Server authoritative, "Auth" or "nonauth", string
:param pref: Level of preference of mail address, int
:Returns: formatted f string ready for output, string
"""
def outputFormatting(response_received_bool, r_type, responseIP, TTL, retries, error_code, auth, pref, record):
    output = f""
    if response_received_bool:
        if r_type == 1:
            output += f"IP \t {responseIP} \t {TTL} \t {auth}\n"
        elif r_type == 5:
            output += f"CNAME \t {record} \t {TTL} \t {auth}\n"
        elif r_type == 15:
            output += f"MX \t {record} \t {pref} \t {TTL} \t {auth}\n"
        elif r_type == 2:
            output += f"NS \t {record} \t{TTL} \t {auth}\n"
    elif error_code == 1:
        output += f"ERROR\tFormat error: the name server was unable to interpret the query\n" 
    elif error_code == 2: 
        output += f"ERROR\tServer failure: the name server was unable to process this query due to a problem with the name server\n"
    elif error_code == 3:
        output += f"ERROR\tNot found: The domain name referenced in the query does not exist\n"
    elif error_code == 4:
        output += f"ERROR\tNot implemented: The name server does not support the requested kind of query\n"
    elif error_code == 5: 
        output += f"ERROR\tRefused: The name server refuses to perform the requested operation for policy reasons\n"
    elif error_code == 6: 
        output += f"ERROR\tMaximum number of retries {retries} exceeded"
        
    return output

"""
Formats a name from the response packet into a valid string

:param response: Response packet received, bytearray
:param index: Starting index of a name field, int
:Returns: Formatted name, string
"""
def parseNameField(response, index):
    name = ""
    oldIndex = index
    flag = False
    loop_check = 0
    while int(response[index]) != 0:
        if(loop_check >= 100):
            raise RuntimeError(f"Error: \t Unexpected response: response packet contains invalid format")
        # Detects if the cur byte is the start of a pointer
        if int(response[index]) - 192 >= 0: # 192 = 11000000 in binary
            flag = True
            oldIndex = index + 2
            temp = response[index]
            temp = temp << 8
            temp += response[index + 1]
            index = int(temp) - 49152 # 49152 = 11000000 00000000 in binary
    
        token_length = int(response[index])
        index += 1
        #print("Before for: ", response[index])
        for i in range(token_length):
            name += chr(response[index])
            index += 1
        if flag == True and int(response[index]) == 0: # Hit end of pointer
            index = oldIndex
            break
        name += "."
        loop_check += 1
    if name[-1] == ".":
        name = name[:-1]
    return name

"""
Finds the length of a name field

:param response: Response packet received, bytearray
:Returns: Length of name field, int
"""
def getRNameLength(response, name_i):
    if int(response[name_i]) - 192 >= 0:
        return 2
    else:
        while response[name_i] != 0:
            name_i += 1
        return i+1
        

"""
Retrieves all the key information from the respponse section of the received packet

:param queryPacket: Query packet sent, bytearray
:param received_packet: Response packet received, bytearray
:param queryName: Domain name in the query, string
:Returns: Key values in answer section of response, 6-tuple
"""
def answerParser(queryPacket, received_packet, nameList, i):
    if i == None:
        start_index = len(queryPacket)
    else:
        start_index = i
    name = parseNameField(received_packet, start_index)
    try:
        if not name in nameList:
            raise  RuntimeError("Error: response is unrelated to the query domain")
    except Exception as e:
        print(e)
        sys.exit()

    start_index += getRNameLength(received_packet, start_index)
    r_type = received_packet[start_index]  
    start_index += 1
    r_type = r_type << 8
    r_type += received_packet[start_index]
    start_index += 1

    r_class = received_packet[start_index]
    start_index += 1
    r_class = r_class << 8
    r_class += received_packet[start_index]
    start_index += 1

    r_cache_time = received_packet[start_index]
    for i in range(3):
        start_index += 1
        r_cache_time = r_cache_time << 8
        r_cache_time += received_packet[start_index]
    start_index += 1

    r_rdlength = received_packet[start_index]
    start_index += 1
    r_rdlength = r_rdlength << 8
    r_rdlength = received_packet[start_index]
    start_index += 1
        
    record = ""
    pref = None
    ip = ""
    if int(r_type) == 1:
        temp_index = start_index
        ip += str(received_packet[temp_index])
        for i in range(3):
            ip += "."
            temp_index += 1
            ip += str(received_packet[temp_index])

    elif int(r_type) == 2:
        record = parseNameField(received_packet, start_index)
    elif int(r_type) == 5:
        record = parseNameField(received_packet, start_index)
    elif int(r_type) == 15:
        pref = received_packet[start_index]
        pref = pref << 8
        pref += received_packet[start_index + 1]
        start_index += 2
        record = parseNameField(received_packet, start_index)

    return (r_type, r_class, r_cache_time, r_rdlength, ip, pref, record, start_index + r_rdlength)


if __name__ == '__main__':
    main()
