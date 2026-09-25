import os
import json
import time
from flask import Flask, render_template, jsonify, request

import uninformed
import informed

app = Flask(__name__)

MAP_DATA_FILE = "map_data.json"

ALGORITHMS = {
    "bfs": uninformed.bfs,
    "dfs": uninformed.dfs,
    "ucs": uninformed.ucs,
    "ids": uninformed.ids,
    "greedy": informed.greedy,
    "astar": informed.astar,
}


def load_map_data():
    """Load graph and location data from map_data.json if available."""
    if os.path.exists(MAP_DATA_FILE):
        try:
            with open(MAP_DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {MAP_DATA_FILE}: {e}")
    return {
        "region": "State / Metro Area",
        "total_cities": 0,
        "total_edges": 0,
        "locations": {},
        "graph": {}
    }


@app.route("/")
def index():
    """Renders the main deployment webpage."""
    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():
    """Returns map locations and graph connections."""
    data = load_map_data()
    return jsonify(data)


@app.route("/api/search", methods=["POST"])
def search():
    """Runs the requested search algorithm between two cities."""
    payload = request.get_json() or {}
    start = payload.get("start", "")
    goal = payload.get("goal", "")
    algorithm = payload.get("algorithm", "")

    data = load_map_data()
    graph = data.get("graph", {})
    locations = data.get("locations", {})

    search_fn = ALGORITHMS.get(algorithm)
    if search_fn is None:
        return jsonify({
            "path": [], "cost": 0, "nodes_expanded": 0,
            "message": f"Unknown algorithm '{algorithm}'."
        }), 400

    if start not in graph or goal not in graph:
        return jsonify({
            "path": [], "cost": 0, "nodes_expanded": 0,
            "message": "Start or goal city not found in the map data."
        }), 400

    started_at = time.perf_counter()
    path, cost, nodes_expanded = search_fn(graph, locations, start, goal)
    time_ms = round((time.perf_counter() - started_at) * 1000, 3)

    if not path:
        return jsonify({
            "path": [], "cost": 0, "nodes_expanded": nodes_expanded,
            "time_ms": time_ms,
            "message": f"No path found between '{start}' and '{goal}'."
        })

    return jsonify({
        "path": path,
        "cost": cost,
        "nodes_expanded": nodes_expanded,
        "time_ms": time_ms,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
