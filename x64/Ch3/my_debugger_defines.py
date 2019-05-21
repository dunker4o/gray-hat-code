# -*- coding: utf-8 -*-
"""
Created on Fri May 10 22:08:30 2019

@author: Borko
"""

from ctypes import Structure, Union, c_ubyte, c_ushort, c_ulong, c_uint64
from ctypes import POINTER, c_char, c_void_p, c_ulonglong, c_long, WINFUNCTYPE
from ctypes import c_char_p

# Mapping Microsoft types to ctypes

# Let's map the Microsoft types to ctypes for clarity
# Good reference on data types:
# https://docs.microsoft.com/en-us/windows/desktop/WinProg/windows-data-types
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
ULONGLONG   = c_ulonglong
DWORD_PTR   = c_ulong
LONG        = c_long
LPSTR       = c_char_p
LPTHREAD_START_ROUTINE = WINFUNCTYPE(WORD, LPVOID)


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

## TODO: Evaluate structs from here on !

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
    _fields_ = [
            ("ExceptionRecord", EXCEPTION_RECORD),
            ("dwFirstChance",   DWORD),
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-create_thread_debug_info
class CREATE_THREAD_DEBUG_INFO(Structure):
    _fields_ = [
            ("hThread",             HANDLE),
            ("lpThreadLocalBase",   LPVOID),
            ("lpStartAddress",      LPTHREAD_START_ROUTINE)
            ]    

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-create_process_debug_info
class CREATE_PROCESS_DEBUG_INFO(Structure):
    _fields_ = [
            ("hFile",                   HANDLE),
            ("hProcess",                HANDLE),
            ("hThread",                 HANDLE),
            ("lpBaseOfImage",           LPVOID),
            ("dwDebugInfoFileOffset",   DWORD),
            ("nDebugInfoSize",          DWORD),
            ("lpThreadLocalBase",       LPVOID),
            ("lpStartAddress",          LPTHREAD_START_ROUTINE),
            ("lpImageName",             LPVOID),
            ("fUnicode",                WORD)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-exit_thread_debug_info
class EXIT_THREAD_DEBUG_INFO(Structure):
    _fields_ = [
            ("dwExitCode", DWORD)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-exit_process_debug_info
class EXIT_PROCESS_DEBUG_INFO(Structure):
    _fields_ = [
            ("dwExitCode", DWORD)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-load_dll_debug_info
class LOAD_DLL_DEBUG_INFO(Structure):
    _fields_ = [
            ("hFile",                   HANDLE),
            ("lpBaseOfDll",             LPVOID),
            ("dwDebugInfoFileOffset",   DWORD),
            ("nDebugInfoSize",          DWORD),
            ("lpImageName",             LPVOID),
            ("fUnicode",                WORD)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-unload_dll_debug_info
class UNLOAD_DLL_DEBUG_INFO(Structure):
    _fields_ = [
            ("lpBaseOfDll", LPVOID)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-output_debug_string_info
class OUTPUT_DEBUG_STRING_INFO(Structure):
    _fields_ = [
            ("lpDebugStringData",   LPSTR),
            ("fUnicode",            WORD),
            ("nDebugStringLength",  WORD)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-rip_info
class RIP_INFO(Structure):
    _fields_ = [
            ("dwError", DWORD),
            ("dwType",  DWORD)
            ]

# Union that is inside debug_event
class DEBUG_EVENT_UNION(Union):
    _fields_ = [
            ("Exception",           EXCEPTION_DEBUG_INFO),
            ("CreateThread",        CREATE_THREAD_DEBUG_INFO),
            ("CreateProcessInfo",   CREATE_PROCESS_DEBUG_INFO),
            ("ExitThread",          EXIT_THREAD_DEBUG_INFO),
            ("ExitProcess",         EXIT_PROCESS_DEBUG_INFO),
            ("LoadDll",             LOAD_DLL_DEBUG_INFO),
            ("UnloadDll",           UNLOAD_DLL_DEBUG_INFO),
            ("DebugString",         OUTPUT_DEBUG_STRING_INFO),
            ("RipInfo",             RIP_INFO)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-debug_event
class DEBUG_EVENT(Structure):
    _fields_ = [
            ("dwDebugEventCode",    DWORD),
            ("dwProcessId",         DWORD),
            ("dwThreadId",          DWORD),
            ("u",                   DEBUG_EVENT_UNION),
            ]

# Not needed for 64-bit architectures.
# See: Flt save in here
# https://docs.microsoft.com/en-us/windows/desktop/api/winnt/ns-winnt-context
# and this answer
# https://stackoverflow.com/a/18814507
#class FLOATING_SAVE_AREA(Structure):

class M128A(Structure):
    _fields_ = [
            ("Low",     DWORD64),
            ("High",    DWORD64)
            ]
    
class XMM_SAVE_AREA32(Structure):
    _pack_   = 1
    _fields_ = [
            ("ControlWord",     WORD),
            ("StatusWord",      WORD),
            ("TagWord",         BYTE),
            ("Reserved1",       BYTE),
            ("ErrorOpcode",     WORD),
            ("ErrorOffset",     DWORD),
            ("ErrorSelector",   WORD),
            ("Reserved2",       WORD),
            ("DataOffset",      DWORD),
            ("DataSelector",    WORD),
            ("Reserved3",       WORD),
            ("MxCsr",           DWORD),
            ("MxCsr_Mask",      DWORD),
            ("FloatRegisters",  M128A *8),
            ("XmmRegisters",    M128A *16),
            ("Reserved4",       BYTE *96)
            ] 

class DUMMY_STRUCT_NAME(Structure):
    _fields_ = [
            ("Header", M128A *2),
            ("Legacy", M128A *8),
            ("Xmm0", M128A),
            ("Xmm1", M128A),
            ("Xmm2", M128A),
            ("Xmm3", M128A),
            ("Xmm4", M128A),
            ("Xmm5", M128A),
            ("Xmm6", M128A),
            ("Xmm7", M128A),
            ("Xmm8", M128A),
            ("Xmm9", M128A),
            ("Xmm10", M128A),
            ("Xmm11", M128A),
            ("Xmm12", M128A),
            ("Xmm13", M128A),
            ("Xmm14", M128A),
            ("Xmm15", M128A),
            ]

class DUMMY_UNION_NAME(Union):
    _fields_ = [
            ("FltSave",         XMM_SAVE_AREA32),
#            ("Q", NEON128 *16),
            ("D",               ULONGLONG *32),
            ("DummyStructName", DUMMY_STRUCT_NAME),
            ("S",               DWORD *32)
            ]

# Implement the 64-bit context, not the 32-bit one.
# https://docs.microsoft.com/en-us/windows/desktop/api/winnt/ns-winnt-context
class CONTEXT(Structure):
    _pack_ = 16
    _fields_ = [
            ("P1Home",          DWORD64),
            ("P2Home",          DWORD64),
            ("P3Home",          DWORD64),
            ("P4Home",          DWORD64),
            ("P5Home",          DWORD64),
            ("P6Home",          DWORD64),
            ("ContextFlags",    DWORD),
            ("MxCsr",           DWORD),
            ("SegCs",           WORD),
            ("SegDs",           WORD),
            ("SegEs",           WORD),
            ("SegFs",           WORD),
            ("SegGs",           WORD),
            ("SegSs",           WORD),
            ("EFlags",          DWORD),
            ("Dr0",             DWORD64),
            ("Dr1",             DWORD64),
            ("Dr2",             DWORD64),
            ("Dr3",             DWORD64),
            ("Dr4",             DWORD64),
            ("Dr5",             DWORD64),
            ("Dr6",             DWORD64),
            ("Dr7",             DWORD64),
            ("Rax",             DWORD64),
            ("Rcx",             DWORD64),
            ("Rdx",             DWORD64),
            ("Rbx",             DWORD64),
            ("Rsp",             DWORD64),
            ("Rbp",             DWORD64),
            ("Rsi",             DWORD64),
            ("Rdi",             DWORD64),
            ("R8",              DWORD64),
            ("R9",              DWORD64),
            ("R10",             DWORD64),
            ("R11",             DWORD64),
            ("R12",             DWORD64),
            ("R13",             DWORD64),
            ("R14",             DWORD64),
            ("R15",             DWORD64),
            ("Rip",             DWORD64),
            ("DUMMYUNIONNAME",  DUMMY_UNION_NAME),
            ("VectorRegister",  M128A *26),
            ("VectorControl",   DWORD64),
            ("DebugControl",    DWORD64),
            ("LastBranchToRip", DWORD64),
            ("LastBranchFromRip", DWORD64),
            ("LastExceptionToRip", DWORD64),
            ("LastExceptionFromRip", DWORD64)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/tlhelp32/ns-tlhelp32-threadentry32
class THREADENTRY32(Structure):
    _fields_ = [
            ("dwSize",              DWORD),
            ("cntUsage",            DWORD),
            ("th32ThreadID",        DWORD),
            ("th32OwnerProcessID",  DWORD),
            ("tpBasePri",           LONG),
            ("tpDeltaPri",          LONG),
            ("dwFlags",             DWORD)
            ]
    
# Next three classes are implementation of this struct
# https://docs.microsoft.com/en-us/windows/desktop/api/sysinfoapi/ns-sysinfoapi-system_info
class PROC_STRUCTURE(Structure):
    _fields_ = [
            ("wProcessorArchitecture", WORD),
            ("wReserved",              WORD)
            ]
    
    
class SYSTEM_INFO_UNION(Union):
    _fields_ = [
            ("dwOemId",         DWORD),
            ("DUMMYSTRUCTNAME", PROC_STRUCTURE)
            ]
    
class SYSTEM_INFO(Structure):
    _fields_ = [
            ("DUMMYUNIONNAME",              SYSTEM_INFO_UNION),
            ("dwPageSize",                  DWORD),
            ("lpMinimumApplicationAddress", LPVOID),
            ("lpMaximumApplicationAddress", LPVOID),
            ("dwActiveProcessorMask",       DWORD_PTR),
            ("dwNumberOfProcessors",        DWORD),
            ("dwProcessorType",             DWORD),
            ("dwAllocationGranularity",     DWORD),
            ("wProcessorLevel",             WORD),
            ("wProcessorRevision",          WORD)
            ]

# https://docs.microsoft.com/en-us/windows/desktop/api/winnt/ns-winnt-memory_basic_information
class MEMORY_BASIC_INFORMATION(Structure):
    _fields_ = [
            ("BaseAddress",         PVOID),
            ("AllocationBase",      PVOID),
            ("AllocationProtect",   DWORD),
            ("RegionSize",          SIZE_T),
            ("State",               DWORD),
            ("Protect",             DWORD),
            ("Type",                DWORD)
            ]
    
    
    