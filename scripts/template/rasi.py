#! /bin/python3

# File: rasi.py
# Desc: configuration helper for .rasi files (rofi settings)
# Author: Vanille-N <vanille@crans.org>
# Updated Dec. 2021

from collections import namedtuple
import jinja2 as j2
import os

templ_dir = f"/home/vanille/.env/scripts/template"
rofi_dir = f"/home/vanille/.config/rofi"

def deepclone(obj):
    if type(obj) == list:
        return [ deepclone(i) for i in obj ]
    elif type(obj) == dict:
        return { k:deepclone(obj[k]) for k in obj }
    else:
        return obj

layout = {
    "window": {
        "width": 100,
        "height": 100,
        "border": 2,
        "padding": 2,
    },
    "listview": {
        "columns": 1,
        "spacing": "2px",
        "padding": "2px 0 0",
        "border": "2px solid 0 0",
    },
    "scrollbar": {
        "width": "4px",
        "border": 0,
        "handle_width": "8px",
        "padding": 0,
    },
    "inputbar": {
        "spacing": 0,
        "padding": "2px",
        "children": "[prompt, textbox-prompt-sep, entry, case-indicator]",
    },
    "element": {
        "border": 0,
        "padding": "2px",
    },
}

normal = {
    "bg": "red-dark",
    "fg": "red-light",
}
active = deepclone(normal)
urgent = deepclone(normal)

nul = {
    "normal": normal,
    "urgent": urgent,
    "active": active,
}
alt = deepclone(nul)
sel = deepclone(nul)

theme = {
    "nul": nul,
    "alt": alt,
    "sel": sel,
}

settings = {
    "layout": layout,
    "theme": theme,
    "config": {},
}

def update(current, diff):
    for k in diff:
        if type(diff[k]) == dict:
            update(current[k], diff[k])
        else:
            current[k] = diff[k]

def theme_location(name):
    return f"{rofi_dir}/{name}/config.rasi"

def generate_file(*, to, file, config):
    src_file = f"{templ_dir}/{file}.rasi.j2"
    to_file = f"{to}/{file}.rasi"
    print(f"  Generating {to_file} from {src_file}")
    with open(src_file, 'r') as f:
        template = j2.Template(f.read())
    text = template.render(**config)
    with open(to_file, 'w') as f:
        f.write(text)

def generate_conf(name, settings):
    destination = f"{rofi_dir}/{name}"
    print(f"Configuring {destination}")
    os.makedirs(destination, exist_ok=True)
    for (file,config) in settings.items():
        generate_file(to=destination, file=file, config=config)

if __name__ == '__main__':
    generate_conf("autogen_test", settings)

