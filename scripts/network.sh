#!/bin/bash

wsprev="$( ~/.config/scripts/i3-curr-ws )"

pkill nm-connection-e && exit 1

i3 workspace "100:×"
kitty --class Scanner \
    --config ~/.config/kitty/kitty.conf \
    --override font_size=8.0 \
    -e ~/.config/scripts/nm.sh &
    # --override initial_window_width=100c \
cpid1=$!
sleep 0.1
kitty --class Scanner \
    --config ~/.config/kitty/kitty.conf \
    --override font_size=8.0 \
    -e ~/.config/scripts/ip.sh &
cpid2=$!
sleep 0.5
i3 split v
bash -c "sleep 0.5; i3 resize shrink width 170 px" &
nm-connection-editor
kill $cpid1
kill $cpid2

newws="$( ~/.config/scripts/i3-curr-ws )"
if [[ "$newws" = "100:×" ]]; then
    i3 workspace "$wsprev"
fi
