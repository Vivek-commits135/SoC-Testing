// reference_solution.cpp
// MENTOR-ONLY reference implementation used to generate/verify expected
// outputs for Week 6 (Simulated Annealing) test cases.
// Not meant to be handed to mentees as-is -- see Week 6/driver.cpp and
// Week 6/SA.h for the student-facing skeleton.

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <limits>
#include <random>
#include <chrono>
#include <nlohmann/json.hpp>

using namespace std;
using json = nlohmann::ordered_json;

const double INF = numeric_limits<double>::infinity();

// ---------- Graph ----------
struct Graph {
    int n;
    vector<vector<double>> adj; // n x n, INF if no direct edge

    Graph(const json& graph_json) {
        n = (int)graph_json["nodes"].size();
        adj.assign(n, vector<double>(n, INF));
        for (int i = 0; i < n; i++) adj[i][i] = 0.0;
        for (auto& e : graph_json["edges"]) {
            int u = e["u"], v = e["v"];
            double w = e["w"];
            if (w < adj[u][v]) { adj[u][v] = w; adj[v][u] = w; }
        }
    }
};

// ---------- Floyd-Warshall (full n x n shortest paths) ----------
vector<vector<double>> floyd_warshall(const vector<vector<double>>& adj) {
    int n = (int)adj.size();
    vector<vector<double>> dist = adj;
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++) {
            if (dist[i][k] == INF) continue;
            for (int j = 0; j < n; j++) {
                if (dist[k][j] == INF) continue;
                double nd = dist[i][k] + dist[k][j];
                if (nd < dist[i][j]) dist[i][j] = nd;
            }
        }
    return dist;
}

// Extract the m x m submatrix of pairwise distances for a subset of nodes
vector<vector<double>> submatrix(const vector<vector<double>>& full, const vector<int>& nodes) {
    int m = (int)nodes.size();
    vector<vector<double>> d(m, vector<double>(m));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < m; j++)
            d[i][j] = full[nodes[i]][nodes[j]];
    return d;
}

double rnd(double x) { return round(x * 1e4) / 1e4; }

double tour_cost(const vector<int>& tour, const vector<vector<double>>& dist) {
    double c = 0;
    for (size_t i = 0; i + 1 < tour.size(); i++) c += dist[tour[i]][tour[i + 1]];
    return c;
}

// ---------- Brute force (exact, only for tiny m) ----------
pair<vector<int>, double> brute_force(const vector<vector<double>>& dist) {
    int m = (int)dist.size();
    vector<int> perm(m);
    iota(perm.begin(), perm.end(), 0);
    vector<int> best;
    double best_cost = INF;
    // fix node 0 as start to avoid rotational duplicates
    vector<int> rest(perm.begin() + 1, perm.end());
    sort(rest.begin(), rest.end());
    do {
        vector<int> tour = {0};
        tour.insert(tour.end(), rest.begin(), rest.end());
        tour.push_back(0);
        double c = tour_cost(tour, dist);
        if (c < best_cost) { best_cost = c; best = tour; }
    } while (next_permutation(rest.begin(), rest.end()));
    return {best, best_cost};
}

// ---------- Held-Karp (exact, bitmask DP, O(m^2 * 2^m)) ----------
pair<vector<int>, double> held_karp(const vector<vector<double>>& dist) {
    int m = (int)dist.size();
    int FULL = 1 << m;
    vector<vector<double>> dp(FULL, vector<double>(m, INF));
    vector<vector<int>> parent(FULL, vector<int>(m, -1));
    dp[1][0] = 0.0; // start at node 0, mask = {0}

    for (int mask = 1; mask < FULL; mask++) {
        if (!(mask & 1)) continue; // must include node 0
        for (int u = 0; u < m; u++) {
            if (!(mask & (1 << u)) || dp[mask][u] == INF) continue;
            for (int v = 0; v < m; v++) {
                if (mask & (1 << v)) continue;
                int nmask = mask | (1 << v);
                double nd = dp[mask][u] + dist[u][v];
                if (nd < dp[nmask][v]) { dp[nmask][v] = nd; parent[nmask][v] = u; }
            }
        }
    }

    double best_cost = INF;
    int best_last = -1;
    int full_mask = FULL - 1;
    for (int u = 1; u < m; u++) {
        if (dp[full_mask][u] == INF) continue;
        double c = dp[full_mask][u] + dist[u][0];
        if (c < best_cost) { best_cost = c; best_last = u; }
    }
    if (m == 1) { return {{0, 0}, 0.0}; }

    vector<int> tour;
    int mask = full_mask, u = best_last;
    while (u != -1) {
        tour.push_back(u);
        int pu = parent[mask][u];
        mask ^= (1 << u);
        u = pu;
    }
    reverse(tour.begin(), tour.end());
    tour.push_back(0);
    return {tour, best_cost};
}

// ---------- Simulated Annealing ----------
struct SAResult {
    vector<int> tour;
    double cost;
    double time_us;
};

vector<int> nearest_neighbor_tour(const vector<vector<double>>& dist) {
    int m = (int)dist.size();
    vector<bool> visited(m, false);
    vector<int> tour = {0};
    visited[0] = true;
    for (int step = 1; step < m; step++) {
        int cur = tour.back();
        int best = -1; double bestd = INF;
        for (int v = 0; v < m; v++) {
            if (!visited[v] && dist[cur][v] < bestd) { bestd = dist[cur][v]; best = v; }
        }
        tour.push_back(best);
        visited[best] = true;
    }
    tour.push_back(0);
    return tour;
}

SAResult simulated_annealing(const vector<vector<double>>& dist,
                              double initial_temp = 10000.0,
                              double cooling_rate = 0.995,
                              double min_temp = 1e-6,
                              int iters_per_temp = 200,
                              unsigned seed = 1) {
    auto t0 = chrono::high_resolution_clock::now();
    int m = (int)dist.size();
    mt19937 rng(seed);
    uniform_real_distribution<double> unif(0.0, 1.0);
    uniform_int_distribution<int> idx(1, m - 1); // keep node 0 fixed as tour start/end

    vector<int> current = nearest_neighbor_tour(dist);
    double current_cost = tour_cost(current, dist);
    vector<int> best = current;
    double best_cost = current_cost;

    double T = initial_temp;
    while (T > min_temp) {
        for (int it = 0; it < iters_per_temp; it++) {
            if (m <= 3) break; // nothing to optimize
            // 2-opt move: reverse a random segment [i, j] of the interior path
            int i = idx(rng), j = idx(rng);
            if (i == j) continue;
            if (i > j) swap(i, j);

            double removed = dist[current[i - 1]][current[i]] + dist[current[j]][current[j + 1]];
            double added   = dist[current[i - 1]][current[j]] + dist[current[i]][current[j + 1]];
            double delta = added - removed;

            if (delta < 0 || unif(rng) < exp(-delta / T)) {
                reverse(current.begin() + i, current.begin() + j + 1);
                current_cost += delta;
                if (current_cost < best_cost) { best_cost = current_cost; best = current; }
            }
        }
        T *= cooling_rate;
    }
    auto t1 = chrono::high_resolution_clock::now();
    double us = chrono::duration<double, micro>(t1 - t0).count();
    return {best, best_cost, us};
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cerr << "Usage: ./reference_solution <graph.json> <queries.json> <output.json> [mode]\n";
        cerr << "  mode: 'small' (brute_force + held_karp + simulated_annealing)\n";
        cerr << "        'large' (held_karp [if m<=20] + simulated_annealing)\n";
        return 1;
    }
    string graph_file = argv[1], query_file = argv[2], out_file = argv[3];
    string mode = argc >= 5 ? argv[4] : "small";

    ifstream f1(graph_file);
    if (!f1) { cerr << "Cannot open " << graph_file << "\n"; return 1; }
    json graph_json; f1 >> graph_json;
    Graph g(graph_json);
    auto full_dist = floyd_warshall(g.adj);

    ifstream f2(query_file);
    if (!f2) { cerr << "Cannot open " << query_file << "\n"; return 1; }
    json query_json; f2 >> query_json;

    json output_json;
    output_json["meta"] = {{"id", query_json["meta"]["id"]}};
    output_json["results"] = json::array();

    for (auto& event : query_json["events"]) {
        vector<int> nodes = event["nodes"].get<vector<int>>();
        int m = (int)nodes.size();
        auto dist = submatrix(full_dist, nodes);

        json out;
        out["id"] = event["id"];
        out["n"] = m;

        if (mode == "small" && m <= 10) {
            auto [bf_tour, bf_cost] = brute_force(dist);
            vector<int> bf_global; for (int x : bf_tour) bf_global.push_back(nodes[x]);
            out["brute_force"] = {{"optimal_cost", rnd(bf_cost)}, {"tour", bf_global}};
        }
        if (m <= 20) {
            auto [hk_tour, hk_cost] = held_karp(dist);
            vector<int> hk_global; for (int x : hk_tour) hk_global.push_back(nodes[x]);
            out["held_karp"] = {{"optimal_cost", rnd(hk_cost)}, {"tour", hk_global}};
        }

        auto sa = simulated_annealing(dist);
        vector<int> sa_global; for (int x : sa.tour) sa_global.push_back(nodes[x]);
        out["simulated_annealing"] = {
            {"cost", rnd(sa.cost)},
            {"tour", sa_global},
            {"time_us", rnd(sa.time_us)}
        };

        output_json["results"].push_back(out);
    }

    ofstream fo(out_file);
    fo << output_json.dump(4);
    cout << "Wrote " << out_file << "\n";
    return 0;
}
