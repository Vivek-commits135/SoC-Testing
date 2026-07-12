#pragma once
#include <vector>
using namespace std;

// ---------------------------------------------------------------------
// Week 6 — Simulated Annealing for TSP
// Fill in the bodies of these functions in SA.cpp (or inline here,
// ---------------------------------------------------------------------

// Cost of a closed tour (tour[0] == tour.back()) given an m x m distance
// matrix. Reuse this — you already wrote it in Week 5.
double tour_cost(const vector<int>& tour, vector<vector<double>>& dist);

// A cheap starting tour. Any valid Hamiltonian cycle works (random shuffle
// is fine), but a greedy Nearest Neighbor tour gives SA a much better
// starting point and fewer iterations to converge.
vector<int> nearest_neighbor_tour(vector<vector<double>>& dist);

// Produce a neighboring tour from `current` by perturbing it slightly.
// The classic choice for TSP is a 2-opt move: pick two positions i < j in
// the tour and reverse the segment between them. Keep node 0 fixed as the
// start/end so every "tour" stays a valid closed cycle.
vector<int> two_opt_neighbor(const vector<int>& current);

// Metropolis acceptance criterion. Always accept improving moves
// (new_cost < old_cost). Accept worsening moves with probability
// exp(-(new_cost - old_cost) / temperature) — this is what lets SA escape
// local minima early on, when temperature is high.
double acceptance_probability(double old_cost, double new_cost, double temperature);

// The main driver of the algorithm. Starting from an initial tour, repeat:
//   1. generate a neighbor (two_opt_neighbor)
//   2. decide whether to move to it (acceptance_probability)
//   3. track the best tour seen so far
//   4. cool down: temperature *= cooling_rate
// until temperature drops below min_temp.
//
// Returns the best tour found, using LOCAL indices [0..m-1] into `dist`
// (same convention as christofides() in Week 5's TSP.h) — driver.cpp maps
// these back to original node IDs.
vector<int> simulated_annealing(vector<vector<double>>& dist,
                                 double initial_temp = 10000.0,
                                 double cooling_rate = 0.995,
                                 double min_temp = 1e-6,
                                 int iters_per_temp = 200);
