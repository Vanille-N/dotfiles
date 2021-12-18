#!/bin/bash

while sleep 1; do
    data="$( nmcli --pretty --color yes dev wifi )"
    clear
    echo -e "$data"
done
