#!/usr/bin/bash

alacritty --class=vis,Mixer \
    -e ~/bin/vis &
cpid=$!
sleep 0.1
alacritty --class=alsamixer,Mixer \
    -e alsamixer
kill $cpid

