# -*- coding: utf-8 -*-
"""
Created on Sat May 11 21:05:56 2019

@author: Borko
@version: 3.42
"""

from ctypes import *
from my_debugger_defines import *
import sys

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        self.h_process          = None
        self.pid                = None
        self.debugger_active    = False
        self.h_thread           = None
        self.context            = None
        self.exception          = None
        self.exception_address  = None
        
    

    def load(self, path_to_exe):
        
        # dwCreation flag determines how to create the process
        # set creation_flags = CREATE_NEW_CONSOLE if you want to see the GUI
        creation_flags = DEBUG_PROCESS
        
        #instantiate structs
        startupinfo         = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        
        # The following options allow the new process to be shown as a 
        # separate window. It also illustrates how different settings
        # in the STARTUPINFO struct can affect the debugee
        startupinfo.dwFlags     = 0x1
        startupinfo.wShowWindow = 0x0
        
        # We then initialise the cb variable in the STARTUPINFO struct which
        # is just the size of the struct itself
        #Note that sizeof is a Ctype function !!!
        startupinfo.cb = sizeof(startupinfo)
        
    
        # Windows system error codes:
        # https://docs.microsoft.com/en-us/windows/desktop/Debug/system-error-codes
        
        # Need to call CreateProcessW because the string is UNICODE!
        # NB: If a function ends in A (e.g. CreateProcessA), it accepts ASCI
        # as per https://stackoverflow.com/a/23423274
        if (sys.version_info > (3, 0)):
            if kernel32.CreateProcessW(path_to_exe,
                                       None,
                                       None,
                                       None,
                                       None,
                                       creation_flags,
                                       None,
                                       None,
                                       byref(startupinfo),
                                       byref(process_information)):
                print("[*] We have successfully launched the process!")
                print("[*] PID: %d" % process_information.dwProcessId)
                
                # Obtain a handle to the newly created process and store it.
                self.h_process = self.open_process(process_information.dwProcessId)
            else:
                print ("[*] Error: 0x%08x." % kernel32.GetLastError())
        else:
            if kernel32.CreateProcessA(path_to_exe,
                                       None,
                                       None,
                                       None,
                                       None,
                                       creation_flags,
                                       None,
                                       None,
                                       byref(startupinfo),
                                       byref(process_information)):
                print("[*] We have successfully launched the process!")
                print("[*] PID: %d" % process_information.dwProcessId)
            else:
                print ("[*] Error: 0x%08x." % kernel32.GetLastError())
                
                
    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)
        return h_process
    
    def attach(self, pid):
        
        self.h_process = self.open_process(pid)
        
        # Attempt to attach to the process. If it fails, exit
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid             = int(pid)
            self.run()
        else:
            print("[*] Unable to attach to the process.")
            
    def run(self):
        # Poll the debugee for debugging events
        
        while self.debugger_active:
            self.get_debug_event()
            
            
    def get_debug_event(self):
        
        debug_event     = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
    
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            
            # Obtain thread and context information
            self.h_thread   = self.open_thread(debug_event.dwThreadId)
            self.context    = self.get_thread_context(self.h_thread)
            
            print("Event Code: %d Thread ID: %d" % 
                  (debug_event.dwDebugEventCode, debug_event.dwThreadId))

            # If the event code is an exception, examine it further
            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                # Obtain the exception code
                self.exception          = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address  = debug_event.u.Exception.ExceptionRecord.ExceptionAddress 
            
            
                if self.exception == EXCEPTION_ACCESS_VIOLATION:
                    print ("[!] Access Violation detected.")
                # If it's a breakpoint, call the internal handler
                elif self.exception == EXCEPTION_BREAKPOINT:
                    continue_status = self.exception_handler_breakpoint()
                elif self.exception == EXCEPTION_GUARD_PAGE:
                    print ("[!] Guard Page access detected.")
                elif self.exception == EXCEPTION_SINGLE_STEP:
                    print ("[*] Single Stepping.")

            kernel32.ContinueDebugEvent(debug_event.dwProcessId,
                                        debug_event.dwThreadId,
                                        continue_status)
            
    def exception_handler_breakpoint(self):

        print("[*] Inside the breakpoint handler.")
        print("Exception Address: 0x%016x" % self.exception_address)
        
        return DBG_CONTINUE
    
    def detach(self):
        
        if kernel32.DebugActiveProcessStop(self.pid):
            print ("[**] Finished debugging. Exiting...")
            return True
        else:
            print("An error ocurred!")
            return False
        
    def open_thread(self, thread_id):
        
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)
        
        if h_thread is not None:
            return h_thread
        else:
            print("[^] Could not obtain a valid thread handle.")
            return False
        
    def enumerate_threads(self):
        
        # Snapshot function returns a list of processes, threads and loaded
        # DLLs inside a process + HEAP list that it owns
        thread_entry    = THREADENTRY32()
        thread_list     = []
        snapshot        = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,
                                                            self.pid)
        
        
        
        # If we manage to get a snapshot, continue with the processing
        if snapshot is not None:
            # Set the size of the struct or the call fails
            # then get the first thread snapshot
            thread_entry.dwSize = sizeof(thread_entry)
            success             = kernel32.Thread32First(snapshot,
                                                         byref(thread_entry))
            
            
            # While there are still threads to enumerate, compare their
            # process ID if it matches our target, append them to the list
            # and then get the next thread from the debugee process
            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                    
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))
            
            
            
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False
        
    def get_thread_context(self, thread_id):
        
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        
        # Obtain a handle to the thread
        # and then try to get all the register values by GetThreadContext
        h_thread = self.open_thread(thread_id)
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return False
        
        
        
    