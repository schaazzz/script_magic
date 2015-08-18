#!/bin/bash

option=$1
set -i

if [ $option = "network" ]; then
    echo Resetting the network...
    systemctl  restart  systemd-networkd
    resolvconf  -u
    echo Done!
elif [ $option = "desktop" ]; then
    echo Resetting the LXQT desktop...
    pcmanfm-qt  --desktop-off  --profile  lxqt
    pcmanfm-qt  --desktop  --profile  lxqt &
    echo Done!
elif [ $option = "clock" ]; then
    echo Resetting the clock...
    ntpd -qg
    hwclock --systohc
    echo Done!
else
    echo Unknown option: $option >&2
fi
