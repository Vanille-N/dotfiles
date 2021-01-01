#!/usr/bin/bash

kitty --class Visualizer \
    --config ~/.config/kitty/kitty.conf \
    --override initial_window_width=190c \
    --override initial_window_height=80c \
    --override background="#101010" \
    --override font_size=2.0 \
    -e vis &
cpid=$!
sleep 0.1
kitty --class Mixer \
    --config ~/.config/kitty/kitty.conf \
    --override initial_window_width=80c \
    --override initial_window_height=43c \
    -e alsamixer
kill $cpid
