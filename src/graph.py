"""Graph loading using an edge-list representation.

Edge format: (source, destination, weight)
Weight = installation cost in rupees = distance_m * cost_per_m.
"""
import csv


def load_buildings(path):
    """Read building names (one per row, column 'building')."""
    with open(path, newline="", encoding="utf-8") as f:
        names = [row["building"].strip() for row in csv.DictReader(f)]
    if len(set(names)) != len(names):
        raise ValueError("buildings file contains duplicate building names")
    return names


def load_connections(path, buildings):
    """Read possible connections and return an edge list of
    (source, destination, cost) tuples. Validates every row."""
    known = set(buildings)
    edges = []
    with open(path, newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            src, dst = row["source"].strip(), row["destination"].strip()
            if src not in known or dst not in known:
                raise ValueError(f"line {line_no}: unknown building in {src!r} - {dst!r}")
            if src == dst:
                raise ValueError(f"line {line_no}: self-loop on {src!r}")
            distance, rate = float(row["distance_m"]), float(row["cost_per_m"])
            if distance <= 0 or rate <= 0:
                raise ValueError(f"line {line_no}: distance and cost must be positive")
            cost = distance * rate
            edges.append((src, dst, int(cost) if cost == int(cost) else cost))
    return edges


def load_campus(buildings_path, connections_path):
    """Load a campus dataset -> (list of buildings, edge list)."""
    buildings = load_buildings(buildings_path)
    return buildings, load_connections(connections_path, buildings)
