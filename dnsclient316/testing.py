from distutils.log import error
import socket
import time
import sys
import threading
import argparse
import random
import re
from dns import DNS

def parseTerminalArguments(args):
    args_dict = {"timeout": 5, "port": 53, "retries": 3, "queryType": 1, "server": None, "domain": None}
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
                args_dict["queryType"] = 2
            case "-ns":
                args_dict["queryType"] = 3
            case _:
                print("Error: bad argument")
                return 
    print(args_dict)
        
                 
            

the_args = sys.argv
#print(the_args[1])
parseTerminalArguments(the_args)
