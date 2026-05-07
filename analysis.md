Analytical Report


# Big-O Explanation

For both the baseline and optimized approach, I will be using V to refer to the number of airports (vertices) and E to refer to the number of routes (edges).

The baseline stores the graph as an edge list and performs linear scans that are repeated throughout the shortest path computation. On each iteration of the outer loop, the baseline must scan all airports to find the closest unvisited one, O(V), and then scan the entire edge list to find outgoing neighbors of the current airport, O(E). One iteration is therefore 
O(V+E), and the outer loop runs up to V times, giving O(V*(V+E)) = O(V² + VE). Since the graph is connected, E ≥ V-1, meaning the VE term dominates V², so this simplifies to O(VE).

The optimized approach stores the graph as an adjacency list and uses a binary heap as a priority queue, which eliminates both linear scans from the baseline. Finding the closest unvisited airport is now a heap pop in O(log V) instead of an O(V) scan, and finding a vertex's neighbors is a direct lookup in the adjacency list instead of an 
O(E) scan over all routes. Each vertex is popped and finalized at most once, contributing O(V log V) total. Each edge can trigger at most one heap push, contributing O(E log V) total. Summing these gives O((V + E) log V).


# Mapping Empirical Results to Theoretical Bounds

The empirical benchmark results closely matched the expected theoretical time complexities of both implementations.

As the number of edges increased, we can see a sizeable increase in the time the baseline takes to complete, matching the expected O(VE) behavior. And as the number of edges increased for the optimized approach, there is hardly any increase to the time needed for completion, which matches the expected O((V+E)log v) behavior.

The benchmark results demonstrated that the adjacency-list structure significantly reduced neighbor lookup overhead by allowing direct access to outgoing routes instead of repeatedly scanning the entire dataset. Memory usage also aligned with expectations. Both implementations showed increasing memory usage as graph size increased because both store the same underlying graph data. However, the optimized implementation consistently used less memory due to more efficient graph organization.

# Amortized Cost Analysis

The optimized approach has an extra upfront cost because it first builds the adjacency list before running Dijkstra’s algorithm. Building this structure takes O(E) time since every route edge must be processed once. Since this only happens once, it has a negligable effect on the overall cost.

The baseline doesn't do this, but in exchange has to keep scanning the data, repeating a lot of work.

This demonstrates amortized cost behavior: the optimized approach spends more time initially to organize the data, but saves a large amount of time during querying, especially as the number of queries increases.

# Reflection Questions

## 2.1
My biggest hurdle was with my initial implementation. Initially I did a very basic implementation of Dijkstra's Algorithm, which I had expected to more significantly outperform the baseline. When it barely did any better, I was worried that my results would not show a large enough improvement over the baseline, so I used the min-heap version instead in the final implementation.

## 2.2
I think it would be cool to add some GUI where you could select a start and end destination, or if I could even find a way to visualize how each one works so that you could watch the algorithm find the shortest path.

## 2.3
After the basic Dijkstra version didn't do as well as I thought, the improved version matched the exact emprical results I expected.