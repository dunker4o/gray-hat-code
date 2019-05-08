# -*- coding: utf-8 -*-
"""
Created on Thu May  9 00:01:37 2019

@author: Borko
"""

from ctypes import Union, c_long, c_int, c_char
import sys

class barley_amount(Union):
    _fields_=[
            ("barley_long", c_long),
            ("barley_int", c_int),
            ("barley_char", c_char*8),
            ]
    
value       = input("Enter the amount of barley to put in the beer vat:")
my_barley   = barley_amount(int(value))
print("Barley amount as a long: %ld" % my_barley.barley_long)
print("Barley amount as an int: %d" % my_barley.barley_int)
print("Barley amount as a char: %s" % my_barley.barley_char.decode(sys.stdout.encoding))