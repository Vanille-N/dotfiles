#!/usr/bin/bash

kitty --class Visualizer \
    --override font_size=2.0 \
    --override background="#101010" \
    --override initial_window_width=190c \
    --override initial_window_height=80c \
    -e vis &
cpid=$!
sleep 0.1
kitty --class Mixer \
    --override initial_window_width=80c \
    --override initial_window_height=43c \
    -e alsamixer
kill $cpid
