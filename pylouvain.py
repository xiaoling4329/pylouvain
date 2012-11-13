#!/usr/bin/env python3

'''
    Implements the Louvain method.
    Input: a weighted undirected graph
    Ouput: a partition whose modularity is maximum
'''
class PyLouvain:

    '''
        Builds a graph from _path.
        _path: a path to a file containing "node_from node_to" edges (one per line)
    '''
    @classmethod
    def from_file(cls, path):
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        nodes = {}
        edges = []
        for line in lines:
            n = line.split()
            nodes[int(n[0])] = 1
            nodes[int(n[1])] = 1
            edges.append(((int(n[0]), int(n[1])), 1))
        # rebuild graph with successive identifiers
        nodes = list(nodes.keys())
        nodes.sort()
        i = 0
        nodes_ = []
        d = {}
        for n in nodes:
            nodes_.append(i)
            d[n] = i
            i += 1
        edges_ = []
        for e in edges:
            edges_.append(((d[e[0][0]], d[e[0][1]]), e[1]))
        print("%d nodes, %d edges" % (len(nodes_), len(edges_)))
        return cls(nodes_, edges_)

    '''
        Initializes the method.
        _nodes: a list of ints
        _edges: a list of ((int, int), weight) pairs
    '''
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        # precompute m2 (2 * sum of the weights of all links in network)
        #            k_i (sum of the weights of the links incident to node i)
        self.m2 = 0
        self.k_i = [0 for n in nodes]
        for e in edges:
            self.m2 += e[1]
            self.k_i[e[0][0]] += e[1]
            self.k_i[e[0][1]] += e[1]
        self.m2 *= 2


    '''
        Applies the Louvain method.
    '''
    def apply_method(self):
        network = (self.nodes, self.edges)
        best_partition = [[node] for node in network[0]]
        while 1:
            # TODO: precompute parameter m (and k vector?)
            partition = [c for c in self.first_phase(network) if c]
            if partition == best_partition:
                break
            network = self.second_phase(network, partition)
            best_partition = partition
            print("%s (%.2f)" % (best_partition, self.compute_modularity(network, partition)))
        return best_partition

    '''
        Computes the modularity of _network.
        _network: a (nodes, edges) pair
        _partition: a list of lists of nodes
    '''
    def compute_modularity(self, network, partition):
        # compute m
        m = 0
        for e in network[1]:
            m += e[1]
        q = 0
        for i in network[0]:
            for j in network[0]:
                if self.get_community(i, partition) != self.get_community(j, partition):
                    continue
                q += self.get_weight(i, j, network[1]) - (self.compute_weights(i, network[1]) * self.compute_weights(j, network[1]) / m)
        return q / m

    '''
        Computes the modularity gain of having node in community _c.
        _node: an int
        _c: an int
        _k_i_in: the sum of the weights of the links from _node to nodes in _c
        _edges: a list of ((node, node), weight) pairs
        _partition: a list of lists of nodes
    '''
    def compute_modularity_gain(self, node, c, k_i_in):
        s_tot_k_i = (self.s_tot[c] + self.k_i[node]) / self.m2
        s_tot_ = self.s_tot[c] / self.m2
        k_i_ = self.k_i[node] / self.m2
        return ((self.s_in[c] + k_i_in) / self.m2 - s_tot_k_i * s_tot_k_i) - (self.s_in[c] / self.m2 - s_tot_ * s_tot_ - k_i_ * k_i_)

    '''
        Computes the sum of the weights of the edges incident to vertex _i.
        _i: a node
        _edges: a list of ((node, node), weight) pairs
    '''
    def compute_weights(self, i, edges):
        w = 0
        for e in edges:
            if e[0][0] == i:
                w += e[1]
        return w

    '''
        Performs the first phase of the method.
        _network: a (nodes, edges) pair
    '''
    def first_phase(self, network):
        # make initial partition
        best_partition = self.make_initial_partition(network)
        while 1:
            improvement = False
            for node in network[0]:
                node_community = self.get_community(node, best_partition)
                # default best community is its own
                best_community = node_community
                best_gain = 0
                # remove _node from its community
                partition = [[pp for pp in p] for p in best_partition]
                partition[node_community].remove(node)
                for e in network[1]:
                    if e[0][0] == node or e[0][1] == node:
                        self.s_in[node_community] -= e[1]
                self.s_tot[node_community] -= self.k_i[node]
                communities = {} # only consider neighbors of different communities
                for neighbor in self.get_neighbors(node, network[1]):
                    community = self.get_community(neighbor, best_partition)
                    if community in communities:
                        continue
                    communities[community] = 1
                    k_i_in = 0
                    for e in network[1]:
                        if e[0][0] == node and self.get_community(e[0][1], partition) == community or e[0][1] == node and self.get_community(e[0][0], partition) == community:
                            k_i_in += e[1]
                    # compute modularity gain obtained by moving _node to the community of _neighbor
                    gain = self.compute_modularity_gain(node, community, k_i_in)
                    if gain > best_gain:
                        best_community = community
                        best_gain = gain
                # insert _node into the community maximizing the modularity gain
                partition[best_community].append(node)
                for e in network[1]:
                    if e[0][0] == node or e[0][1] == node:
                        self.s_in[best_community] += e[1]
                self.s_tot[best_community] += self.k_i[node]
                best_partition = partition
                if node_community != best_community:
                    improvement = True
            if not improvement:
                break
        return best_partition

    '''
        Returns the community in which _node is (among _partition).
        _node: an int
        _partition: a list of lists of nodes
    '''
    def get_community(self, node, partition):
        # TODO: use of an efficient data structure to retrieve one's community
        for i in range(len(partition)):
            if node in partition[i]:
                return i
        return -1

    '''
        Yields the nodes adjacent to _node.
        _node: an int
        _edges: a list of ((node, node), weight) pairs
    '''
    def get_neighbors(self, node, edges):
        for e in edges:
            if e[0][0] == node:
                yield e[0][1]
            if e[0][1] == node:
                yield e[0][0]

    '''
        Returns the weight of edge (_i, _j) among _edges.
        _i: a node
        _j: a node
        _edges: a list of ((node, node), weight) pairs
    '''
    def get_weight(self, i, j, edges):
        for e in edges:
            if e[0][0] == i and e[0][1] == j:
                return e[1]
        return 0

    '''
        Builds the initial partition from _network.
        _network: a (nodes, edges) pair
    '''
    def make_initial_partition(self, network):
        partition = [[node] for node in network[0]]
        self.s_in = [0 for node in network[0]]
        self.s_tot = [self.k_i[node] for node in network[0]]
        for e in network[1]:
            if e[0][0] == e[0][1]: # only self-loops
                self.s_in[e[0][0]] += e[1]
        return partition

    '''
        Performs the second phase of the method.
        _network: a (nodes, edges) pair
        _partition: a list of lists of nodes
    '''
    def second_phase(self, network, partition):
        nodes_ = [i for i in range(len(partition))]
        edges_ = {}
        for e in network[1]:
            ci = self.get_community(e[0][0], partition)
            cj = self.get_community(e[0][1], partition)
            # TODO? add constraint ci < cj
            try:
                edges_[(ci, cj)] += e[1]
            except KeyError:
                edges_[(ci, cj)] = e[1]
        edges_ = [(k, v) for k, v in edges_.items()]
        # recompute k_i vector
        self.k_i = [0 for n in nodes_]
        for e in edges_:
            self.k_i[e[0][0]] += e[1]
            if e[0][0] != e[0][1]: # counting self-loops only once
                self.k_i[e[0][1]] += e[1]
        return (nodes_, edges_)

