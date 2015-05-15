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
import wmi
from helpers import *

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

print '\r\nListing interfaces, filters: {IPEnabled = False}'
print 'Please wait, this might take a few seconds...'

nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled = True)

print '\r\nIndex\tInterface'
print '=====\t=========\r'

for nic in nic_configs:
   print '[%d]\t%s' % (nic.Index, nic.Description)

index = int(get_validated_input('\r\nSelect interface (index): ',
                                r'^\d+$',
                                True)[1])

selected_nic = None
for nic in nic_configs:
   if(index == int(nic.Index)):
      selected_nic = nic
      
if selected_nic:
   print '\r\nSelected NIC: ', selected_nic.Description
   print '...DHCP Enabled:\t', selected_nic.DHCPEnabled
   print '...IP Address:\t\t', selected_nic.IPAddress[0]
   print '...Default IP Gateway:\t', selected_nic.DefaultIPGateway[0]
   print '...Default DNS Server:\t', selected_nic.DNSServerSearchOrder[0]
   dhcp_enabled = selected_nic.DHCPEnabled
   ip_address = selected_nic.IPAddress[0]
   default_dns = selected_nic.DNSServerSearchOrder[0]
   default_gateway = selected_nic.DefaultIPGateway[0]
   
   configure = get_validated_input('\r\nWould you like to configure this interface [Y/N]: ',
                                   r'^(y|Y|n|N)$',
                                   True)[1].lower()
   
   if(configure == 'y'):
      if(dhcp_enabled):
         dhcp_toggle = get_validated_input('Disable DHCP [Y/N]? ',
                                           r'^y|Y|n|N$',
                                           True)[1].lower()
      else:
         dhcp_toggle = get_validated_input('Enable DHCP [Y/N]? ',
                                           r'^(y|Y|n|N)$',
                                           True)[1].lower()
         
      if(dhcp_toggle == 'y'):
         dhcp_enabled= not dhcp_enabled
      
      if(not dhcp_enabled):
         ip_address = unicode(get_validated_input('New IP Address: ',
                                                  (r'^(2[0-5][0-4]|1[0-9][0-9]|[0-9][0-9]|[1-9])\.'
                                                   '(2[0-5][0-4]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.'
                                                   '(2[0-5][0-4]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.'
                                                   '(2[0-5][0-4]|1[0-9][0-9]|[0-9][0-9]|[0-9])$'),
                                                  True)[1],
                              'utf-8')

         default_gateway = raw_input('Default Gateway: ')
         default_dns = raw_input('Default DNS: ')
         
      print selected_nic
else:
   print 'Error: Unknown index!'

