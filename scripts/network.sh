#!/bin/bash

kitty --class Scanner \
    --config ~/.config/kitty/kitty.conf \
    --override initial_window_width=100c \
    -e ~/.config/scripts/nm.sh &
cpid=$!
sleep 0.05
nm-connection-editor
kill $cpid
