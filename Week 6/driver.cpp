#include<iostream>
#include<fstream>
#include<string>
#include<algorithm>
#include<nlohmann/json.hpp>
#include<chrono>
#include"SA.h"

int main(int argc, char* argv[]){

    if (argc < 4) {
        std::cerr << "Usage: ./{executable} <graph.json> <queries.json> <output.json>\n";
        return 1;
    }

    std::string graph_json_file = argv[1];
    std::string query_json_file = argv[2];
    std::string output_file = argv[3];

    std::ifstream file1(graph_json_file);

    if (!file1.is_open()) {
        std::cerr << "Error: Could not open " << graph_json_file << '\n';
        return 1;
    }

    nlohmann::json graph_json;
    file1 >> graph_json; // reading the graph_json file into json

	/*!!! Need changes here !!!*/

	// Create a Graph class that takes the json input
	// and stores the required graph data structures.
	// Remember to include the header file containing the class.
	// Uncomment the line below after implementing the class.
	// Graph map(graph_json);

    std::ifstream file2(query_json_file);

    if (!file2.is_open()) {
        std::cerr << "Error: Could not open " << query_json_file << '\n';
        return 1;
    }

    nlohmann::json query_json;
    file2 >> query_json; // reading the query_json file into json object

    nlohmann::json output_json;

    output_json["meta"] = {{"id", query_json["meta"]["id"]}};
    output_json["results"] = nlohmann::json::array();

    std::string type;

    for(auto event : query_json["events"]){

        type = event["type"];

        if (type == "tsp") {
            /* Refer to the sample code below */
            /*
            // 1. Extract the node subset for this query
            std::vector<int> nodes = event["nodes"].get<std::vector<int>>();

            // 2. Run all-pairs shortest paths on map.adj (Floyd-Warshall,
            //    same as Week 5), then take the m x m submatrix for `nodes`.
            //    auto full_dist = floyd_warshall(map.adj);
            //    auto dist = submatrix(full_dist, nodes);

            // 3. Run simulated annealing on that submatrix.
            auto t0 = std::chrono::high_resolution_clock::now();
            // std::vector<int> local_tour = simulated_annealing(dist);
            auto t1 = std::chrono::high_resolution_clock::now();
            double time_us = std::chrono::duration<double, std::micro>(t1 - t0).count();

            // 4. Map local indices [0..m-1] back to original node IDs.
            // std::vector<int> tour;
            // for (int i : local_tour) tour.push_back(nodes[i]);
            // double cost = tour_cost(local_tour, dist);

            nlohmann::json out;
            out["id"] = event["id"];
            // out["simulated_annealing"] = {
            //     {"cost", cost},
            //     {"tour", tour},
            //     {"time_us", time_us}
            // };
            output_json["results"].push_back(out);
            */
        }
    }

    std::ofstream fout(output_file);
    fout << output_json.dump(4);

    return 0;
}
