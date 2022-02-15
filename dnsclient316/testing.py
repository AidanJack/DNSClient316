from distutils.log import error
import socket
import time
import sys
import threading
import argparse
import random
import re
from dns import DNS

def test():
    raise ValueError("This is a custom error")

try:
    test()
except Exception as e:
    print(e)
    sys.exit()
