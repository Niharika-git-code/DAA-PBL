"""Tests for DSU and Kruskal's algorithm. Run: python -m unittest discover -s tests -v"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.dsu import DSU
from src.graph import load_campus
from src.kruskal import kruskal_mst

DATA = os.path.join(ROOT, "data")


def total(edges):
    return sum(w for _, _, w in edges)


class TestDSU(unittest.TestCase):
    def test_union_find(self):
        d = DSU(["a", "b", "c", "d"])
        self.assertFalse(d.connected("a", "b"))
        self.assertTrue(d.union("a", "b"))
        self.assertTrue(d.connected("a", "b"))
        self.assertFalse(d.union("b", "a"))  # already together
        d.union("c", "d")
        d.union("b", "c")
        self.assertEqual(d.components, 1)


class TestKruskal(unittest.TestCase):
    # TEST 1: normal connected campus graph (main dataset)
    def test_campus_dataset(self):
        buildings, edges = load_campus(os.path.join(DATA, "buildings.csv"),
                                       os.path.join(DATA, "connections.csv"))
        r = kruskal_mst(buildings, edges)
        self.assertTrue(r["is_connected"])
        self.assertEqual(len(r["edges"]), len(buildings) - 1)
        self.assertEqual(r["total_cost"], total(r["edges"]))
        # Hand-checked: 5250+6000+6750+7500+8250+9000+9750+12750+13500
        self.assertEqual(r["total_cost"], 78750)
        touched = {x for u, v, _ in r["edges"] for x in (u, v)}
        self.assertEqual(touched, set(buildings))

    # TEST 2: small graph verifiable by hand
    def test_small_manual(self):
        v = ["A", "B", "C", "D"]
        e = [("A", "B", 1), ("B", "C", 2), ("C", "D", 3), ("A", "D", 10), ("A", "C", 5)]
        r = kruskal_mst(v, e)
        self.assertEqual(r["total_cost"], 6)
        self.assertEqual(r["edges"], [("A", "B", 1), ("B", "C", 2), ("C", "D", 3)])

    def test_small_dataset_file(self):
        b, e = load_campus(os.path.join(DATA, "extra", "small_buildings.csv"),
                           os.path.join(DATA, "extra", "small_connections.csv"))
        r = kruskal_mst(b, e)
        # 30*100 + 40*100 + 50*100 = 12000
        self.assertEqual(r["total_cost"], 12000)
        self.assertEqual(len(r["edges"]), 3)

    # TEST 3: disconnected graph
    def test_disconnected(self):
        r = kruskal_mst(["A", "B", "C", "D"], [("A", "B", 1), ("C", "D", 2)])
        self.assertFalse(r["is_connected"])
        self.assertEqual(r["components"], 2)
        self.assertIn("disconnected", r["message"])

    def test_disconnected_dataset_file(self):
        b, e = load_campus(os.path.join(DATA, "extra", "disconnected_buildings.csv"),
                           os.path.join(DATA, "extra", "disconnected_connections.csv"))
        r = kruskal_mst(b, e)
        self.assertFalse(r["is_connected"])
        self.assertTrue(r["message"].startswith("Error: The campus graph is disconnected"))

    # TEST 4: equal weights - any valid MST has V-1 edges and the same cost
    def test_equal_weights(self):
        v = ["A", "B", "C", "D"]
        e = [("A", "B", 5), ("B", "C", 5), ("C", "D", 5), ("A", "D", 5), ("A", "C", 5)]
        r = kruskal_mst(v, e)
        self.assertTrue(r["is_connected"])
        self.assertEqual(len(r["edges"]), 3)
        self.assertEqual(r["total_cost"], 15)
        d = DSU(v)  # the chosen edges must form no cycle
        for a, b, _ in r["edges"]:
            self.assertTrue(d.union(a, b))

    # TEST 5: cycle - expensive edge rejected
    def test_cycle_rejected(self):
        e = [("A", "B", 1), ("B", "C", 2), ("A", "C", 100)]
        r = kruskal_mst(["A", "B", "C"], e)
        self.assertNotIn(("A", "C", 100), r["edges"])
        self.assertEqual(r["total_cost"], 3)

    def test_edge_cases(self):
        self.assertTrue(kruskal_mst(["A"], [])["is_connected"])  # single building
        self.assertFalse(kruskal_mst([], [])["is_connected"])
        with self.assertRaises(ValueError):
            kruskal_mst(["A"], [("A", "Z", 1)])


if __name__ == "__main__":
    unittest.main()
