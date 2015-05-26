---
layout: post
title: Set NIC Properties
author: Shahzeb Ihsan
---

**Dependencies: pywin32, wmi**

I use this script on my laptop to switch from DHCP (at work) to a static IP addressing scheme (at home) and vice versa.

## Usage:
<pre>
$ python  set_nic_properties.py  True

Listing interfaces, filters: {IPEnabled = False}
Please wait, this might take a few seconds...

Index   Interface
=====   =========
[7]     Intel(R) 82579LM Gigabit Network Connection
[15]    Intel(R) Centrino(R) Advanced-N 6205
[23]    Remote NDIS based Internet Sharing Device
[29]    VirtualBox Host-Only Ethernet Adapter
</pre>

Select an interface index from the listed options when prompted and specify if you want to configure this interface.
<!--more-->
(Note: IP address, domain and DNS information has been replaced with "---.---.---.---")

<pre>
Select interface (index): 15

Selected NIC:  Intel(R) Centrino(R) Advanced-N 6205
...DHCP Enabled:        True
...IP Address:          ---.---.---.---
...Default IP Gateway:  ---.---.---.---
...Default DNS Server:  ---.---.---.---

Would you like to configure this interface [Y/N]: y
</pre>


If you enter "N" above, the script will exit. "Y" will lead you through a series of self-explanatory prompts

<pre>
Disable DHCP [Y/N]? y
New IP Address: 192.168.1.10
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.1.1
Default DNS: 192.168.1.1
</pre>

In case DHCP is disabled and you want to enable it, the output will look something like this:

<pre>
Selected NIC:  Intel(R) Centrino(R) Advanced-N 6205
...DHCP Enabled:        False
...IP Address:          ---.---.---.---
...Default IP Gateway:  ---.---.---.---
...Default DNS Server:  ---.---.---.---

Would you like to configure this interface [Y/N]: y
Enable DHCP [Y/N]? y
</pre>

## How it works
The WMI Python module does most of the heavy lifting for us i.e. interfacing to the Windows Management Interface. The entire script depends on the following Windows [Win32_NetworkAdapterConfiguration](https://msdn.microsoft.com/en-us/library/aa394217%28v=vs.85%29.aspx) methods:

- [EnableStatic](https://msdn.microsoft.com/en-us/library/aa390383%28v=vs.85%29.aspx)
- [SetGateways](https://msdn.microsoft.com/en-us/library/aa393301%28v=vs.85%29.aspx)
- [SetDNSServerSearchOrder](https://msdn.microsoft.com/en-us/library/aa393295%28v=vs.85%29.aspx)
- [EnableDHCP](https://msdn.microsoft.com/en-us/library/aa390378(v=vs.85).aspx)
- [SetDNSServerSearchOrder](https://msdn.microsoft.com/en-us/library/aa393295(v=vs.85).aspx)

Other implementation details are straight forward. The [get\_validated\_input](https://github.com/schaazzz/script_magic/blob/master/helpers.py) is used to get validated user input based on the specified regular expression.

If you don't want to download or clone the whole repository, you can view the complete source for this script on GitHub [here](https://github.com/schaazzz/script_magic/blob/master/set_nic_properties.py) or download the file [here](https://raw.githubusercontent.com/schaazzz/script_magic/master/set_nic_properties.py)
