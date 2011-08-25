#!/usr/bin/env python

from __future__ import print_function, division
import sys
import itertools as it

try: range = xrange
except: pass

class ParseError (Exception) : pass

def run (raw, problem_build):

    def check_types (types):
        pts = filter(lambda(n,x) : x != "continuous", enumerate(types))
        if pts:
            raise NotImplementedError("Found non-continuous feats", pts)

    def split (r):
        tokens = r.split('\t')
        tail = tokens.pop()
        return tokens, tail

    items = it.imap(split, raw);
    problem = problem_build(next(items)[0])

    check_types(next(items)[0]) # Just a check
    next(items) #useless empty row!

    for (fts, cls) in it.ifilter(None, items):
        problem.add_example(fts, cls.strip())
    return problem
