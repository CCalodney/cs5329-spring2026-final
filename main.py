from data_loader import load_graph_edges
from algorithms import build_graph, baseline_shortest_path, dijkstra_shortest_path


edges = load_graph_edges()

start_airport = "LAX"
end_airport = "JFK"

baseline_distance, baseline_path = baseline_shortest_path(
    edges,
    start_airport,
    end_airport
)

graph = build_graph(edges)

dijkstra_distance, dijkstra_path = dijkstra_shortest_path(
    graph,
    start_airport,
    end_airport
)

print("Baseline:")
print(baseline_distance)
print(baseline_path)

print()

print("Dijkstra:")
print(dijkstra_distance)
print(dijkstra_path)