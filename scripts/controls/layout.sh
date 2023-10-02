#! /bin/bash

CONF_DIR="/home/vanille/.env"
EXEC_DIR="$CONF_DIR/scripts/controls"
ENV_DIR="$CONF_DIR/shell"
LAYOUT_DIR="$CONF_DIR/i3/layouts"

pkill nm-connection-e && exit 1
pkill htop && exit 1
pkill alsamixer && exit 1

SELECT="$1"

# Save workspace to restore it afterwards
wsprev="$( ~/.config/scripts/i3-curr-ws )"

# Setup new workspace
. $ENV_DIR/workspaces.sh
i3-msg "workspace $WORKSPACE_X"
i3-msg "append_layout $LAYOUT_DIR/$SELECT.json"
i3-msg "focus child"
i3-msg "focus right"

# Open windows
"$EXEC_DIR/$SELECT.sh"

# Restore previous workspace
newws="$( ~/.config/scripts/i3-curr-ws )"
i3 workspace "$wsprev"
if [ ! "$newws" == "$WORKSPACE_X" ]; then
    i3 workspace "$newws"
fi
