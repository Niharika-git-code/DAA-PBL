"""Demo runner for Member 1 module: Kruskal's Algorithm + DSU.

Usage:
    python main.py
    python main.py <buildings.csv> <connections.csv>
"""
import os
import sys

from src.graph import load_campus
from src.kruskal import kruskal_mst

BASE = os.path.dirname(os.path.abspath(__file__))
LINE = "=" * 40
THIN = "-" * 40


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # so the rupee sign prints on Windows
    if len(argv) == 3:
        b_path, c_path = argv[1], argv[2]
    else:
        b_path = os.path.join(BASE, "data", "buildings.csv")
        c_path = os.path.join(BASE, "data", "connections.csv")

    try:
        buildings, edges = load_campus(b_path, c_path)
    except (OSError, ValueError, KeyError) as err:
        print(f"Error loading dataset: {err}")
        return 1

    result = kruskal_mst(buildings, edges)

    print(LINE)
    print("MINIMUM-COST CAMPUS NETWORK")
    print("Kruskal's Algorithm")
    print(LINE)
    print(f"\nBuildings: {len(buildings)}")
    print(f"Possible Connections: {len(edges)}\n")

    label = "Selected MST Connections:" if result["is_connected"] else \
        "Selected Connections (partial - no complete MST):"
    print(label)
    for u, v, w in result["edges"]:
        print(f"{u} -> {v} : ₹{w:,}")
    print(THIN)
    print(f"Total Minimum Cost: ₹{result['total_cost']:,}")
    print(THIN)
    print(f"Graph Connected: {'Yes' if result['is_connected'] else 'No'}")
    print(result["message"])
    return 0 if result["is_connected"] else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
