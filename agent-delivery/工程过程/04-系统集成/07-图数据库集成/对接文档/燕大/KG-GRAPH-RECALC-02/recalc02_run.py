"""KG-GRAPH-RECALC-02 offline recalculation and diff on the 2026-11-18 snapshot.

Read-only: no database access here. The snapshot (.local/kg-recalc02-20261118,
19,430 nodes / 587,252 edge rows, after KG-GRAPH-COVER-01) is hash-verified via
the shared T08/T09 io helpers. Algorithms reuse the signed T09/T09-S1/T10
recipes verbatim: undirected simple projection, incident (in+out) weighted
degree sum(confidence/100), PageRank alpha=0.85 tol=1e-8 weighted by
confidence, degree-top1500 induced subgraph for unweighted closeness
(wf_improved) and k=300 seeded betweenness, composite = per-population min-max
then equal 0.25 mean, Louvain python-louvain seed 42 resolution 8.0 unweighted.
Never writes T09-S1/T09/T10 archives; only adds files under this directory.
"""
import importlib.util
import json
import math
import random
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
INT = OUT.parents[2]                      # 07-图数据库集成
REPO = OUT.parents[6]                     # gkx-orchestration root
SNAP = REPO / '.local' / 'kg-recalc02-20261118'
T09S1 = INT / '对接文档' / '燕大' / 'T09-S1'
T09D = INT / '对接文档' / '燕大' / 'T09'
T10OUT = INT / 'KG-COMPLY-LOAD-T10-交付-20261112' / 'out'
ANCHOR = 'tech_point:tcn_33d9f4526b23543c77260989ff4439ac'
OLD_ROWS = 541428                         # signed T09/T10 edge row count
OLD_FORMED = 180                          # signed T10 formed (>=2) communities
OLD_MODULARITY = 0.2786                   # signed T10 modularity (nx, resolution=1 readout)

spec = importlib.util.spec_from_file_location('centrality', REPO / 'scripts' / 'kg-comply-centrality.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
io = base.io


def log(message):
    print(message, file=sys.stderr, flush=True)


def preserved_hashes():
    snapshot = {}
    for directory in (T09S1, T09D, T10OUT):
        for path in sorted(directory.glob('*.json*')):
            snapshot[str(path.relative_to(REPO))] = io.sha256(path)
    return snapshot


def load_old():
    old_degree = {r['id']: r['degree'] for r in json.loads((T09S1 / 'degree-full.json').read_text(encoding='utf-8'))['rows']}
    old_weighted = {r['id']: r['weighted_degree_recomputed'] for r in json.loads((T09S1 / 'weighted-degree-full.json').read_text(encoding='utf-8'))['rows']}
    old_comp = json.loads((T09S1 / 'composite-recomputed.json').read_text(encoding='utf-8'))['rows']
    old_comp_rows = {r['id']: r for r in old_comp}
    t10 = json.loads((T10OUT / 't10_full_s42_r8.0_all.json').read_text(encoding='utf-8'))
    return old_degree, old_weighted, old_comp_rows, t10


def main():
    import networkx as nx
    import community as community_louvain

    if any(OUT.glob('*.json')):
        raise io.RunError('Output directory already holds results; refusing to overwrite.')
    before = preserved_hashes()

    manifest = io.read_snapshot(SNAP)
    graph, quality = io.load_graph(SNAP, manifest)
    for key in ('null_confidence', 'invalid_confidence', 'missing_endpoint_rows', 'self_loop_rows'):
        if quality[key]:
            raise io.RunError('Quality gate failed: {}={}'.format(key, quality[key]))
    duplicate_rows = quality['duplicate_undirected_pair_rows']
    rows = quality['exported_edge_rows']
    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()
    log('graph: {} nodes, {} edge rows, {} unique undirected pairs, {} duplicate pair rows'.format(nodes, rows, edges, duplicate_rows))

    # ---- degree / weighted degree (signed T09-S1 recipe) ----
    degree = dict(graph.degree())
    weighted = {v: math.fsum(d['confidence'] / 100 for d in graph[v].values()) for v in graph}
    edge_conf_sum = math.fsum(d['confidence'] / 100 for _, _, d in graph.edges(data=True))

    # independent SQLite check on unique unordered pairs (keep-max confidence, same as load_graph)
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE edges(src TEXT,dst TEXT,rnk INTEGER,confidence REAL,PRIMARY KEY(src,dst,rnk))')
    db.executemany('INSERT INTO edges VALUES (?,?,?,?)',
                   ((r['src'], r['dst'], r['rank'], r['confidence']) for r in io.records(SNAP / 'edges.jsonl')))
    db.execute('CREATE TABLE pairs(a TEXT,b TEXT,conf REAL,PRIMARY KEY(a,b))')
    db.executemany('INSERT INTO pairs(a,b,conf) VALUES (?,?,?) ON CONFLICT(a,b) DO UPDATE SET conf=max(conf,excluded.conf)',
                   ((min(r[0], r[1]), max(r[0], r[1]), r[3]) for r in db.execute('SELECT src,dst,rnk,confidence FROM edges')))
    pair_degree = {r[0]: r[1] for r in db.execute(
        'SELECT n,count(*) FROM (SELECT a AS n FROM pairs UNION ALL SELECT b FROM pairs) GROUP BY n')}
    pair_weight = {r[0]: r[1] for r in db.execute(
        'SELECT n,sum(conf)/100.0 FROM (SELECT a AS n,conf FROM pairs UNION ALL SELECT b AS n,conf FROM pairs) GROUP BY n')}
    weight_error = 0.0
    for v in graph:
        assert degree[v] == pair_degree.get(v, 0), v
        weight_error = max(weight_error, abs(weighted[v] - pair_weight.get(v, 0.0)))
    assert len(db.execute('SELECT * FROM pairs').fetchall()) == edges
    incoming = {r[0]: r[1] for r in db.execute('SELECT dst,count(*) FROM edges GROUP BY dst')}
    outgoing = {r[0]: r[1] for r in db.execute('SELECT src,count(*) FROM edges GROUP BY src')}
    log('independent pair check passed, weight max abs error {:.3e}'.format(weight_error))

    # ---- PageRank full board (signed T09 recipe) ----
    log('PageRank full graph, confidence weighted')
    pr = nx.pagerank(graph, alpha=0.85, tol=1e-8, max_iter=1000, weight='confidence')
    strengths = dict(graph.degree(weight='confidence'))
    dangling = math.fsum(pr[v] for v in graph if strengths[v] == 0)
    expected = {v: (0.15 + 0.85 * dangling) / nodes for v in graph}
    for u, v, data in graph.edges(data=True):
        expected[v] += 0.85 * pr[u] * data['confidence'] / strengths[u]
        expected[u] += 0.85 * pr[v] * data['confidence'] / strengths[v]
    pr_residual = math.fsum(abs(pr[v] - expected[v]) for v in graph)

    # ---- degree-top1500 induced subgraph: closeness / betweenness (signed T09 recipe) ----
    selected = sorted(graph, key=lambda v: (-degree[v], v))[:1500]
    subgraph = graph.subgraph(selected).copy()
    log('closeness on degree-top1500 induced subgraph ({} nodes / {} edges)'.format(subgraph.number_of_nodes(), subgraph.number_of_edges()))
    close = nx.closeness_centrality(subgraph, distance=None, wf_improved=True)
    log('betweenness k=300 sampled sources, seed=42')
    between = nx.betweenness_centrality(subgraph, k=300, normalized=True, weight=None, seed=42)

    # ---- composite 432: all four metrics freshly recomputed on the new population ----
    metrics = {'degree': degree, 'pagerank': pr, 'closeness': close, 'betweenness': between}
    normalized = {key: base.minmax({v: values[v] for v in selected}) for key, values in metrics.items()}
    composite = {v: math.fsum(values[v] for values in normalized.values()) / 4 for v in selected}
    comp_order = sorted(selected, key=lambda v: (-composite[v], v))
    for key, values in metrics.items():
        lo, hi = min(values[v] for v in selected), max(values[v] for v in selected)
        for v in selected:
            expect = (values[v] - lo) / (hi - lo) if hi != lo else 0.0
            assert abs(normalized[key][v] - expect) < 1e-12
    assert all(abs(composite[v] - math.fsum(normalized[k][v] for k in normalized) / 4) < 1e-12 for v in selected)
    assert all(comp_order[i] == comp_order[i - 1] or composite[comp_order[i]] <= composite[comp_order[i - 1]] for i in range(1, 1500))

    # ---- Louvain communities (signed T10 recipe: python-louvain, seed 42, resolution 8.0, unweighted) ----
    log('Louvain python-louvain seed=42 resolution=8.0 unweighted')
    random.seed(42)
    part = community_louvain.best_partition(graph, resolution=8.0, random_state=42)
    assert len(part) == nodes
    comm_members = defaultdict(list)
    for v, c in part.items():
        comm_members[c].append(v)
    modularity = nx.community.modularity(graph, [set(members) for members in comm_members.values()])
    sizes_sorted = sorted((len(m) for m in comm_members.values()), reverse=True)
    formed = {c: m for c, m in comm_members.items() if len(m) >= 2}
    singles = {c: m for c, m in comm_members.items() if len(m) == 1}
    log('communities: {} total, {} formed(>=2), {} singletons, modularity(nx,r=1 readout)={:.4f}'.format(
        len(comm_members), len(formed), len(singles), modularity))

    # ---- 435/437 community summary (signed T10 revision: unordered (min,max) pair dedup) ----
    summary_rows = []
    for c, members in comm_members.items():
        mset = set(members)
        pairs = set()
        for v in members:
            for nb in graph.neighbors(v):
                if nb in mset:
                    pairs.add((v, nb) if v < nb else (nb, v))
        inner_e = len(pairs)
        core = sorted(members, key=lambda v: (-degree[v], v))[:5]
        summary_rows.append({
            'community_id': c, 'size': len(members), 'inner_edges': inner_e,
            'avg_degree': round(2 * inner_e / len(members), 2) if len(members) >= 2 else 0,
            'density': round(2 * inner_e / (len(members) * (len(members) - 1)), 6) if len(members) >= 2 else None,
            'core_points': core, 'core_degree': [degree[v] for v in core]})
    summary_rows.sort(key=lambda r: (-r['size'], r['community_id']))
    assert sum(r['size'] for r in summary_rows) == nodes

    # ---- community_id check (range 4): in-graph values are authoritative ----
    cid_manifest = json.loads((SNAP / 'community-ids-metadata.json').read_text(encoding='utf-8'))
    graph_cid = {r['vid']: r['community_id'] for r in io.records(SNAP / 'community-ids.jsonl')}
    assert len(graph_cid) == cid_manifest['rows'] == nodes
    graph_groups = defaultdict(set)
    for v, c in graph_cid.items():
        graph_groups[str(c)].add(v)
    old_t10_part = None

    def contingency(rows_a, rows_b):
        pairs = defaultdict(int)
        for v in rows_a:
            pairs[(str(rows_a[v]), str(rows_b[v]))] += 1
        return pairs

    def match_report(a, b):
        pairs = contingency(a, b)
        na, nb = len({str(x) for x in a.values()}), len({str(x) for x in b.values()})
        dominant_b, moved = {}, 0
        for ga in {str(x) for x in a.values()}:
            share = defaultdict(int)
            for (x, y), n in pairs.items():
                if x == ga:
                    share[y] = n
            size = sum(share.values())
            top_b, kept = max(share.items(), key=lambda kv: kv[1]) if share else (None, 0)
            dominant_b[ga] = {'size': size, 'dominant_other': top_b, 'retained': kept, 'moved_out': size - kept}
            moved += size - kept
        return {'groups_a': na, 'groups_b': nb, 'cross_pairs': len(pairs),
                'identical_up_to_relabel': len(pairs) == na == nb, 'moved_nodes_total': moved,
                'by_a': dominant_b}

    vs_old_t10 = match_report(graph_cid, json.loads((T10OUT / 't10_full_s42_r8.0_all.json').read_text(encoding='utf-8'))['partition'])
    vs_recalc = match_report(graph_cid, part)
    log('community_id: graph groups={}, recalc groups={}, identical_to_T10_delivery={}, moved_vs_recalc={}'.format(
        len(graph_groups), len(comm_members), vs_old_t10['identical_up_to_relabel'], vs_recalc['moved_nodes_total']))

    # ---- diffs vs signed T09-S1 / T10 ----
    old_degree, old_weighted, old_comp, old_t10 = load_old()
    assert set(old_degree) == set(graph.nodes()) and set(old_t10['partition']) == set(graph.nodes())
    delta_degree = {v: degree[v] - old_degree[v] for v in graph}
    delta_weighted = {v: weighted[v] - old_weighted[v] for v in graph}
    affected = sum(1 for v in graph if delta_degree[v])
    delta_pairs = edges - OLD_ROWS
    assert sum(delta_degree.values()) == 2 * delta_pairs
    assert math.isclose(math.fsum(delta_weighted.values()), 2 * (edge_conf_sum - 260019.52069059), rel_tol=1e-9, abs_tol=1e-6)
    log('edge delta: +{} rows -> +{} unique pairs; {} nodes changed degree; sum(delta_degree)={}'.format(
        rows - OLD_ROWS, delta_pairs, affected, sum(delta_degree.values())))

    def board(values, field, population, section, formula, sampling):
        source = {'space': 'demo_gkx_chain', 'snapshot_started_at': manifest['started_at'],
                  'snapshot_finished_at': manifest['finished_at'],
                  'nodes_sha256': manifest['files']['nodes']['sha256'],
                  'edges_sha256': manifest['files']['edges']['sha256'],
                  'method': 'Recomputed offline from the 2026-11-18 snapshot (post KG-GRAPH-COVER-01, +45,824 tech_rel rows)',
                  'formula': formula}
        scope = {'graph_nodes': nodes, 'graph_edges': edges, 'edge_scope': 'full tech_rel graph, all evidence levels',
                 'direction': 'undirected simple projection; incident = incoming + outgoing as T09-S1',
                 'sampling': sampling, 'tie_break': 'score descending, VID ascending',
                 'freshness': 'new live export 2026-11-18 after KG-GRAPH-COVER-01', 'population_count': len(population)}
        ordered = sorted(population, key=lambda v: (-values[v], v))
        return {'task': 'KG-GRAPH-RECALC-02', 'section': section, 'metric_source': source, 'scope': scope,
                'rows': [{'rank': i + 1, 'id': v, 'name': graph.nodes[v]['name'], field: values[v]}
                         for i, v in enumerate(ordered)]}

    io.write_json(OUT / 'degree-full.json', board(degree, 'degree', list(graph), '428_degree_centrality_recalculated_full',
                                                  'count incident edges in full undirected simple graph', 'none; full 19,430 population'))
    io.write_json(OUT / 'weighted-degree-full.json', board(weighted, 'weighted_degree_recomputed', list(graph), 'platform_weighted_degree_recalculated_full',
                                                           'sum(confidence/100) over incoming + outgoing incident edges', 'none; full 19,430 population'))
    io.write_json(OUT / 'degree-1500.json', board(degree, 'degree', selected, '428_degree_centrality_recalculated_1500',
                                                  'count incident edges in full undirected simple graph', 'top-1500 by full-graph unweighted degree, VID tie break'))
    io.write_json(OUT / 'pagerank-full.json', board(pr, 'pagerank', list(graph), '431_pagerank_recalculated_full',
                                                     'networkx pagerank alpha=0.85 tol=1e-8 max_iter=1000 weight=confidence', 'none; full 19,430 population'))
    io.write_json(OUT / 'closeness-1500.json', board(close, 'closeness', selected, '429_closeness_recalculated_1500',
                                                      'unweighted closeness wf_improved=True on degree-top1500 induced subgraph', 'population = new degree-top1500 induced subgraph'))
    io.write_json(OUT / 'betweenness-1500.json', board(between, 'betweenness', selected, '430_betweenness_recalculated_1500',
                                                        'unweighted normalized betweenness, k=300 sampled sources, seed=42, degree-top1500 induced subgraph',
                                                        'k=300 sampled sources seed=42; population = new degree-top1500 induced subgraph'))
    composite_rows = []
    for i, v in enumerate(comp_order):
        composite_rows.append({'rank': i + 1, 'id': v, 'name': graph.nodes[v]['name'], 'score': composite[v],
                               'raw': {k: metrics[k][v] for k in metrics}, 'normalized': {k: normalized[k][v] for k in normalized}})
    io.write_json(OUT / 'composite-recomputed.json', {
        'task': 'KG-GRAPH-RECALC-02',
        'metric_source': {'space': 'demo_gkx_chain', 'snapshot_started_at': manifest['started_at'],
                          'snapshot_finished_at': manifest['finished_at'],
                          'nodes_sha256': manifest['files']['nodes']['sha256'], 'edges_sha256': manifest['files']['edges']['sha256'],
                          'method': 'All four metrics freshly recomputed on the 2026-11-18 snapshot; population = new degree-top1500',
                          'formula': 'min-max each metric on the same new 1500 VIDs, equal 0.25 mean; degree = full-graph unweighted degree'},
        'scope': {'graph_nodes': nodes, 'graph_edges': edges, 'edge_scope': 'full tech_rel graph, all evidence levels',
                  'direction': 'undirected simple projection as T09', 'sampling': 'closeness/betweenness on new degree-top1500 induced subgraph, betweenness k=300 seed=42',
                  'tie_break': 'score descending, VID ascending', 'freshness': 'new live export 2026-11-18 after KG-GRAPH-COVER-01',
                  'population_count': 1500,
                  'difference_from_T09-S1': 'T09-S1 kept original 429/430/431 raw values and only replaced degree; this run recomputes all four metrics on the new edge set'},
        'rows': composite_rows})

    partition_doc = {'task': 'KG-GRAPH-RECALC-02', 'tag': 'recalc02_full_s42_r8.0_all',
                     'timestamp': io.utc_now(),
                     'params': {'mode': 'full', 'seed': 42, 'resolution': 8.0, 'evidence': 'all', 'weight': 'none'},
                     'input': {'points_read': nodes, 'edges_raw': rows, 'graph_nodes': nodes, 'graph_edges': edges,
                               'edges_dropped_by_evidence': 0,
                               'snapshot': {'nodes_sha256': manifest['files']['nodes']['sha256'],
                                          'edges_sha256': manifest['files']['edges']['sha256']}},
                     'result': {'communities': len(comm_members), 'modularity': round(modularity, 4),
                                'largest_sizes_top10': sizes_sorted[:10], 'singleton_communities': len(singles),
                                'formed_communities': len(formed),
                                'formed_change_vs_signed_T10': len(formed) - OLD_FORMED,
                                'within_10pct_of_signed': abs(len(formed) - OLD_FORMED) <= 0.1 * OLD_FORMED},
                     'partition': part}
    io.write_json(OUT / 'community-partition.json', partition_doc)
    io.write_json(OUT / 'community-summary.json', {
        'task': 'KG-GRAPH-RECALC-02', 'params': partition_doc['params'],
        'input': partition_doc['input'], 'result': partition_doc['result'],
        'formula': {'inner_edges': 'unordered (min,max) endpoint pair dedup within community',
                    'avg_degree': '2E/N rounded 2 (signed T10 revision)', 'density': '2E/(N(N-1)) rounded 6; null for singletons (437 contract)',
                    'core_points': 'top5 members by full-graph unweighted degree, VID tie break'},
        'rows': summary_rows})
    io.write_json(OUT / 'community-id-check.json', {
        'task': 'KG-GRAPH-RECALC-02',
        'policy': 'in-graph tech_point.community_id (backfilled by KG-GRAPH-COVER-01) is authoritative; recalc partition is the refresh candidate; mismatch count recorded',
        'graph_values': {'rows': cid_manifest['rows'], 'distinct_groups': len(graph_groups),
                         'formed_groups': sum(1 for m in graph_groups.values() if len(m) >= 2),
                         'singleton_groups': sum(1 for m in graph_groups.values() if len(m) == 1)},
        'graph_vs_signed_T10_partition': vs_old_t10,
        'graph_vs_recalc_partition': {k: (v if k != 'by_a' else dict(sorted(v.items(), key=lambda kv: -kv[1]['moved_out'])[:50]))
                                      for k, v in vs_recalc.items()},
        'graph_values_sample': {v: graph_cid[v] for v in sorted(graph_cid)[:3]}})

    # four diff tables
    def change_rows(new_values, old_values, field, limit=20):
        shared = [v for v in new_values if v in old_values]
        rows_ = []
        for v in sorted(shared, key=lambda v: (-abs(new_values[v] - old_values[v]), v))[:limit]:
            rows_.append({'id': v, 'name': graph.nodes[v]['name'], 'old': old_values[v], 'new': new_values[v],
                          'delta': new_values[v] - old_values[v], 'delta_degree_pairs': delta_degree[v],
                          'delta_weighted': round(delta_weighted[v], 4)})
        return rows_

    old_pr = {v: r['raw']['pagerank'] for v, r in old_comp.items()}
    old_close = {v: r['raw']['closeness'] for v, r in old_comp.items()}
    old_between = {v: r['raw']['betweenness'] for v, r in old_comp.items()}
    old_score = {v: r['score'] for v, r in old_comp.items()}
    overlap = sorted(set(old_comp) & set(selected))

    def move_rows(new_values, old_values, field, limit=20):
        old_rank = {v: i + 1 for i, v in enumerate(sorted(old_values, key=lambda v: (-old_values[v], v)))}
        new_rank = {v: i + 1 for i, v in enumerate(sorted(new_values, key=lambda v: (-new_values[v], v)))}
        shared = [v for v in new_values if v in old_values]
        rows_ = []
        for v in sorted(shared, key=lambda v: (-abs(new_rank[v] - old_rank[v]), v))[:limit]:
            rows_.append({'id': v, 'name': graph.nodes[v]['name'], 'old_rank': old_rank[v], 'new_rank': new_rank[v],
                          'rank_move': new_rank[v] - old_rank[v], 'old_value': old_values[v], 'new_value': new_values[v],
                          'delta_degree_pairs': delta_degree[v]})
        return rows_

    pr_in_old_pop = {v: pr[v] for v in old_comp}
    diff = {
        'task': 'KG-GRAPH-RECALC-02',
        'baseline': {'degree_full': 'T09-S1 degree-full.json (19,430)', 'weighted_full': 'T09-S1 weighted-degree-full.json',
                     'pagerank_closeness_betweenness_composite': 'T09-S1 composite-recomputed.json raw values (old 1500 population)',
                     'community': 'T10 t10_full_s42_r8.0_all.json partition + in-graph community_id'},
        'edges': {'old_rows': OLD_ROWS, 'new_rows': rows, 'rows_added': rows - OLD_ROWS,
                  'old_unique_pairs': OLD_ROWS, 'new_unique_pairs': edges, 'duplicate_pair_rows_new': duplicate_rows,
                  'unique_pairs_added': delta_pairs, 'nodes_with_degree_change': affected,
                  'identity_sum_delta_degree': sum(delta_degree.values()),
                  'identity_sum_delta_degree_equals_2x_added_pairs': sum(delta_degree.values()) == 2 * delta_pairs,
                  'sum_delta_weighted': math.fsum(delta_weighted.values())},
        'new_nodes': sorted(set(graph) - set(old_degree)),
        'removed_nodes': sorted(set(old_degree) - set(graph)),
        'population_overlap_1500': {'old_only': len(set(old_comp) - set(selected)), 'new_only': len(set(selected) - set(old_comp)),
                                    'both': len(overlap)},
        'score_change_top20': {
            'degree': change_rows(degree, old_degree, 'degree'),
            'weighted_degree': change_rows(weighted, old_weighted, 'weighted'),
            'pagerank': change_rows(pr, old_pr, 'pagerank'),
            'closeness': change_rows(close, old_close, 'closeness'),
            'betweenness': change_rows(between, old_between, 'betweenness'),
            'composite_score': change_rows(composite, old_score, 'score')},
        'rank_move_top20': {
            'degree': move_rows(degree, old_degree, 'degree'),
            'weighted_degree': move_rows(weighted, old_weighted, 'weighted'),
            'pagerank_within_old_population': move_rows(pr_in_old_pop, old_pr, 'pagerank'),
            'composite': move_rows(composite, old_score, 'score')},
        'community': {'old_formed': OLD_FORMED, 'new_formed': len(formed), 'old_singletons': old_t10['result']['singleton_communities'],
                      'new_singletons': len(singles), 'old_total': old_t10['result']['communities'], 'new_total': len(comm_members),
                      'old_modularity_readout': OLD_MODULARITY, 'new_modularity_readout': round(modularity, 4),
                      'formed_change_pct': round((len(formed) - OLD_FORMED) / OLD_FORMED * 100, 2),
                      'within_10pct': abs(len(formed) - OLD_FORMED) <= 0.1 * OLD_FORMED,
                      'moved_nodes_vs_graph_cid': vs_recalc['moved_nodes_total'],
                      'graph_cid_identical_to_signed_T10': vs_old_t10['identical_up_to_relabel']}}
    io.write_json(OUT / 'diff-summary.json', diff)
    io.write_json(OUT / 'snapshot-metadata.json', manifest)

    checks = {
        'snapshot_integrity': True,
        'quality_gates_zero': all(quality[k] == 0 for k in ('null_confidence', 'invalid_confidence', 'missing_endpoint_rows', 'self_loop_rows')),
        'pair_sql_independent_match': weight_error < 1e-8,
        'handshake_unweighted': sum(degree.values()) == 2 * edges,
        'handshake_weighted': math.isclose(math.fsum(weighted.values()), 2 * edge_conf_sum, rel_tol=1e-12, abs_tol=1e-7),
        'pagerank_sum_one': abs(math.fsum(pr.values()) - 1) < 1e-12,
        'pagerank_fixed_point_l1': pr_residual < nodes * 1e-8,
        'composite_formula_and_order': True,
        'louvain_full_coverage': len(part) == nodes,
        'community_summary_consistent': sum(r['size'] for r in summary_rows) == nodes,
        'community_id_fully_filled': len(graph_cid) == nodes,
        'node_population_unchanged': set(old_degree) == set(graph.nodes()),
        'delta_degree_identity': sum(delta_degree.values()) == 2 * delta_pairs,
        'old_archives_unchanged': before == preserved_hashes(),
    }
    io.write_json(OUT / 'verification.json', {
        'passed': all(checks.values()), 'checks': checks, 'quality': quality,
        'versions': {p: io.package_version(p) for p in ('networkx', 'numpy', 'scipy', 'python-louvain', 'nebula3-python')},
        'script_sha256': {'recalc02_run.py': io.sha256(Path(__file__)),
                          'recalc02_export_community_ids.py': io.sha256(OUT / 'recalc02_export_community_ids.py')},
        'anchor': {'id': ANCHOR, 'name': graph.nodes[ANCHOR]['name'],
                   'degree': {'old': old_degree[ANCHOR], 'new': degree[ANCHOR]},
                   'weighted': {'old': old_weighted[ANCHOR], 'new': weighted[ANCHOR]},
                   'row_incoming': incoming.get(ANCHOR, 0), 'row_outgoing': outgoing.get(ANCHOR, 0)},
        'sums': {'degree': sum(degree.values()), 'weighted': math.fsum(weighted.values()), 'edge_conf_sum_div100': edge_conf_sum},
        'outputs': {p.name: io.sha256(p) for p in sorted(OUT.glob('*.json')) if p.name != 'verification.json'},
        'preserved_archive_files': before})
    summary = {'passed': all(checks.values()), 'nodes': nodes, 'edge_rows': rows, 'unique_pairs': edges,
               'duplicate_pair_rows': duplicate_rows, 'pairs_added': delta_pairs, 'nodes_degree_changed': affected,
               'anchor': checks and {'degree': degree[ANCHOR], 'weighted': round(weighted[ANCHOR], 2)},
               'population_overlap_1500': len(overlap), 'communities_total': len(comm_members),
               'communities_formed': len(formed), 'singletons': len(singles), 'modularity': round(modularity, 4),
               'formed_change_pct': diff['community']['formed_change_pct'],
               'moved_nodes_vs_graph_cid': vs_recalc['moved_nodes_total'],
               'graph_cid_identical_to_signed_T10': vs_old_t10['identical_up_to_relabel']}
    log(json.dumps(summary, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise io.RunError('Acceptance verification failed; inspect verification.json.')


if __name__ == '__main__':
    try:
        main()
    except io.RunError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
