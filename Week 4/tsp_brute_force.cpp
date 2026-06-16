/**
 * ============================================================
 *  Week 4 — TSP & Hamiltonian Cycle Exercise
 *  File: tsp_brute_force.cpp
 * ============================================================
 *
 *  LEARNING GOALS
 *  ──────────────
 *   1. Read a weighted graph from input
 *   2. Detect whether a Hamiltonian cycle exists (using DFS + backtracking)
 *   3. Solve TSP using brute-force permutations
 *   4. Measure and observe the runtime growth as n increases
 *   5. (Bonus) Implement Held-Karp bitmask DP for comparison
 *
 *  HOW TO COMPILE
 *  ──────────────
 *   g++ -O2 -std=c++17 -o tsp tsp_brute_force.cpp
 *
 *  INPUT FORMAT
 *  ────────────
 *   Line 1:   n  (number of cities, 1 <= n <= 20)
 *   Line 2:   m  (number of directed edges)
 *   Next m lines:  u v w   (edge from u to v with weight w, 0-indexed)
 *
 *  THEN: number of queries Q, followed by Q lines each with:
 *   - "HAM"        → check if a Hamiltonian cycle exists
 *   - "TSP"        → run brute-force TSP and print min cost + time taken
 *   - "DP"         → run Held-Karp DP TSP (bonus, uncomment when ready)
 *   - "PRINT n"    → print all permutations and their costs for small n (n <= 8)
 *
 *  SAMPLE INPUT  (save as test1.txt and run: ./tsp < test1.txt)
 *  ────────────
 *   4
 *   12
 *   0 1 10
 *   1 0 10
 *   0 2 15
 *   2 0 15
 *   0 3 20
 *   3 0 20
 *   1 2 35
 *   2 1 35
 *   1 3 25
 *   3 1 25
 *   2 3 30
 *   3 2 30
 *   3
 *   HAM
 *   TSP
 *   PRINT 4
 *
 *  EXPECTED OUTPUT
 *  ───────────────
 *   [HAM] Hamiltonian cycle EXISTS. One valid cycle: 0 -> 1 -> 2 -> 3 -> 0
 *   [TSP-BRUTE] Optimal tour cost: 80  |  Tour: 0 -> 1 -> 3 -> 2 -> 0  |  Permutations checked: 6  |  Time: ...
 *   [PRINT] All tours from city 0:
 *     Tour: 0 -> 1 -> 2 -> 3 -> 0  |  Cost: 95
 *     Tour: 0 -> 1 -> 3 -> 2 -> 0  |  Cost: 80   <-- OPTIMAL
 *     Tour: 0 -> 2 -> 1 -> 3 -> 0  |  Cost: 95
 *     ...
 */

#include <bits/stdc++.h>
using namespace std;

// ─────────────────────────────────────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────────────────────────────────────
const long long INF = 1e18;
const int MAXN = 20;

// ─────────────────────────────────────────────────────────────────────────────
// GLOBAL GRAPH REPRESENTATION
// dist[u][v] = weight of edge u→v, or INF if no edge
// ─────────────────────────────────────────────────────────────────────────────
int n, m;
long long dist[MAXN][MAXN];

// ─────────────────────────────────────────────────────────────────────────────
// UTILITY: Pretty-print a tour
// ─────────────────────────────────────────────────────────────────────────────
string tour_to_string(const vector<int>& perm) {
    // perm is a permutation of cities (not including the return to start)
    string s = "";
    for (int i = 0; i < (int)perm.size(); i++) {
        s += to_string(perm[i]);
        s += " -> ";
    }
    s += to_string(perm[0]);
    return s;
}

// ─────────────────────────────────────────────────────────────────────────────
// UTILITY: Compute the cost of a full tour
// tour[0] -> tour[1] -> ... -> tour[n-1] -> tour[0]
// Returns INF if any edge in the tour doesn't exist
// ─────────────────────────────────────────────────────────────────────────────
long long tour_cost(const vector<int>& tour) {
    long long cost = 0;
    int sz = tour.size();
    for (int i = 0; i < sz; i++) {
        int u = tour[i];
        int v = tour[(i + 1) % sz];
        if (dist[u][v] == INF) return INF;
        cost += dist[u][v];
    }
    return cost;
}

// ─────────────────────────────────────────────────────────────────────────────
//  PART 1: HAMILTONIAN CYCLE DETECTION
//  Uses DFS + backtracking
//
//  TODO (Exercise 1): Trace through this function with the sample graph.
//  What is the order in which cities are visited?
//  What happens when we hit a dead end?
// ─────────────────────────────────────────────────────────────────────────────
vector<int> ham_path;     // stores the cycle found (if any)
bool ham_found;

void dfs_hamiltonian(int cur, int visited_count, vector<bool>& visited) {
    if (ham_found) return;

    if (visited_count == n) {
        // All cities visited — check if we can return to start
        if (dist[cur][0] < INF) {
            ham_found = true;
            ham_path.push_back(0);  // close the cycle
        }
        return;
    }

    for (int next = 0; next < n; next++) {
        if (!visited[next] && dist[cur][next] < INF) {
            visited[next] = true;
            ham_path.push_back(next);

            dfs_hamiltonian(next, visited_count + 1, visited);

            // Backtrack
            visited[next] = false;
            ham_path.pop_back();
        }
    }
}

void check_hamiltonian() {
    ham_found = false;
    ham_path.clear();

    vector<bool> visited(n, false);
    visited[0] = true;
    ham_path.push_back(0);

    dfs_hamiltonian(0, 1, visited);

    if (ham_found) {
        cout << "[HAM] Hamiltonian cycle EXISTS. One valid cycle: ";
        for (int i = 0; i < (int)ham_path.size(); i++) {
            cout << ham_path[i];
            if (i + 1 < (int)ham_path.size()) cout << " -> ";
        }
        cout << "\n";
    } else {
        cout << "[HAM] NO Hamiltonian cycle exists in this graph.\n";
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  PART 2: BRUTE-FORCE TSP
//
//  Fix city 0 as start. Try all (n-1)! permutations of remaining cities.
//
//  TODO (Exercise 2): Modify this function to also count how many permutations
//  were pruned (skipped because an intermediate edge doesn't exist).
//  How does that change your observations?
//
//  TODO (Exercise 3): Run this for n = 8, 10, 12, 14 and record the time.
//  Plot it (even on paper). What pattern do you see?
// ─────────────────────────────────────────────────────────────────────────────
void solve_tsp_brute() {
    // Build array of cities to permute (1, 2, ..., n-1)
    vector<int> cities;
    for (int i = 1; i < n; i++) cities.push_back(i);

    long long best_cost = INF;
    vector<int> best_tour;
    long long perm_count = 0;

    auto start_time = chrono::high_resolution_clock::now();

    // next_permutation requires sorted input — cities is already sorted
    do {
        perm_count++;

        // Build full tour: 0, cities[0], cities[1], ..., cities[n-2], (back to 0)
        vector<int> tour = {0};
        for (int c : cities) tour.push_back(c);

        long long cost = tour_cost(tour);
        if (cost < best_cost) {
            best_cost = cost;
            best_tour = tour;
        }
    } while (next_permutation(cities.begin(), cities.end()));

    auto end_time = chrono::high_resolution_clock::now();
    double elapsed_ms = chrono::duration<double, milli>(end_time - start_time).count();

    cout << "[TSP-BRUTE] ";
    if (best_cost == INF) {
        cout << "No valid Hamiltonian tour exists.\n";
    } else {
        cout << "Optimal tour cost: " << best_cost
             << "  |  Tour: " << tour_to_string(best_tour)
             << "  |  Permutations checked: " << perm_count
             << "  |  Time: " << fixed << setprecision(3) << elapsed_ms << " ms\n";
    }

    // ── CURIOSITY BOX ────────────────────────────────────────────────────────
    // Think about it:
    //   For n cities, we check (n-1)! permutations.
    //   n=5  → 24 perms      n=10 → 362,880 perms
    //   n=12 → 39,916,800    n=15 → 87 billion
    //
    // After which n does YOUR computer start slowing down noticeably?
    // ────────────────────────────────────────────────────────────────────────
}

// ─────────────────────────────────────────────────────────────────────────────
//  PART 2b: PRINT ALL TOURS (for small n)
//
//  Shows every possible tour and its cost so students can see all candidates.
// ─────────────────────────────────────────────────────────────────────────────
void print_all_tours(int limit) {
    if (n > limit) {
        cout << "[PRINT] Too many cities (" << n << " > " << limit
             << "). Skipping full print to protect your terminal.\n";
        return;
    }
    vector<int> cities;
    for (int i = 1; i < n; i++) cities.push_back(i);

    long long best_cost = INF;
    cout << "[PRINT] All tours from city 0:\n";

    do {
        vector<int> tour = {0};
        for (int c : cities) tour.push_back(c);
        long long cost = tour_cost(tour);
        best_cost = min(best_cost, cost);

        cout << "  Tour: " << tour_to_string(tour) << "  |  Cost: ";
        if (cost == INF) cout << "INVALID (missing edge)";
        else cout << cost;
        cout << "\n";
    } while (next_permutation(cities.begin(), cities.end()));

    cout << "  ─────────────────────────────────\n";
    cout << "  Best cost: " << (best_cost == INF ? -1 : best_cost) << "\n";
}

// ─────────────────────────────────────────────────────────────────────────────
//  PART 3: HELD-KARP BITMASK DP  (BONUS — uncomment to use)
//
//  dp[mask][i] = minimum cost to reach city i having visited
//               exactly the cities in 'mask' (bit j = city j visited)
//
//  TODO (Exercise 4 — Bonus):
//    1. Implement the Held-Karp algorithm below.
//    2. Compare its runtime with brute force for the same inputs.
//    3. At what n does DP become clearly faster? Why?
//
//  HINT: Start from dp[1][0] = 0.
//        For each mask and each city i in mask:
//          For each city j NOT equal to i, if j is in mask:
//            dp[mask][i] = min(dp[mask][i], dp[mask ^ (1<<i)][j] + dist[j][i])
//        Answer = min over all i of dp[(1<<n)-1][i] + dist[i][0]
// ─────────────────────────────────────────────────────────────────────────────
void solve_tsp_dp() {
    if (n > 20) {
        cout << "[TSP-DP] n too large for bitmask DP (max 20).\n";
        return;
    }

    int states = 1 << n;
    // dp[mask][i]: min cost to visit all cities in mask, ending at i
    vector<vector<long long>> dp(states, vector<long long>(n, INF));
    vector<vector<int>> parent(states, vector<int>(n, -1));

    // Base case: start at city 0
    dp[1][0] = 0;

    auto start_time = chrono::high_resolution_clock::now();

    // ── TODO: Fill in this section ──────────────────────────────────────────
    //
    // for (int mask = 1; mask < states; mask++) {
    //     if (!(mask & 1)) continue;   // city 0 must always be visited
    //     for (int i = 0; i < n; i++) {
    //         if (!(mask & (1 << i))) continue;   // i must be in mask
    //         if (dp[mask][i] == INF) continue;   // unreachable
    //
    //         for (int j = 0; j < n; j++) {
    //             if (mask & (1 << j)) continue;  // j already visited
    //             if (dist[i][j] == INF) continue;
    //
    //             int new_mask = mask | (1 << j);
    //             if (dp[new_mask][j] > dp[mask][i] + dist[i][j]) {
    //                 dp[new_mask][j] = dp[mask][i] + dist[i][j];
    //                 parent[new_mask][j] = i;
    //             }
    //         }
    //     }
    // }
    //
    // ────────────────────────────────────────────────────────────────────────

    cout << "[TSP-DP] Held-Karp DP not yet implemented. Uncomment the code above!\n";
    cout << "         Hint: Fill in the triple nested loop and then find the answer below:\n";
    cout << "         int full_mask = (1 << n) - 1;\n";
    cout << "         long long ans = INF;\n";
    cout << "         for (int i = 1; i < n; i++)\n";
    cout << "             if (dp[full_mask][i] != INF && dist[i][0] != INF)\n";
    cout << "                 ans = min(ans, dp[full_mask][i] + dist[i][0]);\n";

    auto end_time = chrono::high_resolution_clock::now();
    double elapsed_ms = chrono::duration<double, milli>(end_time - start_time).count();
    cout << "         Time so far: " << fixed << setprecision(3) << elapsed_ms << " ms\n";
}

// ─────────────────────────────────────────────────────────────────────────────
//  PART 4: BENCHMARK — Observe factorial growth
//
//  Generates complete graphs of increasing sizes and times brute force TSP.
//
//  TODO (Exercise 5): Run this and fill in the table in the README.
//  What is the ratio of times between consecutive n values?
//  Is it close to n? Why?
// ─────────────────────────────────────────────────────────────────────────────
void run_benchmark() {
    cout << "\n[BENCH] Brute-Force TSP — Factorial Growth Demonstration\n";
    cout << "n  | Perms (n-1)! | Time (ms)  | Ratio\n";
    cout << "---|-------------|------------|------\n";

    double prev_time = -1;
    for (int test_n = 4; test_n <= 13; test_n++) {
        // Build a complete graph with random weights
        int saved_n = n;
        n = test_n;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                dist[i][j] = (i == j) ? INF : (rand() % 100 + 1);

        vector<int> cities;
        for (int i = 1; i < n; i++) cities.push_back(i);

        long long best = INF;
        long long perms = 0;
        auto t0 = chrono::high_resolution_clock::now();
        do {
            perms++;
            vector<int> tour = {0};
            for (int c : cities) tour.push_back(c);
            long long cost = tour_cost(tour);
            best = min(best, cost);
        } while (next_permutation(cities.begin(), cities.end()));
        auto t1 = chrono::high_resolution_clock::now();
        double ms = chrono::duration<double, milli>(t1 - t0).count();

        double ratio = (prev_time > 0) ? ms / prev_time : 0;
        cout << left << setw(3) << test_n << "| "
             << setw(12) << perms << "| "
             << setw(11) << fixed << setprecision(3) << ms << "| ";
        if (prev_time > 0) cout << fixed << setprecision(1) << ratio << "x";
        cout << "\n";

        prev_time = ms;
        n = saved_n;

        // Stop early if it's getting too slow
        if (ms > 10000) {
            cout << "Stopping: time exceeded 10 seconds.\n";
            break;
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  MAIN
// ─────────────────────────────────────────────────────────────────────────────
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    srand(42);

    // Initialize all distances to INF
    for (int i = 0; i < MAXN; i++)
        for (int j = 0; j < MAXN; j++)
            dist[i][j] = (i == j) ? 0 : INF;

    cin >> n >> m;
    for (int e = 0; e < m; e++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        dist[u][v] = w;
    }

    int Q;
    cin >> Q;
    while (Q--) {
        string cmd;
        cin >> cmd;

        if (cmd == "HAM") {
            check_hamiltonian();
        } else if (cmd == "TSP") {
            solve_tsp_brute();
        } else if (cmd == "DP") {
            solve_tsp_dp();
        } else if (cmd == "PRINT") {
            int lim;
            cin >> lim;
            print_all_tours(lim);
        } else if (cmd == "BENCH") {
            run_benchmark();
        } else {
            cout << "Unknown command: " << cmd << "\n";
        }
    }

    return 0;
}

/*
 * ════════════════════════════════════════════════════════════════
 *  EXERCISE QUESTIONS — Answer these after running the code
 * ════════════════════════════════════════════════════════════════
 *
 *  Exercise 1 (Hamiltonian Cycle):
 *    a) Modify the DFS to count how many partial paths it explores
 *       before finding (or failing to find) a cycle.
 *    b) Create a graph with n=6 that has NO Hamiltonian cycle.
 *       How does the DFS behave on it?
 *
 *  Exercise 2 (Brute Force):
 *    a) For a complete graph with n cities, how many permutations
 *       does brute force check? Write a formula.
 *    b) Run BENCH and fill this table:
 *       n  | Time   | Ratio to previous
 *       4  | ___    | —
 *       5  | ___    | ___
 *       6  | ___    | ___
 *       ...
 *    c) What pattern do you notice in the ratio column?
 *
 *  Exercise 3 (Efficiency):
 *    a) What is the maximum n for which brute force runs in < 1 second
 *       on your machine?
 *    b) If brute force takes T seconds for n cities, roughly how long
 *       will it take for n+1 cities? Why?
 *
 *  Exercise 4 (Bonus — Held-Karp DP):
 *    a) Implement the DP section (uncomment the TODO block).
 *    b) Compare DP vs brute force time for n = 10, 15, 20.
 *    c) What is the memory usage of Held-Karp for n = 20?
 *       (Hint: n * 2^n entries, each a long long = 8 bytes)
 *
 *  Exercise 5 (Thinking Ahead):
 *    a) Google "Christofides algorithm". What guarantee does it provide?
 *    b) For practical TSP (e.g., 1000 cities), which approaches are used?
 *       Look up: OR-Tools, LKH3, CONCORDE solver.
 *
 * ════════════════════════════════════════════════════════════════
 */
