#pragma once
#include <vector>
#include <limits>
#include <algorithm>
using namespace std;

const double INF = numeric_limits<double>::infinity();
vector<vector<int>> floyd_warshall(vector<vector<double>>& adj,vector<int>& nodes);
vector<pair<int,int>> prim_mst(vector<vector<double>>& dist);
vector<pair<int,int>> perfect_matching(vector<int>& odds,vector<vector<double>>& dist);
vector<int> eulerian_circuit(int m, vector<vector<pair<int,int>>>& adj_list);
double tour_cost(const vector<int>& tour,vector<vector<double>>& dist);

// Steps: Floyd-Warshall -> MST -> odd vertices -> matching -> Eulerian circuit -> shorcutting
vector<int> christofides(vector<vector<double>>& adj,vector<int>& nodes);
