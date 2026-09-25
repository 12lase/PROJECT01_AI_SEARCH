"""
uninformed.py
=============
Uninformed (blind) search algorithms over the road-network graph:
Breadth-First Search, Depth-First Search, Uniform-Cost Search, and
Iterative Deepening Search.

Graph format: {city: {neighbor_city: edge_weight_miles, ...}, ...}

Every search function shares the same signature so app.py can dispatch
to any of them uniformly:

    fn(graph, locations, start, goal) -> (path, cost, nodes_expanded)

`locations` (lat/lon per city) is unused here but accepted so uninformed
and informed searches share one call signature. `path` is a list of city
names from start to goal (inclusive), or None if no path exists. `cost`
is the sum of edge weights along the returned path. `nodes_expanded` is
the number of nodes popped from the frontier and expanded (a node
already known to be the goal when generated is not counted as expanded
again).
"""

from collections import deque
import heapq


def _path_cost(graph, path):
    if not path:
        return 0
    return round(sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1)), 2)


def bfs(graph, locations, start, goal):
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 0

    frontier = deque([start])
    visited = {start}
    parent = {start: None}
    nodes_expanded = 0

    while frontier:
        node = frontier.popleft()
        nodes_expanded += 1

        for neighbor in graph.get(node, {}):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            parent[neighbor] = node
            if neighbor == goal:
                path = _reconstruct(parent, goal)
                return path, _path_cost(graph, path), nodes_expanded
            frontier.append(neighbor)

    return None, 0, nodes_expanded


def dfs(graph, locations, start, goal):
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 0

    stack = [start]
    visited = {start}
    parent = {start: None}
    nodes_expanded = 0

    while stack:
        node = stack.pop()
        nodes_expanded += 1

        if node == goal:
            path = _reconstruct(parent, goal)
            return path, _path_cost(graph, path), nodes_expanded

        for neighbor in graph.get(node, {}):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            parent[neighbor] = node
            stack.append(neighbor)

    return None, 0, nodes_expanded


def ucs(graph, locations, start, goal):
    if start not in graph or goal not in graph:
        return None, 0, 0

    frontier = [(0, start)]
    best_cost = {start: 0}
    parent = {start: None}
    visited = set()
    nodes_expanded = 0

    while frontier:
        cost, node = heapq.heappop(frontier)

        if node in visited:
            continue
        visited.add(node)
        nodes_expanded += 1

        if node == goal:
            path = _reconstruct(parent, goal)
            return path, round(cost, 2), nodes_expanded

        for neighbor, weight in graph.get(node, {}).items():
            new_cost = cost + weight
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                parent[neighbor] = node
                heapq.heappush(frontier, (new_cost, neighbor))

    return None, 0, nodes_expanded


def ids(graph, locations, start, goal):
    if start not in graph or goal not in graph:
        return None, 0, 0

    total_nodes_expanded = 0
    max_depth = len(graph)

    for limit in range(max_depth + 1):
        path, expanded = _depth_limited_search(graph, start, goal, limit)
        total_nodes_expanded += expanded
        if path is not None:
            return path, _path_cost(graph, path), total_nodes_expanded

    return None, 0, total_nodes_expanded


def _depth_limited_search(graph, start, goal, limit):
    """One depth-limited DFS iteration. Returns (path, nodes_expanded)."""
    stack = [(start, 0)]
    visited = {start}
    parent = {start: None}
    nodes_expanded = 0

    while stack:
        node, depth = stack.pop()
        nodes_expanded += 1

        if node == goal:
            return _reconstruct(parent, goal), nodes_expanded

        if depth == limit:
            continue

        for neighbor in graph.get(node, {}):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            parent[neighbor] = node
            stack.append((neighbor, depth + 1))

    return None, nodes_expanded


def _reconstruct(parent, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path
