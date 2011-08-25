#!/usr/bin/env python

from __future__ import print_function, division
import sys
import itertools as it

try: range = xrange
except: pass

def ensure_list (l, private=False):
    if private or type(l) != list:
        return list(l)
    return l

