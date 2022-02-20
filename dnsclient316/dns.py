import random
class DNS:
    @staticmethod
    def generatePacketID():
        headerID = bytearray()
        for i in range(2):
            r = random.randint(0, 255)
            headerID.append(r)
        return headerID

    @staticmethod
    def generateQueryFlags():
        flags = bytearray("", "UTF-32-BE")
        flags.append(1)
        flags.append(0)
        return flags

    @staticmethod
    def generateQDCount():
        qCount = bytearray("", "UTF-32-BE")
        qCount.append(0)
        qCount.append(1)
        return qCount

    @staticmethod
    def generateANCount():
        aCount = bytearray("", "UTF-32-BE")
        aCount.append(0)
        aCount.append(0)
        return aCount

    @staticmethod
    def generateNSCount():
        nCount = bytearray("", "UTF-32-BE")
        nCount.append(0)
        nCount.append(0)
        return nCount

    @staticmethod
    def generateARCount():
        aCount = bytearray("", "UTF-32-BE")
        aCount.append(0)
        aCount.append(0)
        return aCount

    @staticmethod
    def generateNRCount():
        nrCount = bytearray("", "UTF-32-BE")
        nrCount.append(0)
        nrCount.append(0)
        return nrCount

    @staticmethod
    # Generates  and returns a formatted DNS request Header.
    def generateDNSHeader():
        header = bytearray("", "UTF-32-BE")
        header.extend(DNS.generatePacketID())
        header.extend(DNS.generateQueryFlags())  # For us it should always be 1, and 0
        header.extend(DNS.generateQDCount())  # QDCount is always 1 for us
        header.extend(DNS.generateANCount())  # Default 0, only regarded in response packets
        header.extend(DNS.generateNSCount())
        header.extend(DNS.generateNRCount())
        return header

    @staticmethod
    def generateQName(name):
        qName = bytearray("", "UTF-32-BE")
        tokens = name.split('.')
        for token in tokens:
            token = token.replace(" ", "")
            qName.append(len(token))
            for char in token:
                qName.extend(char.encode("ascii"))
        qName.append(0)
        return qName

    @staticmethod
    def generateQType(q_type): 
        qType = bytearray("", "UTF-32-BE")  # needs to choose between 1, 2, and 15.
        if q_type == "mx":
            qType.append(0)
            qType.append(15)
        elif q_type == "ns":
            qType.append(0)
            qType.append(2)
        else:
            qType.append(0)
            qType.append(1)
        return qType

    @staticmethod
    def generateQClass():
        qClass = bytearray("", "UTF-32-BE")
        qClass.append(0)
        qClass.append(1)
        return qClass

    @staticmethod
    def generateDNSQuestions(name, q_type):
        questions = bytearray("", "UTF-32-BE")
        questions.extend(DNS.generateQName(name))
        questions.extend(DNS.generateQType(q_type))
        questions.extend(DNS.generateQClass())
        return questions

    """
    Finds the number of answers in the response packet

    :param received_packet: Response packet received, bytearray
    :Returns: Number of answers in response packet, int 
    """
    @staticmethod
    def parseAnsCount(received_packet):
        msbits = int(received_packet[6])
        msbits = msbits << 8
        lsbits = received_packet[7]
        anscount = msbits + lsbits
        return anscount
    """
    Retrieves the authoritative flag

    :param received_packet: Response packet received, bytearray
    :Returns: "auth" if server is authoritative, else: "nonauth", string
    """
    @staticmethod
    def parseAuthoritative(received_packet):
        aa_byte = bin(received_packet[2])
        if len(aa_byte)<5:
            return "nonauth"
        if int(aa_byte[-3]) == 0: # AA bit in header
            return "nonauth"
        else:
            return "auth"

    """
    Parses the response error code

    :param received_packet: Response packet received, bytearray
    :Returns: Error code, 0->no error, !=0->some error, int
    """
    #when converted to binary number --> string with form 0bxxxxxxe
    @staticmethod
    def responseCodeParser(received_packet):
        rcode_byte = bin(received_packet[3])
        error_code = 0
        if len(rcode_byte) == 3:
            rcode0 = int(rcode_byte[-1])
            return rcode0
        elif len(rcode_byte) == 4:
            rcode0 = int(rcode_byte[-1])
            rcode1 = int(rcode_byte[-2]) << 1
            error_code = rcode0 + rcode2
            return error_code
        elif len(rcode_byte) == 5:
            rcode0 = int(rcode_byte[-1])
            rcode1 = int(rcode_byte[-2]) << 1
            rcode2 = int(rcode_byte[-3]) << 2
            error_code = rcode0 + rcode1 + rcode2
            return error_code
        elif len(rcode_byte) == 6:
            rcode0 = int(rcode_byte[-1])
            rcode1 = int(rcode_byte[-2]) << 1
            rcode2 = int(rcode_byte[-3]) << 2
            rcode3 = int(rcode_byte[-4]) << 3
            error_code = rcode0 + rcode1 + rcode2+ rcode3
            return error_code #if not 0 - return appropriate error message

    """
    Retrieves the recursive flag bit

    :param received_packet: Reponse packet received, bytearray
    :Returns: True->recursion, False->no recursion, bool
    """
    @staticmethod
    def raParser(received_packet):
        racode_byte = bin(received_packet[3])
        if len(racode_byte) != 10:
            return False
        else: 
            if racode_byte[2] == 1:
                return True

    """
    Finds the length of a name field

    :param response: Response packet received, bytearray
    :Returns: Length of name field, int
    """
    @staticmethod
    def getRNameLength(response, name_i):
        if int(response[name_i]) - 192 >= 0:
            return 2
        else:
            while response[name_i] != 0:
                name_i += 1
            return i+1
