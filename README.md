# Minimum-Cost Network for Connecting Multiple Campus Buildings
### Module: Kruskal's Algorithm + Disjoint Set Union (DSU) + Campus Dataset

**Role:** Member 1 — Sunidhi Singh
**Course:** Design & Analysis of Algorithms (DAA)

This module is fully independent: it needs only Python 3 and its own files.

## Problem Statement
Given the buildings of a university campus and the possible cable connections
between them (each with an installation cost), connect **all** buildings with the
**minimum total cost** and **no unnecessary cycles**.

## Real-World Interpretation
- Building -> vertex
- Possible cable/network link -> undirected edge
- Weight = installation cost in ₹ = `distance_m × cost_per_m`
  (₹150/m for normal conduit, ₹200/m where the route crosses a road or needs trenching)
- Result: the Minimum Spanning Tree (MST) = cheapest set of links that connects every building

## Graph Representation
Edge list of `(source, destination, weight)` tuples, e.g. `("CSE Block", "Library", 6000)`.
Datasets are CSV files loaded by `src/graph.py`, which validates every row
(unknown building, self-loop, non-positive values).

- `data/buildings.csv` — 10 buildings
- `data/connections.csv` — 18 possible connections (`source,destination,distance_m,cost_per_m`)
- `data/extra/` — a small 4-building dataset and a deliberately disconnected one for testing

## Disjoint Set Union (DSU)
Tracks which buildings are already in the same connected group.
- `find(x)` — returns the group's root, with **path compression**
- `union(a, b)` — merges two groups using **union by rank**; returns `False` if they were already joined (a cycle would form)

## Kruskal's Algorithm
Greedy: always take the cheapest edge that does not create a cycle.

**Steps**
1. Put every building in its own DSU set.
2. Sort all edges by weight.
3. Take edges from cheapest to most expensive.
4. If the edge's endpoints are in different sets, add it to the MST and union them; otherwise skip it (cycle).
5. Stop when `V - 1` edges are chosen.
6. If fewer than `V - 1` edges could be chosen, the graph is **disconnected** — an error is reported (only a partial forest is shown, clearly labelled).

`kruskal_mst()` returns `{"edges", "total_cost", "is_connected", "components", "message"}`.

## Complexity
| Part | Time |
|---|---|
| Sorting edges | O(E log E) |
| DSU find/union | ≈ O(α(V)) amortized each (α = inverse Ackermann, practically constant) |
| **Overall Kruskal** | **O(E log E)** (equivalently O(E log V)) |

**Space:** O(V + E) — edge list O(E), DSU parent/rank arrays O(V), MST output O(V).

## Folder Structure
```
sunidhi_kruskal/
├── data/ (buildings.csv, connections.csv, extra/)
├── src/  (dsu.py, graph.py, kruskal.py)
├── tests/ (test_kruskal.py)
├── main.py
├── README.md
└── requirements.txt
```

## How to Run
```bash
python main.py                                   # main campus dataset
python main.py data/extra/disconnected_buildings.csv data/extra/disconnected_connections.csv
python -m unittest discover -s tests -v          # run tests
```

## Sample Output
```
========================================
MINIMUM-COST CAMPUS NETWORK
Kruskal's Algorithm
========================================

Buildings: 10
Possible Connections: 18

Selected MST Connections:
CSE Block -> ECE Block : ₹5,250
Library -> CSE Block : ₹6,000
Administrative Block -> Library : ₹6,750
ECE Block -> Mechanical Block : ₹7,500
Library -> Auditorium : ₹8,250
Main Gate -> Administrative Block : ₹9,000
CSE Block -> Cafeteria : ₹9,750
Hostel -> Sports Complex : ₹12,750
Cafeteria -> Hostel : ₹13,500
----------------------------------------
Total Minimum Cost: ₹78,750
----------------------------------------
Graph Connected: Yes
MST completed successfully.
```

## Test Cases (`tests/test_kruskal.py`)
1. Normal connected campus graph (9 edges, ₹78,750, all buildings covered)
2. Small hand-verifiable graph (+ small CSV dataset)
3. Disconnected graph (in memory and from CSV) -> `is_connected = False` and error message
4. Multiple edges with equal weights (V-1 edges, no cycle, correct cost)
5. Cycle where the expensive edge must be rejected
6. Extras: DSU behaviour, single/empty graph, unknown vertex
