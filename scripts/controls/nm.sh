#!/bin/bash

while sleep 1; do
    data="$( nmcli --pretty --color yes dev wifi | head -n50)"
    clear
    echo -e "$data"
done
