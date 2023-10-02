#! /usr/bin/python3

Name = "_NAME"
Font = "_FONT"
Fg = "_FG"
Text = "_TEXT"
FgExtend = "_FG_EXTEND"
Suffix = "_SUFFIX"
List = "_LIST"
Array = "_ARRAY"

def fontsize(text, size):
    return "<span font='Iosevka Nerd Font {}'>{}</span>".format(size, text)

icons = {
    Font: "Iosevka Nerd Font 12",
    List: [{
        Name: "backlight",
        Suffix: fontsize(" ", 5),
        Array: [
            { Fg: '#ffffff', Text: "" },
            { Fg: '#f5f4f4', Text: "" },
            { Fg: '#ebe9e8', Text: "" },
            { Fg: '#e0dedd', Text: "" },
            { Fg: '#d6d4d1', Text: "" },
            { Fg: '#ccc9c6', Text: "" },
            { Fg: '#c2bebb', Text: "" },
            { Fg: '#b8b3af', Text: "" },
            { Fg: '#ada8a4', Text: "" },
            { Fg: '#a39d98', Text: "" },
            { Fg: '#99928d', Text: "" },
            { Fg: '#8f8782', Text: "" },
            { Fg: '#857d76', Text: "" },
            { Fg: '#7a726b', Text: "" },
            { Fg: '#70675f', Text: "" },
        ],
    }, {
        Name: "bat",
        FgExtend: True,
        List: [
            { Name: "full", Fg: '#98971a', Text: "" },
            { Name: "charging", Fg: '#b16286', Text: "" },
            { Name: "empty", Fg: '#cc241d', Text: "" },
            { Name: "quarter", Fg: '#d65d0e', Text: "" },
            { Name: "half", Fg: '#d79921', Text: "" },
            { Name: "three_quarters", Fg: '#d79921', Text: "" },
        ],
    }, {
        Name: "volume",
        List: [
            { Name: "muted", Text: "婢" },
            { Name: "empty", Text: "奄" },
            { Name: "half", Text: "奔" },
            { Name: "full", Text: "墳" },
        ],
    }, {
        Name: "net",
        Suffix: " ",
        List: [
            { Name: "wired", Text: "" },
            { Name: "wireless", Text: "直" },
            { Name: "up" },
            { Name: "down" },
        ],
    }, {
        Name: "cpu",
        Suffix: " ",
        List: [
            { Text: "﬙" },
            { Name: "boost_on" },
            { Name: "boost_off" },
        ],
    }, {
        Name: "memory",
        Suffix: " ",
        List: [
            { Name: "mem", Text: "" },
            { Name: "swap" },
        ],
    }, {
        Name: "time",
        Suffix: " ",
        List: [
            { Text: "" },
        ],
    }, {
        Name: "toggle_quiet",
        List: [
            { Name: "on", Fg: "#665c54", Text: "" },
            { Name: "off", Fg: "#d79921", Text: "" },
        ],
    }],
}

def get_or_else(key, *args, default=None):
    for x in args:
        if key in x:
            return x[key]
    return default

def generate_icon(*maps):
    text = get_or_else(Text, *maps, default="")
    fg = get_or_else(Fg, *maps)
    extend = get_or_else(FgExtend, *maps, default=False)
    font = get_or_else(Font, *maps)
    suffix = get_or_else(Suffix, *maps, default="")
    if text != "":
        text += suffix
        if font is not None:
            text = "<span font='{}'>{}</span>".format(font, text)
    if fg is not None:
        text = "<span foreground='{}'>".format(fg) + text
        if not extend:
            text += "</span>"
    name = [m.get(Name) for m in maps[::-1]]
    name = [n for n in name if n is not None]
    name = "_".join(name)
    print('{} = "{}"'.format(name, text))

for icon in icons[List]:
    for sub in icon[List]:
        generate_icon(sub, icon, icons)
    print()
