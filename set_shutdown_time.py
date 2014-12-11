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
## @file    set_shutdown_time.py
#  @brief   Script can be used to read the shutdown time from the registry
#           and set it to the current time.
#
#  @author  Shahzeb Ihsan [shahzeb.ihsan@gmail.com]
#  @version 0.1

#--------------------------------------------------------------------------
# Module Imports
import sys, os
import binascii, array
from _winreg import *
from struct import *
from math import *
from datetime import datetime, timedelta
import win32con, win32event, win32process
from win32com.shell import shell, shellcon

#--------------------------------------------------------------------------
# Module Global Attributes
# --- N/A

#--------------------------------------------------------------------------
# Module Global Variables
# --- N/A

#--------------------------------------------------------------------------
# Module Local Attributes
__TIMESTAMP_SIZE = 8
__HKEY = HKEY_LOCAL_MACHINE
__SUB_KEY = r'SYSTEM\CurrentControlSet\Control\Windows'
__INDEX_SHUTDOWN_TIME = 9

#--------------------------------------------------------------------------
# Module Internal Variables
# datetime object for reference time used in LDAP timestamps in Windows
_epoch_start = datetime(year = 1601, month = 1, day = 1)

#--------------------------------------------------------------------------
# Function: set_shutdown_timestamp
def set_shutdown_timestamp():
   """
   Sets the shutdown timestamp in the registry to the current system time
   """

   time_array = [None] * __TIMESTAMP_SIZE
   
   # Read the current system time as a 64-bit timestamp and save it in an arrray
   current_system_timestamp, current_system_time = get_system_time()
   for i in range(__TIMESTAMP_SIZE):
      time_array[i] = (current_system_timestamp & (0xFF << (i * 8))) >> (i * 8)

   # Pack the timestamp array in a format suitable for storing in the registry
   new_shutdown_timestamp = array.array('B', time_array).tostring()
   
   # Set the new shutdown time in the registry
   print("Attempting to set the shutdown time in the registry to: ", binascii.hexlify(new_shutdown_timestamp))
   
   # Open the registry key containing the shutdown time value for writing
   key_handle = ConnectRegistry(None, __HKEY)
   try:
      subkey_handle = OpenKey(key_handle, __SUB_KEY, 0, KEY_ALL_ACCESS)
      
      # Write the new shutdown time to the registry
      SetValueEx(subkey_handle, "ShutdownTime", 0, REG_BINARY, new_shutdown_timestamp)
      
      raw_input("Looks like the write was successful, press Enter to continue...")
      
   except EnvironmentError:
      raw_input("Oh fudge! There was an error while writing to the registry, press Enter to exit...")
      
   except WindowsError:
      raw_input("Oh fudge! There was an error while opening the registry key, press Enter to exit...")
   
   # Close the regsitry key handles
   CloseKey(subkey_handle)
   CloseKey(key_handle)
   
#--------------------------------------------------------------------------
# Function: get_shutdown_time_from_reg
def get_shutdown_time_from_reg():
   """
   Reads the shutdown time from the registry, converts it to a 64-bit timestamp
   and returns a tuple containing the timestamp and the timestamp converted to
   a datetime formatted string.
   
   @return tuple: Timestamp and timestamp converted to a formatted datetime string
   """
   
   time_array = [None] * __TIMESTAMP_SIZE
   
   # Open the registry key containing the shutdown time value
   key_handle = ConnectRegistry(None, __HKEY)
   subkey_handle = OpenKey(key_handle, __SUB_KEY)

   # Read the shutdown time value from the registry
   key_name, key_value, key_type = EnumValue(subkey_handle, __INDEX_SHUTDOWN_TIME)
   
   # Close the regsitry key handles
   CloseKey(subkey_handle)
   CloseKey(key_handle)
   
   # Store the timestamp's ASCII code representation in an array
   for i in range(__TIMESTAMP_SIZE):
      time_array[i] = ord(key_value[i])
   
   # Convert the timestamp to a 64-bit value
   timestamp = 0
   for i in range(__TIMESTAMP_SIZE):
      timestamp |= time_array[i] << (i * 8)
   
   # Convert timestamp to seconds
   timestamp_in_seconds = timestamp / 10**7
   
   # Return the timestamp and timestamp converted to a formatted datetime string
   return timestamp, (_epoch_start + timedelta(seconds = timestamp_in_seconds)).strftime('%d/%m/%Y, %H:%M:%S')

#--------------------------------------------------------------------------
# Function: get_system_time
def get_system_time():
   """
   Reads the system time, converts it to a 64-bit timestamp and returns a tuple
   containing the timestamp and the timestamp converted to a datetime formatted string.
   
   @return tuple: Timestamp and timestamp converted to a formatted datetime string
   """
   
   current_time = datetime.now()
   current_time_delta_since_epoch = current_time - _epoch_start
   current_timestamp = int(floor(current_time_delta_since_epoch.total_seconds())) * 10**7

   # Return the timestamp and timestamp converted to a formatted datetime string
   return current_timestamp, current_time.strftime('%d/%m/%Y, %H:%M:%S')

#--------------------------------------------------------------------------
# Function: main      
if __name__ == '__main__':
   if(len(sys.argv) == 2) and (sys.argv[1] == 'set_shutdown_time_in_reg'):
      set_shutdown_timestamp()
      sys.exit(0)
   else:
      reg_shutdown_timestamp, reg_shutdown_time = get_shutdown_time_from_reg()
      print 'Shutdown time => ', reg_shutdown_timestamp, ' (', reg_shutdown_time, ')'
   
      current_system_timestamp, current_system_time = get_system_time()
      print 'System time => ', current_system_timestamp, ' (', current_system_time, ')'

      prompt = raw_input('Set shutdown time to system time [Y\N]?')
      if prompt.lower() == 'y':
         if(shell.IsUserAnAdmin()):
            print "Looks like this shell already has admin access..."
            set_shutdown_timestamp()
         else:
            print("Ok! Now I will attempt to elevate privileges...")

            proc_info = shell.ShellExecuteEx(nShow = win32con.SW_SHOWNORMAL,
                                             fMask = shellcon.SEE_MASK_NOCLOSEPROCESS,
                                             lpVerb = 'runas',
                                             lpFile = sys.executable,
                                             lpParameters = sys.argv[0] + " " + "set_shutdown_time_in_reg")
            
            proc_handle = proc_info['hProcess']    
            obj = win32event.WaitForSingleObject(proc_handle, win32event.INFINITE)
            ret_code = win32process.GetExitCodeProcess(proc_handle)
            raw_input("If the privileged script has finished, press Enter to exit...")





