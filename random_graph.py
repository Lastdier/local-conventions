# coding: utf-8

import itertools
import graph
import random
import math
import errorhandler


def random_graph(size, p, seed=None):
    """
    :param size:
    :param p:
    :param seed:
    :return:

    Notes
    -----
    This algorithm runs in O(n^2) time.  For sparse graphs (that is, for
    small values of p), func:fast_gnp_random_graph is a faster algorithm.


    References
    ----------
    .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
    .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
    """

    g = graph.Graph(size)

    if p <= 0:
        return g

    if p >= 1:
        g.complete()

    if seed is not None:
        random.seed(seed)

    edges = itertools.combinations(range(size), 2)

    for e in edges:
        if random.random() < p:
            g.add_edge(*e)

    return g


def fast_random_graph(size, p, seed=None):
    """
    :param size:
    :param p:
    :param seed:
    :return:

    Notes
    -----
    The G_{n,p} graph algorithm chooses each of the $[n (n - 1)] / 2$
    (undirected) or $n (n - 1)$ (directed) possible edges with probability p.

    This algorithm runs in O(n + m) time, where m is the expected number of
    edges, which equals p n (n - 1) / 2. This should be faster than
    func:gnp_random_graph when p is small and the expected number of edges
    is small (that is, the graph is sparse).

    References
    ----------
    .. [1] Vladimir Batagelj and Ulrik Brandes,
       "Efficient generation of large random networks",
       Phys. Rev. E, 71, 036113, 2005.
    """

    g = graph.Graph(size)

    if p <= 0:
        return g

    if p >= 1:
        g.complete()

    if seed is not None:
        random.seed(seed)

    u = -1
    v = 1
    lp = math.log(1.0 - p)

    while v < size:
        lr = math.log(1.0 - random.random())
        u += 1 + int(lr / lp)
        while u >= v and v < size:
            u -= v
            v += 1
        if v < size:
            g.add_edge(v, u)

    return g


def random_partition_graph(groups, p_in, p_out, seed=None):
    """
    Return the random partition graph with a partition of sizes.

    A partition graph is a graph of communities with sizes defined by
    s in groups. Nodes in the same group are connected with probability
    p_in and nodes of different groups are connected with probability
    p_out.

    :param groups: list of ints, [3, 4, 1] defines sizes of groups
    :param p_in:
    :param p_out:
    :param seed:
    :return:

    Notes
    -----
    The partition is store as a graph attribute 'partition'.

    References
    ----------
    .. [1] Santo Fortunato 'Community Detection in Graphs' Physical Reports
       Volume 486, Issue 3-5 p. 75-174. https://arxiv.org/abs/0906.0612
    """

    if p_in > 1 or p_in < 0:
        raise errorhandler.ErrorHandler("p_in must be in [0,1]")

    if p_out > 1 or p_out < 0:
        raise errorhandler.ErrorHandler("p_out must be in [0,1]")

    size = sum(groups)
    g = graph.Graph(size, is_partition=True)

    next_group = {}
    start = 0
    group_index = 0
    for n in groups:    # connect nodes inside a group
        edges = ((u + start, v + start) for u, v in fast_random_graph(n, p_in).edges)
        g.add_edges(edges)
        g.partition.append(set(range(start, start+n)))
        next_group.update(dict.fromkeys(range(start, start + n), start + n))
        group_index += 1
        start += n

    # connect nodes between groups
    if p_out == 0:
        return g
    if p_out == 1:
        for n in next_group:
            targets = range(next_group[n], len(g))
            g.add_edges(zip([n] * len(targets), targets))
        return g

    # using method similar to fast_random_graph
    lp = math.log(1.0 - p_out)
    n = len(g)

    for u in range(n - 1):
        v = next_group[u]
        while v < n:
            lr = math.log(1.0 - random.random())
            v += int(lr / lp)
            if v < n:
                g.add_edge(u, v)
                v += 1

    return g


def gaussian_random_partition_graph(n, s, v, p_in, p_out, seed=None):
    """
    Generate a Gaussian random partition graph.

    A Gaussian random partition graph is created by creating k partitions
    each with a size drawn from a normal distribution with mean s and variance
    s/v. Nodes are connected within clusters with probability p_in and
    between clusters with probability p_out

    :param n: int
        Number of nodes in the graph
    :param s: float
        Mean cluster size
    :param v: float
        Shape parameter. The variance of cluster size distribution is s/v.
    :param p_in:
    :param p_out:
    :param seed:
    :return:

    References
    ----------
    .. [1] Ulrik Brandes, Marco Gaertler, Dorothea Wagner,
       Experiments on Graph Clustering Algorithms,
       In the proceedings of the 11th Europ. Symp. Algorithms, 2003.
    """

    if s > n:
        raise errorhandler.ErrorHandler("s must be <= n")
    assigned = 0
    sizes = []
    while True:
        size = int(random.normalvariate(s, float(s) / v + 0.5))
        if size < 1:
            continue
        if assigned + size >= n:
            sizes.append(n - assigned)
            break
        assigned += size
        sizes.append(size)

    return random_partition_graph(sizes, p_in, p_out, seed)


if __name__ == '__main__':
    ttt = gaussian_random_partition_graph(100, 10, .5, .5, .1, 1)
    print ttt.separation_degree
    print ttt.average_degree
    pass
