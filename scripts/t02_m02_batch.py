"""Bounded, resumable M02 batches. Prepare immutable plan, then inspect/apply it.

Credentials: DORIS_USER/DORIS_PASSWORD, NEBULA_USER/NEBULA_PASS.
Only writes missing rank=0 cooperate edges between existing research vertices.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
from pathlib import Path
import time

from t02_m02 import aggregate, execute, grouped, insert_query, quote


def now():
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def save(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temp, path)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''): h.update(block)
    return h.hexdigest()


def prepare(args):
    import pymysql
    folder = Path(args.plan); folder.mkdir(parents=True, exist_ok=True)
    data = folder / 'edges.jsonl'
    if data.exists() or (folder / 'manifest.json').exists():
        raise ValueError('plan exists; use a new directory, never overwrite a fixed source plan')
    if not 1 <= args.limit_pairs <= 100000:
        raise ValueError('bounded preparation requires 1..100000 canonical source pairs')
    if not args.batch.startswith('comply-') or not args.batch.endswith('-t02'):
        raise ValueError('invalid T02 batch')
    counts = Counter(); versions = set(); identities = set()
    started = now()
    conn = pymysql.connect(host=os.environ.get('DORIS_HOST', '47.93.119.170'),
        port=int(os.environ.get('DORIS_PORT', '29030')), user=os.environ['DORIS_USER'],
        password=os.environ['DORIS_PASSWORD'], database='gkx_technology_analysis_dev',
        charset='utf8mb4', connect_timeout=10, read_timeout=180,
        cursorclass=pymysql.cursors.SSDictCursor)
    try:
        with conn.cursor() as cur, data.open('x', encoding='utf-8', newline='\n') as out:
            # Avoid the global pair GROUP BY + joins: it exceeds the source's
            # 256MB query quota. Load the small profile lookup, scan one src at a time.
            cur.execute('SELECT institution_id,institution_type_id FROM ads_institution_profile')
            profiles = {}
            for r in cur:
                if r['institution_id'] in profiles: raise ValueError('duplicate profile ID')
                profiles[r['institution_id']] = r['institution_type_id']
            cur.execute('SELECT DISTINCT institution_id FROM ads_institution_collaboration_yearly '
                        'WHERE institution_id < collaborator_institution_id ORDER BY institution_id')
            source_ids = [r['institution_id'] for r in cur]
            for src in source_ids:
                if counts['source_pairs'] >= args.limit_pairs: break
                cur.execute('SELECT institution_id,collaborator_institution_id,statistics_year,'
                    'co_paper_count,collaboration_strength,data_version,identity_release_id '
                    'FROM ads_institution_collaboration_yearly '
                    'WHERE institution_id=%s AND institution_id < collaborator_institution_id '
                    'ORDER BY collaborator_institution_id,statistics_year', (src,))
                for rows in grouped(cur):
                    if counts['source_pairs'] >= args.limit_pairs: break
                    counts['source_pairs'] += 1; counts['source_rows'] += len(rows)
                    versions.update(str(r['data_version']) for r in rows)
                    identities.update(str(r['identity_release_id']) for r in rows)
                    a = profiles.get(rows[0]['institution_id'])
                    b = profiles.get(rows[0]['collaborator_institution_id'])
                    if a is None or b is None:
                        counts['missing_source_endpoint_pairs'] += 1
                        continue
                    if 'company' in (a, b):
                        counts['excluded_company_pairs'] += 1
                        continue
                    edge = aggregate(rows, args.batch)
                    out.write(json.dumps(edge, ensure_ascii=False, allow_nan=False) + '\n')
                    counts['eligible_pairs'] += 1; counts['eligible_source_rows'] += len(rows)
    finally:
        conn.close()
    manifest = dict(version=1, started_at=started, prepared_at=now(), batch=args.batch,
                    limit_pairs=args.limit_pairs, counters=dict(counts), space='demo_gkx_chain',
                    mapping='M02-canonical-all-years-sum-paper-v1', sha256=digest(data),
                    data_versions=sorted(versions), identity_releases=sorted(identities))
    save(folder / 'manifest.json', manifest)
    print(json.dumps(manifest, ensure_ascii=False), flush=True)


def chunks(stream, size):
    chunk = []
    for line in stream:
        if not line.strip(): continue
        chunk.append(json.loads(line))
        if len(chunk) == size:
            yield chunk; chunk = []
    if chunk: yield chunk


def pair(a, b):
    return tuple(sorted((a, b)))


def check_plan(folder):
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    if manifest['space'] != 'demo_gkx_chain' or manifest['mapping'] != 'M02-canonical-all-years-sum-paper-v1':
        raise ValueError('plan scope mismatch')
    if digest(folder / 'edges.jsonl') != manifest['sha256']:
        raise ValueError('immutable source plan hash mismatch')
    return manifest


def validate_resume(state, manifest, chunk_size):
    if state['sha256'] != manifest['sha256'] or state['batch'] != manifest['batch'] or state['chunk_size'] != chunk_size:
        raise ValueError('checkpoint does not belong to this exact plan/batch/chunk size')


def fetch_properties(session, edges):
    keys = ','.join(f'{quote(e["src"])}->{quote(e["dst"])}@0' for e in edges)
    result = execute(session, 'FETCH PROP ON cooperate ' + keys +
        ' YIELD src(edge) AS src,dst(edge) AS dst,properties(edge).weight AS weight,properties(edge).props AS props')
    found = {}
    for i in range(result.row_size()):
        r = result.row_values(i)
        found[(r[0].as_string(), r[1].as_string())] = (r[2].as_double(), json.loads(r[3].as_string()))
    return found


def verify_expected(edges, found):
    for edge in edges:
        actual = found.get((edge['src'], edge['dst']))
        if actual is None or actual != (edge['weight'], edge['props']):
            raise RuntimeError('readback mismatch; checkpoint NOT advanced')


def process(session, edges, write):
    counts = Counter(planned_pairs=len(edges))
    vids = sorted({e[k] for e in edges for k in ('src', 'dst')})
    result = execute(session, 'FETCH PROP ON research ' + ','.join(map(quote, vids)) +
                     ' YIELD id(vertex) AS vid')
    present = {result.row_values(i)[0].as_string() for i in range(result.row_size())}
    missing = set(vids) - present
    if missing:
        # Fail the chunk rather than permanently lose relationships while T03 is still building.
        raise RuntimeError(f'{len(missing)} research endpoints missing; chunk not written')
    srcs = sorted({e['src'] for e in edges}); dsts = sorted({e['dst'] for e in edges})
    result = execute(session, 'MATCH (a)-[e:cooperate]-(b) '
        f'WHERE id(a) IN {quote(srcs)} AND id(b) IN {quote(dsts)} '
        'RETURN id(a) AS src,id(b) AS dst,rank(e) AS edge_rank,properties(e).props AS props')
    existing = set(); owned = set()
    for i in range(result.row_size()):
        row = result.row_values(i); key = pair(row[0].as_string(), row[1].as_string())
        existing.add(key)
        try:
            props = {} if row[3].is_null() or row[3].is_empty() else json.loads(row[3].as_string())
        except (ValueError, TypeError):
            props = {}
        if props.get('batch') == edges[0]['props']['batch']:
            owned.add(key)
    candidates = [e for e in edges if pair(e['src'], e['dst']) not in existing]
    already_owned = [e for e in edges if pair(e['src'], e['dst']) in owned]
    if already_owned:
        verify_expected(already_owned, fetch_properties(session, already_owned))
    counts['existing_pairs'] = len(edges) - len(candidates)
    counts['existing_same_batch_verified'] = len(already_owned)
    counts['ready_pairs'] = len(candidates)
    if candidates and write:
        prefix = 'INSERT EDGE IF NOT EXISTS cooperate(weight,props) VALUES '
        query = prefix + ','.join(insert_query(e)[len(prefix):] for e in candidates)
        # Retry only this idempotent insert, then ALWAYS read back. A crash leaves the
        # checkpoint before this chunk; resume verifies same-batch existing edges.
        for attempt in range(3):
            try:
                execute(session, query)
                break
            except Exception:
                if attempt == 2: raise
                time.sleep(1 + attempt)
        verify_expected(candidates, fetch_properties(session, candidates))
        counts['verified_written_pairs'] = len(candidates)
    return counts


def run(args):
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool
    folder = Path(args.plan); manifest = check_plan(folder)
    verify_only = getattr(args, 'verify_only', False)
    if verify_only and args.write: raise ValueError('verification cannot write')
    if not 1 <= args.chunk_size <= 200: raise ValueError('chunk_size must be 1..200')
    checkpoint = folder / 'checkpoint.json'
    state = dict(sha256=manifest['sha256'], batch=manifest['batch'], chunk_size=args.chunk_size,
                 next_chunk=0, counters={}, started_at=now(), status='running')
    if args.write and checkpoint.exists():
        state = json.loads(checkpoint.read_text(encoding='utf-8'))
        validate_resume(state, manifest, args.chunk_size)
    state['status'] = 'running'
    state.pop('error_type', None)
    counts = Counter(state['counters']); pool = ConnectionPool(); session = None
    try:
        cfg = Config(); cfg.timeout = 60000
        host, port = os.environ.get('NEBULA_ADDR', '10.50.75.136:9669').rsplit(':', 1)
        if not pool.init([(host, int(port))], cfg): raise RuntimeError('connection failed')
        session = pool.get_session(os.environ['NEBULA_USER'], os.environ['NEBULA_PASS'])
        execute(session, 'USE demo_gkx_chain')
        with (folder / 'edges.jsonl').open(encoding='utf-8') as stream:
            for index, chunk in enumerate(chunks(stream, args.chunk_size)):
                if index < state['next_chunk']: continue
                if verify_only:
                    verify_expected(chunk, fetch_properties(session, chunk))
                    result = Counter(planned_pairs=len(chunk), existing_pairs=len(chunk),
                                     existing_same_batch_verified=len(chunk), ready_pairs=0)
                else:
                    result = process(session, chunk, args.write)
                counts.update(result)
                state.update(next_chunk=index + 1, counters=dict(counts), updated_at=now())
                if args.write: save(checkpoint, state)
                print(json.dumps(dict(chunk=index + 1, counters=dict(counts))), flush=True)
        if counts['planned_pairs'] != manifest['counters']['eligible_pairs']:
            raise RuntimeError('plan reconciliation mismatch')
        state['status'] = 'completed'
    except Exception as exc:
        state['status'] = 'failed'; state['error_type'] = type(exc).__name__
        raise
    finally:
        state['finished_at'] = now(); state['counters'] = dict(counts)
        save(args.output, state)
        if args.write: save(checkpoint, state)
        if session: session.release()
        pool.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'run'])
    p.add_argument('--plan', required=True)
    p.add_argument('--limit-pairs', type=int, default=1000)
    p.add_argument('--batch', default='comply-20261111-t02')
    p.add_argument('--chunk-size', type=int, default=100)
    p.add_argument('--write', action='store_true')
    p.add_argument('--verify-only', action='store_true', help='Exact rank-0 property reread; pair with full graph count/rank audit')
    p.add_argument('--output', default='t02-batch-result.json')
    args = p.parse_args()
    prepare(args) if args.action == 'prepare' else run(args)


if __name__ == '__main__': main()
