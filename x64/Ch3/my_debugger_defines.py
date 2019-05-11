# -*- coding: utf-8 -*-
"""
Created on Fri May 10 22:08:30 2019

@author: Borko
"""

from ctypes import *

# Mapping Microsoft types to ctypes

WORD    = c_ushort
DWORD   = c_ulong
LPBYTE  = POINTER(c_ubyte)
LPTSTR  = POINTER(c_char)
HANDLE  = c_void_p

#Constants
DEBUG_PROCESS       = 0x00000001
CREATE_NEW_CONSOLE  = 0x00000010


#Structure for CreateProcessA() function
class STARTUPINFO(Structure):
    _fields_    = [
            ("cb",              DWORD),
            ("lpReserver",      LPTSTR),
            ("lpDesktop",       LPTSTR),
            ("lpTitle",         LPTSTR),
            ("dwX",             DWORD),
            ("dwY",             DWORD),
            ("dwXSize",         DWORD),
            ("dwYSize",         DWORD),
            ("dwXCountChars",   DWORD),
            ("dwYCountChars",   DWORD),
            ("dwFillAttribute", DWORD),
            ("dwFlags",         DWORD),
            ("wShowWindow",     WORD),
            ("cbReserved2",     WORD),
            ("lpReserved2",     WORD),
            ("hStdInput",       HANDLE),
            ("hStdOutput",      HANDLE),
            ("hStdError",       HANDLE),
            ]
    
    
class PROCESS_INFORMATION(Structure):
    _fields_    = [
            ("hProcess",    HANDLE),
            ("hThread",     HANDLE),
            ("dwProcessId", DWORD),
            ("dwThreadId",  DWORD),
            ]

