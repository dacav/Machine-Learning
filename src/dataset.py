#!/usr/bin/env python

from __future__ import print_function, division
import sys
import itertools as it
import utils
from collections import defaultdict

try: range = xrange
except: pass

class ProblemError (Exception) : pass

class Item :

    def __init__ (self, features, cls):
        self.cls = cls
        self.features = features

class Examples:

    @staticmethod
    def get_val (x):
        return x[0]

    @staticmethod
    def get_class (x): return x[1]

    def __init__ (self, problem):
        self.problem = problem
        self.select = -1
        self.sortcache = defaultdict(self.build_sorting)

    def build_sorting (self):
        exs = self.problem.examples
        sel = self.select
        return sorted(((p.features[sel], p.cls) for p in exs),
                      key=Examples.get_val)

    def sort_by (self, feat_id, cache=False):
        if ( feat_id >= self.problem.nfeats() ):
            raise ProblemError("We have only", self.problem.nfeats(),
                               "features! You asked for feature", feat_id)
        self.select = feat_id
        if cache:
            return self.sortcache[feat_id]
        else:
            return self.build_sorting()

class Classes:

    def __init__ (self):
        self.u = dict()

    def unique (self, name):
        return self.u.setdefault(name, name)

    def cmp (self, name0, name1):
        return id(name0) == id(name1)

    def distrib (self, ex_classes, normalize=True):
        '''
        Given an iterator on the classes of a certain example set, returns
        a dictionary [ class -> count ]. By enabling the normalize flag
        you can shape the result as probability distribution.
        '''
        buckets = dict( (k, 0) for k in self.u )
        cnt = 0
        for x in ex_classes:
            buckets[x] += 1
            cnt += 1
        if normalize and cnt:
            buckets.update( (c, n/cnt) for (c,n) in buckets.iteritems() )
        return buckets

class ProblemStructure :

    def __init__ (self, feat_names):
        self.classes = Classes()
        self.examples = list()
        self.feat_names = feat_names

    def nfeats (self):
        return len(self.feat_names)

    def check_nfeats (self, feats):
        fc = len(self.feat_names)
        nfc = len(feats)
        if fc != nfc:
            raise ProblemError("Incongruent number of features:",
                               "should be", fc, "but we have", nfc)

    def add_example (self, features, class_name):
        features = list( it.imap(float, features) )
        self.check_nfeats(features)
        pat = Item(features, self.classes.unique(class_name))
        self.examples.append(pat)

    def get_examples (self):
        return Examples(self)

    def get_classes (self):
        return self.classes
