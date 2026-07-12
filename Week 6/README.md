# Week 6 — Simulated Annealing for TSP

## Background: Metaheuristic Optimization

So far you've seen two ways to attack TSP:
- **Exact solvers** (Brute Force, Held-Karp) — always correct, but scale
  terribly. Held-Karp's O(n² · 2ⁿ) is already impractical past ~20-22 nodes.
- **Approximation algorithms** (Christofides) — polynomial time with a
  provable bound (1.5× OPT), but only for metric TSP, and the bound is a
  worst case, not a promise of a great tour.

**Simulated Annealing (SA)** is a different kind of tool: a **metaheuristic**.
It gives up on provable guarantees in exchange for scaling to hundreds or
thousands of nodes while still finding tours very close to optimal in
practice. It works by taking a starting tour and repeatedly making small
random changes to it, occasionally accepting a *worse* tour on purpose —
early on — so it doesn't get stuck in the first local minimum it finds.

The name and the idea come from metallurgy: heating a metal and cooling it
slowly lets atoms settle into a low-energy, stable arrangement. Cool it too
fast ("quenching") and it freezes into a defective, higher-energy structure.
SA mimics this with a **temperature** parameter that starts high (accept
almost anything, explore broadly) and decreases over time (accept only
improvements, refine locally).

---

## 1. Resources

* [Simulated Annealing - Wikipedia](https://en.wikipedia.org/wiki/Simulated_annealing)
* [Kirkpatrick, Gelatt, Vecchi (1983) — Optimization by Simulated Annealing](https://www.science.org/doi/10.1126/science.220.4598.671)
* [2-opt - Wikipedia](https://en.wikipedia.org/wiki/2-opt)
* [Visualizing SA on TSP (interactive)](https://toddwschneider.com/posts/traveling-salesman-with-simulated-annealing/)

---

## 2. How It Works

```
current  = some starting tour (e.g. Nearest Neighbor)
best     = current
T        = initial_temp

while T > min_temp:
    repeat iters_per_temp times:
        neighbor = perturb(current)          # e.g. reverse a random segment (2-opt)
        delta    = cost(neighbor) - cost(current)

        if delta < 0:
            current = neighbor                # always take improvements
        else:
            accept with probability exp(-delta / T)   # sometimes take worse moves

        if cost(current) < cost(best):
            best = current

    T = T * cooling_rate                      # cool down

return best
```

Three things control everything:

- **Initial temperature** — too low and SA behaves like plain greedy local
  search (gets stuck fast); too high and it wastes early iterations
  wandering randomly.
- **Cooling schedule** — `T *= cooling_rate` (geometric cooling) is the
  simplest and what we recommend starting with. `cooling_rate` close to 1
  (e.g. 0.995) cools slowly and explores more; further from 1 cools fast
  and converges quicker but risks getting stuck.
- **Neighbor function** — how you perturb a tour. **2-opt** (pick two
  positions, reverse the segment between them) is the standard choice: it
  removes two edges and reconnects the tour the other way, which is a big
  enough change to escape local minima but small enough to keep most of a
  good tour intact.

---

## 3. Understanding the Input JSON

Same format as Weeks 4/5 — you already have a working driver.

**1. `graph.json` (The Map)** — a weighted undirected graph with `nodes`
and `edges` (each edge has `u`, `v`, `w`).

**2. `queries.json` (The Tasks)** — TSP requests. Each event has:
- `id`: unique ID for this run.
- `type`: `"tsp"` — the action to perform.
- `nodes`: the subset of node IDs to find a tour on.

As in Week 5, the graph is **not guaranteed to be complete** on the
requested subset — you still need Floyd-Warshall (or your Week 4/5
shortest-path logic) to build the full pairwise distance matrix before
running SA on it.

---

## 4. Your Tasks

### Step 1: Implement the helpers in `SA.h`
Fill in `tour_cost`, `nearest_neighbor_tour`, `two_opt_neighbor`, and
`acceptance_probability`. You already wrote `tour_cost` in Week 5 — reuse it.

### Step 2: Implement `simulated_annealing()`
This is the main function. It takes the **m×m** distance submatrix for the
query's node subset and returns a tour as **local indices `[0..m-1]`**
(same convention as `christofides()` in Week 5).

1. Build an initial tour with `nearest_neighbor_tour()`.
2. Loop while `T > min_temp`:
   - Generate a neighbor with `two_opt_neighbor()`.
   - Accept/reject using `acceptance_probability()`.
   - Track the best tour seen.
   - Cool down: `T *= cooling_rate`.
3. Return the best tour found.

### Step 3: Wire `driver.cpp`
For each `"tsp"` event: build the distance submatrix → call
`simulated_annealing(dist)` → map local indices back to original node IDs →
write the output (see the format below).

### Step 4: Compile and run

```bash
g++ -O3 -std=c++17 driver.cpp -o driver
./driver "Tests/Test 1/graph.json" "Tests/Test 1/queries_small.json" my_output_small.json
./driver "Tests/Test 1/graph.json" "Tests/Test 1/queries_large.json" my_output_large.json
```

`-O3` matters even more here than in Week 4/5 — SA's inner loop runs
thousands of iterations per query, and each `two_opt_neighbor` call touches
the whole tour.

### Step 5: Check your results
`Tests/Test 1` and `Tests/Test 2` each ship an `output_small.json` /
`output_large.json` containing the **exact optimum** (Brute Force and/or
Held-Karp) alongside a working `simulated_annealing` result, so you can
check both correctness and solution quality:

```bash
python3 visualize.py "Tests/Test 1/output_small.json" my_output_small.json
python3 visualize.py "Tests/Test 2/output_large.json" my_output_large.json
```

This prints a table with the exact optimum, your SA cost, the
approximation ratio (`SA / OPT`), and how long your solver took. On `Test 1`
(n ≤ 7) your ratio should be **exactly 1.0x** most runs — SA has no excuse
not to find the true optimum on graphs that small. `Test 2` goes up to
n = 16, where Held-Karp is still exact but noticeably slower to compute
than SA — this is the regime where SA starts to earn its keep.

### Generate the Output

```json
{
    "meta": {"id": "assignment_04"},
    "results": [
        {
            "id": 1,
            "simulated_annealing": {
                "cost": 274.26,
                "tour": [0, 4, 1, 2, 3, 0],
                "time_us": 30568.45
            }
        }
    ]
}
```

---

## 5. Test Cases

| | Graph | Queries | What it checks |
|---|---|---|---|
| **Test 1** | 7-node sparse graph (same as Week 4/5) | small: 3 & 4 nodes · large: 6 & 7 nodes | Correctness — SA should match the exact optimum every time on inputs this small. |
| **Test 2** | 16-node complete Euclidean graph | small: 5 & 9 nodes · large: 8 & 16 nodes | Scaling — brute force is infeasible on the n=16 query; Held-Karp is still exact here and is your ground truth, but notice SA gets there far faster. |

> **Note:** `Test 1`'s reference costs were regenerated using proper
> Floyd-Warshall shortest-path distances between subset nodes (as the
> Week 4/5 README instructs), not raw direct-edge sums. If you compare
> against the *original* Week 4/5 `output.json` files for the same graph,
> a couple of costs won't match for that reason — a graph this sparse has
> genuine shortcuts through nodes outside the queried subset.

---

## 6. Tuning Tips

- If your SA result is consistently *worse* than OPT even on tiny graphs,
  your cooling is too fast, or `iters_per_temp` is too low — the search
  isn't getting enough chances to explore before freezing.
- If SA is slow but accurate, try raising `cooling_rate` toward 1 for
  better quality, or lowering it for speed — this trade-off is the whole
  point of the algorithm, so it's worth actually plotting cost vs. time
  for a few parameter settings.
- Keeping node `0` fixed as the start/end of every candidate tour
  (rather than treating rotations as distinct) shrinks the search space
  without losing any solutions, since a tour's cost doesn't depend on
  which node you call "first".
- A `nearest_neighbor_tour()` start converges faster than a random start
  — SA still explores, but from a reasonable place instead of a chaotic one.

---

## Problems to be submitted

Exact-answer judges don't suit a randomized heuristic well, so this week's
submissions are **partial-scoring / optimization** judges instead — the
better your tour, the more you score, which is exactly what SA is for.

- [Travelling Salesperson 2D (Kattis)](https://open.kattis.com/problems/tsp) — up to 1000 points, scored by tour length. A great fit for NN + 2-opt + SA under a time limit.
- [Euclidean TSP (Kattis)](https://open.kattis.com/problems/euclideantsp) — same flavor, different constraints; good for testing how your cooling schedule holds up on a second instance size.
