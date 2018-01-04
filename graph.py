class Graph(object):
    """
    This is a class for undirected graph
    """

    def __init__(self, size, is_partition=False):
        """

        :param size: number of nodes in the graph
        :param is_partition: whether this is a partition graph
        """

        self._nodes = [set() for _ in range(size)]

        if is_partition:
            self._partition = []

    def __len__(self):
        return len(self._nodes)

    def __iter__(self):
        # iterate over the nodes
        return iter(self._nodes)

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        e = []
        for u in range(len(self._nodes)):
            for v in self._nodes[u]:
                e.append((u, v))
        return e

    @property
    def partition(self):
        return self._partition

    def complete(self):
        complete_set = set()

        for i in range(len(self._nodes)):
            complete_set.add(i)

        for i in range(len(self._nodes)):
            self._nodes[i] = complete_set.copy()
            self._nodes[i].remove(i)

    def add_edge(self, u, v):
        """
        This method add an edge into the graph

        Examples:
        ---------
        g.add(starting_point, ending_point)
        g.add(*tuple)

        :param u:
        :param v:
        :return:
        """
        self._nodes[u].add(v)
        self._nodes[v].add(u)

    def add_edges(self, list_of_edges):
        for u, v in list_of_edges:
            self.add_edge(u, v)


if __name__ == "__main__":
    g = Graph(100)
    g.complete()
    d = g.edges
    pass
