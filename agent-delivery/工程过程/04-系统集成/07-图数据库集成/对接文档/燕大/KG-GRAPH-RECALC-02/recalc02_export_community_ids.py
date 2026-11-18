"""KG-GRAPH-RECALC-02 supplementary read-only export: tech_point.community_id.

The 2026-11-18 snapshot nodes.jsonl (reused T09 NODE_QUERY) has no community_id
column. Range 4 of the task card compares the in-graph community_id values
(filled by KG-GRAPH-COVER-01) with the recalculated Louvain partition, with the
in-graph values authoritative. This script exports them tag-anchored, paged,
ORDER BY vid, count-guarded, credentials from GKX_GRAPH_USER/GKX_GRAPH_PASSWORD
only. Refuses to overwrite an existing export.
"""
import importlib.util
import os
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location('paths', Path(__file__).resolve().parents[7] / 'scripts' / 'kg-comply-paths.py')
io = importlib.util.module_from_spec(spec)
spec.loader.exec_module(io)

QUERY = ('MATCH (v:tech_point) WHERE v.tech_point.community_id != "" '
         'RETURN id(v) AS vid, v.tech_point.community_id AS community_id '
         'ORDER BY vid SKIP {offset} LIMIT {limit};')
COUNT = 'MATCH (v:tech_point) WHERE v.tech_point.community_id != "" RETURN count(v);'


def main(snapshot_dir):
    destination = snapshot_dir / 'community-ids.jsonl'
    if destination.exists() or (snapshot_dir / 'community-ids-metadata.json').exists():
        raise io.RunError('community-ids export already exists; refusing to overwrite.')
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool
    config = Config()
    config.timeout = 120000
    pool = ConnectionPool()
    session = None
    started = io.utc_now()
    try:
        if not pool.init([('10.50.75.136', 9669)], config):
            raise io.RunError('Graph connection failed.')
        session = pool.get_session(os.environ['GKX_GRAPH_USER'], os.environ['GKX_GRAPH_PASSWORD'])
        io.execute(session, 'USE demo_gkx_chain;')
        before = io.scalar(io.execute(session, COUNT).row_values(0)[0])
        export = io.export_pages(session, QUERY, ('vid', 'community_id'), destination, 10000)
        after = io.scalar(io.execute(session, COUNT).row_values(0)[0])
        if before != after or before != export['rows']:
            raise io.RunError('community_id counts changed during export; discard the file.')
    finally:
        if session is not None:
            session.release()
        pool.close()
    destination.with_name(destination.name + '.tmp').replace(destination)
    io.write_json(snapshot_dir / 'community-ids-metadata.json', {
        'purpose': 'KG-GRAPH-COVER-01 backfilled tech_point.community_id; in-graph values are authoritative for range 4 comparison',
        'started_at': started, 'finished_at': io.utc_now(),
        'rows': export['rows'], 'count_before': before, 'count_after': after,
        'sha256': io.sha256(destination), 'query_template': QUERY})


if __name__ == '__main__':
    try:
        main(Path(sys.argv[1]).resolve())
    except io.RunError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
