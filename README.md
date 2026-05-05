# Final Project - Analyzing Shortest Path Performance with Dijkstra's Algorithm

**Course:** CS 5329 – Algorithm Design and Analysis  
**Student Name:** Chase Calodney 
**Semester:** Spring 2026

---

## Overview
This project compares a baseline linear scanning approach with an optimized graph-based method for finding shortest paths between airports. Flight route data from the OpenFlights dataset is used to build a weighted graph. The baseline repeatedly scans all routes to find neighbors and determine the next node, while the optimized version uses an adjacency list and Dijkstra’s algorithm with a min-heap to significantly improve performance.

---

## How to Run the Code
From the repository directory, run:

```bash
pip install -r requirements.txt
```
Then to collect data, run:
python data_loader.py

To run the benchmark, run:
python benchmark.py

