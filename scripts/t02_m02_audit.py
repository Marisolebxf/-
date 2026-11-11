"""Read-only full-plan reconciliation after t02_m02_full run and reread."""
import argparse
from collections import Counter,defaultdict,deque
import json
from pathlib import Path

from t02_m02 import execute
from t02_m02_batch import save,now,digest
from t02_m02_full import load_full,graph_connect,source_connect,signature


def acyclic(edges):
    degree=Counter();adj=defaultdict(list)
    for a,b in edges:
        degree.setdefault(a,0);degree[b]+=1;adj[a].append(b)
    queue=deque(n for n,d in degree.items() if d==0);visited=0
    while queue:
        node=queue.popleft();visited+=1
        for target in adj[node]:
            degree[target]-=1
            if degree[target]==0:queue.append(target)
    return visited==len(degree)


def main(root):
    m=load_full(root);plan_hash=digest(root/'full-manifest.json')
    for stage in ['write','verify']:
        r=json.loads((root/(stage+'-result.json')).read_text(encoding='utf-8'))
        if r['status']!='completed' or r['plan_sha256']!=plan_hash:raise ValueError('full run incomplete')
    out=dict(started_at=now(),plan_sha256=plan_hash,expected=m['counters'],checks={})
    pool,s=graph_connect(timeout=180000)
    try:
        queries={
          'M15':'MATCH ()-[e:depends_on]->() RETURN count(e)',
          'M17':'MATCH (a:enterprise)-[e:participates]->(b:segment) RETURN count(e)',
          'M19':'MATCH ()-[e:research_coop]->() RETURN count(e)',
          'M22':'MATCH (a:enterprise)-[e:cooperate]->(b:enterprise) RETURN count(e)',
          'research':'MATCH (a:research) RETURN count(a)',
          'M02':'MATCH (a:research)-[e:cooperate]->(b:research) RETURN count(e)',
          'M02_weight':'MATCH (a:research)-[e:cooperate]->(b:research) RETURN sum(e.weight)',
          'M02_noncanonical':'MATCH (a:research)-[e:cooperate]->(b:research) WHERE id(a)>=id(b) RETURN count(e)',
          'M02_nonzero_rank':'MATCH (a:research)-[e:cooperate]->(b:research) WHERE rank(e)!=0 RETURN count(e)'}
        expected=dict(M15=1073,M17=178731,M19=0,M22=94824,research=83745,
                      M02=m['counters']['eligible_pairs'],M02_weight=m['counters']['weight_sum'],
                      M02_noncanonical=0,M02_nonzero_rank=0)
        for name,q in queries.items():
            cell=execute(s,q).row_values(0)[0]
            value=cell.as_double() if name=='M02_weight' else cell.as_int()
            out['checks'][name]=dict(actual=value,expected=expected[name],passed=value==expected[name])
            save(root/'audit-progress.json',out);print(name,value,flush=True)
        r=execute(s,'MATCH (a)-[e:depends_on]->(b) RETURN id(a),id(b)')
        edges=[tuple(v.as_string() for v in r.row_values(i)) for i in range(r.row_size())]
        out['checks']['M15_DAG']=dict(passed=acyclic(edges),edges=len(edges))
    finally:s.release();pool.close()
    conn=source_connect()
    try:
        after,_=signature(conn)
        out['checks']['source_stable']=dict(passed=after==m['signature'],after=after)
    finally:conn.close()
    out.update(finished_at=now(),status='passed' if all(v['passed'] for v in out['checks'].values()) else 'failed')
    save(root/'audit-result.json',out)
    if out['status']!='passed':raise RuntimeError('reconciliation failed; no completion claim')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--plan',required=True)
    main(Path(p.parse_args().plan))
