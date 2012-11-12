#!/usr/bin/env python3

import unittest
from pylouvain import PyLouvain

class PylouvainTest(unittest.TestCase):

    def setUp(self):
        self.nodes = [i for i in range(10)]
        self.edges = [((0, 4), 1),
                 ((0, 1), 1),
                 ((1, 4), 1),
                 ((3, 1), 1),
                 ((3, 6), 1),
                 ((6, 7), 1),
                 ((7, 9), 1),
                 ((6, 9), 1),
                 ((3, 2), 1),
                 ((5, 8), 1),
                 ((8, 2), 1),
                 ((5, 2), 1)]
        self.karate_nodes = [i for i in range(34)]
        self.karate_edges = [((1, 0), 1),
                             ((2, 0), 1),
                             ((2, 1), 1),
                             ((3, 0), 1),
                             ((3, 1), 1),
                             ((3, 2), 1),
                             ((4, 0), 1),
                             ((5, 0), 1),
                             ((6, 0), 1),
                             ((6, 4), 1),
                             ((6, 5), 1),
                             ((7, 0), 1),
                             ((7, 1), 1),
                             ((7, 2), 1),
                             ((7, 3), 1),
                             ((8, 0), 1),
                             ((8, 2), 1),
                             ((9, 2), 1),
                             ((10, 0), 1),
                             ((10, 4), 1),
                             ((10, 5), 1),
                             ((11, 0), 1),
                             ((12, 0), 1),
                             ((12, 3), 1),
                             ((13, 0), 1),
                             ((13, 1), 1),
                             ((13, 2), 1),
                             ((13, 3), 1),
                             ((16, 5), 1),
                             ((16, 6), 1),
                             ((17, 0), 1),
                             ((17, 1), 1),
                             ((19, 0), 1),
                             ((19, 1), 1),
                             ((21, 0), 1),
                             ((21, 1), 1),
                             ((25, 23), 1),
                             ((25, 24), 1),
                             ((27, 2), 1),
                             ((27, 23), 1),
                             ((27, 24), 1),
                             ((28, 2), 1),
                             ((29, 23), 1),
                             ((29, 26), 1),
                             ((30, 1), 1),
                             ((30, 8), 1),
                             ((31, 0), 1),
                             ((31, 24), 1),
                             ((31, 25), 1),
                             ((31, 28), 1),
                             ((32, 2), 1),
                             ((32, 8), 1),
                             ((32, 14), 1),
                             ((32, 15), 1),
                             ((32, 18), 1),
                             ((32, 20), 1),
                             ((32, 22), 1),
                             ((32, 23), 1),
                             ((32, 29), 1),
                             ((32, 30), 1),
                             ((32, 31), 1),
                             ((33, 8), 1),
                             ((33, 9), 1),
                             ((33, 13), 1),
                             ((33, 14), 1),
                             ((33, 15), 1),
                             ((33, 18), 1),
                             ((33, 19), 1),
                             ((33, 20), 1),
                             ((33, 22), 1),
                             ((33, 23), 1),
                             ((33, 26), 1),
                             ((33, 27), 1),
                             ((33, 28), 1),
                             ((33, 29), 1),
                             ((33, 30), 1),
                             ((33, 31), 1),
                             ((33, 32), 1)]
        self.pyl = PyLouvain(self.nodes, self.edges)
        self.karate_pyl = PyLouvain(self.karate_nodes, self.karate_edges)

    def test_modularity(self):
        self.assertEqual(-0.16666666666666663, self.pyl.compute_modularity((self.nodes, self.edges), [[i] for i in range(10)]))

    def test_method(self):
        self.assertEqual([[0], [1], [2], [3]], self.pyl.apply_method())

    def test_karate_club(self):
        self.karate_pyl.apply_method()

    def test_arxiv(self):
        pyl = PyLouvain.from_file("/home/patapizza/Dropbox/cours/2012_2013/q1/LINMA1691/Projets/hep-th-citations")
        pyl.apply_method()

if __name__ == '__main__':
    unittest.main()
