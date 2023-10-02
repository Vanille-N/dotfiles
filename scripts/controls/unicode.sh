#!/bin/bash

panic() {
    notify-send "Unicode" "$1"
}

MAPPING=( )
mapping_file=/tmp/unicode.numpad.map
debug_mapping() {
    return 0
    echo "Mapping {"
    for i in {0..9}; do
        echo "${MAPPING[i]}"
    done
    echo "}"
}
load_mapping() {
    touch $mapping_file
    MAPPING=( $( cat $mapping_file ) )
    debug_mapping
}
edit_mapping() {
    MAPPING[$1]="$2"
    debug_mapping
}
save_mapping() {
    for i in {0..9}; do
        echo "${MAPPING[i]}"
    done > $mapping_file
}
write_mapping() {
    code="${MAPPING[$1]}"
    if [[ $code == '' ]]; then
        return 0
    fi
    chr="$( printf "\U$code" )"
    xdotool keyup Super_L
    sleep 0.1
    xdotool type "$chr"
    sleep 0.1
    xdotool keydown Super_L
}

case "$1" in
    (type) MODE=Type ;;
    (clip) MODE=Clip ;;
    (wmap) MODE=Record; NTH="$2" ;;
    (rmap) MODE=Latest; NTH="$2" ;;
    (*) panic "Invalid argument $1; expected type, clip, wmap [N], rmap [N]" ;;
esac

case "$MODE" in
    (Type|Clip|Record)
        MENU="$( rofi -no-lazy-grab -sep "
        " -dmenu -i -p "$MODE :" \
        -font "Iosevka Nerd Font 12" \
        -theme "/home/vanille/.config/rofi/unicode/config.rasi" \
        < ~/.env/unicode-list )"

        selection=$(echo "$MENU" | sed -re 's,.*\(U\+([0-9A-F]+)\).*,\1,')
        if [[ $selection != "" ]]; then
            chr="$( printf "\U$selection" )"
            case "$MODE" in
                (Type) sleep 0.2; xdotool type "$chr";;
                (Clip) echo "$chr" | xclip -rmlastnl -selection clipboard;;
                (Record)
                    load_mapping
                    edit_mapping "$NTH" "$selection"
                    save_mapping
                    ;;
                (*) panic 'unreachable';;
            esac
        fi
        ;;
    (Latest)
        load_mapping
        write_mapping "$NTH"
        ;;
    (*) panic 'unreachable';;
esac
