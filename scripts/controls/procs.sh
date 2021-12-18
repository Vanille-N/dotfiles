#!/bin/bash

alacritty --class=btm,Procs \
    -e btm &
cpid=$!

alacritty --class=htop,Procs \
    -e htop
kill $cpid

