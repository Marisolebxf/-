#!/usr/bin/env python3
"""Independent, read-only verification of the approved T03 import.

The verifier checks live graph counts, all research endpoint types, and fixed
samples spread across immutable source files. It never invokes the writer or
uses its SQLite journal as a substitute for querying the graph. Credentials
come only from GKX_GRAPH_USER and GKX_GRAPH_PASSWORD.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys


HOST = '10.50.75.136'
PORT = 9669
SPACE = 'demo_gkx_chain'
BATCH = 'comply-2026-11-11-t03'
KINDS = ('person', 'research', 'm01', 'm04')
EXPECTED = {'person':100000, 'research':83745, 'm01':2525789, 'm04':72099}
SAMPLE_SIZE = 20
# The T03 writer emits sort_keys=True JSON with no spaces. In M01/M04 the
# alphabetically first key is batch. This anchored root prefix compares the
# complete batch value, not an unanchored substring or a partial batch name.
OWN_BATCH_PREFIX = '{"batch":"' + BATCH + '",'


class VerificationError(RuntimeError):
    """A diagnostic that never contains a connection secret or raw record."""


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                    allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def log(message):
    print(message, file=sys.stderr, flush=True)


def cast(value):
    if hasattr(value, 'is_null') and (value.is_null() or value.is_empty()):
        return None
    result = value.cast() if hasattr(value, 'cast') else value
    if isinstance(result, bytes):
        return result.decode('utf-8')
    if isinstance(result, dict):
        return {cast(key):cast(item) for key, item in result.items()}
    if isinstance(result, (list, tuple)):
        return [cast(item) for item in result]
    return result


def sample_indices(count, size=SAMPLE_SIZE):
    if count <= 0 or size <= 0:
        return []
    if count <= size:
        return list(range(count))
    if size == 1:
        return [count // 2]
    return sorted({i * (count - 1) // (size - 1) for i in range(size)})


def source_samples(path, expected_rows):
    wanted = set(sample_indices(expected_rows))
    samples = []
    rows = 0
    with Path(path).open(encoding='utf-8') as source:
        for index, line in enumerate(source):
            if index in wanted:
                samples.append((index, json.loads(line)))
            rows += 1
    if rows != expected_rows or len(samples) != len(wanted):
        raise VerificationError('A source file row count does not match its manifest.')
    return samples


def source_contract(run_dir):
    snapshot = run_dir / 'snapshot'
    manifest_path = snapshot / 'manifest.json'
    result_path = run_dir / 'full-result.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    full_result = json.loads(result_path.read_text(encoding='utf-8'))
    if (manifest.get('status') != 'complete' or manifest.get('batch') != BATCH or
            manifest.get('space') != SPACE or full_result.get('status') != 'verified' or
            full_result.get('stage') != 'full' or full_result.get('space') != SPACE or
            full_result.get('batch') != BATCH):
        raise VerificationError('A complete source snapshot and full verified run are required.')
    manifest_hash = sha256(manifest_path)
    if full_result.get('manifest_sha256') != manifest_hash:
        raise VerificationError('The full writer result belongs to another source manifest.')
    hashes = {}
    for kind in KINDS:
        info = manifest['files'][kind]
        path = snapshot / (kind + '.jsonl')
        if int(info['rows']) != EXPECTED[kind] or sha256(path) != info['sha256']:
            raise VerificationError('A source snapshot count or checksum differs from the approved population: ' + kind)
        stats = (full_result.get('files', {}).get(kind) or
                 full_result.get('counts', {}).get(kind) or {})
        if (not stats.get('completed') or stats.get('source_records') != EXPECTED[kind] or
                stats.get('snapshot_sha256') != info['sha256'] or
                any(stats.get(key, 0) for key in ('missing_source', 'missing_target', 'missing_endpoint_records'))):
            raise VerificationError('The full writer did not verify every expected source identity: ' + kind)
        hashes[kind] = info['sha256']
    return manifest, {
        'manifest_sha256':manifest_hash, 'full_result_sha256':sha256(result_path),
        'files_sha256':hashes, 'expected_rows':dict(EXPECTED),
        'source_started_at':manifest.get('started_at'),
        'source_finished_at':manifest.get('finished_at'),
        'source_consistency':manifest.get('consistency'),
        'research_type_authority':'snapshot/research.jsonl from ads_institution_profile',
    }


class GraphReader:
    def __init__(self, user, password):
        from nebula3.Config import Config
        from nebula3.gclient.net import ConnectionPool
        config = Config()
        config.max_connection_pool_size = 1
        config.timeout = 120000
        self.pool = ConnectionPool()
        self.session = None
        try:
            if not self.pool.init([(HOST, PORT)], config):
                raise VerificationError('The verification graph connection could not initialize.')
            self.session = self.pool.get_session(user, password)
            self.query('USE ' + SPACE + ';')
        except VerificationError:
            self.close()
            raise
        except Exception as error:
            self.close()
            raise VerificationError('Graph authentication or connection failed (' + type(error).__name__ + ').') from None

    def query(self, statement):
        if not statement.lstrip().startswith(('MATCH ', 'FETCH PROP ', 'USE ')):
            raise VerificationError('The verifier accepts read-only graph statements only.')
        try:
            result = self.session.execute(statement)
        except Exception as error:
            raise VerificationError('A verification graph request failed (' + type(error).__name__ + ').') from None
        if not result.is_succeeded():
            raise VerificationError('A verification statement failed with graph code ' + str(result.error_code()) + '.')
        return [[cast(value) for value in result.row_values(index)]
                for index in range(result.row_size())]

    def vertices(self, tag, vids):
        if tag not in ('person', 'research'):
            raise VerificationError('Unexpected endpoint Tag.')
        vids = set(vids)
        if not vids:
            return {}
        statement = ('MATCH (v:`' + tag + '`) WHERE id(v) IN ' + canonical(sorted(vids)) +
                     ' RETURN id(v) AS vid, v.' + tag + '.name AS name, v.' + tag + '.props AS props;')
        found = {}
        for vid, name, props in self.query(statement):
            if vid not in vids or vid in found:
                raise VerificationError('An endpoint query returned an unexpected or duplicate identity.')
            found[vid] = {'name':name, 'props':props}
        return found

    def edges(self, kind, records):
        edge_type = {'m01':'cooperate', 'm04':'belong'}[kind]
        requested = {(row['src'], row['dst'], 0) for row in records}
        values = ','.join(canonical(src) + '->' + canonical(dst) + '@0'
                          for src, dst, _ in sorted(requested))
        statement = ('FETCH PROP ON `' + edge_type + '` ' + values +
                     ' YIELD src(edge) AS src, dst(edge) AS dst, rank(edge) AS edge_rank, '
                     'properties(edge) AS attrs;')
        found = {}
        for src, dst, rank, attrs in self.query(statement):
            key = (src, dst, rank)
            if key not in requested or key in found or not isinstance(attrs, dict):
                raise VerificationError('An edge query returned an unexpected identity or value shape.')
            found[key] = attrs
        return found

    def close(self):
        if self.session is not None:
            try:
                self.session.release()
            finally:
                self.session = None
        self.pool.close()


def count_queries():
    owned = 'e.props STARTS WITH ' + canonical(OWN_BATCH_PREFIX)
    result = {}
    for kind, a, edge, b in (('m01','person','cooperate','person'), ('m04','person','belong','research')):
        pattern = 'MATCH (a:' + a + ')-[e:' + edge + ']->(b:' + b + ') '
        # M04 is directed; rank alone is constrained, its different VID prefixes
        # do not have an undirected lexical order requirement.
        canonical_case = ('sum(CASE WHEN src(e) < dst(e) THEN 0 ELSE 1 END)' if kind == 'm01' else '0')
        result[kind] = pattern + (
            'RETURN count(e) AS total, sum(CASE WHEN ' + owned + ' THEN 1 ELSE 0 END) AS own_batch, '
            'sum(CASE WHEN rank(e) == 0 THEN 0 ELSE 1 END) AS nonzero_rank, ' +
            canonical_case + ' AS noncanonical;')
    result.update({
        'person':'MATCH (v:person) RETURN count(v) AS total;',
        'research':'MATCH (v:research) RETURN count(v) AS total;',
        'm03':'MATCH (a:person)-[e:cooperate]->(b:research) RETURN count(e) AS total;',
        'm20':'MATCH (a:person)-[e:talent_coop]->(b:person) WHERE ' + owned + ' RETURN count(e) AS own_batch;',
        'm19':'MATCH (a:research)-[e:research_coop]->(b:research) WHERE ' + owned + ' RETURN count(e) AS own_batch;',
        'm22_existing':'MATCH (a:enterprise)-[e:cooperate]->(b:enterprise) RETURN count(e) AS total;',
    })
    return result


def verify_counts(reader):
    summary = {}
    for label, query in count_queries().items():
        log('T03 independent count: ' + label)
        rows = reader.query(query)
        expected = ([EXPECTED[label],EXPECTED[label],0,0] if label in ('m01','m04') else
                    [EXPECTED[label]] if label in ('person','research') else
                    [94824] if label == 'm22_existing' else [0])
        if len(rows) != 1 or len(rows[0]) != len(expected):
            raise VerificationError('A graph aggregate returned an unexpected result shape: ' + label)
        # Empty SUM populations may return NULL, which means zero for the
        # explicitly zero/one violation counters used here.
        actual = [0 if value is None else int(value) for value in rows[0]]
        summary[label] = {'query':query, 'expected':expected, 'actual':actual,
                          'passed':actual == expected}
    return summary


def verify_research(reader, path):
    expected_types = Counter()
    observed_types = Counter()
    checked = missing = invalid_props = mismatched_type = empty_name = 0
    pending = []
    def batch(records):
        nonlocal checked, missing, invalid_props, mismatched_type, empty_name
        found = reader.vertices('research', [row['id'] for row in records])
        for row in records:
            checked += 1
            expected_type = row['props']['institution_type_id']
            expected_types[canonical(expected_type)] += 1
            actual = found.get(row['id'])
            if actual is None:
                missing += 1
                continue
            if not isinstance(actual['name'], str) or not actual['name'].strip():
                empty_name += 1
            try:
                props = json.loads(actual['props'])
                if not isinstance(props, dict) or 'institution_type_id' not in props:
                    raise ValueError()
            except (TypeError, ValueError):
                invalid_props += 1
                continue
            actual_type = props['institution_type_id']
            observed_types[canonical(actual_type)] += 1
            mismatched_type += actual_type != expected_type
    with Path(path).open(encoding='utf-8') as source:
        for line in source:
            pending.append(json.loads(line))
            if len(pending) == 500:
                batch(pending)
                pending = []
                if checked % 10000 == 0:
                    log('T03 independent research type check: ' + str(checked))
        if pending:
            batch(pending)
    return {
        'query_template':'MATCH (v:research) WHERE id(v) IN <500 source VIDs> RETURN id(v), v.research.name, v.research.props;',
        'expected_rows':EXPECTED['research'], 'checked_rows':checked,
        'missing':missing, 'invalid_props':invalid_props, 'type_mismatch':mismatched_type,
        'empty_name':empty_name, 'expected_types':dict(sorted(expected_types.items())),
        'observed_types':dict(sorted(observed_types.items())),
        'existing_owner_policy':'Any owner is accepted; existing names and props are preserved.',
        'passed':checked == EXPECTED['research'] and not any((missing,invalid_props,mismatched_type,empty_name)),
    }


def verify_person_sample(reader, path):
    samples = source_samples(path, EXPECTED['person'])
    found = reader.vertices('person', [row['id'] for _, row in samples])
    missing = sum(row['id'] not in found for _, row in samples)
    empty_name = sum(not isinstance(found[row['id']]['name'], str) or not found[row['id']]['name'].strip()
                     for _, row in samples if row['id'] in found)
    return {'query_template':'MATCH (v:person) WHERE id(v) IN <fixed source sample VIDs> RETURN id(v), v.person.name, v.person.props;',
            'sample_indices':[index for index, _ in samples], 'sample_size':len(samples),
            'missing':missing, 'empty_name':empty_name,
            'full_population_evidence':'full-result.json records per-VID Tag verification; independent total count checked separately.',
            'passed':not missing and not empty_name}


def verify_edge_samples(reader, kind, path):
    samples = source_samples(path, EXPECTED[kind])
    found = reader.edges(kind, [row for _, row in samples])
    failures = Counter()
    sample_facts = Counter()
    for index, row in samples:
        actual = found.get((row['src'], row['dst'], 0))
        if actual is None:
            failures['missing'] += 1
            continue
        try:
            props = json.loads(actual.get('props'))
        except (ValueError, TypeError):
            failures['invalid_props'] += 1
            continue
        if not isinstance(props, dict):
            failures['invalid_props'] += 1
            continue
        failures['props_mismatch'] += props != row['props']
        failures['batch_mismatch'] += props.get('batch') != BATCH
        weight = actual.get('weight')
        if (isinstance(weight, bool) or not isinstance(weight, (int,float)) or
                not math.isfinite(weight) or not math.isclose(weight, row['weight'], rel_tol=1e-12, abs_tol=1e-12)):
            failures['weight_mismatch'] += 1
        if kind == 'm01':
            failures['semantic_mismatch'] += props.get('match_method') != 'coauthor' or row['src'] >= row['dst']
        else:
            failures['company_endpoint'] += props.get('institution_type_id') == 'company'
            ids = props.get('source_experience_ids', [])
            failures['stint_mismatch'] += props.get('stint_count') != len(set(ids))
            failures['semantic_mismatch'] += props.get('experience_type') != 2 or not isinstance(props.get('is_current'), bool)
            sample_facts['current_true' if props.get('is_current') else 'current_false'] += 1
            sample_facts['multi_stint' if props.get('stint_count', 0) > 1 else 'single_stint'] += 1
    edge_type = 'cooperate' if kind == 'm01' else 'belong'
    return {'query_template':'FETCH PROP ON ' + edge_type + ' <fixed source src->dst@0 identities> YIELD src(edge), dst(edge), rank(edge), properties(edge);',
            'sample_indices':[index for index, _ in samples], 'sample_size':len(samples),
            'observed_rows':len(found), 'failures':dict(failures), 'sample_facts':dict(sample_facts),
            'comparison':'Exact parsed JSON props, complete batch value, numeric weight, identity/rank and relation semantics.',
            'passed':len(found) == len(samples) and not any(failures.values())}


def verify(run_dir, reader=None):
    run_dir = Path(run_dir).resolve()
    output = run_dir / 'verification.json'
    report = {'task':'KG-COMPLY-LOAD-T03', 'batch':BATCH, 'space':SPACE,
              'host':HOST, 'port':PORT, 'started_at':now(), 'status':'running',
              'verifier_sha256':sha256(Path(__file__)), 'read_only':True,
              'scope':'T03 person/research endpoint verification and M01/M04; M02 belongs to T02.',
              'batch_count_predicate':{'method':'canonical JSON root prefix', 'prefix':OWN_BATCH_PREFIX,
                                      'exact_sample_check':'json.loads(props)[batch] equals the complete batch value'},
              'checks':{}}
    owned_reader = reader is None
    try:
        manifest, report['source_evidence'] = source_contract(run_dir)
        write_json(output, report)
        if reader is None:
            reader = GraphReader(os.environ['GKX_GRAPH_USER'], os.environ['GKX_GRAPH_PASSWORD'])
        report['checks']['counts'] = verify_counts(reader)
        write_json(output, report)
        snapshot = run_dir / 'snapshot'
        report['checks']['research_full_types'] = verify_research(reader, snapshot / 'research.jsonl')
        write_json(output, report)
        report['checks']['person_sample'] = verify_person_sample(reader, snapshot / 'person.jsonl')
        for kind in ('m01','m04'):
            report['checks'][kind + '_sample'] = verify_edge_samples(reader, kind, snapshot / (kind + '.jsonl'))
        checks = list(report['checks']['counts'].values()) + [value for key, value in report['checks'].items() if key != 'counts']
        report['status'] = 'passed' if all(value['passed'] for value in checks) else 'failed'
        report['completed_at'] = now()
        write_json(output, report)
        log('T03 independent verification: ' + report['status'])
        return report
    except Exception as error:
        report['status'] = 'failed'
        report['error_type'] = type(error).__name__
        if isinstance(error, VerificationError):
            report['error'] = str(error)
        report['completed_at'] = now()
        write_json(output, report)
        raise
    finally:
        if owned_reader and reader is not None:
            reader.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.run_dir)
    if result['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
