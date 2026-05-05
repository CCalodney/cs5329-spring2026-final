# Runs the timing and memory tests.

import csv
import time
import tracemalloc

from data_loader import load_graph_edges
from algorithms import build_graph, baseline_shortest_path, dijkstra_shortest_path


def measure_memory_and_time(function, *args):
    tracemalloc.start()

    start_time = time.perf_counter()
    result = function(*args)
    end_time = time.perf_counter()

    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed_time = end_time - start_time
    peak_memory_kb = peak_memory / 1024

    return result, elapsed_time, peak_memory_kb


def run_benchmark():
    edges = load_graph_edges()

    input_sizes = [5000, 10000, 20000, 30000, 35000]

    start_airport = "AUS"
    end_airport = "CDG"

    results = []

    for size in input_sizes:
        test_edges = edges[:size]

        print("Running size:", size)

        baseline_result, baseline_time, baseline_memory = measure_memory_and_time(
            baseline_shortest_path,
            test_edges,
            start_airport,
            end_airport
        )

        graph_build_start = time.perf_counter()
        graph = build_graph(test_edges)
        graph_build_end = time.perf_counter()

        graph_build_time = graph_build_end - graph_build_start

        dijkstra_result, dijkstra_time, dijkstra_memory = measure_memory_and_time(
            dijkstra_shortest_path,
            graph,
            start_airport,
            end_airport
        )

        baseline_distance, baseline_path = baseline_result
        dijkstra_distance, dijkstra_path = dijkstra_result

        if baseline_distance == dijkstra_distance and baseline_path == dijkstra_path:
            same_result = True
        else:
            same_result = False

        results.append([
            size,
            baseline_time,
            graph_build_time,
            dijkstra_time,
            graph_build_time + dijkstra_time,
            baseline_memory,
            dijkstra_memory,
            same_result,
            baseline_distance,
            dijkstra_distance,
            baseline_path,
            dijkstra_path
        ])

    save_results(results)


def save_results(results):
    with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "input_size",
            "baseline_time_seconds",
            "graph_build_time_seconds",
            "dijkstra_query_time_seconds",
            "dijkstra_total_time_seconds",
            "baseline_memory_kb",
            "dijkstra_memory_kb",
            "same_result",
            "baseline_distance",
            "dijkstra_distance",
            "baseline_path",
            "dijkstra_path"
        ])

        writer.writerows(results)


if __name__ == "__main__":
    run_benchmark()