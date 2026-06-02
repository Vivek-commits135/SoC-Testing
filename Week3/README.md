# Week 3 — Magic of A*

## 1. What You Will Learn

* **Uninformed vs. Informed Search:** Transitioning from Dijkstra's expansion to goal-oriented heuristics ($$g(n)$$ vs $$h(n)$$).
* **Heuristic Admissibility:** Proving the optimality condition where a heuristic must never overestimate the true remaining cost ($$0 \le h(n) \le h^*(n)$$).
* **Heuristic Consistency (Monotonicity):** Formulating the triangle inequality constraint ($$h(n) \le c(n, n') + h(n')$$) required for graph searches.
* **API-Style I/O Architecture:** You will learn how to read JSON inputs and write JSON outputs. We are setting this up now because you will reuse this exact same format for all future assignments, like the Traveling Salesperson Problem (TSP).
---

## 2. Resources

* A* part in Lecture 17 from [DSA Slides](https://www.cse.iitb.ac.in/~akg/courses/2025-ds/).
* Chapter 13 (Shortest Paths) from [CP Handbook](https://github.com/Vivek-commits135/Soc-2026-The-Optimal-Odessey/blob/main/Resources/cp_handbook.pdf).
* [Red Blob Games: Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) *(Interactive spatial pathfinding visualizer).*

---
## Setup
**nlohmann/json** for JSON parsing. 

The easiest way is to use the single-header version.
1. Download the latest [`json.hpp`](https://github.com/nlohmann/json/releases/latest/download/json.hpp) file directly from their releases page.
2. Place `json.hpp` in the same folder as your `main.cpp`.
3. Include it in your code using `#include "json.hpp"` (Note: The provided template uses `<nlohmann/json.hpp>` assuming a global install, so simply change that line to `"json.hpp"` if you download the file locally)
---
## 3. Assignment

You are required to build a single pathfinding program that processes dynamic event queries and evaluates search spaces.

### Understanding the Input JSON

Your program will read from two different input files.

**1. `graph.json` (The Map)**
This file defines the environment. 
- `grid_size`: Tells you the total number of `rows` and `cols`.
- `obstacles`: A list of coordinates `{"y": row, "x": col}` where you cannot walk. 

**2. `queries.json` (The Tasks)**
This file contains the pathfinding requests you need to run on the map.
- `meta`: Contains an `id` for the assignment.
- `events`: A list of paths you need to find. Each event specifies:
  - `id`: The unique ID for this specific run.
  - `type`: The action to perform (e.g., `find_path`).
  - `start` and `goal`: The starting and ending `{"y": row, "x": col}` coordinates.


### Your Tasks

#### 1. Build the `Graph` Class
Complete the `Graph` class so that it parses `graph.json`. It should store the grid dimensions and flag the obstacle coordinates. It must include a method `std::vector<Node> get_neighbors(Node current)` that returns only valid, non-obstacle adjacent nodes.

#### 2. Implement the Search Algorithms
For *every* `find_path` event in `queries.json`, you must run these three algorithms back-to-back to compare their efficiency:
1.  **`dijkstra`**:  A* with no heuristic $h(n) = 0$
2.  **`astar_euclidean`**: A* using straight-line distance. 
    $h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$
3.  **`astar_manhattan`**: A* using grid distance. 
    $h(n) = |x_1 - x_2| + |y_1 - y_2|$

#### 3. Generate the Output
For every `find_path` event, your program must push a JSON object to the `results` array in `output.json`. This object must contain the results and execution time (in milliseconds) for all three algorithms. 

*(Note: Use `<chrono>` in C++ to measure the `time_ms` for each algorithm run. If you aren't familiar with it, here is a [quick guide on how to measure execution time using chrono](https://www.geeksforgeeks.org/measure-execution-time-function-cpp/)).*

**Example Output:**
```json
{
    "meta": {"id": "assignment_01"},
    "results": [
        {
            "id": 1,
            "dijkstra": {
                "path_found": true,
                "path_length": 24,
                "nodes_explored": 312,
                "time_ms": 1.5
            },
            "astar_euclidean": {
                "path_found": true,
                "path_length": 24,
                "nodes_explored": 184,
                "time_ms": 0.9
            },
            "astar_manhattan": {
                "path_found": true,
                "path_length": 24,
                "nodes_explored": 25,
                "time_ms": 0.1
            }
        }
    ]
}
```
#### 4. Performance Visualization

A reference Python visualization script (`visualize.py`) is provided to analyze the generated `output.json`.

Install the required Python packages:

```bash
pip install numpy matplotlib
```


Basic usage:

```bash
python visualize_summary.py output.json
```

Specify a custom output image filename:

```bash
python visualize_summary.py output.json --save astar_summary.png
```

The script generates:

- A summary visualization (`performance_summary.png` by default)
- Aggregate statistics printed to the terminal
---
## ❗️ Note

> It is highly recommended that you share your doubts, methods, progress, and problems related to the questions and/or content on the **WhatsApp group**.
