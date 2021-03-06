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

# Get NIC configurations...
nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled = True)

print '\r\nIndex\tInterface'
print '=====\t=========\r'

# Print all configus
for nic in nic_configs:
    print '[%d]\t%s' % (nic.Index, nic.Description)

# Ask the user to select an interface...
index = int(get_validated_input('\r\nSelect interface (index): ', r'^\d+$', True)[1])
selected_nic = None
for nic in nic_configs:
    if(index == int(nic.Index)):
        selected_nic = nic
        print nic

# Print the selected configuration
if selected_nic:
    print '\r\nSelected NIC: ', selected_nic.Description
    print '...DHCP Enabled:\t', selected_nic.DHCPEnabled
    print '...IP Address:\t\t', selected_nic.IPAddress[0]
    print '...Default IP Gateway:\t', selected_nic.DefaultIPGateway[0]
    print '...Default DNS Server:\t', selected_nic.DNSServerSearchOrder[0]

    # Initialize configurable parameters
    dhcp_enabled = selected_nic.DHCPEnabled
    ip_address = selected_nic.IPAddress[0]
    default_dns = selected_nic.DNSServerSearchOrder[0]
    default_gateway = selected_nic.DefaultIPGateway[0]

    # Ask the user if this interface needs to be configured...
    configure = get_validated_input('\r\nWould you like to configure this interface [Y/N]: ',
                                    r'^(y|Y|n|N)$',
                                    True)[1].lower()

    if(configure == 'y'):
        # Configure DHCP based on user input
        if(dhcp_enabled):
            dhcp_toggle = get_validated_input('Disable DHCP [Y/N]? ', r'^y|Y|n|N$', True)[1].lower()
        else:
            dhcp_toggle = get_validated_input('Enable DHCP [Y/N]? ', r'^(y|Y|n|N)$', True)[1].lower()

        if(dhcp_toggle == 'y'):
            dhcp_enabled= not dhcp_enabled

        # If DHCP has been disabled, get the interface's IP address, default gateway,
        # default DNS and subnet mask
        if(not dhcp_enabled):
            # Regular expression for verifying IP address input
            regex_ip = r'^(2[0-5][0-4]|1[0-9][0-9]|[0-9][0-9]|[1-9])\.'    \
                        '(2[0-5][0-4]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.'     \
                        '(2[0-5][0-4]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.'     \
                        '(2[0-5][0-4]|1[0-9][0-9]|[0-9][0-9]|[0-9])$'      \

            # Regular expression for verifying subnet mask input
            regex_subnet_mask = r'^(2[4-5][0-5]|1[0-9][0-9]|[0-9][0-9]|[1-9])\.'    \
                                 '(2[0-5][0-5]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.'     \
                                 '(2[0-5][0-5]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.'     \
                                 '(2[0-5][0-5]|1[0-9][0-9]|[0-9][0-9]|[0-9])$'      \

            # Get the required information from the user
            ip_address = unicode(get_validated_input('New IP Address: ', regex_ip, True)[1],'utf-8')
            subnet_mask = unicode(get_validated_input('Subnet Mask: ', regex_subnet_mask, True)[1],'utf-8')
            default_gateway = unicode(get_validated_input('Default Gateway: ', regex_ip, True)[1],'utf-8')
            default_dns = unicode(get_validated_input('Default DNS: ', regex_ip, True)[1],'utf-8')

            result0 = selected_nic.EnableStatic(IPAddress = [ip_address], SubnetMask = [subnet_mask])
            result1 = selected_nic.SetGateways(DefaultIPGateway = [default_gateway])
            result2 = selected_nic.SetDNSServerSearchOrder(DNSServerSearchOrder = [default_dns])

        else:
            # DHCP has to be enabled, configure accordingly
            result0 = selected_nic.EnableDHCP()
            result1 = selected_nic.SetDNSServerSearchOrder()

else:
    print 'Error: Unknown index!'
