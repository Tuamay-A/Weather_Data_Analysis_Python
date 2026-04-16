"""
Visualizer: Generates and saves benchmark charts as PNG files.
Chart 1: Comparisons count vs Input Size
Chart 2: Execution Time vs Input Size
"""

import os
import matplotlib.pyplot as plt

SCREENSHOTS_DIR = "screenshots"


def plot_results(results):
    """
    Generate and save two charts based on benchmark results.

    Parameters
    ----------
    results : list of dicts from analysis_engine.run_benchmark()
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    sizes       = [r["size"]        for r in results]
    iter_comps  = [r["iter_comps"]  for r in results]
    dc_comps    = [r["dc_comps"]    for r in results]
    iter_times  = [r["iter_time"] * 1000 for r in results]   # convert to ms
    dc_times    = [r["dc_time"]   * 1000 for r in results]

    # ── Chart 1: Comparisons ─────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(sizes, iter_comps, marker="o", color="steelblue",
            linewidth=2, label="Iterative  (2n − 2)")
    ax.plot(sizes, dc_comps,   marker="s", color="tomato",
            linewidth=2, label="Divide & Conquer  (3n/2 − 2)")

    ax.set_title("Number of Comparisons vs Input Size", fontsize=14, fontweight="bold")
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Comparison Count", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xticks(sizes)

    # annotate each point
    for x, y in zip(sizes, iter_comps):
        ax.annotate(str(y), (x, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=9, color="steelblue")
    for x, y in zip(sizes, dc_comps):
        ax.annotate(str(y), (x, y), textcoords="offset points",
                    xytext=(0, -16), ha="center", fontsize=9, color="tomato")

    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/comparisons_chart.png", dpi=150)
    plt.close()
    print(f"[Visualizer] Saved -> {SCREENSHOTS_DIR}/comparisons_chart.png")

    # ── Chart 2: Execution Time ───────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(sizes, iter_times, marker="o", color="steelblue",
            linewidth=2, label="Iterative")
    ax.plot(sizes, dc_times,   marker="s", color="tomato",
            linewidth=2, label="Divide & Conquer")

    ax.set_title("Execution Time vs Input Size  (avg of 20 runs)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Time (milliseconds)", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xticks(sizes)

    # annotate each point
    for x, y in zip(sizes, iter_times):
        ax.annotate(f"{y:.3f}ms", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=9, color="steelblue")
    for x, y in zip(sizes, dc_times):
        ax.annotate(f"{y:.3f}ms", (x, y), textcoords="offset points",
                    xytext=(0, -16), ha="center", fontsize=9, color="tomato")

    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/execution_time_chart.png", dpi=150)
    plt.close()
    print(f"[Visualizer] Saved -> {SCREENSHOTS_DIR}/execution_time_chart.png")
