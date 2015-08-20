#!/bin/bash

option=$1
set -i

if [ $option = "network" ]; then
    echo Resetting the network...
    sudo systemctl restart systemd-networkd
    sudo resolvconf -u
    echo Done!
elif [ $option = "desktop" ]; then
    echo Resetting the LXQT desktop...
    sudo pcmanfm-qt --desktop-off --profile lxqt
    sleep 3 
    sudo pcmanfm-qt --desktop --profile lxqt &
    echo Done!
elif [ $option = "clock" ]; then
    echo Resetting the clock...
    sudo ntpd -qg
    sudo hwclock --systohc
    echo Done!
else
    echo Unknown option: $option >&2
fi
