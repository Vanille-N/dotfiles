#!/bin/bash

alacritty --class=nm.sh,Scanner \
    -e ~/.config/scripts/controls/nm.sh &
cpid1=$!
sleep 0.1
alacritty --class=ip.sh,Scanner \
    -e ~/.config/scripts/controls/ip.sh &
cpid2=$!

nm-connection-editor
kill $cpid1
kill $cpid2

