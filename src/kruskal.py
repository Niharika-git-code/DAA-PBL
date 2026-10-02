"""Kruskal's Minimum Spanning Tree algorithm (edge list + DSU)."""
from .dsu import DSU


def kruskal_mst(vertices, edges):
    """Compute the MST of an undirected weighted graph.

    vertices: iterable of building names
    edges:    list of (source, destination, weight)

    Returns a dict:
        edges        - selected MST edges [(u, v, w), ...] in the order chosen
        total_cost   - sum of selected edge weights
        is_connected - True if all vertices were connected (a full MST exists)
        components   - number of separate groups remaining (1 = connected)
        message      - human-readable status
    If the graph is disconnected, `edges` holds the minimum spanning FOREST
    and is_connected is False, so the result is never mistaken for a full MST.
    """
    vertices = list(vertices)
    known = set(vertices)
    for u, v, _ in edges:
        if u not in known or v not in known:
            raise ValueError(f"Edge ({u!r}, {v!r}) uses an unknown vertex")

    dsu = DSU(vertices)
    mst_edges, total_cost = [], 0

    # Step 1: sort all edges by weight (stable sort keeps input order on ties).
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        # Add the edge only if it joins two different groups (no cycle).
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total_cost += w
            # Stop once V - 1 edges are selected.
            if len(mst_edges) == len(vertices) - 1:
                break

    is_connected = len(vertices) > 0 and dsu.components == 1
    if is_connected:
        message = "MST completed successfully."
    elif not vertices:
        message = "Error: The campus has no buildings."
    else:
        message = ("Error: The campus graph is disconnected. "
                   "A complete minimum spanning network cannot be formed.")
    return {
        "edges": mst_edges,
        "total_cost": total_cost,
        "is_connected": is_connected,
        "components": dsu.components,
        "message": message,
    }
