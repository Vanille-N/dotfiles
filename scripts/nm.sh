#!/bin/bash
while sleep 1; do
    data="$( nmcli --color yes dev wifi )"
    clear
    echo -e "$data"
done
