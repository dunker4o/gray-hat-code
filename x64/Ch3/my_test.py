# -*- coding: utf-8 -*-
"""
Created on Sat May 11 21:21:41 2019

@author: Borko
@version: 3.38
"""

import my_debugger

debugger = my_debugger.debugger()

pid = input("Enter the PID of the process to attach to: ")

debugger.attach(int(pid))

thread_list = debugger.enumerate_threads()

# For each thread in the list print the value in each register
for thread in thread_list:
    
    thread_context = debugger.get_thread_context(thread)
    
    # Print the contents of some of the registers
    print("[*] Dumping registers for thread ID: 0x%016x" % thread)
    print("[**] IP: 0x%016x" % thread_context.Rip)
    print("[**] SP: 0x%016x" % thread_context.Rsp)
    print("[**] BP: 0x%016x" % thread_context.Rbp)
    print("[**] AX: 0x%016x" % thread_context.Rax)
    print("[**] BX: 0x%016x" % thread_context.Rbx)
    print("[**] CX: 0x%016x" % thread_context.Rcx)
    print("[**] DX: 0x%016x" % thread_context.Rdx)
    print("[**] SI: 0x%016x" % thread_context.Rsi)
    print("[**] DI: 0x%016x" % thread_context.Rdi)
    print("[*] END OF DUMP")
    
debugger.detach()