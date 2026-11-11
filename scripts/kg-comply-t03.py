#!/usr/bin/env python3
"""Execute the approved T03 mapping against the fixed compliance space.

Connection secrets come from the process environment. Source snapshots and the
SQLite progress journal remain on the execution machine, outside Git.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

KINDS = ('person', 'research', 'm01', 'm04')
BATCH = 'comply-2026-11-11-t03'


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    tmp.replace(path)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for data in iter(lambda: source.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def source_connection():
    import pymysql
    user = os.environ['GKX_SOURCE_USER']
    password = os.environ['GKX_SOURCE_PASSWORD']
    connection = pymysql.connect(host=os.environ.get('GKX_SOURCE_HOST', '47.93.119.170'),
        port=int(os.environ.get('GKX_SOURCE_PORT', '29030')),
        database='gkx_technology_analysis_dev', user=user, password=password,
        charset='utf8mb4', connect_timeout=10, read_timeout=600,
        autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute('SET query_timeout = 3600')
    return connection


def run_apply(args):
    from kg_comply_t03_graph import GraphWriter
    directory = args.run_dir.resolve()
    snapshot = directory / 'snapshot'
    if not (snapshot / 'manifest.json').is_file():
        raise RuntimeError('A complete source snapshot is required.')
    manifest = json.loads((snapshot / 'manifest.json').read_text(encoding='utf-8'))
    if (manifest.get('status') != 'complete' or manifest.get('batch') != BATCH or
            manifest.get('space') != 'demo_gkx_chain'):
        raise RuntimeError('The snapshot is incomplete or belongs to another mapping target.')
    files = {kind: snapshot / (kind + '.jsonl') for kind in KINDS}
    # Validate the original immutable export even when applying a canary slice.
    expected_counts = {}
    for kind, path in files.items():
        info = manifest['files'][kind]
        if not path.is_file() or digest(path) != info['sha256']:
            raise RuntimeError('Incomplete source snapshot: ' + path.name)
        expected_counts[kind] = int(info['rows'])
    if args.canary:
        canary = directory / 'canary'
        canary.mkdir(exist_ok=True)
        for kind, original in files.items():
            target = canary / original.name
            with original.open('rb') as src, target.open('wb') as dst:
                for _ in range(20):
                    line = src.readline()
                    if not line:
                        break
                    dst.write(line)
            files[kind] = target
            expected_counts[kind] = min(20, expected_counts[kind])
    stage = 'canary' if args.canary else 'full'
    writer = GraphWriter('10.50.75.136', 9669,
        os.environ['GKX_GRAPH_USER'], os.environ['GKX_GRAPH_PASSWORD'],
        'demo_gkx_chain', directory / (stage + '-journal.sqlite3'))
    report_path = directory / (stage + '-result.json')
    report = {'task':'KG-COMPLY-LOAD-T03','batch':BATCH,'stage':stage,
        'space':'demo_gkx_chain','started_at':datetime.now(timezone.utc).isoformat(),
        'manifest_sha256':digest(snapshot / 'manifest.json'), 'files':{}, 'status':'running'}
    report['runtime_source_sha256'] = {
        name: digest(Path(__file__).with_name(name))
        for name in ('kg-comply-t03.py','kg_comply_t03_graph.py','kg_comply_t03_source.py')
    }
    try:
        report['preflight'] = writer.preflight()
        write_json(report_path, report)
        for kind in args.kinds:
            print(json.dumps({'event':'applying','kind':kind,'stage':stage}), flush=True)
            report['files'][kind] = writer.apply_file(kind, files[kind], batch_size=args.batch_size)
            stats = report['files'][kind]
            if (not stats['completed'] or stats['source_records'] != expected_counts[kind] or
                    any(stats.get(key, 0) for key in ('missing_source', 'missing_target', 'missing_endpoint_records'))):
                raise RuntimeError('A requested source population was not completely verified: ' + kind)
            write_json(report_path, report)
        report['counts'] = writer.counts()
        report['status'] = 'verified'
        report['completed_at'] = datetime.now(timezone.utc).isoformat()
        write_json(report_path, report)
        print(json.dumps({'event':'complete','stage':stage,'result':str(report_path)}), flush=True)
    except Exception as error:
        report['status'] = 'failed'
        report['error_type'] = type(error).__name__
        # Never serialize connection exceptions, which can include auth details.
        write_json(report_path, report)
        raise
    finally:
        writer.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('snapshot','apply'))
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--canary', action='store_true')
    parser.add_argument('--batch-size', type=int, default=500)
    parser.add_argument('--kinds', nargs='+', choices=KINDS, default=list(KINDS))
    args = parser.parse_args()
    args.run_dir.mkdir(parents=True, exist_ok=True)
    if args.command == 'snapshot':
        from kg_comply_t03_source import export_snapshot
        conn = source_connection()
        try:
            export_snapshot(conn, args.run_dir / 'snapshot')
        finally:
            conn.close()
    else:
        run_apply(args)


if __name__ == '__main__':
    main()
