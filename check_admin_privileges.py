#--------------------------------------------------------------------------
# The MIT License (MIT)
# 
# Copyright (c) 2014 Shahzeb Ihsan
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#--------------------------------------------------------------------------
## @file    check_admin_privileges.py
#  @brief   Script can be used to check if a shell has administraive privileges.
#
#  @author  Shahzeb Ihsan [shahzeb.ihsan@gmail.com]
#  @version 0.1

#--------------------------------------------------------------------------
# Module Imports
from win32com.shell import shell

#--------------------------------------------------------------------------
# Module Global Attributes
# --- N/A

#--------------------------------------------------------------------------
# Module Global Variables
# --- N/A

#--------------------------------------------------------------------------
# Module Local Attributes
# --- N/A
#--------------------------------------------------------------------------
# Module Internal Variables
# --- N/A

#--------------------------------------------------------------------------
if shell.IsUserAnAdmin():
   print "You have administrator privileges!"
else:
   print "You don't have administrator privileges!"
   
raw_input("Press Enter to exit")