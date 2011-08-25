#!/usr/bin/env python

# Warning:
#
#   This file contains the logic of the program. For sake of simplicity I
#   made a relevant assumption, namely: we are working with a binary
#   classification. This module is not supposed to be generic, but
#   strictly related to the problem.
#

from __future__ import print_function, division
import sys
import itertools as it
import math

import utils

try: range = xrange
except: pass

def entropy (P):
    log2 = lambda x : math.log(x, 2)
    return - sum(x * log2(x) for x in P if x)

def candidate_thresholds (xs_byfeat, classes, get_val, get_class):
    '''
    Given an ordered set of examples (output from Examples.sort_by
    method), yields all the average between two consecutive examples
    belonging to different classes.
    '''
    prevs, nexts = iter(xs_byfeat), iter(xs_byfeat)
    next(nexts)

    for (p,n) in it.izip(prevs, nexts):
        if not classes.cmp(get_class(p), get_class(n)):
            # They're different, thus we have a candidate threshold
            yield ( get_val(p) + get_val(n) ) / 2

def threshold (xs_byfeat, classes, get_val, get_class):
    '''
    Input:
        - A set of examples sorted by some feature;
        - The classes manager;
        - The callbacks to extract value and class from an example
    Output:
        The threshold value which, if used wrt the selected feature,
        maximizes the information gain.
    '''
    classes_of = lambda xs : it.imap( get_class, xs )
    H = lambda xs : entropy(classes.count_by(classes_of(xs)).itervalues())

    xs_entropy = H(xs_byfeat)
    def IG (thr):
        predicate = lambda x : x < thr
        h0 = H( it.ifilter(predicate, xs_byfeat) ) 
        h1 = H( it.ifilterfalse(predicate, xs_byfeat) )
        return (thr, xs_entropy - h0 - h1)

    cts = candidate_thresholds(xs_byfeat, classes, get_val, get_class)
    return max( it.imap(IG, cts), key=lambda x : x[1] )[0]

def run (problem):
    examples = problem.get_examples()
    classes = problem.get_classes()
    for i in range(problem.nfeats()):
        thr = threshold(examples.sort_by(i), classes, 
                        examples.get_val, examples.get_class)
        print("Working with examples for gene", i, ":", thr)
    
