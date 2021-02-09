#!/bin/bash

. ~/.config/env/vars

wsprev="$( ~/.config/scripts/i3-curr-ws )"

pkill htop && exit 1

i3 workspace "$WORKSPACE_X"
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
i3 workspace "$newws"
