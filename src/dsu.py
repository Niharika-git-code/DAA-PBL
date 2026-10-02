"""Disjoint Set Union (Union-Find) data structure.

Why Kruskal needs it:
    Kruskal adds the cheapest edges first, but must reject an edge whose two
    buildings are already connected (that would create a cycle). DSU answers
    "are these two buildings already in the same connected group?" in
    nearly constant time.
"""


class DSU:
    def __init__(self, items):
        """make-set: every building starts in its own group."""
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}
        self.components = len(self.parent)  # number of separate groups

    def find(self, item):
        """Return the representative (root) of item's group.

        Path compression: every node visited is pointed directly at the root,
        which flattens the tree and speeds up future finds.
        """
        if item not in self.parent:
            raise KeyError(f"Unknown item: {item!r}")
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != root:  # compress the path
            self.parent[item], item = root, self.parent[item]
        return root

    def union(self, a, b):
        """Merge the groups of a and b using union by rank.

        Returns True if a merge happened, False if a and b were already in
        the same group (i.e. connecting them would form a cycle).
        """
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        # Attach the shorter tree under the taller one to keep trees shallow.
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        self.components -= 1
        return True

    def connected(self, a, b):
        """True if a and b are in the same group."""
        return self.find(a) == self.find(b)
