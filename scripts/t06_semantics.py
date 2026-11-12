"""T06 read-only, Tag-anchored semantic audit; sequential bounded queries.

Credentials: GKX_GRAPH_USER / GKX_GRAPH_PASSWORD. No DDL or graph writes.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time

spec = importlib.util.spec_from_file_location('paths', Path(__file__).with_name('kg-comply-paths.py'))
io = importlib.util.module_from_spec(spec)
spec.loader.exec_module(io)


def overlap(a, b):
    intersection = len(a & b)
    return {'apply_to_unique_pairs': len(a), 'support_unique_pairs': len(b),
            'intersection': intersection, 'apply_to_only': len(a-b), 'support_only': len(b-a),
            'intersection_over_apply_to': intersection/len(a) if a else None,
            'intersection_over_support': intersection/len(b) if b else None,
            'jaccard': intersection/len(a | b) if a | b else None}


def run(output, snapshot):
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool
    output.mkdir(parents=True, exist_ok=True)
    snapshot.mkdir(parents=True, exist_ok=True)
    result = {'task': 'KG-COMPLY-LOAD-T06', 'started_at': io.utc_now(),
              'space': 'demo_gkx_chain', 'read_only': True, 'queries': [], 'status': 'running'}
    def save():
        io.write_json(output/'audit.json', result)
    def query(label, statement, sample=False):
        started = time.monotonic()
        response = session.execute(statement)
        entry = {'label': label, 'query': statement, 'seconds': round(time.monotonic()-started,3), 'success': response.is_succeeded()}
        result['queries'].append(entry)
        if not response.is_succeeded():
            entry['error'] = str(response.error_msg())
            save()
            raise RuntimeError('Query failed: '+label+' '+entry['error'])
        rows = []
        for i in range(response.row_size()):
            converted = []
            for v in response.row_values(i):
                try:
                    converted.append(io.scalar(v))
                except io.RunError:
                    converted.append(str(v))
            rows.append(converted)
        entry['row_count'] = len(rows)
        if sample:
            entry['rows'] = rows
        save()
        print(label+': '+str(len(rows))+' rows', flush=True)
        return rows
    pool = None
    session = None
    try:
        for attempt in range(4):
            pool = ConnectionPool()
            config = Config(); config.timeout = 60000; config.max_connection_pool_size = 1
            try:
                if pool.init([('10.50.75.136',9669)],config):
                    session = pool.get_session(os.environ['GKX_GRAPH_USER'],os.environ['GKX_GRAPH_PASSWORD'])
                    break
            except Exception:
                pass
            pool.close()
            time.sleep(2)
        if session is None:
            raise RuntimeError('Unable to establish graph session after four attempts')
        query('space', 'USE demo_gkx_chain;')
        groups = [('apply_to','policy'),('support','policy'),('participates','enterprise'),('participates','institution'),('belongs_to','segment')]
        counts = {}
        for edge, tag in groups:
            label = edge+'_'+tag
            counts[label] = query(label+'_groups', f'MATCH (a:{tag})-[e:{edge}]->(b) RETURN tags(a)[0] AS source_tag, tags(b)[0] AS target_tag, count(e) AS edge_count;', True)
            # All labels in templates are from the fixed allowlist above.
            query(label+'_sample20', f'MATCH (a:{tag})-[e:{edge}]->(b) RETURN id(a), id(b), tags(a)[0], tags(b)[0], rank(e), properties(a), properties(b), e.weight, e.props LIMIT 20;', True)
        result['group_counts'] = counts
        pairs = {}; attributes = {}
        for edge in ('apply_to','support'):
            records = []; offset = 0; last = None
            while True:
                rows = query(edge+'_page_'+str(offset), f'MATCH (a:policy)-[e:{edge}]->(b) RETURN id(a) AS src, id(b) AS dst, rank(e) AS edge_rank, e.weight, e.props ORDER BY src, dst, edge_rank SKIP {offset} LIMIT 1000;')
                for row in rows:
                    key = tuple(row[:3])
                    if last is not None and key <= last:
                        raise RuntimeError('Repeated or unordered identities during pagination')
                    last = key
                records.extend(rows); offset += len(rows)
                if len(rows) < 1000:
                    break
            expected = sum(r[2] for r in counts[edge+'_policy'])
            if len(records) != expected:
                raise RuntimeError('Export count differs from anchored group count')
            path = snapshot/(edge+'-pairs.json')
            io.write_json(path, records)
            pairs[edge] = {tuple(r[:2]) for r in records}
            attributes[edge] = {tuple(r[:3]): r[3:] for r in records}
            result[edge+'_export'] = {'rows': len(records), 'unique_pairs': len(pairs[edge]), 'sha256': io.sha256(path), 'rank_nonzero': sum(r[2] != 0 for r in records)}
        result['overlap'] = overlap(pairs['apply_to'],pairs['support'])
        same_keys = set(attributes['apply_to']) & set(attributes['support'])
        def parsed(value):
            if isinstance(value,str):
                try:
                    return json.loads(value)
                except ValueError:
                    pass
            return value
        result['attribute_comparison'] = {'same_src_dst_rank':len(same_keys),
            'weight_different':sum(attributes['apply_to'][k][0] != attributes['support'][k][0] for k in same_keys),
            'props_different_after_json_parse':sum(parsed(attributes['apply_to'][k][1]) != parsed(attributes['support'][k][1]) for k in same_keys),
            'weight_values':{e:sorted({str(v[0]) for v in attributes[e].values()}) for e in attributes}}
        membership = query('belongs_to_all', 'MATCH (a:segment)-[e:belongs_to]->(b) RETURN id(a), id(b), tags(b)[0], rank(e) LIMIT 10000;', True)
        segment_count = query('segment_count','MATCH (v:segment) RETURN count(v);',True)[0][0]
        result['membership'] = {'edge_rows':len(membership), 'linked_segments':len({r[0] for r in membership}), 'segment_count':segment_count, 'unlinked_segments':segment_count-len({r[0] for r in membership}), 'all_targets_chain':all(r[2]=='chain' for r in membership)}
        after = {}
        for edge,tag in groups:
            after[edge+'_'+tag] = query(edge+'_'+tag+'_postcount',f'MATCH (a:{tag})-[e:{edge}]->(b) RETURN tags(a)[0] AS source_tag, tags(b)[0] AS target_tag, count(e) AS edge_count;',True)
        result['counts_stable'] = all(sorted(counts[k]) == sorted(after[k]) for k in counts)
        result['membership']['complete'] = len(membership) == sum(r[2] for r in counts['belongs_to_segment']) and len(membership)<10000
        if not result['counts_stable'] or not result['membership']['complete']:
            raise RuntimeError('Consistency/completeness guard failed')
        result['status'] = 'passed'
    except Exception as error:
        result['status'] = 'failed'; result['error'] = str(error)
        raise
    finally:
        result['finished_at'] = io.utc_now()
        result['script_sha256'] = io.sha256(Path(__file__))
        save()
        if session is not None:
            session.release()
        if pool is not None:
            pool.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--snapshot-dir',type=Path,required=True)
    args = parser.parse_args()
    run(args.output_dir,args.snapshot_dir)
