import unittest
from backend.graph import Graph


class TestGraph(unittest.TestCase):
    def test_add_node_and_edge(self):
        g = Graph()
        g.add_node(1, 100, 200)
        g.add_node(2, 150, 250)
        g.add_edge(1, 2, 5)

        self.assertIn(1, g.adjacency_list)
        self.assertIn(2, g.adjacency_list)
        self.assertEqual(g.get_neighbors(1), [(2, 5)])
        self.assertEqual(g.get_coordinates(1), (100, 200))


if __name__ == "__main__":
    unittest.main()
