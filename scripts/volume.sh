#!/usr/bin/bash

. ~/.config/env/vars

wsprev="$( ~/.config/scripts/i3-curr-ws )"

pkill alsamixer && exit 1
pkill htop && exit 1
pkill nm-connection-e && exit 1

i3 workspace "$WORKSPACE_X"
i3 layout split
i3 split h
kitty --class Visualizer \
    --config ~/.config/kitty/kitty.conf \
    --override background="#101010" \
    --override font_size=2.0 \
    -e ~/.config/scripts/vis &
    # --override initial_window_width=190c \
    # --override initial_window_height=80c \
cpid=$!
sleep 0.1
kitty --class Mixer \
    --config ~/.config/kitty/kitty.conf \
    -e alsamixer
    # --override initial_window_width=80c \
    # --override initial_window_height=43c \
kill $cpid

newws="$( ~/.config/scripts/i3-curr-ws )"
i3 workspace "$wsprev"
if [ ! "$newws" == "$WORKSPACE_X" ]; then
    i3 workspace "$newws"
fi
