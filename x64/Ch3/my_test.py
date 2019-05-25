# -*- coding: utf-8 -*-
"""
Created on Sat May 11 21:21:41 2019

@author: Borko
@version: 3.32
"""

import my_debugger

debug_test = my_debugger.debugger()

pid = input("Enter the PID of the process to attach to: ")

debug_test.attach(int(pid))

debug_test.detach()
