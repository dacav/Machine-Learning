#!/usr/bin/env python

# Warning:
#
#   This file contains the logic of the program. For sake of simplicity I
#   made a relevant assumption, namely: we are working with a binary
#   classification. This module is not supposed to be generic, but
#   strictly related to the problem.
#

from __future__ import print_function, division
import itertools as it
import math
import sys
from operator import itemgetter

import utils, const

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
        A tuple containing:
        - The threshold value which, if used wrt the selected feature,
          maximizes the information gain;
        - The value of the information gain itself.
    '''
    classes_of = lambda xs : it.imap( get_class, xs )
    H = lambda xs : entropy(classes.count_by(classes_of(xs)).itervalues())
    xs_entropy = H(xs_byfeat)

    def IG (thr):
        predicate = lambda x : x[0] < thr
        h0 = H( it.ifilter(predicate, xs_byfeat) )
        h1 = H( it.ifilterfalse(predicate, xs_byfeat) )
        return (thr, xs_entropy - h0 - h1)

    cts = candidate_thresholds(xs_byfeat, classes, get_val, get_class)
    return max( it.imap(IG, cts), key=itemgetter(1) )

def run (problem):
    examples = problem.get_examples()
    classes = problem.get_classes()
    compute_threshold = lambda gen_id : threshold(
        utils.ensure_list(examples.sort_by(gen_id)),
        classes,
        examples.get_val,
        examples.get_class
    )
    genes = sorted(
        ((i, compute_threshold(i)) for i in range(problem.nfeats())),
        key=lambda (gen_id, (thrs, igain)) : igain,
        reverse=True
    )
    return genes

