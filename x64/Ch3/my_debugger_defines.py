# -*- coding: utf-8 -*-
"""
Created on Fri May 10 22:08:30 2019

@author: Borko
"""

from ctypes import *

# Mapping Microsoft types to ctypes

# Let's map the Microsoft types to ctypes for clarity
BYTE        = c_ubyte
WORD        = c_ushort
DWORD       = c_ulong
DWORD64     = c_uint64
LPBYTE      = POINTER(c_ubyte)
LPTSTR      = POINTER(c_char) 
HANDLE      = c_void_p
PVOID       = c_void_p
LPVOID      = c_void_p
UINT_PTR    = c_ulong
SIZE_T      = c_ulong

# Constants
DEBUG_PROCESS         = 0x00000001
CREATE_NEW_CONSOLE    = 0x00000010
PROCESS_ALL_ACCESS    = 0x001F0FFF
INFINITE              = 0xFFFFFFFF
DBG_CONTINUE          = 0x00010002


# Debug event constants
EXCEPTION_DEBUG_EVENT      =    0x1
CREATE_THREAD_DEBUG_EVENT  =    0x2
CREATE_PROCESS_DEBUG_EVENT =    0x3
EXIT_THREAD_DEBUG_EVENT    =    0x4
EXIT_PROCESS_DEBUG_EVENT   =    0x5
LOAD_DLL_DEBUG_EVENT       =    0x6
UNLOAD_DLL_DEBUG_EVENT     =    0x7
OUTPUT_DEBUG_STRING_EVENT  =    0x8
RIP_EVENT                  =    0x9

# debug exception codes.
EXCEPTION_ACCESS_VIOLATION     = 0xC0000005
EXCEPTION_BREAKPOINT           = 0x80000003
EXCEPTION_GUARD_PAGE           = 0x80000001
EXCEPTION_SINGLE_STEP          = 0x80000004


# Thread constants for CreateToolhelp32Snapshot()
TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPPROCESS  = 0x00000002
TH32CS_SNAPTHREAD   = 0x00000004
TH32CS_SNAPMODULE   = 0x00000008
TH32CS_INHERIT      = 0x80000000
TH32CS_SNAPALL      = (TH32CS_SNAPHEAPLIST | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD | TH32CS_SNAPMODULE)
THREAD_ALL_ACCESS   = 0x001F03FF

# Context flags for GetThreadContext()
CONTEXT_FULL                   = 0x00010007
CONTEXT_DEBUG_REGISTERS        = 0x00010010

# Memory permissions
PAGE_EXECUTE_READWRITE         = 0x00000040

# Hardware breakpoint conditions
HW_ACCESS                      = 0x00000003
HW_EXECUTE                     = 0x00000000
HW_WRITE                       = 0x00000001

# Memory page permissions, used by VirtualProtect()
PAGE_NOACCESS                  = 0x00000001
PAGE_READONLY                  = 0x00000002
PAGE_READWRITE                 = 0x00000004
PAGE_WRITECOPY                 = 0x00000008
PAGE_EXECUTE                   = 0x00000010
PAGE_EXECUTE_READ              = 0x00000020
PAGE_EXECUTE_READWRITE         = 0x00000040
PAGE_EXECUTE_WRITECOPY         = 0x00000080
PAGE_GUARD                     = 0x00000100
PAGE_NOCACHE                   = 0x00000200
PAGE_WRITECOMBINE              = 0x00000400

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
    
# https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/ns-processthreadsapi-process_information

class PROCESS_INFORMATION(Structure):
    _fields_    = [
            ("hProcess",    HANDLE),
            ("hThread",     HANDLE),
            ("dwProcessId", DWORD),
            ("dwThreadId",  DWORD),
            ]

## TODO: Evaluate strutcts from here on !

# When the dwDebugEventCode is evaluated
class EXCEPTION_RECORD(Structure):
    pass
    
EXCEPTION_RECORD._fields_ = [
        ("ExceptionCode",        DWORD),
        ("ExceptionFlags",       DWORD),
        ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",     PVOID),
        ("NumberParameters",     DWORD),
        ("ExceptionInformation", UINT_PTR * 15),
        ]

class _EXCEPTION_RECORD(Structure):
    _fields_ = [
        ("ExceptionCode",        DWORD),
        ("ExceptionFlags",       DWORD),
        ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",     PVOID),
        ("NumberParameters",     DWORD),
        ("ExceptionInformation", UINT_PTR * 15),
        ]


# Exceptions
# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-exception_debug_info
class EXCEPTION_DEBUG_INFO(Structure):
    
  
# Union that is inside debug_event
class DEBUG_EVENT_UNION(Union):
    

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-debug_event
class DEBUG_EVENT(Structure):
    

# Not needed for 64-bit architectures.
# See: Flt save in here
# https://docs.microsoft.com/en-us/windows/desktop/api/winnt/ns-winnt-context
# and this answer
# https://stackoverflow.com/a/18814507
class FLOATING_SAVE_AREA(Structure):
    

# Implement the 64-bit context, not the 32-bit one.
# https://docs.microsoft.com/en-us/windows/desktop/api/winnt/ns-winnt-context
class CONTEXT(Structure):
    
  
# https://docs.microsoft.com/en-us/windows/desktop/api/tlhelp32/ns-tlhelp32-threadentry32
class THREADENTRY32(Structure):
    
    
# Next three classes are implementation of this struct
# https://docs.microsoft.com/en-us/windows/desktop/api/sysinfoapi/ns-sysinfoapi-system_info
class PROC_STRUCTURE(Structure):
    
    
class SYSTEM_INFO_UNION(Union):
    
    
class SYSTEM_INFO(Structure):
    

# https://docs.microsoft.com/en-us/windows/desktop/api/winnt/ns-winnt-memory_basic_information
class MEMORY_BASIC_INFORMATION(Structure):
    
    
    
    