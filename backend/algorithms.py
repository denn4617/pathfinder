from collections import deque
import heapq
import math


def bfs_shortest_path(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for (neighbor, _) in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None


def dijkstra_shortest_path(graph, start, goal):
    distances = {node: math.inf for node in graph.get_all_nodes()}
    distances[start] = 0
    visited = set()
    pq = [(0, start, [start])]  # (distance, node, path)

    while pq:
        current_dist, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path

        for (neighbor, weight) in graph.get_neighbors(node):
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))

    return None


def a_star_search(graph, start, goal):
    """A* uses Euclidean distance to goal as a heuristic."""
    def heuristic(n1, n2):
        x1, y1 = graph.get_coordinates(n1)
        x2, y2 = graph.get_coordinates(n2)
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    distances = {node: math.inf for node in graph.get_all_nodes()}
    distances[start] = 0
    visited = set()
    pq = [(0, start, [start])]  # (f_score, node, path)

    while pq:
        f_score, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path

        for (neighbor, weight) in graph.get_neighbors(node):
            g_score = distances[node] + weight
            if g_score < distances[neighbor]:
                distances[neighbor] = g_score
                h = heuristic(neighbor, goal)
                heapq.heappush(pq, (g_score + h, neighbor, path + [neighbor]))

    return None
