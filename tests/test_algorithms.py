import unittest
from backend.graph import Graph
from backend.algorithms import (
    bfs_shortest_path,
    dijkstra_shortest_path,
    a_star_search
)


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        # small graph
        self.g = Graph()
        self.g.add_node(1, 0, 0)
        self.g.add_node(2, 10, 0)
        self.g.add_node(3, 20, 0)
        self.g.add_edge(1, 2, 5)
        self.g.add_edge(2, 3, 5)

    def test_bfs(self):
        path = bfs_shortest_path(self.g, 1, 3)
        self.assertEqual(path, [1, 2, 3])

    def test_dijkstra(self):
        path = dijkstra_shortest_path(self.g, 1, 3)
        self.assertEqual(path, [1, 2, 3])

    def test_a_star(self):
        path = a_star_search(self.g, 1, 3)
        self.assertEqual(path, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
