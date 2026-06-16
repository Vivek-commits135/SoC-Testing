# Week 4 — K Shortest Paths & TSP Consolidation

> **Combined Week 4+5 module** — Graph algorithm consolidation, Hamiltonian cycles, and the Travelling Salesman Problem.

---

## 📁 Folder Structure

```
week4/
├── README.md                          ← You are here
├── theory/
│   └── Week4_Theory_TSP_Hamiltonian.pdf   ← Start here! Full theory notes
├── exercises/
│   ├── tsp_brute_force.cpp            ← Main coding exercise (well-commented)
│   ├── test1.txt                      ← Sample input: complete K4 graph
│   ├── test2_no_ham.txt               ← Sample input: graph with no Ham cycle
│   └── test3_benchmark.txt            ← Input to trigger factorial growth demo
└── resources/
    └── (see links below)
```

---

## 🎯 Learning Goals for This Week

By the end of Week 4, you should be able to:

- [ ] Define a **Hamiltonian cycle** and explain how it differs from an Eulerian cycle
- [ ] Determine whether a Hamiltonian cycle *might* exist (Dirac's / Ore's theorem)
- [ ] Detect a Hamiltonian cycle using **DFS + backtracking**
- [ ] Formally state the **Travelling Salesman Problem (TSP)**
- [ ] Explain why brute-force TSP is **O(n!)** and why that's catastrophic
- [ ] Understand that TSP is **NP-hard** and what that implies
- [ ] Know the **Held-Karp bitmask DP** approach: `O(n² × 2ⁿ)`
- [ ] Solve **K shortest paths** using a modified Dijkstra / Yen's algorithm

---

## 📖 How to Use This Module

**Recommended order:**

1. **Read the theory PDF** → `theory/Week4_Theory_TSP_Hamiltonian.pdf`
2. **Read through `tsp_brute_force.cpp`** carefully (all the comments!)
3. **Compile and run** the provided test cases
4. **Answer the exercise questions** embedded at the bottom of the `.cpp` file
5. **Attempt the practice problems** listed below

---

## 🛠️ Running the Code

```bash
# Step 1: Compile
g++ -O2 -std=c++17 -o tsp exercises/tsp_brute_force.cpp

# Step 2: Run with sample input
./tsp < exercises/test1.txt          # Complete K4 graph — TSP + Ham cycle
./tsp < exercises/test2_no_ham.txt   # Graph with NO Hamiltonian cycle
./tsp < exercises/test3_benchmark.txt  # Factorial growth benchmark

# Step 3: Experiment! Create your own input files.
```

**Input format reminder:**
```
n m
u1 v1 w1
u2 v2 w2
... (m edges)
Q
QUERY1
QUERY2
...
```
Available queries: `HAM`, `TSP`, `PRINT <limit>`, `DP` (bonus), `BENCH`

---

## 🧠 Key Concepts at a Glance

### Hamiltonian Cycle
- Visits **every vertex exactly once** and returns to start
- **Detecting** it: NP-complete (use DFS + backtracking for small graphs)
- **Not all graphs have one** — Dirac's theorem gives a sufficient condition

### TSP (Travelling Salesman Problem)
- Find the **minimum-cost Hamiltonian cycle** in a weighted complete graph
- Brute force: **O(n!)** — infeasible beyond ~12 cities
- Held-Karp DP: **O(n² × 2ⁿ)** — feasible up to ~22 cities
- NP-hard — no known polynomial algorithm

### Factorial Growth (The Core Insight)
| n cities | Permutations | Time @ 10⁹ ops/sec |
|----------|-------------|---------------------|
| 8 | 5,040 | < 1 ms |
| 10 | 362,880 | < 1 ms |
| 12 | 39,916,800 | ~40 ms |
| 15 | 87 billion | ~87 sec |
| 20 | 121 quadrillion | ~3.8 million years |

### K Shortest Paths
- Find the k cheapest paths from source s to destination t
- Yen's algorithm for simple paths: **O(k × n × (m + n log n))**
- Heap-based approach (paths may repeat vertices): **O(k × m × log(nk))**

---

## 📝 Exercises

These are embedded in `tsp_brute_force.cpp` — work through them in order.

**Exercise 1 — Hamiltonian Cycle Detection:**
- Trace the DFS backtracking on `test1.txt`
- Create a graph with n=6 and NO Hamiltonian cycle. What happens?

**Exercise 2 — Brute Force Observation:**
- Run `BENCH` and record times for n = 4 to 12
- What is the time ratio between consecutive n values?

**Exercise 3 — Efficiency Limits:**
- Find the maximum n where brute force runs in < 1 second on your machine
- Extrapolate: how long for n = 20?

**Exercise 4 (Bonus) — Implement Held-Karp DP:**
- Uncomment the TODO block in `solve_tsp_dp()`
- Compare runtimes with brute force for n = 10, 15, 20

**Exercise 5 (Research) — Beyond Exact Algorithms:**
- Look up "Christofides algorithm" — what guarantee does it give?
- What solvers are used in industry for large TSP instances?

---

## 🔗 External Resources

### 📺 Video Explanations

| Topic | Link | Duration |
|-------|------|----------|
| Hamiltonian Cycle — William Fiset | https://www.youtube.com/watch?v=dQr4wZCiJJ4 | 12 min |
| TSP Introduction — Abdul Bari | https://www.youtube.com/watch?v=1FEP_sNb62k | 19 min |
| Held-Karp Bitmask DP — Errichto | https://www.youtube.com/watch?v=cY4HiiFHO1o | 25 min |
| K Shortest Paths — Tushar Roy | https://www.youtube.com/watch?v=WDm6505YLQQ | 15 min |

### 📚 Reading

| Resource | Link | What to Read |
|----------|------|-------------|
| CP-Algorithms: TSP | https://cp-algorithms.com/graph/travelling_salesman_problem.html | Full article |
| CP-Algorithms: Hamiltonian paths | https://cp-algorithms.com/graph/hamiltonian_path.html | Full article |
| USACO Guide: Bitmask DP | https://usaco.guide/gold/dp-bitmask | Sections 1–3 |
| Visualgo: Graph traversal | https://visualgo.net/en/dfsbfs | Interactive |

### 🎮 Interactive Visualisers

- **TSP Solver (visual):** https://www.math.uwaterloo.ca/tsp/games/tspfun.html
- **Hamiltonian Cycle puzzle:** https://www.hamiltonian-cycle.info/
- **Graph editor + DFS visualiser:** https://csacademy.com/app/graph_editor/

### 🏋️ Practice Problems

#### Warm-up (Hamiltonian / Graph)
| Problem | Platform | Link |
|---------|----------|------|
| Find Hamiltonian cycle (if exists) | CSES | https://cses.fi/problemset/task/1690 |
| Graph paths I | CSES | https://cses.fi/problemset/task/1723 |

#### K Shortest Paths
| Problem | Platform | Link |
|---------|----------|------|
| k-th Shortest Path | CSES | https://cses.fi/problemset/task/1196 |
| K Shortest Paths | Kattis | https://open.kattis.com/problems/shortestpath3 |

#### TSP / Bitmask DP
| Problem | Platform | Link |
|---------|----------|------|
| Salesman's Trip | CSES (TSP) | https://cses.fi/problemset/task/1690 |
| Hamiltonian Flights | CSES | https://cses.fi/problemset/task/1690 |
| Bitmask DP warmup | LeetCode 847 | https://leetcode.com/problems/shortest-path-visiting-all-nodes/ |
| CF: Bitmask DP | Codeforces 8C | https://codeforces.com/contest/8/problem/C |
| SPOJ TSP | SPOJ | https://www.spoj.com/problems/ATSP/ |

---

## 💡 Common Mistakes to Avoid

1. **Confusing Hamiltonian and Eulerian cycles**
   - Eulerian: traverses every *edge* exactly once
   - Hamiltonian: visits every *vertex* exactly once
   - They are completely different!

2. **Forgetting to close the cycle**
   - TSP tour must return to the starting city
   - Always add `dist[last_city][start]` to your cost

3. **Off-by-one in bitmask DP**
   - `(1 << n) - 1` is the full mask (all n cities visited)
   - `1 << i` sets bit for city i (0-indexed)
   - Check: `mask & (1 << i)` to see if city i is in the mask

4. **Pruning too late in brute force**
   - If any intermediate edge doesn't exist, you can skip remaining permutations
   - Early termination can speed up brute force significantly

---

## 📊 Complexity Summary

| Algorithm | Time | Space | When to Use |
|-----------|------|-------|-------------|
| Ham. cycle DFS | O(n! / k) pruned | O(n) | n ≤ 15, just detection |
| TSP Brute Force | O(n!) | O(n) | n ≤ 12 |
| TSP Held-Karp DP | O(n² × 2ⁿ) | O(n × 2ⁿ) | n ≤ 20–22 |
| Christofides (approx) | O(n³) | O(n²) | Large n, metric TSP |
| K-SP (heap) | O(k×m×log(nk)) | O(nk) | Any n, repeated vertices OK |
| Yen's Algorithm | O(k×n×(m+n log n)) | O(kn) | Simple paths required |

---

## 🚀 Checkpoint Questions

Before moving to Week 5, make sure you can answer these without looking them up:

1. What is a Hamiltonian cycle? Give an example on a graph with 4 nodes.
2. For n = 6 cities, how many permutations does brute-force TSP check?
3. What does it mean for TSP to be NP-hard?
4. What is the state in the Held-Karp DP? What does `dp[mask][i]` represent?
5. What is the time complexity of Held-Karp? How does it compare to brute force for n=20?
6. In what real-world situation would you use k shortest paths instead of single shortest path?

---

*Week 4 materials prepared for mentorship programme. Reach out in the group chat if you get stuck — post your code, the test input, and what output you got vs. what you expected.*
