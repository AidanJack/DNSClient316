from distutils.log import error
import socket
import time
import sys
import random
from dns import DNS
from argumentparser import Parser

def main():
        args = Parser(sys.argv)
    packet = DNS.generateDNSHeader()
    packet.extend(DNS.generateDNSQuestions(args.domain))

    serverIP = args.server.replace("@", "").replace(" ", "") 

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# Initializes a socket object and connects to the server.
    
    response_time = 0
    num_retries = 0
    addr = (serverIP, args.port)
    retried_max = False
    print(f"\nDNS Client sending request for\n{args.domain} Server: {serverIP}\nRequest type: {args.queryType}\n\n")

    for i in range(args.retries):
        sock.sendto(packet, addr) 
        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time > int(args.timeout):
                num_retries = num_retries+1
                break
            received_packet, _ = sock.recvfrom(4096)
            flag = True
            break
        if flag == True:
            break
        if i == int(args.retries) - 1:
            retried_max = True

    if retried_max == True: #Case 1: Server never received
        print(f"ERROR\tMaximum number of retries {args.retries} exceeded")
    else:                   # Case 2: Recevied response
        response_fields = answerParser(packet, received_packet, args.domain) #r_type ->0, r_class->1, r_ttl->2, rdlength->3, record->4, pref->5
        response_time = end_time-start_time
        num_answers = parseAnsCount(received_packet)
        print(outputFormatting(True, response_fields[0], response_fields[4], response_fields[2], response_time, 
        num_retries, num_answers, responseCodeParser(received_packet), parseAuthoritative(received_packet), response_fields[5]))


def initializeSocket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s


#r_type: 1->IP 2->CNAME 3->MX 4->NS
def outputFormatting(response_received_bool, r_type, responseIP, TTL, RTT, retries, n_answers, error_code, auth, pref):
    output = f""
    if response_received_bool:
        output += f"Response received after {RTT} seconds ({retries} retries)\n\n***Answer Section ({n_answers} records)***\n\n"
        if r_type == 1:
            output += f"IP\t{responseIP}\t{TTL}\t{auth}\n"
        elif r_type == 2:
            output += f"CNAME <tab> [alias] <tab> {TTL}\t{auth}\n"
        elif r_type == 3:
            output += f"MX <tab> [alias] <tab> {pref}\t{TTL}\t{auth}\n"
        elif r_type == 4:
            output += f"NS <tab> [alias] <tab> {TTL}\t{auth}\n"
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
        output += f"ERROR\tMaximum number of retries {args.retries} exceeded"
        
    return output


def parseAnsCount(received_packet):
    msbits = int(received_packet[6])
    msbits = msbits << 8
    lsbits = received_packet[7]
    anscount = msbits + lsbits
    return anscount


def parseAuthoritative(received_packet):
    aa_byte = bin(received_packet[2])
    if len(aa_byte)<5:
        return "nonauth"
    if int(aa_byte[-3]) == 0: # AA bit in header
        return "nonauth"
    else:
        return "auth"


def parseRecursive(received_packet):
    ra_byte = bin(received_packet[3])
    if len(ra_byte)<10 or int(ra_byte[2]) == 0:
        return False
    else:
        return True


#when converted to binary number --> string with form 0bxxxxxxe
def responseCodeParser(received_packet):
    rcode_byte = bin(received_packet[1])
    error_code = 0
    rcode0 = int(rcode_byte[-1])
    rcode1 = int(rcode_byte[-2]) << 1
    rcode2 = int(rcode_byte[-3]) << 2
    rcode3 = int(rcode_byte[-4]) << 3
    error_code = rcode0 + rcode1 + rcode2+ rcode3
    return error_code #if not 0 - return appropriate error message


def parseNameField(response, index):
    name = ""
    oldIndex = index
    flag = False
    #print("starts at ", index)
    while int(response[index]) != 0:
        if int(response[index]) - 192 >= 0:
            flag = True
            oldIndex = index + 2
            temp = response[index]
            temp = temp << 8
            temp += response[index + 1]
            index = int(temp) - 49152 #not sure if this index is indexed by 0 or 1
    
        token_length = int(response[index])
        index += 1
        for i in range(token_length):
            #print("in for loop ", index)
            #print("Name is : ", name)
            name += chr(response[index])
            index += 1
        if flag == True and int(response[index]) == 0: # Hit end of pointer
            index = oldIndex
        name += "."
    return name[:-1]


def getRNameLength(response):
    if int(response[0]) - 192 >= 0:
        return 2
    else:
        for i in range(len(response)):
            if int(response[i]) == 0:
                return i+1


def answerParser(queryPacket, received_packet, queryName):
    answer = received_packet[len(queryPacket):]
    return_list = []
    name = parseNameField(received_packet, len(queryPacket))
    if(name != queryName):
        return "Error"
    else:
        start_index = getRNameLength(answer)
        r_type = answer[start_index]  
        start_index += 1
        r_type = r_type << 8
        r_type += answer[start_index]
        start_index += 1

        r_class = answer[start_index]
        start_index += 1
        r_class = r_class << 8
        r_class += answer[start_index]
        start_index += 1

        r_cache_time = answer[start_index]
        for i in range(3):
            start_index += 1
            r_cache_time = r_cache_time << 8
            r_cache_time += answer[start_index]
        start_index += 1

        r_rdlength = answer[start_index]
        start_index += 1
        r_rdlength = r_rdlength << 8
        r_rdlength = answer[start_index]
        start_index += 1

        record = 0
        pref = None
        if int(r_type) == 1:
            ip = ""
            record = answer[start_index]
            ip += str(record)
            for i in range(3):
                ip += "."
                start_index += 1
                record = answer[start_index]
                ip += str(record)

            start_index += 1
        elif int(r_type) == 2:
            record = parseNameField(answer, start_index)
        elif int(r_type) == 5:
            record = parseNameField(answer, start_index)
        elif int(r_type) == 15:
            pref = answer[start_index]
            pref = pref << 8
            pref += answer[start_index + 1]
            start_index += 2
            record = parseNameField(answer, start_index)

        return (r_type, r_class, r_cache_time, r_rdlength, ip, pref)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
