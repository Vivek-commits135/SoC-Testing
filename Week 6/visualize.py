import json
import argparse


def best_known(result):
    """Prefer Held-Karp's exact optimum; fall back to brute force."""
    if "held_karp" in result:
        return result["held_karp"]["optimal_cost"], "held_karp"
    if "brute_force" in result:
        return result["brute_force"]["optimal_cost"], "brute_force"
    return None, None


def compare_results(reference_file, sa_file):
    with open(reference_file, "r") as f1, open(sa_file, "r") as f2:
        ref_data = json.load(f1)
        sa_data = json.load(f2)

    ref_results = {r["id"]: r for r in ref_data.get("results", [])}
    sa_results = {r["id"]: r for r in sa_data.get("results", [])}

    print(f"{'Query ID':<10} | {'n':<4} | {'Best Known':<12} | {'SA Cost':<12} | "
          f"{'Ratio (SA/OPT)':<16} | {'SA Time (us)':<12}")
    print("-" * 78)

    ratios = []
    for qid in sorted(ref_results.keys() & sa_results.keys()):
        ref = ref_results[qid]
        sa = sa_results[qid]

        opt_cost, src = best_known(ref)
        sa_result = sa.get("simulated_annealing", sa)  # allow flat or nested
        sa_cost = sa_result.get("cost")
        sa_time = sa_result.get("time_us", "N/A")
        n = ref.get("n", "N/A")

        if opt_cost is not None and sa_cost is not None:
            ratio = sa_cost / opt_cost if opt_cost != 0 else float("inf")
            ratios.append(ratio)
            ratio_str = f"{ratio:.4f}x" + ("  ✅ optimal" if abs(ratio - 1) < 1e-6 else "")
        else:
            ratio_str = "N/A (no exact ref)"

        print(f"{qid:<10} | {str(n):<4} | {str(opt_cost):<12} | {str(sa_cost):<12} | "
              f"{ratio_str:<16} | {str(sa_time):<12}")

    if ratios:
        avg_ratio = sum(ratios) / len(ratios)
        worst_ratio = max(ratios)
        print("-" * 78)
        print(f"Average approximation ratio: {avg_ratio:.4f}x   "
              f"Worst-case ratio in this run: {worst_ratio:.4f}x")
    else:
        print("\nNo query in this file has an exact reference (n too large for "
              "brute force / Held-Karp) — SA's cost is the only signal available.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare Simulated Annealing output against exact "
                     "(Held-Karp / brute force) TSP solutions."
    )
    parser.add_argument("reference_file", help="Expected/reference output.json "
                                                 "(contains held_karp / brute_force)")
    parser.add_argument("sa_file", help="Your driver's output.json "
                                          "(contains simulated_annealing)")
    args = parser.parse_args()

    print(f"Comparing {args.sa_file} against {args.reference_file}\n")
    compare_results(args.reference_file, args.sa_file)
