#! /usr/bin/python3

Name = "_NAME"
Font = "_FONT"
Fg = "_FG"
Text = "_TEXT"
FgExtend = "_FG_EXTEND"
Suffix = "_SUFFIX"
List = "_LIST"

def fontsize(text, size):
    return "<span font='Iosevka Nerd Font {}'>{}</span>".format(size, text)

icons = {
    Font: "Iosevka Nerd Font 12",
    List: [{
        Name: "backlight",
        Suffix: fontsize(" ", 5),
        List: [
            { Name: "empty", Fg: '#ffffff', Text: "" },
            { Name: "1", Fg: '#f5f4f4', Text: "" },
            { Name: "2", Fg: '#ebe9e8', Text: "" },
            { Name: "3", Fg: '#e0dedd', Text: "" },
            { Name: "4", Fg: '#d6d4d1', Text: "" },
            { Name: "5", Fg: '#ccc9c6', Text: "" },
            { Name: "6", Fg: '#c2bebb', Text: "" },
            { Name: "7", Fg: '#b8b3af', Text: "" },
            { Name: "8", Fg: '#ada8a4', Text: "" },
            { Name: "9", Fg: '#a39d98', Text: "" },
            { Name: "10", Fg: '#99928d', Text: "" },
            { Name: "11", Fg: '#8f8782', Text: "" },
            { Name: "12", Fg: '#857d76', Text: "" },
            { Name: "13", Fg: '#7a726b', Text: "" },
            { Name: "full", Fg: '#70675f', Text: "" },
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
