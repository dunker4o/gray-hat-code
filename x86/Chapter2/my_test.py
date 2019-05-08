import my_debugger

debugger = my_debugger.debugger()

pid = raw_input("Enter the PID of the process to test: ")

#debugger.load("C:\\WINDOWS\\system32\\calc.exe")

debugger.attach(int(pid))

printf_address  = debugger.func_resolve("msvcrt.dll", "printf")
print "[*] Address of printf: 0x%08x" % printf_address
debugger.bp_set(printf_address)

debugger.run()

#list = debugger.enumerate_threads()
# For each thread in the list we want to grab the value of each of the registers
#for thread in list:
#    thread_context = debugger.get_thread_context(thread)
    
#    print "[*] Dumping registers for thread ID: 0x%08x" % thread
#    print "[**] EIP: 0x%08x" % thread_context.Eip
#    print "[**] ESP: 0x%08x" % thread_context.Esp
#    print "[**] EBP: 0x%08x" % thread_context.Ebp
#    print "[**] EAX: 0x%08x" % thread_context.Eax
#    print "[**] EBX: 0x%08x" % thread_context.Ebx
#    print "[**] ECX: 0x%08x" % thread_context.Ecx
#    print "[**] EDX: 0x%08x" % thread_context.Edx
#    print "[**] ESI: 0x%08x" % thread_context.Esi
#    print "[**] EDI: 0x%08x" % thread_context.Edi
#    print "[*] END OF DUMP"

debugger.detach()