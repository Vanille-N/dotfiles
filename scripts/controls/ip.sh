#!/bin/bash

while sleep 1; do
    data="$( ip -c a )"
    clear
    echo -e "$data"
done
