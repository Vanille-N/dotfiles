#! /bin/python3

# File: rofi.py
# Desc: menu sorter for dmenu-likes
# Author: Vanille-N <vanille@crans.org>
# Updated: Dec. 2021


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

from itertools import zip_longest
import jinja2 as j2
import os

import rasi

templ_dir = "/home/vanille/.env/scripts/template"

class Fitness:
    """Check query fitness and evaluate cost"""
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
        """Cost of typing a key.
        Please adjust depending on keyboard layout and personal preference.
        Lowercase only.
        """
        s = 0
        for c in l:
            if c in "aoeuhtns":
                s += 1
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
        print(f"Best for {min_entry} is '{min_query}' with cost {min_cost}")
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
        return c

    def unimplemented(title):
        return Cmd("notify-send", "Unimplemented", title)

class CmdSeq:
    def __init__(self, *cmds):
        self.cmds = cmds

    def __str__(self):
        return " && ".join(c.__str__() for c in self.cmds)

class Menu:
    """A collection of entries"""
    def __init__(self, name, *, dir, prompt, font_size=12, formatter=Fmt.line(19)):
        self.name = name
        self.dir = dir
        self.prompt = prompt
        self.entries = []
        self.pre = ""
        self.sortable = False
        self.select = 0
        self.font_size = font_size
        self.formatter = formatter
        self.rasi = rasi.settings

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

    def gen_rasi(self):
        """Regenerate the .rasi configuration files"""
        rasi.generate_conf(self.name, self.rasi)

    def update_rasi(self, settings):
        """Edit the rasi options"""
        rasi.update(self.rasi, settings)

    def render(self):
        """Generate output files 'menu' and 'main.sh'"""
        src_file = f"{templ_dir}/main.sh.j2"
        to_file = f"{self.dir}/main.sh"
        data_file = f"{self.dir}/menu"
        print(f"Generating {to_file} from {src_file}")
        print(f"  Metadata in {data_file}")
        if self.sortable:
            self.sort()
        with open(data_file, 'w') as f:
            for i,e in enumerate(self.entries):
                if e is not None:
                    f.write(self.formatter.fmt(e))
                    if e.select:
                        self.select = i
                f.write("|")

        with open(src_file, 'r') as f:
            template = j2.Template(f.read())
        text = template.render(
            name=self.name,
            prompt=self.prompt,
            dir=os.path.abspath(self.dir),
            theme=rasi.theme_location(self.name),
            pre=self.pre,
            sel_row=self.select,
            font=self.font_size,
            eh=self.formatter.height,
            entries=self.entries,
        )
        with open(to_file, 'w') as f:
            f.write(text)

    def count_freq(self):
        """Read log file to look at usage frequencies.
        Also updates log for caching.
        """
        freqs = {}
        logfile = f"{self.dir}/log"
        print(f"Updating {logfile}")
        with open(logfile, 'a+') as f:
            f.seek(0)
            for line in f.readlines():
                #print(line)
                tag,count = line.split(',')
                if tag not in freqs:
                    freqs[tag] = 0
                freqs[tag] += int(count)
        with open(logfile, 'w') as f:
            for k in freqs:
                f.write("{},{}\n".format(k, freqs[k]))
        return freqs

    def sort(self):
        """Order entries according to best known criteria.
        Current: frequency only
        Objective: mix of frequency and collisions
        """
        f = Fitness()
        freq = self.count_freq()
        for e in self.entries:
            e.weight *= freq.get(e.uid) or 1
            f.push(e)
        f.freeze()
        f.optimize()
        self.entries = f.extract()
        #self.entries.sort(key=lambda e: freq.get(e.uid) or 0, reverse=True)
        f.check_queries()
        print(f.measure_cost())
        #print(self.entries)

