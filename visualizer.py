"""
Visualizer: Generates and saves benchmark charts as PNG files.
Chart 1: Comparisons count vs Input Size (line)
Chart 2: Execution Time vs Input Size (line)
Chart 3: Comparisons count vs Input Size (bar)
Chart 4: Comparison savings (D&C vs Iterative)
Chart 5: Execution time ratio (D&C overhead vs Iterative)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

SCREENSHOTS_DIR = "screenshots"


def plot_results(results):
    """
    Generate and save five charts based on benchmark results.

    Parameters
    ----------
    results : list of dicts from analysis_engine.run_benchmark()
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    sizes      = [r["size"]                   for r in results]
    iter_comps = [r["iter_comps"]             for r in results]
    dc_comps   = [r["dc_comps"]               for r in results]
    iter_times = [r["iter_time"] * 1000       for r in results]  # ms
    dc_times   = [r["dc_time"]   * 1000       for r in results]  # ms

    # ── Chart 1: Comparisons line ─────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sizes, iter_comps, marker="o", color="steelblue", linewidth=2, label="Iterative  (2n-2)")
    ax.plot(sizes, dc_comps,   marker="s", color="tomato",    linewidth=2, label="Divide & Conquer  (3n/2-2)")
    ax.set_title("Number of Comparisons vs Input Size", fontsize=14, fontweight="bold")
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Comparison Count", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xticks(sizes)
    for x, y in zip(sizes, iter_comps):
        ax.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 8),  ha="center", fontsize=9, color="steelblue")
    for x, y in zip(sizes, dc_comps):
        ax.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, -16), ha="center", fontsize=9, color="tomato")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/comparisons_chart.png", dpi=150)
    plt.close()
    print(f"[Visualizer] Saved -> {SCREENSHOTS_DIR}/comparisons_chart.png")

    # ── Chart 2: Execution Time line ──────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sizes, iter_times, marker="o", color="steelblue", linewidth=2, label="Iterative")
    ax.plot(sizes, dc_times,   marker="s", color="tomato",    linewidth=2, label="Divide & Conquer")
    ax.set_title("Execution Time vs Input Size  (avg of 20 runs)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Time (milliseconds)", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xticks(sizes)
    for x, y in zip(sizes, iter_times):
        ax.annotate(f"{y:.3f}ms", (x, y), textcoords="offset points", xytext=(0, 8),  ha="center", fontsize=9, color="steelblue")
    for x, y in zip(sizes, dc_times):
        ax.annotate(f"{y:.3f}ms", (x, y), textcoords="offset points", xytext=(0, -16), ha="center", fontsize=9, color="tomato")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/execution_time_chart.png", dpi=150)
    plt.close()
    print(f"[Visualizer] Saved -> {SCREENSHOTS_DIR}/execution_time_chart.png")

    # ── Chart 3: Comparisons bar chart ───────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    x     = np.arange(len(sizes))
    width = 0.35
    bars1 = ax.bar(x - width/2, iter_comps, width, color="steelblue", label="Iterative  (2n-2)",          alpha=0.85)
    bars2 = ax.bar(x + width/2, dc_comps,   width, color="tomato",    label="Divide & Conquer  (3n/2-2)", alpha=0.85)
    ax.set_title("Comparisons Count — Side by Side", fontsize=14, fontweight="bold")
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Comparison Count", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in sizes])
    ax.legend(fontsize=11)
    ax.grid(True, axis="y", linestyle="--", alpha=0.6)
    for bar in bars1:
        ax.annotate(str(int(bar.get_height())),
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9, color="steelblue")
    for bar in bars2:
        ax.annotate(str(int(bar.get_height())),
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9, color="tomato")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/comparisons_bar_chart.png", dpi=150)
    plt.close()
    print(f"[Visualizer] Saved -> {SCREENSHOTS_DIR}/comparisons_bar_chart.png")

    # ── Chart 4: Comparison savings (n/2) ────────────────────────────────────
    savings = [ic - dc for ic, dc in zip(iter_comps, dc_comps)]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(sizes, savings, color="mediumseagreen", alpha=0.85, width=300)
    ax.plot(sizes, savings, marker="o", color="darkgreen", linewidth=2)
    ax.set_title("Comparisons Saved by D&C over Iterative  (= n/2)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Comparisons Saved", fontsize=12)
    ax.set_xticks(sizes)
    ax.grid(True, axis="y", linestyle="--", alpha=0.6)
    for x_val, y_val in zip(sizes, savings):
        ax.annotate(str(y_val), (x_val, y_val), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=10, color="darkgreen", fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/savings_chart.png", dpi=150)
    plt.close()
    print(f"[Visualizer] Saved -> {SCREENSHOTS_DIR}/savings_chart.png")

    # ── Chart 5: Execution time ratio (D&C / Iterative) ──────────────────────
    ratios = [dc / it if it > 0 else 0 for dc, it in zip(dc_times, iter_times)]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(sizes, ratios, color="mediumpurple", alpha=0.85, width=300)
    ax.axhline(y=1.0, color="black", linestyle="--", linewidth=1.5, label="Baseline (ratio = 1)")
    ax.set_title("D&C Execution Time Overhead vs Iterative", fontsize=14, fontweight="bold")
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Time Ratio  (D&C / Iterative)", fontsize=12)
    ax.set_xticks(sizes)
    ax.legend(fontsize=11)
    ax.grid(True, axis="y", linestyle="--", alpha=0.6)
    for x_val, y_val in zip(sizes, ratios):
        ax.annotate(f"{y_val:.2f}x", (x_val, y_val), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=10, color="mediumpurple", fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/time_ratio_chart.png", dpi=150)
    plt.close()
    print(f"[Visualizer] Saved -> {SCREENSHOTS_DIR}/time_ratio_chart.png")
