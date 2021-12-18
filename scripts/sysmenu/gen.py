#! /bin/python3

import rofi
from rofi import Entry, Cmd, CmdSeq, Fmt

name = "sysmenu"
dir_home = "/home/vanille"
dir_config = f"{dir_home}/.config"
dir_here = f"{dir_config}/scripts/{name}"
dir_rasi = f"{dir_config}/rofi/{name}"

menu = rofi.Menu(
    name,
    dir=dir_here,
    prompt="Sys",
    font_size=30,
    formatter=Fmt.center(10),
)

e_lock = Entry("lock", icon="", text="Lock", cmd=Cmd("betterlockscreen", "-l"))
e_iconut = Entry("ulog", icon="", text="Logout",
    cmd=Cmd.unimplemented("Logout"))
e_suspend = Entry("susp", icon="望", text="Suspend",
    cmd=CmdSeq(Cmd("systemctl", "suspend"), Cmd("betterlockscreen", "-l")))
e_reboot = Entry("rebt", icon="", text="Reboot", cmd=Cmd("systemcl", "reboot"))
e_shutdown = Entry("shut", icon="", text="Shutdown", cmd=Cmd("systemctl", "-i", "poweroff"))
e_killx = Entry("kilx", icon="", text="Killx", cmd=Cmd("pkill", "Xorg"))

menu.grid(
    [e_lock, e_suspend.selected(), e_shutdown],
    [None, e_reboot, e_killx],
)

menu.rasi.update({
    'layout': {
        'window': {
            'padding': 5,
            'width': 675,
            'height': 265,
        },
        'listview': {
            'columns': 3,
            'spacing': "7px",
            'border': 0,
            'padding': "5px 0 5 5",
        },
        'element': {
            'border': 1,
            'padding': "5px",
        },
        'inputbar': {
            'padding': "0px",
            'children': "[]",
        },
        'scrollbar': {
            'width': "0px",
            'handle_width': "0px",
        },
    },
    'theme': {
        'nul': { 'normal': { "fg": "fg1", "bg": "bg0" }},
        'sel': { 'normal': { "fg": "bg0-hard", "bg": "purple-dark" }},
        'alt': { 'normal': { "fg": "fg1", "bg": "bg0" }},
    },
})

menu.main()
