"""T02 M02 loader. Default: read-only sample. Credentials only from environment.

Never creates vertices/schema, never updates existing edges. One canonical
institution pair -> one rank=0 cooperate edge after aggregating ALL its years.
Run with --help. Requires pymysql and nebula3-python.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import json
import os
from pathlib import Path


TABLE = 'ads_institution_collaboration_yearly'
PROFILE = 'ads_institution_profile'


def quote(value):
    return json.dumps(value, ensure_ascii=False)


def aggregate(rows, batch):
    """Rows must be one canonical pair; reject bad/duplicate years, never coerce NULL to 0."""
    if not rows:
        raise ValueError('empty pair')
    a, b = rows[0]['institution_id'], rows[0]['collaborator_institution_id']
    if not a or not b or not a < b:
        raise ValueError('noncanonical pair')
    years, strength, total = set(), {}, 0
    for row in rows:
        if (row['institution_id'], row['collaborator_institution_id']) != (a, b):
            raise ValueError('mixed pair')
        year = int(row['statistics_year'])
        if year in years:
            raise ValueError('duplicate pair/year')
        years.add(year)
        count = row['co_paper_count']
        if count is None or int(count) != count or count < 0:
            raise ValueError('invalid co_paper_count')
        total += int(count)
        value = row['collaboration_strength']
        strength[str(year)] = None if value is None else float(value)
    # double cannot exactly represent larger integers; fail instead of silently rounding.
    if total > 2**53:
        raise ValueError('weight exceeds exact double integer range')
    src, dst = 'inst:' + a, 'inst:' + b
    if max(len(src.encode()), len(dst.encode())) > 80:
        raise ValueError('VID too long')
    props = dict(first_year=min(years), latest_year=max(years), year_count=len(years),
                 co_paper_count_total=total, match_method='coauthor', batch=batch,
                 source_table=TABLE, institution_id=a, collaborator_institution_id=b,
                 source_row_count=len(rows), strength_by_year=strength,
                 strength_note='normalized separately each year; do not compare across years',
                 undirected=True, canonical_order='institution_id < collaborator_institution_id')
    return dict(src=src, dst=dst, weight=total, props=props)


def source_sql(limit):
    # Select PAIRS first, then fetch every year. LIMIT on source rows would truncate years.
    pair_limit = '' if limit == 0 else ' LIMIT %s'
    return f'''SELECT r.institution_id,r.collaborator_institution_id,
        r.statistics_year,r.co_paper_count,r.collaboration_strength,r.data_version,
        r.identity_release_id,
        a.institution_type_id AS src_type,b.institution_type_id AS dst_type
        FROM {TABLE} r
        JOIN (SELECT institution_id,collaborator_institution_id FROM {TABLE}
              WHERE institution_id < collaborator_institution_id
              GROUP BY institution_id,collaborator_institution_id
              ORDER BY institution_id,collaborator_institution_id{pair_limit}) p
          ON r.institution_id=p.institution_id
         AND r.collaborator_institution_id=p.collaborator_institution_id
        LEFT JOIN {PROFILE} a ON r.institution_id=a.institution_id
        LEFT JOIN {PROFILE} b ON r.collaborator_institution_id=b.institution_id
        ORDER BY r.institution_id,r.collaborator_institution_id,r.statistics_year'''


def grouped(cursor):
    key, group = None, []
    for row in cursor:
        current = row['institution_id'], row['collaborator_institution_id']
        if key is not None and current != key:
            yield group
            group = []
        key = current
        group.append(row)
    if group:
        yield group


def execute(session, query):
    result = session.execute(query)
    if not result.is_succeeded():
        raise RuntimeError(str(result.error_msg()))
    return result


def edge_exists(session, src, dst):
    result = execute(session, f'FETCH PROP ON cooperate {quote(src)}->{quote(dst)}@0 '
                     'YIELD properties(edge).weight AS weight, properties(edge).props AS props')
    return result


def vertex_exists(session, vid):
    result = execute(session, f'FETCH PROP ON research {quote(vid)} YIELD properties(vertex).name AS name')
    return result.row_size() > 0


def any_existing_edge(session, src, dst):
    # Check BOTH orientations and ALL ranks, including noncanonical historical data.
    return execute(session, 'MATCH (a)-[e:cooperate]-(b) '
                   f'WHERE id(a)=={quote(src)} AND id(b)=={quote(dst)} '
                   'RETURN rank(e) AS edge_rank LIMIT 1').row_size() > 0


def insert_query(edge):
    # No destructive statements or updates: IF NOT EXISTS protects historical rank=0 edges.
    props = json.dumps(edge['props'], ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    return ('INSERT EDGE IF NOT EXISTS cooperate(weight,props) VALUES '
            f'{quote(edge["src"])}->{quote(edge["dst"])}@0:({edge["weight"]},{quote(props)})')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit-pairs', type=int, default=100,
                        help='Canonical pairs before company filtering; 0 means full source')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--batch', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.limit_pairs < 0 or not args.batch.startswith('comply-') or not args.batch.endswith('-t02'):
        parser.error('invalid limit or T02 batch')
    if args.write and args.limit_pairs == 0:
        parser.error('full write intentionally disabled until sampled run reviewed')
    import pymysql
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool
    report = dict(started_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
                  space='demo_gkx_chain', mode='write' if args.write else 'dry_run',
                  batch=args.batch, limit_pairs=args.limit_pairs, counters={}, examples=[],
                  scope='canonical source pairs, all years; company excluded by profile',
                  status='running')
    counts = defaultdict(int)
    pool, session, conn = ConnectionPool(), None, None
    cache = {}
    try:
        cfg = Config(); cfg.timeout = 30000
        host, port = os.environ.get('NEBULA_ADDR', '10.50.75.136:9669').rsplit(':', 1)
        if not pool.init([(host, int(port))], cfg):
            raise RuntimeError('graph connection failed')
        session = pool.get_session(os.environ['NEBULA_USER'], os.environ['NEBULA_PASS'])
        execute(session, 'USE demo_gkx_chain')
        conn = pymysql.connect(host=os.environ.get('DORIS_HOST', '47.93.119.170'),
            port=int(os.environ.get('DORIS_PORT', '29030')), user=os.environ['DORIS_USER'],
            password=os.environ['DORIS_PASSWORD'], database='gkx_technology_analysis_dev',
            charset='utf8mb4', connect_timeout=10, read_timeout=180,
            cursorclass=pymysql.cursors.SSDictCursor)
        with conn.cursor() as cur:
            cur.execute(source_sql(args.limit_pairs), (args.limit_pairs,) if args.limit_pairs else ())
            for rows in grouped(cur):
                counts['source_pairs'] += 1; counts['source_rows'] += len(rows)
                if any(r['src_type'] is None or r['dst_type'] is None for r in rows):
                    counts['missing_source_endpoint_pairs'] += 1
                    continue
                if any('company' in (r['src_type'], r['dst_type']) for r in rows):
                    counts['excluded_company_pairs'] += 1
                    continue
                edge = aggregate(rows, args.batch)
                counts['eligible_pairs'] += 1
                counts['eligible_source_rows'] += len(rows)
                for vid in (edge['src'], edge['dst']):
                    if vid not in cache:
                        cache[vid] = vertex_exists(session, vid)
                if len(report['examples']) < 5:
                    report['examples'].append(edge)
                if not cache[edge['src']] or not cache[edge['dst']]:
                    counts['missing_graph_endpoint_pairs'] += 1
                    continue
                # Skip reverse orientation as well: old undirected edges must not be duplicated.
                if any_existing_edge(session, edge['src'], edge['dst']):
                    counts['existing_edge_pairs'] += 1
                    continue
                counts['ready_pairs'] += 1
                if args.write:
                    execute(session, insert_query(edge))
                    check = edge_exists(session, edge['src'], edge['dst'])
                    if check.row_size() != 1:
                        raise RuntimeError('write readback missing')
                    record = check.row_values(0)
                    actual = json.loads(record[1].as_string())
                    if actual != edge['props'] or record[0].as_double() != edge['weight']:
                        raise RuntimeError('readback mismatch or concurrent writer; stopped')
                    counts['verified_written_pairs'] += 1
                if counts['source_pairs'] % 20 == 0:
                    print(json.dumps(dict(counts)), flush=True)
        report['status'] = 'completed'
    except Exception as exc:
        report['status'] = 'failed'
        report['error_type'] = type(exc).__name__
        # Do not store driver exceptions containing connection secrets.
        raise
    finally:
        report['counters'] = dict(counts)
        report['unique_graph_endpoints_checked'] = len(cache)
        report['graph_endpoints_present'] = sum(cache.values())
        report['finished_at'] = datetime.now(timezone(timedelta(hours=8))).isoformat()
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        if conn: conn.close()
        if session: session.release()
        pool.close()
        print(json.dumps({'status': report['status'], 'counters': dict(counts)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
