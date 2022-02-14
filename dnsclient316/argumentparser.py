import re

class Parser:
    def __init__(self, args):
        temp_dict = self.parseTerminalArguments(args)
        self.timeout = temp_dict.get("timeout")
        self.port = temp_dict.get("port")
        self.retries = temp_dict.get("retries")
        self.queryType = temp_dict.get("queryType")
        self.server = temp_dict.get("server")
        self.domain = temp_dict.get("domain")



    def parseTerminalArguments(self, args):
        args_dict = {"timeout": 5, "port": 53, "retries": 3, "queryType": "ip", "server": None, "domain": None}
        pattern_ip = "@[0-9]*.[0-9]*.[0-9]*.[0-9]"
        pattern_domain = "[0-9a-zA-Z]*.([0-9a-zA-Z]*)+.[0-9a-zA-Z]*"

        if re.search(pattern_ip, args[len(args)-2]) and re.search(pattern_domain, args[len(args)-1]):
            args_dict["server"] = args[len(args)-2].replace("@", "")
            args_dict["domain"] = args[len(args)-1]
        else:
            print("Error! Valid server ip and domain required")
            return

        flags = args[1:-2]
        for i in range(len(flags)):
            if flags[i].isdigit():
                continue
            match flags[i]:
                case "-t":
                    if not flags[i+1].isdigit():
                        return "Error! Bad argument"
                    args_dict["timeout"] = flags[i+1]
                case "--timeout":
                    if not flags[i+1].isdigit():
                        return "Error! Bad argument"
                    args_dict["timeout"] = flags[i+1]
                case "-p": 
                    if not flags[i+1].isdigit():
                        return "Error! Bad argument"
                    args_dict["port"] = flags[i+1]
                case "--port":
                    if not flags[i+1].isdigit():
                        return "Error! Bad argument"
                    args_dict["port"] = flags[i+1]
                case "-r":
                    if not flags[i+1].isdigit():
                        return "Error! Bad argument"
                    args_dict["retries"] = flags[i+1]        
                case "--retries":
                    if not flags[i+1].isdigit():
                        return "Error! Bad argument"
                    args_dict["retries"] = flags[i+1]
                case "-mx":
                    args_dict["queryType"] = "mx"
                case "-ns":
                    args_dict["queryType"] = "ns"
                case _:
                    print("Error: bad argument")
                    return 
        return args_dict