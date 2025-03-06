import json


class Graph:
    def __init__(self):
        # adjacency list: {node_id: [(neighbor_id, weight), ...], ...}
        self.adjacency_list = {}
        # store node coordinates separately: {node_id: (x, y)}
        self.coordinates = {}

    def add_node(self, node_id, x=0, y=0):
        if node_id not in self.adjacency_list:
            self.adjacency_list[node_id] = []
            self.coordinates[node_id] = (x, y)

    def add_edge(self, src, dst, weight=1):
        # assume directed or undirected as needed
        self.adjacency_list[src].append((dst, weight))

    def get_neighbors(self, node_id):
        """Return a list of (neighbor, weight) for this node."""
        return self.adjacency_list.get(node_id, [])

    def get_all_nodes(self):
        return list(self.adjacency_list.keys())

    def get_coordinates(self, node_id):
        return self.coordinates.get(node_id, (0, 0))

    @staticmethod
    def from_json(path):
        """Load graph from a JSON file with 'nodes' and 'edges'."""
        g = Graph()
        with open(path, 'r') as f:
            data = json.load(f)
            # Add nodes
            for n in data.get("nodes", []):
                g.add_node(n["id"], n["x"], n["y"])
            # Add edges
            for e in data.get("edges", []):
                g.add_edge(e["source"], e["target"], e["distance"])
        return g
