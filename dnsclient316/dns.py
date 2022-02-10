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
        flags = bytearray()
        flags.append(1)
        flags.append(0)
        return flags

    @staticmethod
    def generateQDCount():
        qCount = bytearray()
        qCount.append(0)
        qCount.append(1)
        return qCount

    @staticmethod
    def generateANCount():
        aCount = bytearray()
        aCount.append(0)
        aCount.append(0)
        return aCount

    @staticmethod
    def generateNSCount():
        nCount = bytearray()
        nCount.append(0)
        nCount.append(0)
        return nCount

    @staticmethod
    def generateARCount():
        aCount = bytearray()
        aCount.append(0)
        aCount.append(0)
        return aCount

    @staticmethod
    def generateNRCount():
        nrCount = bytearray()
        nrCount.append(0)
        nrCount.append(0)
        return nrCount

    @staticmethod
    # Generates  and returns a formatted DNS request Header.
    def generateDNSHeader():
        header = bytearray()
        header.append(DNS.generatePacketID())
        header.extend(DNS.generateQueryFlags())  # For us it should always be 1, and 0
        header.extend(DNS.generateQDCount())  # QDCount is always 1 for us
        header.extend(DNS.generateANCount())  # Default 0, only regarded in response packets
        header.extend(DNS.generateNSCount())
        header.extend(DNS.generateNRCount())
        return header

    @staticmethod
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

    @staticmethod
    def generateQType():
        qType = bytearray()  # needs to choose between 1, 2, and 3. for now use 1 since default ip type.
        qType.append(0)
        qType.append(1)
        return qType

    @staticmethod
    def generateQClass():
        qClass = bytearray()
        qClass.append(0)
        qClass.append(1)
        return qClass

    @staticmethod
    def generateDNSQuestions(name):
        questions = bytearray()
        questions.extend(DNS.generateQName(name))
        questions.extend(DNS.generateQType())
        questions.extend(DNS.generateQClass())
        return questions

    @staticmethod
    def sendDNSRequest():
        print("Sent")