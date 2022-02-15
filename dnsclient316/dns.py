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
        qType = bytearray("", "UTF-32-BE")  # needs to choose between 1, 2, and 15. for now use 1 since default ip type.
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
