#!/usr/bin/bash

alacritty --class=vis,Mixer \
    -e ~/.config/scripts/controls/vis &
cpid=$!
sleep 0.1
alacritty --class=alsamixer,Mixer \
    -e alsamixer
kill $cpid

