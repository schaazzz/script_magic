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
## @file    set_nic_properties.py
#  @brief   Can be used to enable/disable DHCP and (in case of disabled DHCP)
#           set static IP/Default Gateway/Default DNS for the selected NIC.
#
#  @author  Shahzeb Ihsan [shahzeb.ihsan@gmail.com]
#  @version 0.1

#--------------------------------------------------------------------------
# Module Imports
import re

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
# Function: get_validated_input
def get_validated_input(prompt, regex_str, loop_till_valid = False):
   """
   Get validated user input.
   
   @param prompt String: Prompt to show
   @param regex_str String: String containing the regular expression for validating the input
   @param loop_till_valid bool: If True, continously prompt user in case of invalid input
   @return tuple: Validity of input (True/False) and regex match result ('None' if invalid )
   """
   is_input_valid = False
   search_result = None
   
   regex = re.compile(regex_str)
   
   while loop_till_valid:
      user_input = raw_input(prompt)
      match_obj = regex.search(user_input)
      
      if(match_obj):
         search_result = match_obj.group(0)
         is_input_valid = True
         break
   
   return (is_input_valid, search_result)