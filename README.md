# Minimum-Cost Network for Connecting Multiple Campus Buildings

Design & Analysis of Algorithms – project.
Campus buildings are vertices, possible network links are weighted edges, and the goal is the
**Minimum Spanning Tree (MST)** with the lowest total connection cost.

| Member | Algorithm | Folder |
|--------|-----------|--------|
| Sunidhi Singh | Kruskal's (DSU) | `kruskal/`, `data/` |
| Niharika Jha | Prim's (Min-Heap) | `prim/` |

## Repository structure

```
data/        Campus buildings and connections      (Sunidhi)
kruskal/     DSU + Kruskal implementation + tests  (Sunidhi)
prim/        Prim + Priority Queue + tests         (Niharika)
README.md    Project overview and algorithm details
```

This repository currently contains the **Prim's module**. Merge it with Sunidhi's work by copying
the `prim/` folder into the shared repository. See [`prim/README.md`](prim/README.md) for usage,
tests and the time/space complexity.

## Quick start (Prim's module)

```bash
cd prim
python prim.py datasets/campus_small.json
python -m unittest discover -s tests -v
```

## Final integration (team step)

A small `main.py` can later load the same dataset, run both Kruskal and Prim, and check that both
give the same minimum cost.
