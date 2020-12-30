#!/bin/bash

kitty --class Bottom --config ~/.config/kitty/kitty.conf \
    --override initial_window_width=93c \
    --override font_size=7.0 \
    --override initial_window_height=60c \
    -e btm &
cpid=$!
sleep 0.05
kitty --class Top --config ~/.config/kitty/kitty.conf \
    -e htop
kill $cpid
