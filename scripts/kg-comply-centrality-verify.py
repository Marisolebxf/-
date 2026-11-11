#!/usr/bin/env python3
"""Independent T09 snapshot verification with BFS and sampled Brandes sums.

No database connection, no NetworkX centrality calls. Checks all 1500 subgraph
closeness scores and all sampled-source betweenness results, plus full rankings.
"""
import argparse
from collections import deque
import hashlib
import json
import math
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def verify(snapshot, output):
    manifest = read(snapshot / 'metadata.json')
    for info in manifest['files'].values():
        assert hashlib.sha256((snapshot / info['filename']).read_bytes()).hexdigest() == info['sha256']
    scores = read(snapshot / 'all-scores.json')
    selected = scores['subgraph_nodes']
    adjacency = {v: set() for v in selected}
    all_degrees = {}
    for line in (snapshot / 'nodes.jsonl').read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        assert row['weighted_degree'] == scores['metrics']['degree'][row['vid']]
        all_degrees[row['vid']] = 0
    for line in (snapshot / 'edges.jsonl').read_text(encoding='utf-8').splitlines():
        e = json.loads(line)
        u, v = e['src'], e['dst']
        all_degrees[u] += 1
        all_degrees[v] += 1
        if u in adjacency and v in adjacency:
            adjacency[u].add(v)
            adjacency[v].add(u)
    assert set(sorted(all_degrees, key=lambda v: (-all_degrees[v], v))[:1500]) == set(selected)
    sources = set(scores['betweenness_sources'])
    assert len(sources) == 300 and sources <= set(selected)
    between = dict.fromkeys(selected, 0.0)
    close = {}
    n = len(selected)
    for source in selected:
        distance = {source: 0}
        sigma = dict.fromkeys(selected, 0.0)
        sigma[source] = 1.0
        predecessors = {v: [] for v in selected}
        queue = deque([source])
        order = []
        while queue:
            v = queue.popleft()
            order.append(v)
            for w in adjacency[v]:
                if w not in distance:
                    distance[w] = distance[v] + 1
                    queue.append(w)
                if source in sources and distance[w] == distance[v] + 1:
                    sigma[w] += sigma[v]
                    predecessors[w].append(v)
        total = sum(distance.values())
        reached = len(distance) - 1
        close[source] = reached * reached / ((n - 1) * total) if total else 0.0
        if source in sources:
            dependency = dict.fromkeys(selected, 0.0)
            for w in reversed(order):
                for v in predecessors[w]:
                    dependency[v] += sigma[v] / sigma[w] * (1 + dependency[w])
                if w != source:
                    between[w] += dependency[w]
    factor = n / len(sources) / ((n - 1) * (n - 2))
    between = {v: score * factor for v, score in between.items()}
    close_error = max(abs(close[v] - scores['metrics']['closeness'][v]) for v in selected)
    between_error = max(abs(between[v] - scores['metrics']['betweenness'][v]) for v in selected)
    composite = read(output / 'composite.json')
    ranges = {key: (min(values[v] for v in selected), max(values[v] for v in selected)) for key, values in scores['metrics'].items()}
    for row in composite:
        parts = []
        for key, (low, high) in ranges.items():
            raw = scores['metrics'][key][row['id']]
            scaled = (raw-low)/(high-low) if high != low else 0.0
            assert raw == row['raw'][key] and abs(scaled - row['normalized'][key]) < 1e-12
            parts.append(scaled)
        assert abs(math.fsum(parts) / 4 - row['score']) < 1e-12
    assert len(composite) == 1500 and len({r['id'] for r in composite}) == 1500
    assert composite == sorted(composite, key=lambda r: (-r['score'], r['id']))
    layer = read(output / 'result.json')['tech_layer']
    for section, metric in [('428_degree_centrality','degree'),('431_pagerank','pagerank'),('429_closeness','closeness'),('430_betweenness','betweenness')]:
        values = scores['metrics'][metric]
        assert [r['id'] for r in layer[section]['top20']] == sorted(values, key=lambda v: (-values[v], v))[:20]
    assert [r['id'] for r in layer['432_multi_centrality']['top20']] == [r['id'] for r in composite[:20]]
    result = {'passed': close_error < 1e-12 and between_error < 1e-12,
              'independent_closeness_nodes': n, 'independent_betweenness_sources': len(sources),
              'closeness_max_abs_error': close_error, 'betweenness_max_abs_error': between_error,
              'composite_rows_verified': len(composite), 'rankings_verified': 5,
              'snapshot_sha256_verified': True, 'weighted_degree_all_nodes_verified': len(all_degrees),
              'result_sha256': hashlib.sha256((output / 'result.json').read_bytes()).hexdigest(),
              'composite_sha256': hashlib.sha256((output / 'composite.json').read_bytes()).hexdigest(),
              'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'implementation': 'stdlib BFS distances and Brandes dependency accumulation; no NetworkX centrality calls'}
    (output / 'independent-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))
    assert result['passed']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    verify(args.snapshot_dir, args.output_dir)
