#!/bin/bash

. ~/.config/env/vars

wsprev="$( ~/.config/scripts/i3-curr-ws )"

pkill htop && exit 1
pkill nm-connection-e && exit 1
pkill alsamixer && exit 1

i3 workspace "$WORKSPACE_X"
i3 layout split
i3 split h
kitty --class Bottom \
    --config ~/.config/kitty/kitty.conf \
    --override font_size=7.0 \
    -e btm &
    # --override initial_window_width=93c \
    # --override initial_window_height=60c \
cpid=$!
sleep 0.05
kitty --class Top \
    --config ~/.config/kitty/kitty.conf \
    -e htop
kill $cpid

newws="$( ~/.config/scripts/i3-curr-ws )"
i3 workspace "$wsprev"
if [ ! "$newws" == "$WORKSPACE_X" ]; then
    i3 workspace "$newws"
fi
