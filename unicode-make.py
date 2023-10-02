#!/usr/bin/python

from unicodedata import name

for i in range(1_000_000):
    try:
        print(" {} (U+{}) {}".format(chr(i), i, name(chr(i))))
    except ValueError:
        pass
