#!/usr/bin/env python3
"""Run T08 checks against synthetic local snapshots, without graph access.

Use the same Python environment as kg-comply-paths.py. NetworkX must be
installed. All fixtures are created in temporary directories and removed.
"""

from contextlib import redirect_stderr
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().with_name("kg-comply-paths.py")
SPEC = importlib.util.spec_from_file_location("kg_comply_paths_under_test", SCRIPT)
paths = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(paths)


def node(name):
    return {"vid": "tech_point:" + name, "name": name}


def edge(source, target, confidence, rank=0):
    return {
        "src": "tech_point:" + source,
        "dst": "tech_point:" + target,
        "rank": rank,
        "confidence": confidence,
    }


def pair(source, target):
    return {
        "from": {"id": "tech_point:" + source, "name": source},
        "to": {"id": "tech_point:" + target, "name": target},
        "bfs_hops": 1,
        "dijkstra_hops": 2,
    }


def write_snapshot(directory, nodes, edges):
    directory.mkdir()
    manifest = {"format_version": 1, "space": paths.SPACE, "files": {}}
    for category, rows in (("nodes", nodes), ("edges", edges)):
        filename = category + ".jsonl"
        destination = directory / filename
        with destination.open("w", encoding="utf-8", newline="\n") as target:
            for row in rows:
                target.write(json.dumps(row, allow_nan=False) + "\n")
        manifest["files"][category] = {
            "filename": filename,
            "rows": len(rows),
            "sha256": paths.sha256(destination),
        }
    paths.write_json(directory / "metadata.json", manifest)
    return manifest


def ten_pair_fixture():
    nodes, edges, pairs = [], [], []
    for i in range(10):
        a, b, c = (f"{letter}{i}" for letter in "abc")
        nodes.extend([node(a), node(b), node(c)])
        edges.extend([edge(a, b, 0.1), edge(a, c, 0.9), edge(c, b, 0.9)])
        pairs.append(pair(a, b))
    return nodes, edges, pairs


class PathsSelfcheck(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="kg-comply-t08-selfcheck-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def snapshot(self, nodes, edges, name="snapshot"):
        directory = self.directory / name
        manifest = write_snapshot(directory, nodes, edges)
        graph, quality = paths.load_graph(directory, manifest)
        return directory, manifest, graph, quality

    def offline_main(self, directory, pairs):
        baseline = self.directory / "baseline.json"
        report = self.directory / "report.json"
        paths.write_json(baseline, {"tech_layer": {paths.PATH_KEY: {"pairs": pairs}}})
        argv = [
            str(SCRIPT), "--reuse-snapshot", "--snapshot-dir", str(directory),
            "--baseline", str(baseline), "--output", str(report),
        ]
        with mock.patch.object(sys, "argv", argv), redirect_stderr(io.StringIO()):
            with mock.patch.object(paths, "export_snapshot", side_effect=AssertionError("Offline check attempted graph access")):
                code = paths.main()
        return code, json.loads(report.read_text(encoding="utf-8"))

    def test_higher_confidence_can_win_with_more_hops(self):
        _, _, graph, _ = self.snapshot(
            [node("a"), node("b"), node("c")],
            [edge("a", "b", 0.1), edge("a", "c", 0.9), edge("c", "b", 0.9)],
        )
        result = paths.run_pair(graph, pair("a", "b"), 5)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["bfs_path_ids"], ["tech_point:a", "tech_point:b"])
        self.assertEqual(result["dijkstra_path_ids"], ["tech_point:a", "tech_point:c", "tech_point:b"])
        self.assertEqual(result["bfs_hops"], 1)
        self.assertEqual(result["dijkstra_hops"], 2)
        self.assertAlmostEqual(result["dijkstra_cost"], 2 / 0.9)
        self.assertLess(result["dijkstra_cost"], result["bfs_cost"])
        self.assertGreater(result["weighted_cost_improvement"], 0)
        self.assertTrue(result["weighted_path_differs"])
        self.assertEqual(result["alt_path_count"], 2)
        self.assertEqual([p["hops"] for p in result["alt_paths"]], [1, 2])
        self.assertEqual(len({tuple(p["node_ids"]) for p in result["alt_paths"]}), 2)

    def test_reverse_and_rank_duplicates_keep_maximum_confidence(self):
        rows = [edge("a", "b", 0.2), edge("b", "a", 0.9, 7), edge("a", "b", 0.4, 4)]
        for index, edges in enumerate((rows, list(reversed(rows)))):
            with self.subTest(order=index):
                _, _, graph, quality = self.snapshot([node("a"), node("b")], edges, str(index))
                self.assertEqual(graph.number_of_edges(), 1)
                self.assertEqual(quality["duplicate_undirected_pair_rows"], 2)
                self.assertEqual(graph["tech_point:a"]["tech_point:b"]["confidence"], 0.9)
                self.assertAlmostEqual(graph["tech_point:a"]["tech_point:b"]["cost"], 1 / 0.9)

    def test_invalid_weights_fail_before_path_search_and_leave_diagnostics(self):
        invalid_values = [None, 0, -0.1, True, "NaN", "Infinity", "not-a-number", 1e-320]
        for index, value in enumerate(invalid_values):
            with self.subTest(confidence=value):
                directory = self.directory / str(index)
                write_snapshot(
                    directory, [node("a"), node("b"), node("c")],
                    [edge("a", "b", 0.8), edge("b", "c", value)],
                )
                baseline = self.directory / "baseline.json"
                report = self.directory / "report.json"
                paths.write_json(baseline, {"tech_layer": {paths.PATH_KEY: {
                    "pairs": [pair("a", "unused-" + str(i)) for i in range(10)],
                }}})
                argv = [str(SCRIPT), "--reuse-snapshot", "--snapshot-dir", str(directory),
                        "--baseline", str(baseline), "--output", str(report)]
                with mock.patch.object(sys, "argv", argv), redirect_stderr(io.StringIO()):
                    with mock.patch.object(paths, "run_pair", side_effect=AssertionError("Invalid weights reached path search")):
                        with self.assertRaises(paths.RunError):
                            paths.main()
                result = json.loads(report.read_text(encoding="utf-8"))
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["tech_layer"][paths.PATH_KEY]["pairs"], [])
                self.assertEqual(result["quality"]["null_confidence" if value is None else "invalid_confidence"], 1)

    def test_unreachable_has_explicit_empty_result(self):
        _, _, graph, _ = self.snapshot(
            [node("a"), node("b"), node("c")], [edge("b", "c", 0.8)],
        )
        result = paths.run_pair(graph, pair("a", "b"), 5)
        self.assertEqual((result["status"], result["reason"]), ("empty", "unreachable"))
        self.assertIsNone(result["bfs_hops"])
        self.assertIsNone(result["dijkstra_cost"])
        self.assertEqual(result["bfs_path_ids"], [])
        self.assertEqual(result["dijkstra_path_ids"], [])
        self.assertEqual(result["alt_paths"], [])

    def test_missing_endpoint_has_distinct_empty_reason(self):
        _, _, graph, _ = self.snapshot([node("a"), node("b")], [edge("a", "b", 0.8)])
        result = paths.run_pair(graph, pair("a", "missing"), 5)
        self.assertEqual((result["status"], result["reason"]), ("empty", "endpoint_missing"))
        self.assertEqual(result["alt_paths"], [])

    def test_snapshot_hash_detects_tampering_without_a_row_count_change(self):
        directory, _, _, _ = self.snapshot([node("a"), node("b")], [edge("a", "b", 0.8)])
        paths.read_snapshot(directory)
        with (directory / "edges.jsonl").open("a", encoding="utf-8") as target:
            target.write("\n")
        with self.assertRaisesRegex(paths.RunError, "integrity"):
            paths.read_snapshot(directory)

    def test_snapshot_manifest_row_count_is_checked(self):
        directory, manifest, _, _ = self.snapshot([node("a"), node("b")], [edge("a", "b", 0.8)])
        manifest["files"]["edges"]["rows"] += 1
        with self.assertRaisesRegex(paths.RunError, "row counts"):
            paths.load_graph(directory, manifest)

    def test_self_loops_and_dangling_edges_are_counted(self):
        _, _, graph, quality = self.snapshot(
            [node("a"), node("b")],
            [edge("a", "b", 0.8), edge("a", "a", 0.9), edge("a", "missing", 0.7)],
        )
        self.assertEqual(graph.number_of_nodes(), 2)
        self.assertEqual(graph.number_of_edges(), 1)
        self.assertEqual(quality["self_loop_rows"], 1)
        self.assertEqual(quality["missing_endpoint_rows"], 1)

    def test_ten_pair_report_roundtrip_uses_only_the_synthetic_snapshot(self):
        nodes, edges, pairs = ten_pair_fixture()
        directory = self.directory / "snapshot"
        write_snapshot(directory, nodes, edges)
        code, result = self.offline_main(directory, pairs)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["mode"], "read_only")
        self.assertEqual(result["verification"]["pairs_reported"], 10)
        self.assertEqual(result["verification"]["reachable_pairs"], 10)
        self.assertEqual(result["verification"]["weighted_hop_differences"], 10)
        self.assertEqual(result["quality"]["invalid_confidence"], 0)
        self.assertEqual(result["verification"]["weighted_cost_improved_pairs"], 10)
        self.assertTrue(all(math.isfinite(p["dijkstra_cost"]) for p in result["tech_layer"][paths.PATH_KEY]["pairs"]))

    def test_missing_baseline_endpoint_keeps_overall_report_in_review(self):
        nodes, edges, pairs = ten_pair_fixture()
        missing = "tech_point:a9"
        nodes = [n for n in nodes if n["vid"] != missing]
        edges = [e for e in edges if missing not in (e["src"], e["dst"])]
        directory = self.directory / "snapshot"
        write_snapshot(directory, nodes, edges)
        code, result = self.offline_main(directory, pairs)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["verification"]["empty_pairs"], 1)
        self.assertEqual(result["quality"]["missing_endpoint_rows"], 0)
        self.assertEqual(result["tech_layer"][paths.PATH_KEY]["pairs"][-1]["reason"], "endpoint_missing")

    def test_dangling_exported_edge_keeps_overall_report_in_review(self):
        nodes, edges, pairs = ten_pair_fixture()
        edges.append(edge("a0", "missing", 0.8))
        directory = self.directory / "snapshot"
        write_snapshot(directory, nodes, edges)
        code, result = self.offline_main(directory, pairs)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["verification"]["reachable_pairs"], 10)
        self.assertEqual(result["quality"]["missing_endpoint_rows"], 1)

    def test_equal_cost_tie_does_not_prove_weighted_improvement(self):
        # Bidirectional unweighted search and weighted search can select
        # different equal-cost paths even when every edge has the same weight.
        rows = [("a", "i"), ("b", "g"), ("b", "h"), ("b", "j"), ("c", "g"),
                ("d", "e"), ("d", "i"), ("e", "j"), ("g", "j"), ("h", "i")]
        nodes, edges, pairs = [], [], []
        for i in range(10):
            nodes.extend(node(letter + str(i)) for letter in "abcdefghij")
            edges.extend(edge(a + str(i), b + str(i), 1.0) for a, b in rows)
            baseline_pair = pair("a" + str(i), "j" + str(i))
            baseline_pair.update(bfs_hops=4, dijkstra_hops=4)
            pairs.append(baseline_pair)
        directory = self.directory / "snapshot"
        write_snapshot(directory, nodes, edges)
        code, result = self.offline_main(directory, pairs)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["verification"]["reachable_pairs"], 10)
        self.assertGreater(result["verification"]["weighted_path_differences"], 0)
        self.assertEqual(result["verification"]["weighted_cost_improved_pairs"], 0)
        for computed in result["tech_layer"][paths.PATH_KEY]["pairs"]:
            self.assertEqual(computed["bfs_cost"], computed["dijkstra_cost"])
            self.assertFalse(computed["weighted_cost_improved"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
