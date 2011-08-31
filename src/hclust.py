#!/usr/bin/env python

from __future__ import print_function, division
import sys
import itertools as it
import operator

from utils import avg
from vecspace import Vector

try: range = xrange
except: pass

class ClustComparers :
    # All those algorithms must return a scalar value which gives a
    # neighborhood index

    @staticmethod
    def distances (c0, c1):
        return it.starmap(Vector.distance, it.product(c0, c1))

    @staticmethod
    def nearest_neighbor (c0, c1):
        return min( ClustComparers.distances(c0, c1) )

    @staticmethod
    def farthest_neighbor (c0, c1):
        return max( ClustComparers.distances(c0, c1) )

    @staticmethod
    def average_distance (c0, c1):
        return avg( ClustComparers.distances(c0, c1) )

    @staticmethod
    def dist_average (c0, c1):
        return Vector.distance(avg(c0), avg(c1))

class ClusterManager :

    def __init__ (self, items, clust_cmp = ClustComparers.dist_average,
                  history=None):
        # The cmp_clusters function will return a tuple containing the
        # couple of compared clusters as first item and the comparison
        # score on the second
        self.cmp_clusters = lambda c0, c1 : ((c0, c1), clust_cmp(c0, c1))

        # The cluster set is a mapping from the unique id of a cluster to
        # the set corresponding to the cluster. Note: all clusters are
        # contained here, thus this trick works pretty well.
        clusters = dict( it.imap(lambda x : (id(x), x),
                                 it.imap(lambda *xs : set(xs), items)) )
        self.clusters = clusters

        # History callback: used as: history(c0, c1, merged(c0, c1))
        self.history = history
        if history:
            # if we keep some history, then we need to avoid
            # garbage-collecting of the clusters.
            self.all_clusters = list(self)

    def fixed_point (self):
        return len(self.clusters) == 1

    def step (self):
        # Merge the closest pair of clusters, return True if there's only
        # one cluster left.
        self.merge(*self.neirest_pair())
        return self.fixed_point()

    def all_steps (self):
        while not self.step(): pass

    def nclusts (self):
        return len(self.clusters)

    def __iter__ (self):
        return self.clusters.itervalues()

    def neirest_pair (self):
        # Among all the possible pair of clusters find the two with are
        # most similar

        # getter for iterators among clusters
        clusters = self.clusters.itervalues

        # cartesian product for which we avoid a cluster to be compared
        # with itself.
        pairs = it.ifilter(lambda (c0, c1) : id(c0) != id(c1),
                           it.product(clusters(), clusters()))
        get1 = operator.itemgetter(1)
        return min( it.starmap(self.cmp_clusters, pairs), key=get1 )[0]

    def merge (self, c0, c1):
        if id(c0) != id(c1):
            del self.clusters[id(c0)]
            del self.clusters[id(c1)]
            newclust = set.union(c0, c1)
            if self.history:
                self.history(c0, c1, newclust)
                self.all_clusters.append(newclust)
            self.clusters[id(newclust)] = newclust
        else:
            print("Trying to join cluster with itself", file=sys.stderr)

    def flatten (self):
        def to_flat (D):
            for clid, cl in D.iteritems():
                if len(cl) == 1:
                    yield clid, cl
                else:
                    for s in it.imap(set, cl):
                        yield id(s), s
        self.clusters = dict(to_flat(self.clusters))

    def __str__ (self):
        def aux ():
            yield 'Clusters:'
            for n, c in enumerate(self.clusters.itervalues()):
                yield '\n  Cluster '
                yield str(n)
                yield '\n  '
                yield str(c)
        return ''.join(aux())

    def sum_of_squared_errors (self):
        normsq = lambda v : abs(Vector.norm(v, 1))
        clust_avg = lambda clst : (clst, avg(clst))
        clust_sqerr = lambda (clst, mu) : sum(normsq(v - mu) for v in clst)
        return sum( it.imap(clust_sqerr, it.imap(clust_avg, self)) )

def main (argv=None):
    import re

    # This is some example code which I used to test the hierarchical
    # clustering. Needs pylab to be installed in order to work!
    try:
        import pylab
    except:
        print("Pylab needs to be installed for this!", file=sys.stderr)
        return 1

    def get_couples (f):
        pat = re.compile(r'^ *x= *(-?\d+\.?\d*) *y= *(-?\d+\.?\d*) *$')
        return it.imap(lambda x : Vector(it.imap(float, x.groups())), 
                       it.ifilter(None, it.imap(pat.match, f)))

    cnt = it.count()
    def plot_clusters (cm):
        pylab.clf()
        for cl in cm:
            for vec in cl:
                pylab.plot(vec[0], vec[1], 'o')
            pylab.plot(list( v[0] for v in cl ),
                       list( v[1] for v in cl ))
        pylab.savefig("Out%02d.png" % next(cnt))

    if not argv: argv = sys.argv

    assert len(argv) > 1, "Require file name"
    f = open(argv[1], 'rt')
    couples = list( get_couples(f) )
    f.close()

    pylab.ion()

    cm = ClusterManager(couples)
    plot_clusters(cm)
    while not cm.step():
        plot_clusters(cm)

    return 0

if __name__ == '__main__':
    sys.exit(main())

