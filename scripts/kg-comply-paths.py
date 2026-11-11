#!/usr/bin/env python3
"""T08 read-only path reproduction against the compliance technology graph.

The cost formula chosen for this run is 1 / relation_confidence_score. The
historical report names its confidence field but does not publish its formula.
Credentials are read only from GKX_GRAPH_USER and GKX_GRAPH_PASSWORD.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib import metadata
from itertools import islice
import json
import math
import os
from pathlib import Path
import platform
import sys
from time import perf_counter


TASK_ID = "KG-COMPLY-LOAD-T08"
SPACE = "demo_gkx_chain"
PATH_KEY = "423_424_425_path"
SCRIPT_VERSION = "1.0.0"
NODE_QUERY = (
    "MATCH (v:tech_point) RETURN id(v) AS vid, "
    "v.tech_point.name_zh AS name ORDER BY vid SKIP {offset} LIMIT {limit};"
)
EDGE_QUERY = (
    "MATCH ()-[e:tech_rel]->() RETURN src(e) AS src, dst(e) AS dst, "
    "rank(e) AS edge_rank, e.relation_confidence_score AS confidence "
    "ORDER BY src, dst, edge_rank SKIP {offset} LIMIT {limit};"
)


class RunError(Exception):
    """A diagnostic safe to print without exposing connection credentials."""


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def log(message):
    print(message, file=sys.stderr, flush=True)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as target:
        json.dump(value, target, ensure_ascii=False, indent=2, allow_nan=False)
        target.write("\n")
    temporary.replace(path)


def package_version(name):
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def scalar(value):
    if value.is_empty() or value.is_null():
        return None
    if value.is_string():
        result = value.as_string()
        return result.decode("utf-8") if isinstance(result, bytes) else result
    if value.is_int():
        return value.as_int()
    if value.is_double():
        result = value.as_double()
        return result if math.isfinite(result) else str(result)
    if value.is_bool():
        return value.as_bool()
    raise RunError("The graph returned an unsupported scalar type.")


def execute(session, query):
    try:
        result = session.execute(query)
    except Exception as error:
        raise RunError("Graph request failed ({}).".format(type(error).__name__)) from None
    if not result.is_succeeded():
        raise RunError("Graph query failed with code {}.".format(result.error_code()))
    return result


def export_pages(session, query, columns, destination, page_size):
    temporary = destination.with_name(destination.name + ".tmp")
    offset = 0
    previous_key = None
    started_at = utc_now()
    with temporary.open("w", encoding="utf-8", newline="\n") as target:
        while True:
            result = execute(session, query.format(offset=offset, limit=page_size))
            count = result.row_size()
            for index in range(count):
                values = [scalar(value) for value in result.row_values(index)]
                if len(values) != len(columns):
                    raise RunError("The graph returned an unexpected column count.")
                record = dict(zip(columns, values))
                key = (record["vid"],) if "vid" in record else (
                    record["src"], record["dst"], record["rank"]
                )
                if any(value is None for value in key):
                    raise RunError("An exported graph identity contains NULL.")
                if previous_key is not None and key <= previous_key:
                    raise RunError("Export identities are repeated or out of order; discard this export.")
                previous_key = key
                target.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
            offset += count
            log("Exported {} rows into {}".format(offset, destination.name))
            if count < page_size:
                break
    return {
        "filename": destination.name,
        "rows": offset,
        "sha256": sha256(temporary),
        "bytes": temporary.stat().st_size,
        "started_at": started_at,
        "finished_at": utc_now(),
        "query_template": query,
    }


def export_snapshot(args):
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool

    user = os.environ.get("GKX_GRAPH_USER")
    password = os.environ.get("GKX_GRAPH_PASSWORD")
    if not user or not password:
        raise RunError("Set GKX_GRAPH_USER and GKX_GRAPH_PASSWORD before exporting.")
    directory = args.snapshot_dir
    directory.mkdir(parents=True, exist_ok=True)
    if any((directory / name).exists() for name in ("metadata.json", "nodes.jsonl", "edges.jsonl")):
        raise RunError("The snapshot directory already contains data; choose a fresh directory or --reuse-snapshot.")
    config = Config()
    config.max_connection_pool_size = 1
    config.timeout = args.timeout * 1000
    pool = ConnectionPool()
    session = None
    started_at = utc_now()
    try:
        try:
            initialized = pool.init([(args.host, args.port)], config)
            if not initialized:
                raise RunError("The graph connection pool could not initialize.")
            session = pool.get_session(user, password)
        except RunError:
            raise
        except Exception as error:
            raise RunError("Graph authentication/connection failed ({}).".format(type(error).__name__)) from None
        execute(session, "USE {};".format(SPACE))
        nodes = export_pages(session, NODE_QUERY, ("vid", "name"), directory / "nodes.jsonl", args.page_size)
        edges = export_pages(session, EDGE_QUERY, ("src", "dst", "rank", "confidence"), directory / "edges.jsonl", args.page_size)
    finally:
        if session is not None:
            session.release()
        pool.close()
    manifest = {
        "format_version": 1,
        "space": SPACE,
        "source": {"host": args.host, "port": args.port, "protocol": "Nebula native"},
        "started_at": started_at,
        "finished_at": utc_now(),
        "page_size": args.page_size,
        "consistency": "Ordered sequential reads; source-side transactional snapshot is not provided.",
        "files": {"nodes": nodes, "edges": edges},
    }
    for name in ("nodes.jsonl", "edges.jsonl"):
        (directory / (name + ".tmp")).replace(directory / name)
    write_json(directory / "metadata.json", manifest)
    return manifest


def read_snapshot(directory):
    with (directory / "metadata.json").open(encoding="utf-8") as source:
        manifest = json.load(source)
    if manifest.get("format_version") != 1 or manifest.get("space") != SPACE:
        raise RunError("The snapshot format or space does not match this task.")
    for category, filename in (("nodes", "nodes.jsonl"), ("edges", "edges.jsonl")):
        file_info = manifest["files"][category]
        path = directory / filename
        if file_info.get("filename") != filename or sha256(path) != file_info.get("sha256"):
            raise RunError("Snapshot integrity verification failed for {}.".format(filename))
    return manifest


def records(path):
    with path.open(encoding="utf-8") as source:
        for line in source:
            if line.strip():
                yield json.loads(line)


def load_graph(directory, manifest):
    import networkx as nx

    graph = nx.Graph()
    counts = Counter()
    scores = []
    for record in records(directory / "nodes.jsonl"):
        vid = record["vid"]
        if not isinstance(vid, str) or not vid or vid in graph:
            raise RunError("The node snapshot has an empty, invalid, or repeated VID.")
        graph.add_node(vid, name=record.get("name") or "")
        counts["exported_nodes"] += 1
    for record in records(directory / "edges.jsonl"):
        counts["exported_edge_rows"] += 1
        confidence = record.get("confidence")
        if confidence is None:
            counts["null_confidence"] += 1
            continue
        try:
            score = float(confidence)
        except (TypeError, ValueError):
            counts["invalid_confidence"] += 1
            continue
        if isinstance(confidence, bool) or not math.isfinite(score) or score <= 0:
            counts["invalid_confidence"] += 1
            continue
        cost = 1.0 / score
        if not math.isfinite(cost):
            counts["invalid_confidence"] += 1
            continue
        scores.append(score)
        source, target = record["src"], record["dst"]
        if source not in graph or target not in graph:
            counts["missing_endpoint_rows"] += 1
            continue
        if source == target:
            counts["self_loop_rows"] += 1
            continue
        if graph.has_edge(source, target):
            counts["duplicate_undirected_pair_rows"] += 1
            if score <= graph[source][target]["confidence"]:
                continue
        graph.add_edge(source, target, confidence=score, cost=cost)
    for category, key in (("nodes", "exported_nodes"), ("edges", "exported_edge_rows")):
        if counts[key] != manifest["files"][category]["rows"]:
            raise RunError("Snapshot row counts do not match the manifest.")
    quality = {key: counts[key] for key in (
        "exported_nodes", "exported_edge_rows", "null_confidence", "invalid_confidence",
        "missing_endpoint_rows", "self_loop_rows", "duplicate_undirected_pair_rows",
    )}
    quality.update({
        "graph_nodes": graph.number_of_nodes(),
        "graph_edges": graph.number_of_edges(),
        "null_confidence_rate": counts["null_confidence"] / max(counts["exported_edge_rows"], 1),
        "confidence_min": min(scores) if scores else None,
        "confidence_max": max(scores) if scores else None,
        "cost_formula": "1 / relation_confidence_score; confidence must be finite and > 0, and the resulting cost must be finite",
        "formula_status": "Explicit choice for this reproduction; the 2026-11-07 formula is not documented.",
        "duplicate_policy": "For an undirected node pair, retain the highest confidence (lowest cost).",
        "missing_endpoint_policy": "Skip the edge and count it; preserve the exported node population.",
    })
    return graph, quality


def baseline_pairs(path):
    with path.open(encoding="utf-8-sig") as source:
        baseline = json.load(source)
    pairs = baseline["tech_layer"][PATH_KEY]["pairs"]
    identities = [(pair["from"]["id"], pair["to"]["id"]) for pair in pairs]
    if len(pairs) != 10 or len(set(identities)) != 10:
        raise RunError("The baseline must contain exactly 10 distinct endpoint pairs.")
    return pairs


def path_cost(graph, path):
    return sum(graph[source][target]["cost"] for source, target in zip(path, path[1:]))


def path_names(graph, path):
    return [graph.nodes[vid]["name"] for vid in path]


def run_pair(graph, baseline, alternative_limit):
    import networkx as nx

    source, target = baseline["from"]["id"], baseline["to"]["id"]
    result = {
        "from": baseline["from"], "to": baseline["to"], "status": "empty",
        "reason": None, "bfs_hops": None, "dijkstra_hops": None,
        "bfs_ms": None, "dijkstra_ms": None, "bfs_cost": None, "dijkstra_cost": None,
        "bfs_path_ids": [], "bfs_path_names": [],
        "dijkstra_path_ids": [], "dijkstra_path_names": [], "alt_paths": [],
        "baseline_hops": {"bfs": baseline.get("bfs_hops"), "dijkstra": baseline.get("dijkstra_hops")},
    }
    if source not in graph or target not in graph:
        result["reason"] = "endpoint_missing"
        return result
    started = perf_counter()
    try:
        bfs = nx.shortest_path(graph, source, target)
    except nx.NetworkXNoPath:
        result["bfs_ms"] = round((perf_counter() - started) * 1000, 3)
        result["reason"] = "unreachable"
        return result
    result["bfs_ms"] = round((perf_counter() - started) * 1000, 3)
    started = perf_counter()
    dijkstra = nx.shortest_path(graph, source, target, weight="cost", method="dijkstra")
    result["dijkstra_ms"] = round((perf_counter() - started) * 1000, 3)
    alternatives = list(islice(nx.shortest_simple_paths(graph, source, target), alternative_limit))
    bfs_cost = path_cost(graph, bfs)
    dijkstra_cost = path_cost(graph, dijkstra)
    improvement = bfs_cost - dijkstra_cost
    improvement_tolerance = 1e-12 + 1e-9 * max(abs(bfs_cost), abs(dijkstra_cost))
    result.update({
        "status": "ok", "bfs_hops": len(bfs) - 1, "dijkstra_hops": len(dijkstra) - 1,
        "bfs_cost": bfs_cost, "dijkstra_cost": dijkstra_cost,
        "bfs_path_ids": bfs, "bfs_path_names": path_names(graph, bfs),
        "dijkstra_path_ids": dijkstra, "dijkstra_path_names": path_names(graph, dijkstra),
        "alt_paths": [{"hops": len(path) - 1, "nodes": path_names(graph, path),
                       "node_ids": path, "cost": path_cost(graph, path)} for path in alternatives],
        "alt_path_count": len(alternatives),
        "weighted_path_differs": bfs != dijkstra,
        "weighted_hops_differ": len(bfs) != len(dijkstra),
        "weighted_cost_improvement": improvement,
        "weighted_cost_improved": improvement > improvement_tolerance,
        "cost_improvement_tolerance": improvement_tolerance,
        "hops_match_baseline": {
            "bfs": len(bfs) - 1 == baseline.get("bfs_hops"),
            "dijkstra": len(dijkstra) - 1 == baseline.get("dijkstra_hops"),
        },
    })
    return result


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="10.50.75.136")
    parser.add_argument("--port", type=int, default=9669)
    parser.add_argument("--space", choices=[SPACE], default=SPACE)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--snapshot-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=os.environ.get("T08_SOURCE_REVISION"), help="Source revision recorded in the result metadata.")
    parser.add_argument("--reuse-snapshot", action="store_true", help="Verify and read the saved snapshot without connecting to the graph.")
    parser.add_argument("--page-size", type=int, default=10000)
    parser.add_argument("--timeout", type=int, default=120, help="Graph request timeout in seconds.")
    parser.add_argument("--alternatives", type=int, choices=[5], default=5)
    args = parser.parse_args()
    if args.page_size < 1 or args.timeout < 1 or not 1 <= args.port <= 65535:
        parser.error("page-size, timeout and port must be positive and valid")
    reserved = {args.baseline.resolve()}
    reserved.update((args.snapshot_dir / name).resolve() for name in (
        "metadata.json", "nodes.jsonl", "edges.jsonl",
        "metadata.json.tmp", "nodes.jsonl.tmp", "edges.jsonl.tmp",
    ))
    if args.output.resolve() in reserved:
        parser.error("output must not overwrite the baseline or snapshot files")
    return args


def main():
    args = parse_args()
    started_at = utc_now()
    pairs = baseline_pairs(args.baseline)
    manifest = read_snapshot(args.snapshot_dir) if args.reuse_snapshot else export_snapshot(args)
    graph, quality = load_graph(args.snapshot_dir, manifest)
    report = {
        "task": TASK_ID, "generated_at": utc_now(), "mode": "read_only",
        "script_version": SCRIPT_VERSION, "script_sha256": sha256(Path(__file__)),
        "source_commit": args.source_commit,
        "runtime": {"python": platform.python_version(), "networkx": package_version("networkx"),
                    "nebula3-python": package_version("nebula3-python")},
        "baseline": {"filename": args.baseline.name, "sha256": sha256(args.baseline)},
        "snapshot": manifest, "quality": quality,
        "tech_layer": {PATH_KEY: {"algorithm": "BFS / Dijkstra with reciprocal confidence cost / unweighted k shortest simple paths", "pairs": []}},
    }
    if quality["null_confidence"] or quality["invalid_confidence"] or not quality["graph_edges"]:
        report.update(status="failed", error="Graph weights contain NULL/invalid values or no usable edges.")
        write_json(args.output, report)
        raise RunError("Weight validation failed; see the output quality report.")
    results = []
    for index, pair in enumerate(pairs, 1):
        result = run_pair(graph, pair, args.alternatives)
        results.append(result)
        log("Computed pair {}/10: {}".format(index, result["status"]))
    report["tech_layer"][PATH_KEY]["pairs"] = results
    different_paths = sum(bool(pair.get("weighted_path_differs")) for pair in results)
    improved_pairs = sum(bool(pair.get("weighted_cost_improved")) for pair in results)
    missing_baseline_pairs = sum(pair.get("reason") == "endpoint_missing" for pair in results)
    baseline_differences = sum(pair.get("bfs_hops") != pair.get("dijkstra_hops") for pair in pairs)
    report["verification"] = {
        "pairs_reported": len(results),
        "reachable_pairs": sum(pair["status"] == "ok" for pair in results),
        "empty_pairs": sum(pair["status"] == "empty" for pair in results),
        "baseline_endpoint_missing_pairs": missing_baseline_pairs,
        "edge_endpoints_complete": quality["missing_endpoint_rows"] == 0,
        "weighted_path_differences": different_paths,
        "weighted_cost_improved_pairs": improved_pairs,
        "cost_improvement_tolerance": "1e-12 + 1e-9 * max(abs(bfs_cost), abs(dijkstra_cost))",
        "weighted_hop_differences": sum(bool(pair.get("weighted_hops_differ")) for pair in results),
        "baseline_json_hop_differences": baseline_differences,
        "baseline_markdown_claimed_hop_differences": 4,
        "baseline_discrepancy": "The baseline Markdown says 4 pairs differ in hops; its JSON contains {}.".format(baseline_differences),
        "fixed_pairs": True,
        "weight_null_rate_zero": quality["null_confidence_rate"] == 0,
    }
    passed = improved_pairs > 0 and missing_baseline_pairs == 0 and quality["missing_endpoint_rows"] == 0
    report["status"] = "passed" if passed else "needs_review"
    report["started_at"] = started_at
    report["finished_at"] = utc_now()
    write_json(args.output, report)
    log("Saved {} ({})".format(args.output, report["status"]))
    return 0 if passed else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RunError as error:
        log(str(error))
        sys.exit(1)
    except Exception as error:
        log("Run failed ({}); inspect the inputs and saved snapshot.".format(type(error).__name__))
        sys.exit(1)
