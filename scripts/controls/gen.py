#! /bin/python3

import rofi
from rofi import Entry, Cmd

name = "controls"
dir_home = "/home/vanille"
dir_config = f"{dir_home}/.config"
dir_here = f"{dir_home}/.env/scripts/{name}"
dir_dest = f"{dir_config}/scripts/{name}"
dir_rasi = f"{dir_config}/rofi/{name}"

menu = rofi.Menu(
    name,
    dir=dir_dest,
    prompt="Monitor",
    font_size=30,
    formatter=rofi.Fmt.center(10),
)

def local(cmd, *args):
    return Cmd(f"{dir_here}/{cmd}", *args)
def layout(*args):
    return local("layout.sh", *args)
def unicode(*args):
    return local("unicode.sh", *args)

menu.pre_text("""\
pkill nm-connection-e && exit 1
pkill htop && exit 1
pkill alsamixer && exit 1
""".format(here=dir_here))

e_net = Entry("netw", icon="", text="Net", cmd=layout("network"))
e_proc = Entry("proc", icon="", text="Procs", cmd=layout("procs"))
e_click = Entry("clic", icon="", text="Click", cmd=local("auclick", "--until", "e"))
e_mix = Entry("mixr", icon="\u200Eﰝ", text="Mixer", cmd=layout("volume"))
e_pass = Entry("pass", icon="\u200Eﳳ", text="Pass", cmd=Cmd("passmenu"))
e_clip = Entry("clip", icon="", text="Clip", cmd=unicode("clip"))
e_write = Entry("writ", icon="", text="Write", cmd=unicode("type"))

menu.grid(
    [e_net, e_mix, e_clip],
    [e_proc, e_pass.selected(), e_write],
    [e_click, None, None],
)

menu.rasi.update({
    'layout': {
        'window': {
            'padding': 5,
            'width': 650,
            'height': 385,
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
        'sel': { 'normal': { "fg": "bg0-hard", "bg": "green-dark" }},
        'alt': { 'normal': { "fg": "fg1", "bg": "bg0" }},
    },
})

menu.main()
