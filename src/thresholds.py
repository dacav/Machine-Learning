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
        A tuple containing:
        - The threshold value which, if used wrt the selected feature,
          maximizes the information gain;
        - The value of the information gain itself.
    '''
    classes_of = lambda xs : it.imap( get_class, xs )
    H = lambda xs : entropy(classes.distrib(classes_of(xs)).itervalues())
    xs_entropy = H(xs_byfeat)

    def IG (thr):
        predicate = lambda x : x[0] < thr
        split = list( it.ifilter(predicate, xs_byfeat) )
        h0 = H(split) * len(split)
        split = list( it.ifilterfalse(predicate, xs_byfeat) )
        h1 = H(split) * len(split)
        return (thr, xs_entropy - (h0 + h1) / len(xs_byfeat))

    cts = candidate_thresholds(xs_byfeat, classes, get_val, get_class)
    return max( it.imap(IG, cts), key=itemgetter(1) )

def run (problem):
    '''
    Input:
        the problem (instance of dataset.ProblemStructure)
    Output:
        An iterator over pairs:
        - The first value is the identifier of the feature we are
          referring to;
        - The second value is a pair containing the threshold value used
          to discriminate the class and the information gain we obtained
          when analyzing the dataset.
    The output is well suited to be placed as constructor parameter for a
    dictionary.
    '''
    examples = problem.get_examples()
    classes = problem.get_classes()
    compute_threshold = lambda gen_id : threshold(
        utils.ensure_list(examples.sort_by(gen_id)),
        classes,
        examples.get_val,
        examples.get_class
    )
    return ((i, compute_threshold(i)) for i in range(problem.nfeats()))

