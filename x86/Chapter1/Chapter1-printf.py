from ctypes import *

msvcrt = cdll.msvcrt
message_string = "Hello, Gray Hat Python!\n"
msvcrt.printf("A message has been received: %s", message_string)