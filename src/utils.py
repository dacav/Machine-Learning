#!/usr/bin/env python

from __future__ import print_function, division
import sys
import itertools as it
import math

try: range = xrange
except: pass

def ensure_list (l, private=False):
    if private or type(l) != list:
        return list(l)
    return l

def avg (xs):
    # Would be much easier to do sum(xs) / len(xs), however xs might not
    # be a list, but a generic iterator!
    xs = iter(xs)
    cnt = 1
    acc = next(xs)
    for x in xs:
        cnt += 1
        acc += x
    return acc * (1 / cnt)

