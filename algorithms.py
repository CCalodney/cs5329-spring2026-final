# Contains the pure implementations of your baseline and optimized approaches.
import heapq
import math


def build_graph(edges):
    graph = {}

    for source, destination, distance in edges:
        if source not in graph:
            graph[source] = []

        if destination not in graph:
            graph[destination] = []

        graph[source].append((destination, distance))

    return graph


def rebuild_path(previous_airports, start_airport, end_airport):
    if end_airport not in previous_airports:
        return []

    path = []
    current_airport = end_airport

    while current_airport is not None:
        path.append(current_airport)

        if current_airport == start_airport:
            break

        current_airport = previous_airports[current_airport]

    path.reverse()

    if len(path) == 0 or path[0] != start_airport:
        return []

    return path


def get_all_airports(edges):
    airports = set()

    for source, destination, distance in edges:
        airports.add(source)
        airports.add(destination)

    return airports


def get_neighbors_slow(edges, airport):
    neighbors = []

    for source, destination, distance in edges:
        if source == airport:
            neighbors.append((destination, distance))

    return neighbors


def baseline_shortest_path(edges, start_airport, end_airport):
    airports = get_all_airports(edges)

    if start_airport not in airports or end_airport not in airports:
        return math.inf, []

    distances = {}
    previous_airports = {}
    visited = set()

    for airport in airports:
        distances[airport] = math.inf
        previous_airports[airport] = None

    distances[start_airport] = 0

    while len(visited) < len(airports):
        current_airport = None
        current_distance = math.inf

        for airport in airports:
            if airport not in visited and distances[airport] < current_distance:
                current_airport = airport
                current_distance = distances[airport]

        if current_airport is None:
            break

        if current_airport == end_airport:
            break

        visited.add(current_airport)

        neighbors = get_neighbors_slow(edges, current_airport)

        for neighbor, distance in neighbors:
            new_distance = distances[current_airport] + distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_airports[neighbor] = current_airport

    path = rebuild_path(previous_airports, start_airport, end_airport)

    return distances.get(end_airport, math.inf), path


def dijkstra_shortest_path(graph, start_airport, end_airport):
    if start_airport not in graph or end_airport not in graph:
        return math.inf, []
    distances = {}
    previous_airports = {}

    for airport in graph:
        distances[airport] = math.inf
        previous_airports[airport] = None

    distances[start_airport] = 0

    priority_queue = [(0, start_airport)]
    visited = set()

    while priority_queue:
        current_distance, current_airport = heapq.heappop(priority_queue)

        if current_airport in visited:
            continue

        visited.add(current_airport)

        if current_airport == end_airport:
            break

        for neighbor, distance in graph[current_airport]:
            new_distance = current_distance + distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_airports[neighbor] = current_airport
                heapq.heappush(priority_queue, (new_distance, neighbor))

    path = rebuild_path(previous_airports, start_airport, end_airport)
    return distances.get(end_airport, math.inf), path