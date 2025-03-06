from flask import Flask, request, jsonify
from flask_cors import CORS
from graph import Graph
from algorithms import bfs_shortest_path, dijkstra_shortest_path, a_star_search
import os

app = Flask(__name__)
CORS(app)

# Load graph from JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sample_map.json")
graph = Graph.from_json(DATA_PATH)


@app.route("/nodes", methods=["GET"])
def get_nodes():
    """Return a list of all nodes with their coordinates."""
    nodes_data = []
    for node_id in graph.get_all_nodes():
        x, y = graph.get_coordinates(node_id)
        nodes_data.append({"id": node_id, "x": x, "y": y})
    return jsonify(nodes_data)


@app.route("/edges", methods=["GET"])
def get_edges():
    """Return all edges (source, target, weight)."""
    edges_list = []
    for node_id in graph.get_all_nodes():
        for (neighbor, weight) in graph.get_neighbors(node_id):
            edges_list.append({
                "source": node_id,
                "target": neighbor,
                "weight": weight
            })
    return jsonify(edges_list)


@app.route("/path", methods=["POST"])
def compute_path():
    """
    Expects JSON:
    {
      "start": int,
      "goal": int,
      "algo": "bfs" | "dijkstra" | "astar"
    }
    Returns: { "path": [1,2,3,...] } or { "error": ... }
    """
    data = request.get_json()
    start = data.get("start")
    goal = data.get("goal")
    algo = data.get("algo")

    if not all([start, goal, algo]):
        return jsonify({"error": "Missing parameters"}), 400

    if algo == "bfs":
        path = bfs_shortest_path(graph, start, goal)
    elif algo == "dijkstra":
        path = dijkstra_shortest_path(graph, start, goal)
    elif algo == "astar":
        path = a_star_search(graph, start, goal)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    if path:
        return jsonify({"path": path})
    else:
        return jsonify({"error": "No path found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
