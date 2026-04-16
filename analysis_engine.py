"""
Task 4 : Analysis Engine
Runs both algorithms on dataset slices of 500, 1000, and 5000 records.
Each algorithm is run RUNS times and the average time is reported
to eliminate noise and give reliable timing results.
"""

import time
from iterative_min_max      import IterativeMinMax
from divide_conquer_min_max import DivideConquerMinMax


SIZES = [500, 1000, 5000]
RUNS  = 20   # number of repetitions for averaging


def run_benchmark(data):
    """
    Run both algorithms on slices of `data` for each size in SIZES.
    Each algorithm is executed RUNS times; average time is recorded.

    Returns
    -------
    list of dicts with keys:
        size, iter_min, iter_max, iter_comps, iter_expected, iter_time,
        dc_min, dc_max, dc_comps, dc_expected, dc_time
    """
    iterative = IterativeMinMax()
    dc        = DivideConquerMinMax()
    results   = []

    for n in SIZES:
        if n > len(data):
            print(f"[Engine] Skipping n={n}: dataset only has {len(data)} records.")
            continue

        slice_ = data[:n]

        #  Iterative — average over RUNS 
        i_times = []
        for _ in range(RUNS):
            t0 = time.perf_counter()
            i_min, i_max, i_comps = iterative.find(slice_)
            i_times.append(time.perf_counter() - t0)
        i_time = sum(i_times) / RUNS

        #  Divide & Conquer — average over RUNS 
        d_times = []
        for _ in range(RUNS):
            t0 = time.perf_counter()
            d_min, d_max, d_comps = dc.find(slice_)
            d_times.append(time.perf_counter() - t0)
        d_time = sum(d_times) / RUNS

        results.append({
            "size"         : n,
            "iter_min"     : i_min,
            "iter_max"     : i_max,
            "iter_comps"   : i_comps,
            "iter_expected": 2 * n - 2,
            "iter_time"    : i_time,
            "dc_min"       : d_min,
            "dc_max"       : d_max,
            "dc_comps"     : d_comps,
            "dc_expected"  : (3 * n) // 2 - 2,   # exact for n=2^k; approx otherwise
            "dc_time"      : d_time,
        })

        print(f"[Engine] n={n:>5} done  ({RUNS} runs averaged)")

    return results


def print_table(results):
    """Print a formatted comparison table to stdout."""

    sep  = "+" + "-"*8 + "+" + "-"*22 + "+" + "-"*22 + "+"
    sep2 = "+" + "="*8 + "+" + "="*22 + "+" + "="*22 + "+"

    print("\n" + sep2)
    print(f"| {'BENCHMARKING RESULTS  (avg of ' + str(RUNS) + ' runs)':^52} |")
    print(sep2)
    print(f"| {'n':^6} | {'--- ITERATIVE ---':^20} | {'--- D&C ---':^20} |")
    print(f"| {'':^6} | {'Comps':^9} {'Expected':^9}{'Time(s)':^5}| {'Comps':^9} {'Expected':^9}{'Time(s)':^5}|")
    print(sep)

    for r in results:
        print(
            f"| {r['size']:^6} "
            f"| {r['iter_comps']:^9} {r['iter_expected']:^9}{r['iter_time']:>6.6f}"
            f"| {r['dc_comps']:^9} {r['dc_expected']:^9}{r['dc_time']:>6.6f}|"
        )

    print(sep)
    print("  * D&C 'Expected' column uses formula 3n/2-2 (exact for n=2^k; actual")
    print("    count may be slightly higher for non-power-of-2 sizes — this is correct.)")
    print()

    # Verify correctness
    print("[Verification] Min/Max agreement between algorithms:")
    for r in results:
        match = (r['iter_min'] == r['dc_min']) and (r['iter_max'] == r['dc_max'])
        status = "OK" if match else "MISMATCH"
        print(
            f"  n={r['size']:>5}: min={r['iter_min']:>7.2f}  "
            f"max={r['iter_max']:>7.2f}  [{status}]"
        )
    print()
