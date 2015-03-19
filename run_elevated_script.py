#--------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

##
## (C) COPYRIGHT ? Preston Landers 2010
## Released under the same license as Python 2.6.5
##

# Original script by Preseton Landers modified slightly, if run without any
# parameters, it will call the "test()" function, resulting in this script
# being re-run with admin privileges. If it is run with another script's
# path as the first parameter, that script will be run with administrator
# privileges, i.e.
#
#          python run_elevated_script.py .\check_admin_privileges
#

#--------------------------------------------------------------------------
# Module Imports
import sys, os, traceback, types
import win32api, win32con, win32event, win32process
from win32com.shell import shell
from win32com.shell import shellcon

#--------------------------------------------------------------------------
# Function: run_as_admin
def run_as_admin(script, wait = True):
   """
   Run the specified script with elevated privileges.
   
   @param script String: Absolute path to the script
   @param wait bool: If the script should wait for the privileged script, default to "True"
   
   @return int: Return code from the launched script("None" if wait is "False")
   """
   
   python_exe = sys.executable

   proc_info = shell.ShellExecuteEx(nShow = win32con.SW_SHOWNORMAL,
                                    fMask = shellcon.SEE_MASK_NOCLOSEPROCESS,
                                    lpVerb = 'runas',
                                    lpFile = python_exe,
                                    lpParameters = script)

   print script
   print python_exe
    
   if wait:
      proc_handle = proc_info['hProcess']    
      obj = win32event.WaitForSingleObject(proc_handle, win32event.INFINITE)
      ret_code = win32process.GetExitCodeProcess(proc_handle)
   else:
      ret_code = None

   return ret_code

#--------------------------------------------------------------------------
# Function: test
def test():
   """
   Demo function, if no script is provided as a parameter, this function will
   be called to demonstrate how this works.
   
   @return int: Return code
   """
    
   ret_code = 0
   if not shell.IsUserAnAdmin():
      print "=> You're not an admin! PID: ", os.getpid(), ", params: ", sys.argv
      ret_codec = run_as_admin(script = os.path.abspath(sys.argv[0]),
                                 wait = True)
   else:
      print "=> You are an admin! PID: ", os.getpid(), ", params: ", sys.argv
      ret_code = 0
    
   return ret_code

#--------------------------------------------------------------------------
#--- Script entry point
if __name__ == "__main__":
   """
   Script entry point.
   """
   
   if(len(sys.argv) == 1):  
      ret_code = test()
   else:
      ret_code = run_as_admin(script = sys.argv[1],
                              wait = True)
    
   raw_input('Press Enter to exit')
   sys.exit(ret_code)
