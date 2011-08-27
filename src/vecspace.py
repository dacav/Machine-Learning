#!/usr/bin/env python

from __future__ import print_function, division
import sys
import itertools as it
import operator

try: range = xrange
except: pass

class Vector (tuple) :
    # A very simple class implementing a very simple vectorial algebra. I
    # don't want to include cumbersome packages

    def __init__ (self, vals):
        super(Vector, self).__init__(vals)

    def _apply (self, f):
        return Vector( it.imap(f, self) )

    def _zipapply (self, f, x):
        return Vector( it.starmap(f, it.izip(self, x)) )

    def __add__ (self, x):
        try:
            return self._zipapply(operator.add, x)
        except:
            return self._apply( lambda y : y + x )

    def __sub__ (self, x):
        try:
            return self._zipapply(operator.sub, x)
        except Exception as e:
            return self._apply( lambda y : y - x )

    def __mul__ (self, x):
        return self._apply(lambda y : y * x)

    def __div__ (self, x):
        return self._apply(lambda y : y / x)

    def __str__ (self):
        return repr(self)

    def __repr__ (self):
        return "Vector" + super(Vector, self).__repr__()

    @staticmethod
    def distance (v0, v1, power=2):
        return sum( x**power for x in (v0 - v1) )**(1/power)

