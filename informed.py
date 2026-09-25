"""
informed.py
===========
Informed (heuristic-based) search algorithms over the road-network graph:
Greedy Best-First Search and A* Search.

Both use a straight-line (haversine) distance heuristic in miles from a
node to the goal, computed from the `locations` lat/lon data returned by
`/api/map`. Same signature/return convention as uninformed.py:

    fn(graph, locations, start, goal) -> (path, cost, nodes_expanded)
"""

import heapq

from data_fetcher import haversine_distance
from uninformed import _path_cost, _reconstruct


def _heuristic(locations, node, goal):
    if node not in locations or goal not in locations:
        return 0
    c1 = (locations[node]["lat"], locations[node]["lon"])
    c2 = (locations[goal]["lat"], locations[goal]["lon"])
    return haversine_distance(c1, c2)


def greedy(graph, locations, start, goal):
    if start not in graph or goal not in graph:
        return None, 0, 0

    frontier = [(_heuristic(locations, start, goal), start)]
    parent = {start: None}
    visited = set()
    nodes_expanded = 0

    while frontier:
        _, node = heapq.heappop(frontier)

        if node in visited:
            continue
        visited.add(node)
        nodes_expanded += 1

        if node == goal:
            path = _reconstruct(parent, goal)
            return path, _path_cost(graph, path), nodes_expanded

        for neighbor in graph.get(node, {}):
            if neighbor in visited:
                continue
            if neighbor not in parent:
                parent[neighbor] = node
                heapq.heappush(frontier, (_heuristic(locations, neighbor, goal), neighbor))

    return None, 0, nodes_expanded


def astar(graph, locations, start, goal):
    if start not in graph or goal not in graph:
        return None, 0, 0

    frontier = [(_heuristic(locations, start, goal), 0, start)]
    best_cost = {start: 0}
    parent = {start: None}
    visited = set()
    nodes_expanded = 0

    while frontier:
        _, cost, node = heapq.heappop(frontier)

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
                priority = new_cost + _heuristic(locations, neighbor, goal)
                heapq.heappush(frontier, (priority, new_cost, neighbor))

    return None, 0, nodes_expanded
