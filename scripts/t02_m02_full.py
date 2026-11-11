"""Full M02 orchestration: immutable source shards, verified writes, full reread.

Uses the validated batch executor. Credentials are process environment only.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from t02_m02 import aggregate, grouped, execute, quote
from t02_m02_batch import save, now, digest, check_plan

TABLE = 'ads_institution_collaboration_yearly'
PROFILE = 'ads_institution_profile'
MAPPING = 'M02-canonical-all-years-sum-paper-v1'


def source_execute(cursor, sql, params=None):
    # Shared source workload group has only four queue slots. Never add concurrency.
    for attempt in range(6):
        try:
            return cursor.execute(sql, params)
        except Exception as exc:
            if 'query waiting queue is full' not in str(exc) or attempt==5: raise
            time.sleep(min(60,10*(2**attempt)))


def source_connect():
    import pymysql
    return pymysql.connect(host='47.93.119.170', port=29030,
        user=os.environ['DORIS_USER'], password=os.environ['DORIS_PASSWORD'],
        database='gkx_technology_analysis_dev', charset='utf8mb4',
        connect_timeout=10, read_timeout=180, cursorclass=pymysql.cursors.SSDictCursor)


def signature(conn):
    with conn.cursor() as cur:
        source_execute(cur,f'SELECT data_version,identity_release_id,COUNT(*) AS n,'
                    f'SUM(co_paper_count) AS papers FROM {TABLE} '
                    'GROUP BY data_version,identity_release_id ORDER BY data_version,identity_release_id')
        versions = [{k: str(v) for k,v in r.items()} for r in cur]
        source_execute(cur,f'SELECT institution_id,institution_type_id FROM {PROFILE} ORDER BY institution_id')
        profiles = {}
        for r in cur:
            if r['institution_id'] in profiles: raise ValueError('duplicate profile')
            profiles[r['institution_id']] = r['institution_type_id']
    ph = hashlib.sha256(json.dumps(profiles, sort_keys=True).encode()).hexdigest()
    return dict(versions=versions, profile_sha256=ph, profile_count=len(profiles)), profiles


def partitions(ids, size):
    if ids != sorted(set(ids)): raise ValueError('source IDs must be unique and ordered')
    return [ids[i:i+size] for i in range(0,len(ids),size)]


def prepare(args):
    root = Path(args.plan); root.mkdir(parents=True, exist_ok=True)
    conn = source_connect()
    try:
        sig, profiles = signature(conn)
        expected = [('202610201700','institution_ads_mvp_v1_20261007')]
        if [(v['data_version'],v['identity_release_id']) for v in sig['versions']] != expected:
            raise ValueError('source release changed; do not mix pilot and full plan')
        with conn.cursor() as cur:
            source_execute(cur,f'SELECT DISTINCT institution_id FROM {TABLE} '
                        'WHERE institution_id < collaborator_institution_id ORDER BY institution_id')
            ids = [r['institution_id'] for r in cur]
            source_execute(cur,f'SELECT COUNT(*) AS n FROM {TABLE} WHERE institution_id < collaborator_institution_id')
            canonical_rows = int(next(iter(cur))['n'])
        layout = dict(signature=sig, source_ids=ids, source_ids_per_shard=args.source_ids_per_shard,
                      canonical_rows=canonical_rows, batch=args.batch, mapping=MAPPING)
        layout_path = root/'layout.json'
        if layout_path.exists():
            if json.loads(layout_path.read_text(encoding='utf-8')) != layout:
                raise ValueError('source or partition layout changed; refusing resume')
        else: save(layout_path, layout)
        total = Counter(); shards = []; endpoints = set()
        for index, subset in enumerate(partitions(ids,args.source_ids_per_shard)):
            folder = root/f'{index:04d}'; folder.mkdir(exist_ok=True)
            manifest_path = folder/'manifest.json'; data = folder/'edges.jsonl'
            if manifest_path.exists():
                m = check_plan(folder)
            else:
                counts = Counter(eligible_pairs=0); temp = folder/'edges.partial.jsonl'
                with conn.cursor() as cur, temp.open('w',encoding='utf-8',newline='\n') as out:
                    source_execute(cur,f'SELECT institution_id,collaborator_institution_id,statistics_year,'
                        f'co_paper_count,collaboration_strength,data_version,identity_release_id FROM {TABLE} '
                        'WHERE institution_id >= %s AND institution_id <= %s '
                        'AND institution_id < collaborator_institution_id '
                        'ORDER BY institution_id,collaborator_institution_id,statistics_year',
                        (subset[0],subset[-1]))
                    for rows in grouped(cur):
                        counts['source_pairs'] += 1; counts['source_rows'] += len(rows)
                        if any((str(r['data_version']),r['identity_release_id']) != expected[0] for r in rows):
                            raise ValueError('mixed source release')
                        a=profiles.get(rows[0]['institution_id']); b=profiles.get(rows[0]['collaborator_institution_id'])
                        if a is None or b is None:
                            counts['missing_source_endpoint_pairs'] += 1; continue
                        if 'company' in (a,b):
                            counts['excluded_company_pairs'] += 1; continue
                        edge=aggregate(rows,args.batch)
                        out.write(json.dumps(edge,ensure_ascii=False,allow_nan=False)+'\n')
                        counts['eligible_pairs'] += 1; counts['eligible_source_rows'] += len(rows)
                        counts['weight_sum'] += edge['weight']
                os.replace(temp,data)
                m=dict(version=1,prepared_at=now(),batch=args.batch,space='demo_gkx_chain',mapping=MAPPING,
                       sha256=digest(data),counters=dict(counts),source_first=subset[0],source_last=subset[-1],
                       data_versions=[expected[0][0]],identity_releases=[expected[0][1]])
                save(manifest_path,m)
                time.sleep(1)
            total.update(m['counters']); shards.append(dict(folder=folder.name,sha256=m['sha256']))
            with data.open(encoding='utf-8') as stream:
                for line in stream:
                    e=json.loads(line); endpoints.update((e['src'],e['dst']))
            progress=dict(shards_done=index+1,total_shards=len(partitions(ids,args.source_ids_per_shard)),counters=dict(total),at=now())
            save(root/'prepare-progress.json',progress); print(json.dumps(progress),flush=True)
        after,_=signature(conn)
        if after != sig: raise ValueError('source signature changed during extraction')
        if total['source_rows'] != canonical_rows: raise ValueError('source partition coverage mismatch')
        if total['missing_source_endpoint_pairs']: raise ValueError('source endpoints missing; no full write')
        save(root/'endpoints.json',sorted(endpoints))
        save(root/'full-manifest.json',dict(prepared_at=now(),signature=sig,layout_sha256=digest(layout_path),
             shards=shards,counters=dict(total),endpoint_count=len(endpoints),endpoints_sha256=digest(root/'endpoints.json'),
             batch=args.batch,space='demo_gkx_chain',mapping=MAPPING))
    finally: conn.close()


def load_full(root):
    m=json.loads((root/'full-manifest.json').read_text(encoding='utf-8'))
    if m['space']!='demo_gkx_chain' or m['mapping']!=MAPPING: raise ValueError('scope mismatch')
    if digest(root/'layout.json')!=m['layout_sha256']: raise ValueError('layout changed')
    if digest(root/'endpoints.json')!=m['endpoints_sha256']: raise ValueError('endpoints changed')
    total=Counter()
    for shard in m['shards']:
        sm=check_plan(root/shard['folder'])
        if sm['sha256']!=shard['sha256'] or sm['batch']!=m['batch']: raise ValueError('shard changed')
        total.update(sm['counters'])
    if dict(total)!=m['counters']: raise ValueError('full counters mismatch')
    return m


def graph_connect(timeout=60000):
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool
    pool=ConnectionPool();cfg=Config();cfg.timeout=timeout
    if not pool.init([('10.50.75.136',9669)],cfg): raise RuntimeError('graph unavailable')
    session=pool.get_session(os.environ['NEBULA_USER'],os.environ['NEBULA_PASS'])
    execute(session,'USE demo_gkx_chain')
    return pool,session


def preflight(root,m):
    conn=source_connect()
    try:
        sig,_=signature(conn)
        if sig!=m['signature']: raise ValueError('source changed after plan freeze')
    finally: conn.close()
    pool,s=graph_connect()
    try:
        ids=json.loads((root/'endpoints.json').read_text(encoding='utf-8'))
        for i in range(0,len(ids),200):
            batch=ids[i:i+200]
            r=execute(s,'FETCH PROP ON research '+','.join(map(quote,batch))+' YIELD id(vertex) AS vid')
            actual={r.row_values(j)[0].as_string() for j in range(r.row_size())}
            if set(batch)!=actual: raise RuntimeError('missing research endpoints; full write not started')
        save(root/'preflight.json',dict(at=now(),endpoints_verified=len(ids),signature=sig,status='passed'))
    finally:s.release();pool.close()


def run_shard(root, shard, write):
    folder=root/shard['folder'];name='write' if write else 'verify'
    output=folder/(name+'.json')
    command=[sys.executable,'-B',str(Path(__file__).with_name('t02_m02_batch.py')),
             'run','--plan',str(folder),'--chunk-size','200','--output',str(output)]
    if write:command.append('--write')
    with (folder/(name+'.log')).open('a',encoding='utf-8') as log:
        subprocess.run(command,stdout=log,stderr=log,check=True)
    c=json.loads(output.read_text(encoding='utf-8'))['counters']
    if c.get('existing_pairs',0)!=c.get('existing_same_batch_verified',0):
        raise RuntimeError('foreign preexisting edges require reconciliation')
    if not write and (c.get('ready_pairs',0) or c.get('existing_pairs',0)!=c.get('planned_pairs',0)):
        raise RuntimeError('full verification found missing edges')
    return c


def apply(args):
    root=Path(args.plan);m=load_full(root)
    # Exclusive lock is held by the OS; automatically released on process exit.
    import msvcrt
    with (root/'run.lock').open('a+b') as lock:
        if lock.tell()==0:lock.write(b'0');lock.flush()
        lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        if args.write: preflight(root,m)
        totals=Counter();name='write' if args.write else 'verify'
        iterator=iter(m['shards']);completed=[]
        # Bound both active and scheduled work. On failure do not enqueue more;
        # the other active shard finishes its verified checkpoint before exit.
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            pending={}
            for _ in range(args.workers):
                shard=next(iterator,None)
                if shard:pending[executor.submit(run_shard,root,shard,args.write)]=shard
            while pending:
                done,_=wait(pending,return_when=FIRST_COMPLETED)
                for future in done:
                    c=future.result();shard=pending.pop(future)
                    totals.update(c);completed.append(shard['folder'])
                progress=dict(at=now(),shards_done=len(completed),total_shards=len(m['shards']),
                              completed_shards=sorted(completed),counters=dict(totals),workers=args.workers)
                save(root/(name+'-progress.json'),progress)
                print(json.dumps({k:v for k,v in progress.items() if k!='completed_shards'}),flush=True)
                for _ in done:
                    shard=next(iterator,None)
                    if shard:pending[executor.submit(run_shard,root,shard,args.write)]=shard
        if totals['planned_pairs']!=m['counters']['eligible_pairs']: raise ValueError('full total mismatch')
        save(root/(name+'-result.json'),dict(progress,status='completed',plan_sha256=digest(root/'full-manifest.json')))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['prepare','run'])
    p.add_argument('--plan',required=True)
    p.add_argument('--source-ids-per-shard',type=int,default=100)
    p.add_argument('--batch',default='comply-20261111-t02')
    p.add_argument('--write',action='store_true')
    p.add_argument('--workers',type=int,choices=[1,2],default=1)
    args=p.parse_args()
    if not 1<=args.source_ids_per_shard<=200:raise ValueError('shard size must be 1..200')
    prepare(args) if args.action=='prepare' else apply(args)
