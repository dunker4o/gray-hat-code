from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    
    def __init__(self):
        self.h_process              = None
        self.pid                    = None
        self.debugger_active        = False
        self.h_thread               = None
        self.context                = None
        self.breakpoints            = {}
        self.exception              = None
        self.exception_address      = None
        self.first_breakpoint       = True
        self.hardware_breakpoints    = {}
    
    def load(self, path_to_exe):
        # dwCreation flag shows how to create the process
        # set creation_flags = CREATE_NEW_CONSOLE if I want to see the GUI
        creation_flags = CREATE_NEW_CONSOLE
        
        # instantiate the structures
        startupInfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        
        # The following options allow the process to be shown as a separate window. It also
        # illustrates how different settings in the STARTUPINFO structure can affect the debuggee.
        startupInfo.dwFlags = 0x1
        startupInfo.wShowWindow = 0x0
        
        # Then the cb variable is initialised in the STARTUPINFO structure, which is just its SIZE
        startupInfo.cb = sizeof(startupInfo)
        
        if kernel32.CreateProcessA(path_to_exe, None, None, None, None, creation_flags, None, None, byref(startupInfo), byref(process_information)):
            print "[*] The process has been successfully launched!"
            print "[*] PID: %d" % process_information.dwProcessId
            
            #Obtain a valid handle to the newly created process
            # and store it for future access
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print "[:(] Error: 0x%08x." % kernel32.GetLastError()


    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)
        return h_process
    
    def attach(self, pid):
        
        self.h_process = self.open_process(pid)
        #We attempt to attach to the process
        # if this fails we exit the Call
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid             = int(pid)
            self.run()
        else:
            print "[*] Unable to attach to the process"
            
    def run(self):
        #Now  we have to poll the debugee for debugging events
        while self.debugger_active == True:
            self.get_debug_event()
    
    def get_debug_event(self):
        debug_event     = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            #Obtain the thread and context information
            self.h_thread   = self.open_thread(debug_event.dwThreadId)
            self.context    = self.get_thread_context(self.h_thread)
            print "Event Code %d Thread ID %d" % (debug_event.dwDebugEventCode, debug_event.dwThreadId)
            
            #If it is an exception, we drill deeper
            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                exception               = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address  = debug_event.u.Exception.ExceptionRecord.ExceptionAddress
                
                if exception == EXCEPTION_ACCESS_VIOLATION:
                    print "[!] Access violation detected."
            
                elif exception == EXCEPTION_BREAKPOINT:
                    continue_status = self.exception_handler_breakpoint()
                elif exception == EXCEPTION_GUARD_PAGE:
                    print "[!] Guard page access detected."
                elif exception == EXCEPTION_SINGLE_STEP:
                    print "[#] Single stepping."
                
            
            kernel32.ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, continue_status)
    
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print "[**] Finished debugging and closing the door after.."
            return True
        else:
            print "Executer error 66"
            return False

    def open_thread(self, thread_id):

        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)

        if h_thread is not None:
            return h_thread
        else:
            print "[*] Could not obtain a valid thread handle."
            return False

    def enumerate_threads(self):
        thread_entry 	= THREADENTRY32()
        thread_list 	= []
        snapshot		= kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)

        if snapshot is not None:
            # Set the size of the struct or the call will fail

            thread_entry.dwSize = sizeof(thread_entry)
            success 			= kernel32.Thread32First(snapshot, byref(thread_entry))

            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))
                
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False
    
    def get_thread_context(self, thread_id):
        
        context                 = CONTEXT()
        context.ContextFlags    = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        
        # Obtain a handle to the thread
        
        h_thread    = self.open_thread(thread_id)
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return False
        
    def exception_handler_breakpoint(self):
        print "[#] Inside the breakpoint handler."
        print "Exception address: 0x%08x" % self.exception_address
        
        return DBG_CONTINUE
    
    def read_process_memory(self, address, length):
        data        =""
        read_buf    = create_string_buffer(length)
        count       = c_ulong(0)
        
        if not kernel32.ReadProcessMemory(self.h_process, address, read_buf, length, byref(count)):
            return False
        else:
            data += read_buf.raw
            return data
        
    def write_process_memory(self, address, data):
        count   = c_ulong(0)
        length  = len(data)
        
        c_data  = c_char_p(data[count.value:])
        if not kernel32.WriteProcessMemory(self.h_process, address, c_data, length, byref(count)):
            return False
        else:
            return True
        
    def bp_set(self, address):
        
        if not self.breakpoints.has_key(address):
            try:
                # Store the original byte
                original_byte   = self.read_process_memory(address, 1)
                
                #Write the INT3 opcode
                self.write_process_memory(address, "\xCC")
                
                #Register the breakpoint in our list
                self.breakpoints[address] = (address, original_byte)
                
            except:
                return False
            
        return True

    def func_resolve(self, dll, function):
        handle  = kernel32.GetModuleHandleA(dll)
        address = kernel32.GetProcAddress(handle, function)
        
        kernel32.CloseHandle(handle)
        
        return address
    
    def bp_set_hw(self, address, length, condition):
        #Check for a valid length Value
        if length not in (1, 2, 4):
            return False
        else:
            length -= 1
            
        #Check for a valid Condition
        if condition not in (HW_ACCESS, HW_EXECUTE, HW_WRITE):
            return False
        
        #Check for available debug register
        if not self.hardware_breakpoints.has_key(0):
            available = 0
        elif not self.hardware_breakpoints.has_key(1):
            available = 1
        elif not self.hardware_breakpoints.has_key(2):
            available = 2
        elif not self.hardware_breakpoints.has_key(3):
            available = 3
        else:
            return False
        
        #Set the debug registers in every thread 
        for thread_id in self.enumerate_threads():
            context = self.get_thread_context(thread_id = thread_id)
            
            #Enable the right flat in the DR7 register to set the Breakpoint
            context.Dr7 |= 1 << (available * 2)
            
        #Save the address of the breakpoint in the free register we located
        if available == 0:
            context.Dr0 = address
        elif available == 1:
            context.Dr1 = address
        elif available == 2:
            context.Dr2 = address
        elif available == 3:
            context.Dr3 = address
            
        #Set the breakpoint Condition
        context.Dr7 |= condition << ((available * 4) + 16)
        
        #Set the length
        context.Dr7 |= length << ((available*4) + 18)
        
        #Set thread context with the break set
        h_thread = self.open_thread(thread_id)
        kernel32.SetThreadContext(h_thread, byref(context))
        
        #Update the internal hardware breakpoint array at the used slot index
        self.hardware_breakpoints[available] = (address, length, condition)
        
        return True