# Week 4 — Christofides' Algorithm for Metric TSP


## Background: Approximation Algorithms

TSP is **NP-hard** — there's no known efficient algorithm to find the
optimal tour for large inputs. Instead, we use **approximation algorithms**
that run in polynomial time and guarantee a solution close to optimal.

- **OPT** — the cost of the optimal (best possible) tour. We usually
  can't compute this, but we can prove our solution is within some
  factor of it.
- **1.5-approximation** — our algorithm always finds a tour costing at
  most 1.5 × OPT (at most 50% worse than optimal).
- **Christofides** is one such approximation for **metric TSP** (where
  distances satisfy triangle inequality).

---

## 1. Resources

* [Christofides algorithm - Wikipedia](https://en.wikipedia.org/wiki/Christofides_algorithm)
* [Christofides (1976) — Original paper](https://doi.org/10.1007/BFb0009840)
* [Floyd-Warshall algorithm - Wikipedia](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)
* [Perfect matching - Wikipedia](https://en.wikipedia.org/wiki/Perfect_matching)


## 2. Assignment

### Understanding the Input JSON

**1. `graph.json` (The Map)**
A weighted undirected graph with a `nodes` array and an `edges` array. Each edge has `u`, `v`, and `w` (weight).

**2. `queries.json` (The Tasks)**
TSP routing requests. Each event has:
- `id`: Unique ID for this run.
- `type`: `"tsp"` — the action to perform.
- `nodes`: A subset of node IDs to find a tour on.

### Your Tasks

#### 2. Implement the helpers in TSP.h
Fill `floyd_warshall`, `prim_mst`, `prefect_matching`, `eulerian_circuit`, and `tour_cost`.

#### 3. Implement `christofides()`
This is the main function. It takes the full **n×n** adjacency matrix and a subset of node IDs (`nodes`). It does:
1. Run Floyd-Warshall all-pairs shortest paths on `adj`
2. Extract the **m×m** distance submatrix for the given `nodes`
3. Run the Christofides pipeline on that submatrix:
   - Build MST via `prim_mst()`
   - Collect odd-degree vertices
   - Pair them with `greedy_matching()`
   - Merge MST + matching edges into a multigraph
   - Find an Eulerian circuit via `eulerian_circuit()`
   - Shortcut — remove duplicate visits — to get a Hamiltonian cycle

The function returns a tour as local indices `[0..m-1]`.

#### 4. Wire `driver.cpp`
For each `"tsp"` event, call `christofides(map.adj, nodes)` → map local indices back to original node IDs → write the output.

### Generate the Output

```json
{
    "meta": {"id": "assignment_01"},
    "results": [
        {
            "id": 1,
            "tour": [0, 2, 1],
            "cost": 8.0,
            "time_us": 4.2
        }
    ]
}
```

