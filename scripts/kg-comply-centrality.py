#!/usr/bin/env python3
"""T09: read-only technology graph export and reproducible centrality batch.

Uses the reviewed T08 export/validation helpers. No graph mutation statements.
Run with networkx==3.4.2, numpy, scipy, nebula3-python==3.8.3.
"""
import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import random
import sys

SPEC = importlib.util.spec_from_file_location('paths', Path(__file__).with_name('kg-comply-paths.py'))
io = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(io)
NODE_QUERY = ('MATCH (v:tech_point) RETURN id(v) AS vid, '
              'v.tech_point.name_zh AS name, v.tech_point.weighted_degree AS weighted_degree '
              'ORDER BY vid SKIP {offset} LIMIT {limit};')


def export(directory):
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool
    directory.mkdir(parents=True, exist_ok=True)
    if any(directory.glob('*.json*')):
        raise io.RunError('Choose an empty snapshot directory, or use --reuse-snapshot.')
    config = Config()
    config.timeout = 180000
    pool = ConnectionPool()
    session = None
    started = io.utc_now()
    try:
        if not pool.init([('10.50.75.136', 9669)], config):
            raise io.RunError('Graph connection failed.')
        session = pool.get_session(os.environ['GKX_GRAPH_USER'], os.environ['GKX_GRAPH_PASSWORD'])
        io.execute(session, 'USE demo_gkx_chain;')
        counts = {}
        queries = {'nodes': 'MATCH (v:tech_point) RETURN count(v);',
                   'edges': 'MATCH ()-[e:tech_rel]->() RETURN count(e);'}
        for key, query in queries.items():
            counts[key] = io.scalar(io.execute(session, query).row_values(0)[0])
        nodes = io.export_pages(session, NODE_QUERY, ('vid', 'name', 'weighted_degree'), directory / 'nodes.jsonl', 10000)
        edges = io.export_pages(session, io.EDGE_QUERY, ('src', 'dst', 'rank', 'confidence'), directory / 'edges.jsonl', 20000)
        after = {key: io.scalar(io.execute(session, query).row_values(0)[0]) for key, query in queries.items()}
        if counts != after or counts != {'nodes': nodes['rows'], 'edges': edges['rows']}:
            raise io.RunError('Source counts changed during export; discard snapshot.')
    finally:
        if session is not None:
            session.release()
        pool.close()
    for filename in ('nodes.jsonl', 'edges.jsonl'):
        (directory / (filename + '.tmp')).replace(directory / filename)
    manifest = {'format_version': 1, 'space': 'demo_gkx_chain', 'started_at': started,
                'finished_at': io.utc_now(), 'files': {'nodes': nodes, 'edges': edges},
                'counts_before': counts, 'counts_after': after,
                'consistency': 'Ordered sequential reads, count guards; not a transactional snapshot.'}
    io.write_json(directory / 'metadata.json', manifest)


def minmax(values):
    low, high = min(values.values()), max(values.values())
    return {key: (value-low)/(high-low) if high != low else 0.0 for key, value in values.items()}


def calculate(directory, output, baseline):
    import networkx as nx
    import numpy as np
    manifest = io.read_snapshot(directory)
    graph, quality = io.load_graph(directory, manifest)
    for key in ('null_confidence', 'invalid_confidence', 'missing_endpoint_rows', 'self_loop_rows', 'duplicate_undirected_pair_rows'):
        if quality[key]:
            raise io.RunError('Graph quality gate failed: ' + key)
    ids = list(graph)
    weighted = {r['vid']: r['weighted_degree'] for r in io.records(directory / 'nodes.jsonl')}
    if len(ids) < 1500 or any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) or v < 0 for v in weighted.values()):
        raise io.RunError('Invalid weighted_degree coverage or insufficient graph population.')
    degree = dict(graph.degree())
    correlation = float(np.corrcoef([degree[v] for v in ids], [weighted[v] for v in ids])[0, 1])
    io.log('Calculating full-graph confidence-weighted PageRank')
    # tol is NetworkX average-per-node stopping tolerance, not global L1 residual.
    pr = nx.pagerank(graph, alpha=0.85, tol=1e-8, max_iter=1000, weight='confidence')
    selected = sorted(ids, key=lambda v: (-degree[v], v))[:1500]
    subgraph = graph.subgraph(selected).copy()
    io.log('Calculating unweighted closeness on degree-top1500 induced subgraph')
    close = nx.closeness_centrality(subgraph, distance=None, wf_improved=True)
    io.log('Calculating unweighted betweenness, 300 sampled sources, seed=42')
    between = nx.betweenness_centrality(subgraph, k=300, normalized=True, weight=None, seed=42)
    # Only the common population has four observed scores. Never impute unsampled nodes as zero.
    metrics = {'degree': weighted, 'pagerank': pr, 'closeness': close, 'betweenness': between}
    normalized = {name: minmax({v: values[v] for v in selected}) for name, values in metrics.items()}
    composite = {v: sum(values[v] for values in normalized.values()) / 4 for v in selected}
    def top(values, field):
        return [{'id': v, 'name': graph.nodes[v]['name'], field: values[v]} for v in sorted(values, key=lambda v: (-values[v], v))[:20]]
    layer = {
        'scope': {'space': 'demo_gkx_chain', 'tech_graph': {'nodes': len(graph), 'edges': graph.number_of_edges()}, 'projection': 'undirected simple graph; all evidence levels retained'},
        '428_degree_centrality': {'source': 'tech_point.weighted_degree (SDD T09)', 'top20': top(weighted, 'weighted_degree'), 'vs_weighted_degree': {'n': len(ids), 'pearson': correlation, 'comparison': 'recomputed unweighted degree vs stored weighted_degree'}, 'recomputed_degree_top20': top(degree, 'degree')},
        '431_pagerank': {'alpha': .85, 'tol': 1e-8, 'weight': 'relation_confidence_score', 'sum': math.fsum(pr.values()), 'top20': top(pr, 'pagerank')},
        '429_closeness': {'scope': 'unweighted degree top1500 induced subgraph; VID tie break', 'subgraph': {'nodes': len(subgraph), 'edges': subgraph.number_of_edges()}, 'distance': None, 'wf_improved': True, 'top20': top(close, 'closeness')},
        '430_betweenness': {'scope': 'same induced subgraph; k=300 sampled sources', 'seed': 42, 'weight': None, 'normalized': True, 'top20': top(between, 'betweenness')},
        '432_multi_centrality': {'scope': '1500 nodes with all four measured scores; each min-max over this same population; arithmetic mean', 'top20': top(composite, 'score')},
    }
    # Independently check PageRank fixed-point equation using edge transitions.
    strengths = dict(graph.degree(weight='confidence'))
    dangling = math.fsum(pr[v] for v in ids if strengths[v] == 0)
    expected = {v: (.15 + .85 * dangling) / len(ids) for v in ids}
    for u, v, data in graph.edges(data=True):
        expected[v] += .85 * pr[u] * data['confidence'] / strengths[u]
        expected[u] += .85 * pr[v] * data['confidence'] / strengths[v]
    residual = math.fsum(abs(pr[v] - expected[v]) for v in ids)
    checks = {'confidence_null_rate_zero': quality['null_confidence_rate'] == 0,
              'pearson_at_least_095': math.isfinite(correlation) and correlation >= .95,
              'pagerank_sum_one': abs(math.fsum(pr.values()) - 1) < 1e-12,
              'pagerank_fixed_point_l1': residual < len(ids) * 1e-8,
              'degree_handshake': sum(degree.values()) == 2 * graph.number_of_edges(),
              'four_top20_and_composite': all(len(layer[key]['top20']) == 20 for key in layer if 'top20' in layer[key]),
              'finite_nonnegative_scores': all(math.isfinite(v) and v >= 0 for values in [*metrics.values(), composite] for v in values.values())}
    original = json.loads(baseline.read_text(encoding='utf-8-sig'))['tech_layer']
    comparison = {}
    for key, data in layer.items():
        if 'top20' in data and key in original:
            old = original[key]['top20']
            comparison[key] = {'top20_overlap': len({v['id'] for v in old} & {v['id'] for v in data['top20']}), 'note': 'Descriptive comparison only: stored weighted_degree and explicit composite scope differ from legacy degree output; legacy seed/tie ordering not recorded.'}
    output.mkdir(parents=True, exist_ok=True)
    io.write_json(output / 'snapshot-metadata.json', manifest)
    io.write_json(output / 'verification.json', {'passed': all(checks.values()), 'checks': checks, 'quality': quality, 'degree_weighted_degree_pearson': correlation, 'pagerank_fixed_point_l1_residual': residual, 'baseline_comparison': comparison})
    io.write_json(output / 'result.json', {'task': 'KG-COMPLY-LOAD-T09', 'generated_at': io.utc_now(), 'mode': 'read-only export; local calculation; no graph writes', 'versions': {p: io.package_version(p) for p in ('networkx', 'numpy', 'scipy', 'nebula3-python')}, 'script_sha256': io.sha256(Path(__file__)), 'helper_sha256': io.sha256(Path(io.__file__)), 'tech_layer': layer})
    io.write_json(output / 'composite.json', [{'id': v, 'name': graph.nodes[v]['name'], 'score': composite[v], 'raw': {k: d[v] for k, d in metrics.items()}, 'normalized': {k: d[v] for k, d in normalized.items()}} for v in sorted(selected, key=lambda v: (-composite[v], v))])
    io.write_json(directory / 'all-scores.json', {'metrics': metrics, 'subgraph_nodes': list(subgraph), 'betweenness_sources': random.Random(42).sample(list(subgraph), 300)})
    io.log(json.dumps({'passed': all(checks.values()), 'nodes': len(graph), 'edges': graph.number_of_edges(), 'pearson': correlation, 'pagerank_sum': math.fsum(pr.values())}))
    if not all(checks.values()):
        raise io.RunError('Acceptance verification failed; inspect verification.json.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--snapshot-dir', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--baseline', type=Path, required=True)
    p.add_argument('--reuse-snapshot', action='store_true')
    args = p.parse_args()
    if not args.reuse_snapshot:
        export(args.snapshot_dir)
    calculate(args.snapshot_dir, args.output_dir, args.baseline)


if __name__ == '__main__':
    try:
        main()
    except io.RunError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
