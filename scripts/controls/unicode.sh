#!/bin/bash

case "$1" in
    (type) MODE=Write ;;
    (clip) MODE=Clip ;;
    (*) MODE='???' ;;
esac

MENU="$( rofi -no-lazy-grab -sep "
" -dmenu -i -p "$MODE :" \
-font "Iosevka Nerd Font 12" \
-theme "/home/vanille/.config/rofi/unicode/config.rasi" \
< ~/.config/unicode-list )"

selection=$(echo "$MENU" | sed -re 's,.*\(U\+([0-9A-F]+)\).*,\1,')
if [[ $selection != "" ]]; then
  chr="$(printf "\U$selection")"
  case "$1" in
      (type) xdotool type "$chr";;
      (clip) echo "$chr" | xclip -rmlastnl -selection clipboard;;
      (*) notify-send "Invalid action '$1' for unicode-menu";;
  esac
fi
