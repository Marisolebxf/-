"""T09-S1 offline supplement on the original, hash-verified T09 snapshot.

No database connections. Never overwrite the signed T09 artifacts.
Independent verification uses SQLite directed endpoint aggregation.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sqlite3

spec = importlib.util.spec_from_file_location('centrality',Path(__file__).with_name('kg-comply-centrality.py'))
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
io = base.io
ANCHOR = 'tech_point:tcn_33d9f4526b23543c77260989ff4439ac'


def run(snapshot, original, output):
    if output.resolve() == original.resolve() or original.resolve() in output.resolve().parents:
        raise ValueError('Use a separate supplement directory outside signed T09.')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output must be empty; preserve prior runs.')
    preserved = {p.name:io.sha256(p) for p in original.iterdir() if p.is_file()}
    manifest = io.read_snapshot(snapshot)
    signed_manifest = json.loads((original/'snapshot-metadata.json').read_text(encoding='utf-8'))
    assert manifest == signed_manifest, 'Snapshot is not the signed T09 snapshot'
    graph, quality = io.load_graph(snapshot, manifest)
    assert all(quality[k] == 0 for k in ('null_confidence','invalid_confidence','missing_endpoint_rows','self_loop_rows','duplicate_undirected_pair_rows'))
    old = json.loads((original/'composite.json').read_text(encoding='utf-8'))
    ids = [r['id'] for r in old]
    assert len(ids) == len(set(ids)) == 1500
    assert set(ids) <= set(graph)
    degree = dict(graph.degree())  # exact same function/projection as signed T09
    weighted = {v: math.fsum(d['confidence']/100 for d in graph[v].values()) for v in graph}
    baseline = json.loads((original/'result.json').read_text(encoding='utf-8'))
    rank_ids = sorted(graph, key=lambda v:(-degree[v],v))
    assert set(rank_ids[:1500]) == set(ids)
    prior_top = baseline['tech_layer']['428_degree_centrality']['recomputed_degree_top20']
    assert [(r['id'],r['degree']) for r in prior_top] == [(v,degree[v]) for v in rank_ids[:20]]
    # Independent method: aggregate original directed rows separately by dst and src.
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE edges(src TEXT,dst TEXT,rnk INTEGER,confidence REAL,PRIMARY KEY(src,dst,rnk))')
    db.executemany('INSERT INTO edges VALUES (?,?,?,?)',((r['src'],r['dst'],r['rank'],r['confidence']) for r in io.records(snapshot/'edges.jsonl')))
    incoming = {r[0]:(r[1],r[2]) for r in db.execute('SELECT dst,count(*),sum(confidence)/100.0 FROM edges GROUP BY dst')}
    outgoing = {r[0]:(r[1],r[2]) for r in db.execute('SELECT src,count(*),sum(confidence)/100.0 FROM edges GROUP BY src')}
    error = 0.0
    for v in graph:
        inc,iw = incoming.get(v,(0,0.0)); out,ow = outgoing.get(v,(0,0.0))
        assert degree[v] == inc+out
        error = max(error,abs(weighted[v]-iw-ow))
    edge_total = db.execute('SELECT count(*),sum(confidence)/100.0 FROM edges').fetchone()
    assert error < 1e-8 and sum(degree.values()) == 2*edge_total[0]
    assert math.isclose(math.fsum(weighted.values()),2*edge_total[1],rel_tol=1e-12,abs_tol=1e-7)
    assert degree[ANCHOR] == 2914 and round(weighted[ANCHOR],2) == 1478.05
    assert incoming[ANCHOR][0] == 2347 and outgoing[ANCHOR][0] == 567
    source = {'space':'demo_gkx_chain','snapshot_started_at':manifest['started_at'],'snapshot_finished_at':manifest['finished_at'],
              'nodes_sha256':manifest['files']['nodes']['sha256'],'edges_sha256':manifest['files']['edges']['sha256'],
              'method':'Recomputed from original T09 tech_rel snapshot, not stored tech_point.weighted_degree'}
    scope = {'graph_nodes':len(graph),'graph_edges':graph.number_of_edges(),'edge_scope':'full tech_rel graph, all evidence levels',
             'direction':'both incoming and outgoing incident edges; undirected simple projection as T09',
             'sampling':'none for degree; 1500 population is the unchanged T09 composite population',
             'tie_break':'score descending, VID ascending','freshness':'original T09 snapshot; not a new live export'}
    def rows(values,population,field):
        return [{'rank':i+1,'id':v,'name':graph.nodes[v]['name'],field:values[v]} for i,v in enumerate(sorted(population,key=lambda v:(-values[v],v)))]
    def payload(key,values,population,field,formula):
        return {'task':'KG-COMPLY-LOAD-T09-S1','section':key,'metric_source':dict(source,formula=formula),
                'scope':dict(scope,population_count=len(population)),'rows':rows(values,population,field)}
    output.mkdir(parents=True,exist_ok=True)
    io.write_json(output/'degree-1500.json',payload('428_degree_centrality_recomputed_1500',degree,ids,'degree','count incident edges in full undirected simple graph'))
    io.write_json(output/'degree-full.json',payload('428_degree_centrality_recomputed_full',degree,graph,'degree','count incident edges in full undirected simple graph'))
    io.write_json(output/'weighted-degree-full.json',payload('weighted_degree_recomputed_rank',weighted,graph,'weighted_degree_recomputed','sum(confidence/100) over incoming + outgoing incident edges'))
    # Supplementary revised composite; keep original 429/430/431 raw values verbatim.
    metrics = {key:{r['id']:r['raw'][key] for r in old} for key in old[0]['raw']}
    metrics['degree'] = {v:degree[v] for v in ids}
    normalized = {key:base.minmax(values) for key,values in metrics.items()}
    combined = {v:math.fsum(values[v] for values in normalized.values())/4 for v in ids}
    revised = rows(combined,ids,'score')
    for r in revised:
        v=r['id'];r['raw']={k:d[v] for k,d in metrics.items()};r['normalized']={k:d[v] for k,d in normalized.items()}
    for key,values in metrics.items():
        lo=min(values.values()); hi=max(values.values())
        for r in revised:
            expected=(values[r['id']]-lo)/(hi-lo) if hi!=lo else 0.0
            assert abs(r['normalized'][key]-expected)<1e-12
    assert all(abs(r['score']-sum(r['normalized'].values())/4)<1e-12 for r in revised)
    io.write_json(output/'composite-recomputed.json',{'task':'KG-COMPLY-LOAD-T09-S1','metric_source':dict(source,formula='min-max each metric on same 1500 VIDs, equal 0.25 mean; degree replaced with full-graph unweighted degree'),
        'scope':dict(scope,population_count=1500,other_metrics='original T09 closeness/betweenness on 1500 subgraph, betweenness 300 sampled sources; PageRank full graph unchanged'),'rows':revised})
    assert preserved == {p.name:io.sha256(p) for p in original.iterdir() if p.is_file()}
    result = {'passed':True,'at':io.utc_now(),'snapshot_matches_signed_manifest':True,'signed_artifacts_unchanged':preserved,
        'population_1500_identical':True,'prior_recomputed_top20_identical':True,'independent_sql_all_nodes_checked':len(graph),
        'sql_weight_max_abs_error':error,'unweighted_degree_handshake':True,'weighted_degree_handshake':True,
        'sum_unweighted_degree':sum(degree.values()),'sum_weighted_degree':math.fsum(weighted.values()),'sum_edge_confidence_div100':edge_total[1],
        'anchor':{'id':ANCHOR,'degree':degree[ANCHOR],'weighted_degree':weighted[ANCHOR],'incoming':incoming[ANCHOR],'outgoing':outgoing[ANCHOR]},
        'direction_note':'Task card says incoming in some places; only incoming gives 2347 and ~1177.65, not required 2914/1478.05. Uses incident=incoming+outgoing per signed acceptance appendix and original T09 algorithm; request reviewer confirmation of wording.',
        'revised_composite_formula_verified':True,'outputs':{p.name:io.sha256(p) for p in output.glob('*.json')},'script_sha256':io.sha256(Path(__file__))}
    io.write_json(output/'verification.json',result)
    print(json.dumps({k:result[k] for k in ('passed','independent_sql_all_nodes_checked','sql_weight_max_abs_error','anchor')},ensure_ascii=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--snapshot-dir',type=Path,required=True)
    p.add_argument('--original-dir',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args();run(a.snapshot_dir,a.original_dir,a.output_dir)
