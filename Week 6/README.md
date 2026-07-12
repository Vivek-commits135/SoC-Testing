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

  Concretely: if your tour is `... A → B → ... → C → D ...`, a 2-opt move
  deletes edges `A–B` and `C–D` and reconnects as `A–C` and `B–D` — the
  only way to reconnect two removed edges that keeps the tour a single
  loop. That reconnection is exactly the same as reversing the segment
  from `B` to `C` in place, which is why the code for it is just
  `reverse(tour.begin()+i, tour.begin()+j+1)`. It's a good default move
  because it's the smallest change that can undo a "crossing" in the
  tour, and its cost delta only needs 4 edge lookups — no need to
  recompute the whole tour cost after every move.

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

`-O3` matters even more here — SA's inner loop runs
thousands of iterations per query, and each `two_opt_neighbor` call touches
the whole tour.

---
### Step 5: Generate your own reference optimum
`Tests/Test 1` and `Tests/Test 2` only ship `graph.json`,
`queries_small.json`, and `queries_large.json`. You
already have exact solvers from Weeks 4/5 (Brute Force, Held-Karp), so use
them: run your Week 4/5 driver on these same inputs to produce your own
"ground truth" output, then run this week's driver (SA) on the same inputs
and compare the two.

```bash
# From your Week 4 or Week 5 folder — your own Brute Force / Held-Karp
./driver "../Week 6/Tests/Test 1/graph.json" "../Week 6/Tests/Test 1/queries_small.json" reference_small.json
./driver "../Week 6/Tests/Test 1/graph.json" "../Week 6/Tests/Test 1/queries_large.json" reference_large.json

# From this week's folder — your Simulated Annealing
./driver "Tests/Test 1/graph.json" "Tests/Test 1/queries_small.json" my_output_small.json
./driver "Tests/Test 1/graph.json" "Tests/Test 1/queries_large.json" my_output_large.json

python3 visualize.py reference_small.json my_output_small.json
python3 visualize.py reference_large.json my_output_large.json
```

### Generate the Output

Your driver's output should look like this — one `simulated_annealing`
entry per query, with `cost`, the resulting `tour`, and how long it took:

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


## 5. Tuning Tips

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
## 6. Test Cases

| | Graph | Queries | What it checks |
|---|---|---|---|
| **Test 1** | 7-node sparse graph (same as Week 4/5) | small: 3 & 4 nodes · large: 6 & 7 nodes | Correctness — run your Week 4/5 Brute Force / Held-Karp on these same files to get your own exact optimum, then confirm SA matches it. |
| **Test 2** | 16-node complete Euclidean graph | small: 5 & 9 nodes · large: 8 & 16 nodes | Scaling — the n=16 query is too big for Brute Force, so this is where your Held-Karp implementation earns its keep as ground truth, and where SA's speed advantage starts to show. |

Feel free to generate your own graphs and queries too, and stress-test your
implementation beyond these two.
---


## 7. More Methods to Explore (Optional)

2-opt + geometric cooling is the standard starting point, but it's just one
point in a much bigger design space. If you finish early or want to push
your Kattis score further, these are worth trying — roughly in order of
"small tweak" to "different algorithm entirely":

**Better moves (swap in for `two_opt_neighbor`)**
- **Or-opt** — instead of reversing a segment, relocate a short chain of
  1–3 consecutive cities to a different point in the tour. Cheaper per
  move than 2-opt and catches a different class of improvements (good
  combined with 2-opt: alternate between the two).
- **3-opt** — remove three edges instead of two. Strictly more powerful
  than 2-opt (it includes Or-opt as a special case), but O(n³) candidate
  moves instead of O(n²) — usually only worth it on smaller instances or
  with a randomized/segment-limited variant.
- [**Lin–Kernighan**](https://en.wikipedia.org/wiki/Lin%E2%80%93Kernighan_heuristic) — the
  classic "variable-depth" move: chains several edge swaps together,
  keeping a move only if the *whole chain* improves the tour. This is
  what state-of-the-art TSP heuristics (like LKH) are built on — a serious
  step up in complexity, but the single most impactful thing you can read
  about after this week.

**Better cooling schedules (swap in for geometric cooling)**
- **Adaptive cooling** — adjust the cooling rate based on the acceptance
  ratio (fraction of moves accepted) at each temperature, instead of a
  fixed multiplier.
- **Reheating** — if the best-so-far cost hasn't improved in a while,
  bump the temperature back up instead of letting it keep dropping. Turns
  a single annealing run into several shorter ones that each get a chance
  to explore a different part of the search space.

**Other metaheuristics entirely (same problem, different search strategy)**
- [**Tabu Search**](https://en.wikipedia.org/wiki/Tabu_search) — like SA
  but deterministic: always take the best available move, and maintain a
  short-term memory ("tabu list") of recently-visited tours/moves so you
  can't immediately undo your own progress and loop forever.
- [**Genetic Algorithms**](https://en.wikipedia.org/wiki/Genetic_algorithm) —
  keep a *population* of tours, "breed" good ones together (e.g. Ordered
  Crossover, which is worth reading about specifically — naive crossover
  breaks the "visit each city once" constraint), and mutate with 2-opt.
- [**Ant Colony Optimization**](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms) —
  simulate many "ants" building tours greedily but randomly, laying down
  more pheromone on shorter tours so future ants are biased toward them.
  Fun to implement and visualize, and a nice contrast to SA since it's
  population-based rather than single-solution.

---

## 8. Test Yourself (Optional)

if you want to see how your SA holds up outside these test cases, both of these are scored by tour length rather than a strict pass/fail — a good fit for a heuristic:

- [Travelling Salesperson 2D (Kattis)](https://open.kattis.com/problems/tsp) — up to 1000 points, scored by tour length. A good fit for NN + 2-opt + SA under a time limit.
- [Euclidean TSP (Kattis)](https://open.kattis.com/problems/euclideantsp) — same flavor, different constraints; good for testing how your cooling schedule holds up on a second instance size.