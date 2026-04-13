"""
Task 4: Main Entry Point
Orchestrates dataset generation, benchmarking, and result display.
Also prints the mathematical proof (Task 5).
"""

import os
import sys

from dataset_generator   import WeatherLoader
from analysis_engine     import run_benchmark, print_table
from visualizer          import plot_results


CSV_PATH = "weather_data.csv"


def print_math_proof():
    """Task 5 — Print the mathematical proof explaining 1.5n vs 2n."""

    proof = """
╔══════════════════════════════════════════════════════════════════════════════╗
║          MATHEMATICAL PROOF: WHY D&C USES ~1.5n vs ITERATIVE ~2n           ║
╚══════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. ITERATIVE APPROACH  —  T_iter(n) = 2n - 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Algorithm:
    current_min = current_max = data[0]
    for i in range(1, n):
        if data[i] < current_min:   ← comparison 1
        if data[i] > current_max:   ← comparison 2

  Each of the (n-1) elements after the first triggers exactly 2 comparisons.

  Total = 2 × (n - 1) = 2n - 2

  Example  n = 8:  T_iter(8) = 2(8) - 2 = 14 comparisons

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 2. DIVIDE & CONQUER  —  T_dc(n) = 3n/2 - 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Recurrence relation:
    T(1) = 0          (single element, no comparison)
    T(2) = 1          (one comparison to decide min/max)
    T(n) = 2T(n/2) + 2   for n > 2

  Solving by substitution (assume n = 2^k):

    T(2^k) = 2 · T(2^(k-1)) + 2
           = 2 · [2 · T(2^(k-2)) + 2] + 2
           = 4 · T(2^(k-2)) + 4 + 2
           = 4 · [2 · T(2^(k-3)) + 2] + 4 + 2
           = 8 · T(2^(k-3)) + 8 + 4 + 2
           ...
           = 2^(k-1) · T(2) + 2^(k-1) + 2^(k-2) + ... + 2
           = 2^(k-1) · 1   + (2^k - 2)          [geometric series]
           = n/2            + n - 2
           = 3n/2 - 2

  Example  n = 8:  T_dc(8) = 3(8)/2 - 2 = 12 - 2 = 10 comparisons

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 3. COMPARISON SAVINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Savings = T_iter(n) - T_dc(n)
          = (2n - 2) - (3n/2 - 2)
          = 2n - 2 - 3n/2 + 2
          = n/2

  D&C saves exactly n/2 comparisons over the iterative approach.

  Why? The iterative method blindly compares every element against BOTH
  current_min and current_max (2 comparisons each).

  D&C first pairs adjacent elements (1 comparison per pair = n/2 comparisons),
  then only the smaller of each pair is a candidate for the global minimum,
  and only the larger is a candidate for the global maximum.
  This halves the work at each merge step.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 4. ASYMPTOTIC COMPLEXITY (both are O(n))
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  | Algorithm   | Comparisons  | Time Complexity | Space Complexity |
  |-------------|--------------|-----------------|------------------|
  | Iterative   | 2n - 2       | O(n)            | O(1)             |
  | D&C         | 3n/2 - 2     | O(n)            | O(log n) stack   |

  Both are linear, but D&C is optimal in the number of comparisons.
  The lower bound for finding both min and max is ⌊3n/2⌋ - 2 comparisons,
  which D&C achieves — making it comparison-optimal.

══════════════════════════════════════════════════════════════════════════════
"""
    print(proof)


def main():
    print("=" * 60)
    print("   METEOROLOGICAL DATA — MIN/MAX BENCHMARKING TOOL")
    print("=" * 60)

    #  Step 1: Load or generate dataset 
    loader = WeatherLoader(CSV_PATH)

    if not os.path.exists(CSV_PATH):
        print("\n[Main] CSV not found. Generating synthetic dataset...")
        loader.generate_csv(5000)
    else:
        print(f"\n[Main] Found existing '{CSV_PATH}'.")

    data = loader.load_csv()

    #  Step 2: Run benchmarks 
    print(f"\n[Main] Running benchmarks on slices: 500, 1000, 5000 records (20 runs averaged)...\n")
    results = run_benchmark(data)

    #  Step 3: Print results table 
    print_table(results)

    #  Step 4: Generate charts 
    print("[Main] Generating charts...")
    plot_results(results)

    #  Step 5: Print mathematical proof 
    print_math_proof()


if __name__ == "__main__":
    main()
