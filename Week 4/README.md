# Week 4: Graph Optimization & TSP

Welcome to the hands-on exercise for Week 4! This week, we transition from finding shortest paths between two points to optimizing routes across an entire graph—specifically, the **Traveling Salesperson Problem (TSP)**.

## 📖 Prerequisites
Before starting the implementation, please review the theory:
1. Read `Theory.pdf`.
2. Grasp why finding the exact TSP solution is computationally hard $O(n!)$.

## 📂 Directory Structure
```text
Week4_TSP/
├── README.md       
├── Theory.pdf 
├── driver.cpp                 <- Existing query processor (DO NOT MODIFY structure, just add TSP event handling)
├── visualize.py         <- Python script to compare your algorithm outputs
└── testcases/
    ├── graph.json             <- Graph definitions
    ├── queries_small.json     <- Queries with small N (use for Brute Force)
    └── queries_large.json     <- Queries with large N (use for Optimized)
```

## 🛠️ The Task

You should already have a working `driver.cpp` from week 3 that reads `graph.json` and `queries.json`. We are introducing a new query type: `"tsp"`.

### Step 1: Update the Driver
In `driver.cpp`, inside the query processing loop, intercept the new `"tsp"` query type:
```cpp
if (type == "tsp") {
    // Extract the nodes to visit from the query
    // Build an NxN distance matrix for these nodes using your existing shortest path logic (e.g., Dijkstra/Floyd-Warshall)
    // Pass the matrix to the solver classes.
}
```

### Step 2: Implement the Solvers
You need to implement two classes or functions that handle a tsp query:
1. **`TSPBruteForce`**: Implement a permutation-based approach that evaluates all $(N-1)!$ possible routes.
2. **`TSPOptimized`**: Implement a significantly faster algorithm. You can choose to write an exact solver using **Held-Karp Bitmask DP**, or an approximation/heuristic like **Nearest Neighbor** or **2-opt**. You can refer to [Heuristics](https://pirun.ku.ac.th/~fengpppa/02206337/htsp.pdf) for an idea on some common ones. You can also browse for any such heuristic and approximations on the internet. Take some time after starting on approximations and cycle through the methods to find good ones.

### Step 3: Compilation (CRITICAL)
Because TSP is heavily reliant on permutation and DP state evaluation, unoptimized C++ code will be agonizingly slow. **You must compile with the `-O3` flag** to enable vectorization and loop unrolling, which speeds up the code dramatically (often ~4x).

```bash
g++ -O3 driver.cpp -o driver
```

### Step 4: Run and Compare
Run your executable twice (once using the Brute Force class, once using the Optimized class) and direct the outputs to different JSON files. Note that JSON formats are similar to the last week's.

```bash
./driver testcases/graph.json testcases/queries_small.json output_brute.json
./driver testcases/graph.json testcases/queries_small.json output_opt.json
```

Use the provided Python visualizer script to compare the results:
```bash
python3 visualize.py output_brute.json output_opt.json
```
*If you implemented Held-Karp, the outputs should match exactly. If you implemented a heuristic, the script will show you how close your approximation was to the optimal brute-force answer!*
