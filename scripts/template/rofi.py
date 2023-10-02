#! /bin/python3

# File: rofi.py
# Desc: menu sorter for dmenu-likes
# Author: Vanille-N <vanille@crans.org>
# Updated: Dec. 2021


### Purpose
# In order to make dmenu/rofi more efficient and reliable, this program
# is tasked with generating scripts and organizing entries in an order
# that minimizes keystrokes
#
# It looks at
# - frequency of use
# - query collisions
# to organize menu entries in the best order
#
# To illustrate, here is a simple example. Suppose there are just 3 entries.
#    program     frequency
#      abcde             1
#       abde             2
#       acde             3
# Then for the order abcde,abde,acde the optimal keystrokes are a,bd,ac
# for an expected cost of 1*1 + 2*2 + 3*2 = 11
# Reordering to acde,abde,abcde yields the keystrokes c,b,bc
# which only cost 3*1 + 2*1 + 1*2 = 7
# Finding the optimal ordering, or at least one that is as close to
# that as possible, is the goal of this program

### Algorithm
# Builds the list in reverse order by getting out of the way the entries
# with the least costly unique query.
# More details at the bottom.

from itertools import zip_longest
import jinja2 as j2
import os
import sys

templ_dir = "/home/vanille/.env/scripts/template"

def deepclone(obj):
    if type(obj) == list:
        return [ deepclone(i) for i in obj ]
    elif type(obj) == dict:
        return { k:deepclone(obj[k]) for k in obj }
    else:
        return obj

class Targets:
    """Which targets to build
    - all
      - menu
      - shell
      - freq
      - sort
      - rasi
        - theme
        - config
        - layout
    """

    keys = ['menu', 'shell', 'freq', 'sort', 'theme', 'config', 'layout']
    features = {
        'rasi': ['theme', 'config', 'layout'],
        'all': ['menu', 'shell', 'freq', 'sort', 'rasi'],
    }
    def __init__(self):
        self.settings = { k: True for k in Targets.keys }

    def set(self, feature, value):
        if feature in Targets.keys:
            self.settings[feature] = value
        elif feature in Targets.features:
            for sub in Targets.features[feature]:
                self.set(sub, value)
        else:
            print(f"Invalid feature: '{feature}' is not defined")

    def parse(args):
        t = Targets()
        for a in args:
            if a[0] == '-':
                action = False
            elif a[0] == '+':
                action = True
            else:
                print(f"Invalid argument: '{a}' should start with '+' or '-'")
                continue
            param = a[1:]
            t.set(param, action)
        return t

    def gated(self, setting):
        if not self.settings[setting]:
            print(f"Feature '{setting}' is deactivated")
        return self.settings[setting]

class Fitness:
    """Determine optimal queries and evaluate cost"""
    def __init__(self):
        self.entries = []
        self.queries = set()
        self.frozen = False

    def frozen(status):
        def decorator(f):
            def wrapped(self, *args, **kwargs):
                assert self.frozen == status
                return f(self, *args, **kwargs)
            return wrapped
        return decorator

    def cost(l):
        """Cost of typing a sequence of keys.
        Please adjust depending on keyboard layout and personal preference.
        Lowercase only.
        """
        s = 0.0
        for c in l:
            if c in "aoeuhtns":
                s += 1.0
            elif c in "idcrljmgp":
                s += 1.2
            elif c in "xkbwvzqfy":
                s += 1.4
            elif c in "135246":
                s += 1.5
            elif c in "7908":
                s += 1.6
            else:
                print("'{}' has no attributed cost".format(c))
                raise ValueError(c)
        return s

    def substrings(s):
        """Set of all (contiguous) substrings of the input"""
        sub = { s[i:j] for i in range(len(s)) for j in range(i+1, len(s)+1) }
        return { s for s in sub if ' ' not in s }

    @frozen(False)
    def freeze(self):
        """Mark the end of the modification phase and the beginning of the query phase"""
        self.frozen = True
        self.queries = sorted(list(self.queries), key=Fitness.cost)
        self.match_query = None
        self.match_entry = None

    @frozen(False)
    def push(self, entry):
        """Register a new entry and all its matching queries"""
        self.entries.append(entry)
        self.queries = self.queries.union(Fitness.substrings(entry.text.lower()))

    @frozen(True)
    def check_queries(self):
        """Create double-access maps of queries-to-entries"""
        if self.match_query is not None:
            return (self.match_query, self.match_entry)
        match_query = {}
        match_entry = {}
        for e in self.entries:
            for q in self.queries:
                if q in e.text.lower():
                    if e not in match_entry:
                        match_entry[e] = set()
                    if q not in match_query:
                        match_query[q] = set()
                    match_entry[e].add(q)
                    match_query[q].add(e)
        match_entry = { e:sorted(list(q), key=Fitness.cost) for e,q in match_entry.items() }
        self.match_query = match_query
        self.match_entry = match_entry
        return (self.match_query, self.match_entry)

    @frozen(True)
    def measure_cost(self):
        """Measure average cost of a query
        (depending on keystrokes and frequency)
        """
        self.check_queries()
        used = set()
        cost = 0
        for e in self.entries:
            for q in self.match_entry[e]:
                if q not in used:
                    print(f"{e}: {q} ({e.weight})")
                    cost += Fitness.cost(q) * e.weight
                    break
            else:
                print("{}: unreachable".format(e))
                cost += 10 * e.weight
            used = used.union(set(self.match_entry[e]))
        return cost / sum(e.weight for e in self.entries)

    @frozen(True)
    def least_cost_unique(self, work):
        """Extract least costly query that disturbs no other entry"""
        self.check_queries()
        min_cost = 1_000_000
        min_query = None
        min_entry = None
        for e in work:
            for q in self.match_entry[e]:
                cost = Fitness.cost(q) * e.weight
                if cost < min_cost:
                    #print(f"Seeing if {q} is unique to {e}")
                    matches = work.intersection(self.match_query[q])
                    #print(f"  Matches: {matches}")
                    if len(matches) == 1:
                        #print(f"  Cost: {cost}")
                        min_cost = cost
                        min_query = q
                        min_entry = e
        unit_cost = min_cost / min_entry.weight
        print(f"Best for {min_entry} is '{min_query}': cost {min_cost} ({unit_cost} each)")
        return (min_query, min_entry)

    @frozen(True)
    def optimize(self):
        opt = []
        work = {*self.entries}
        while len(work) > 0:
            (q, e) = self.least_cost_unique(work)
            e.best_query = q
            work.remove(e)
            opt.append(e)
        self.entries = opt[::-1]

    @frozen(True)
    def extract(self):
        return self.entries

class Entry:
    """A menu line and its command invocation"""
    def __init__(self, uid, *, icon, text, cmd, weight=1):
        self.uid = uid
        self.icon = icon
        self.text = text
        self.cmd = cmd
        self.weight = weight
        self.select = False
        self.best_query = None

    def __str__(self):
        return "Entry({}, {})".format(self.text, self.cmd.prog)
    def __repr__(self):
        return self.__str__()

    def selected(self):
        self.select = True
        return self

class Fmt:
    """Custom formatters for entries.
    Each formatter should define
    - fmt : Entry -> str
        the text to be produced
    - height : int
        the number of lines on which the formatter places text
    """
    def line(width):
        """
        -----------------
        | icon     text |
        -----------------
        """
        def fmt(e):
            base = f"  {e.icon}   {e.text}"
            if e.best_query is not None:
                base += " " * (width - len(e.text))
                base += f"<span size=\"xx-small\">({e.best_query})</span>"
            return base

        f = Fmt()
        f.fmt = fmt
        f.height = 1
        return f

    def center(width):
        """
        ----------------
        |     icon     |
        |     text     |
        ----------------
        """
        def pad(text, width):
            text = f"{text}"
            n = len(text)
            margin = (width - n) // 2
            return " " * margin + text

        def fmt(e):
            icon = pad(e.icon, width)
            text = pad(e.text, width)
            return f"{icon}\n{text}"

        f = Fmt()
        f.fmt = fmt
        f.height = 2
        return f

class Cmd:
    """A command to execute"""
    def __init__(self, prog, *args):
        self.prog = prog
        self.args = args

    def __str__(self):
        c = self.prog
        for a in self.args:
            c += " '{}'".format(a)
        return c + " &>> /tmp/rofi.log"

    def unimplemented(title):
        return Cmd("notify-send", "Unimplemented", title)

class CmdSeq:
    def __init__(self, *cmds):
        self.cmds = cmds

    def __str__(self):
        return " && ".join(c.__str__() for c in self.cmds)

class Rasi:
    """Config helper for .rasi files"""
    def __init__(self, dir_home, name):
        self.directory = f"{dir_home}/.config/rofi"
        self.name = name
        layout =  {
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

        self.settings = {
            "layout": layout,
            "theme": theme,
            "config": {},
        }

    def update(self, diff):
        def aux(current, diff):
            for k in diff:
                if type(diff[k]) == dict:
                    aux(current[k], diff[k])
                else:
                    current[k] = diff[k]
        aux(self.settings, diff)

    def theme_location(self):
        return f"{self.directory}/{self.name}/config.rasi"

    def generate_file(self, *, to, file, config, targets=Targets()):
        src_file = f"{templ_dir}/{file}.rasi.j2"
        to_file = f"{to}/{file}.rasi"
        if targets.gated(file):
            print(f"  Generating {to_file} from {src_file}")
            with open(src_file, 'r') as f:
                template = j2.Template(f.read())
            text = template.render(**config)
            with open(to_file, 'w') as f:
                f.write(text)

    def generate(self, targets):
        destination = f"{self.directory}/{self.name}"
        print(f"Configuring {destination}")
        os.makedirs(destination, exist_ok=True)
        for (file,config) in self.settings.items():
            self.generate_file(to=destination, file=file, config=config, targets=targets)

class Menu:
    """A collection of entries"""
    def __init__(self, name, *, dir, prompt, font_size=12, formatter=Fmt.line(18)):
        self.name = name
        self.dir = dir
        self.prompt = prompt
        self.entries = []
        self.pre = ""
        self.sortable = False
        self.select = 0
        self.font_size = font_size
        self.formatter = formatter
        self.rasi = Rasi("/home/vanille", self.name)

    def list(self, *entries):
        """A List menu.
        Suitable for:
        - many entries
        - text filtering
        """
        self.entries = list(entries)
        self.sortable = True

    def pre_text(self, t):
        self.pre += t

    def grid(self, *lines):
        """A Grid menu.
        Suitable for:
        - few entries
        - arrow navigation
        """
        columns = zip_longest(*lines)
        self.entries = [ i for c in columns for i in c ]

    def render(self, targets=Targets()):
        """Generate output files 'menu' and 'main.sh'"""
        src_file = f"{templ_dir}/main.sh.j2"
        to_file = f"{self.dir}/main.sh"
        data_file = f"{self.dir}/menu"
        print(f"Generating {to_file} from {src_file}")
        print(f"  Metadata in {data_file}")
        if self.sortable:
            self.sort(targets)
        if targets.gated('menu'):
            print(f"Generate {data_file}")
            with open(data_file, 'w') as f:
                for i,e in enumerate(self.entries):
                    if e is not None:
                        f.write(self.formatter.fmt(e))
                        if e.select:
                            self.select = i
                    f.write("|")

        if targets.gated('shell'):
            with open(src_file, 'r') as f:
                template = j2.Template(f.read())
            text = template.render(
                name=self.name,
                prompt=self.prompt,
                dir=os.path.abspath(self.dir),
                theme=self.rasi.theme_location(),
                pre=self.pre,
                sel_row=self.select,
                font=self.font_size,
                eh=self.formatter.height,
                entries=self.entries,
            )
            with open(to_file, 'w') as f:
                f.write(text)

    def count_freq(self, targets=Targets()):
        """Read log file to look at usage frequencies.
        Also updates log for caching.
        """
        freqs = {}
        logfile = f"{self.dir}/log"
        with open(logfile, 'a+') as f:
            f.seek(0)
            for line in f.readlines():
                #print(line)
                tag,count = line.split(',')
                if tag not in freqs:
                    freqs[tag] = 0
                freqs[tag] += int(count)
        if targets.gated('freq'):
            print(f"Updating {logfile}")
            with open(logfile, 'w') as f:
                for k in freqs:
                    f.write("{},{}\n".format(k, freqs[k]))
        return freqs

    def sort(self, targets=Targets()):
        """Order entries.
        Best known criterion is a mix of frequency and collisions.
        """
        f = Fitness()
        freq = self.count_freq(targets)
        for e in self.entries:
            e.weight *= freq.get(e.uid) or 1
            f.push(e)
        f.freeze()
        if targets.gated('sort'):
            f.optimize()
            self.entries = f.extract()
            #self.entries.sort(key=lambda e: freq.get(e.uid) or 0, reverse=True)
        f.check_queries()
        print(f.measure_cost())
        #print(self.entries)

    def main(self, args=sys.argv[1:]):
        targets = Targets.parse(args)
        self.render(targets)
        self.rasi.generate(targets)

### Algorithm (details & proof)
# Define:
#   - match
#     q matches e if q is a substring of e.text
#   - reach
#     q reaches e among E if e is the first entry in E to be matched by q
#   - unique
#     q is unique for e among E a list of entries
#     if q matches e and no other entry in E.
#       unique q E e := forall e', In e' E -> (e' = e <-> match q e')
#
# Observe that:
#   - a query which reaches the last element is unique to the last element
#   - if several queries are unique to different elements these elements can
#     be ordered in any way among themselves
#   - if sereval queries are unique to a single element, the least global cost comes
#     comes from choosing the query with the least cost
#
# Procedure:
#   least_cost entries:
#     for each entry:
#       compute cost of all unique queries
#     return the minimum
#
#   order entries:
#     sorted = ()
#     while entries not empty:
#       extract least_cost from entries
#       prepend it to sorted
#     return sorted
#
# The algorithm repeatedly finds the entry which is least costly
# to place in last because it has the unique query with the smallest
# cost.
