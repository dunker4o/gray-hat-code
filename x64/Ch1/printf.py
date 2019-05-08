# -*- coding: utf-8 -*-
"""
Created on Wed May  8 23:30:04 2019

@author: Borko
"""

from ctypes import *
import sys

msvcrt = cdll.msvcrt
messageString = "Hello world!".encode(sys.stdout.encoding)
msvcrt.printf(b"Testing: %s", messageString)