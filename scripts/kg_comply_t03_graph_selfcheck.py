"""Synthetic T03 writer checks. Never connects to a database."""

import copy
import json
from pathlib import Path
import re
import tempfile
import unittest

from kg_comply_t03_graph import BATCH, SPACE, GraphWriter, GraphWriteError, _json


class SimulatedCrash(BaseException):
    pass


class Backend:
    def __init__(self):
        self.vertices = {"person": {}, "research": {}}
        self.edges = {"cooperate": {}, "belong": {}}
        self.queries = []
        self.insert_calls = 0
        self.fail_after = None
        self.crash = False
        self.unsupported = False
        self.corrupt = False
        self.concurrent = None


class FakeWriter(GraphWriter):
    def __init__(self, backend, journal, host="synthetic"):
        self.backend = backend
        super().__init__(host, 9669, "test", "not-a-real-credential", SPACE, journal)

    def _connect(self):
        pass

    def _disconnect(self):
        pass

    @staticmethod
    def _parts(text):
        """Decode generated JSON scalars, leaving nGQL punctuation explicit."""
        decoder = json.JSONDecoder()
        result = []
        while text:
            text = text.lstrip()
            if text[0] in '"0123456789' or (text[0] == '-' and len(text) > 1 and text[1].isdigit()):
                value, end = decoder.raw_decode(text)
                result.append(value)
                text = text[end:]
            else:
                text = text[1:]
        return result

    def _query(self, statement):
        b = self.backend
        b.queries.append(statement)
        if statement.startswith("DESCRIBE TAG"):
            return [["name", "string"], ["props", "string"]]
        if statement.startswith("DESCRIBE EDGE"):
            return [["weight", "double"], ["props", "string"]]
        if statement.startswith("MATCH"):
            tag = re.search(r"v:`([^`]+)`", statement).group(1)
            vids = json.loads(statement.split(" IN ", 1)[1].split(" RETURN ", 1)[0])
            return [[vid, b.vertices[tag][vid]["name"], b.vertices[tag][vid]["props"]]
                    for vid in vids if vid in b.vertices[tag]]
        if statement.startswith("FETCH PROP"):
            tag = re.search(r"ON `([^`]+)`", statement).group(1)
            parts = self._parts(statement.split("` ", 1)[1].split(" YIELD ", 1)[0])
            rows = []
            for i in range(0, len(parts), 3):
                key = tuple(parts[i:i + 3])
                if key in b.edges[tag]:
                    rows.append([*key, copy.deepcopy(b.edges[tag][key])])
            return rows
        if statement.startswith("INSERT"):
            self.assert_conditional(statement)
            b.insert_calls += 1
            if b.unsupported:
                raise GraphWriteError("synthetic unsupported IF", -1004)
            if b.concurrent:
                tag, key, value = b.concurrent
                b.vertices[tag][key] = value
                b.concurrent = None
            tag = re.search(r"EXISTS `([^`]+)`", statement).group(1)
            parts = self._parts(statement.split(" VALUES ", 1)[1])
            width = 3 if "VERTEX" in statement else 5
            for ordinal, start in enumerate(range(0, len(parts), width), 1):
                row = parts[start:start + width]
                if width == 3:
                    value = {"name": row[1], "props": row[2]}
                    b.vertices[tag].setdefault(row[0], value)
                else:
                    value = {"weight": row[3], "props": row[4]}
                    if b.corrupt:
                        value["weight"] += 0.125
                    b.edges[tag].setdefault(tuple(row[:3]), value)
                if b.fail_after == ordinal:
                    b.fail_after = None
                    if b.crash:
                        raise SimulatedCrash()
                    raise GraphWriteError("synthetic partial network loss")
            return []
        raise AssertionError("Unrecognized synthetic query: " + statement)

    @staticmethod
    def assert_conditional(statement):
        if " IF NOT EXISTS " not in statement:
            raise AssertionError("Writer attempted an unconditional write")


def entity(vid, name="姓名", batch=BATCH):
    return {"id": vid, "name": name, "props": {"batch": batch, "origin": "synthetic"}}


def edge(src="person:1", dst="person:2", **updates):
    value = {"src": src, "dst": dst, "rank": 0, "weight": 2.5,
             "props": {"batch": BATCH, "type": "M01", "count": 3}}
    value.update(updates)
    return value


class WriterChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.backend = Backend()
        self.writers = []

    def tearDown(self):
        for writer in self.writers:
            writer.close()
        self.temp.cleanup()

    def writer(self, name="journal.sqlite", **kwargs):
        value = FakeWriter(self.backend, self.root / name, **kwargs)
        self.writers.append(value)
        return value

    def source(self, records, name="source.jsonl"):
        path = self.root / name
        path.write_text("".join(_json(value) + "\n" for value in records), encoding="utf-8")
        return path

    def endpoints(self):
        self.backend.vertices["person"] = {
            "person:1": {"name": "old", "props": "T04 arbitrary props"},
            "person:2": {"name": "old2", "props": "{}"},
        }

    def pending(self, writer):
        return writer._db.execute("SELECT state,prior FROM batches").fetchall()

    def test_existing_entity_preserved_and_positive_cache(self):
        self.endpoints()
        old = copy.deepcopy(self.backend.vertices)
        writer = self.writer()
        stats = writer.apply_file("person", self.source([entity("person:1"), entity("person:2")]))
        self.assertEqual(stats["existing_other_batch"], 2)
        self.assertEqual(self.backend.vertices, old)
        self.assertEqual(self.backend.insert_calls, 0)
        before = sum(query.startswith("MATCH") for query in self.backend.queries)
        writer.apply_file("m01", self.source([edge()], "edges.jsonl"))
        after = sum(query.startswith("MATCH") for query in self.backend.queries)
        self.assertEqual(before, after, "confirmed Tag IDs should be cached")

    def test_new_entity_and_completed_resume(self):
        writer = self.writer()
        path = self.source([entity('person:quote"\\中文')])
        stats = writer.apply_file("person", path)
        self.assertEqual(stats["new_verified"], 1)
        self.assertEqual(self.pending(writer), [("verified", "{}")])
        calls = self.backend.insert_calls
        self.assertEqual(writer.apply_file("person", path), stats)
        self.assertEqual(calls, self.backend.insert_calls)

    def test_new_edge_and_canary_replay(self):
        self.endpoints()
        writer = self.writer()
        path = self.source([edge()])
        self.assertEqual(writer.apply_file("m01", path)["new_verified"], 1)
        old = copy.deepcopy(self.backend.edges)
        replay = self.writer("replay.sqlite")
        stats = replay.apply_file("m01", path)
        self.assertEqual(stats["existing_own_batch"], 1)
        self.assertEqual(stats["batch_owned_verified"], 1)
        self.assertEqual(self.backend.edges, old)

    def test_research_and_belong_edges_preserve_legacy_enterprise_edge(self):
        self.endpoints()
        self.backend.vertices["research"] = {
            "inst:1": {"name": "机构一", "props": "{}"},
            "inst:2": {"name": "机构二", "props": "{}"},
        }
        legacy_key = ("enterprise:old1", "enterprise:old2", 123)
        legacy = {"weight": 0.125, "props": "legacy enterprise evidence"}
        self.backend.edges["cooperate"][legacy_key] = copy.deepcopy(legacy)
        writer = self.writer()
        research = self.source([entity("inst:1"), entity("inst:2")], "research.jsonl")
        self.assertEqual(writer.apply_file("research", research)["existing_other_batch"], 2)
        m02 = self.source([edge(src="inst:1", dst="inst:2")], "m02.jsonl")
        m04 = self.source([edge(dst="inst:1", weight=0)], "m04.jsonl")
        self.assertEqual(writer.apply_file("m02", m02)["new_verified"], 1)
        self.assertEqual(writer.apply_file("m04", m04)["new_verified"], 1)
        self.assertEqual(self.backend.edges["cooperate"][legacy_key], legacy)
        self.assertIn(("person:1", "inst:1", 0), self.backend.edges["belong"])

    def test_missing_typed_endpoint_stops_without_advancing(self):
        self.endpoints()
        self.backend.vertices["person"]["inst:1"] = {"name": "wrong tag", "props": "{}"}
        writer = self.writer()
        with self.assertRaisesRegex(GraphWriteError, "endpoints are missing"):
            writer.apply_file("m04", self.source([edge(dst="inst:1")]))
        self.assertEqual(self.backend.insert_calls, 0)
        self.assertEqual(writer._db.execute("SELECT cursor,complete FROM files").fetchone(), (0, 0))
        self.assertEqual(writer.counts()["m04"]["missing_target"], 1)
        self.assertEqual(self.pending(writer)[0][0], "pending")

    def test_missing_endpoint_repair_resumes_and_clears_failure_audit(self):
        self.endpoints()
        writer = self.writer()
        path = self.source([edge(dst="inst:1")])
        with self.assertRaisesRegex(GraphWriteError, "endpoints are missing"):
            writer.apply_file("m04", path)
        with self.assertRaisesRegex(GraphWriteError, "endpoints are missing"):
            writer.apply_file("m04", path)
        self.assertEqual(self.backend.insert_calls, 0)
        self.assertEqual(writer.counts()["m04"]["missing_endpoint_records"], 1)
        self.backend.vertices["research"]["inst:1"] = {"name": "now present", "props": "{}"}
        stats = writer.apply_file("m04", path)
        self.assertEqual(stats["new_verified"], 1)
        self.assertEqual(stats["missing_endpoint_records"], 0)
        self.assertEqual(stats["missing_target"], 0)
        self.assertTrue(stats["completed"])
        self.assertEqual(self.pending(writer), [("verified", "{}")])

    def test_endpoint_repair_preserves_original_new_before_map(self):
        self.endpoints()
        self.backend.vertices["research"]["inst:1"] = {"name": "present", "props": "{}"}
        first, second = edge(dst="inst:1"), edge(src="person:2", dst="inst:2")
        writer = self.writer()
        path = self.source([first, second])
        with self.assertRaisesRegex(GraphWriteError, "endpoints are missing"):
            writer.apply_file("m04", path)
        self.backend.edges["belong"][("person:1", "inst:1", 0)] = writer._expected(writer._record("m04", first))
        self.backend.vertices["research"]["inst:2"] = {"name": "repaired", "props": "{}"}
        stats = writer.apply_file("m04", path)
        self.assertEqual(stats["new_verified"], 2)
        self.assertEqual(stats["existing_own_batch"], 0)

    def test_concurrent_entity_keeps_other_team_properties(self):
        value = {"name": "T04 won race", "props": '{"batch":"T04"}'}
        self.backend.concurrent = ("person", "person:1", value)
        writer = self.writer()
        stats = writer.apply_file("person", self.source([entity("person:1")]))
        self.assertEqual(self.backend.vertices["person"]["person:1"], value)
        self.assertEqual(stats["concurrent_other_batch"], 1)
        self.assertEqual(stats["new_verified"], 0)

    def test_partial_write_retry_is_idempotent(self):
        writer = self.writer()
        self.backend.fail_after = 1
        stats = writer.apply_file("person", self.source([entity("person:1"), entity("person:2")]))
        self.assertEqual(stats["new_verified"], 2)
        self.assertEqual(stats["write_attempts"], 2)
        self.assertEqual(len(self.backend.vertices["person"]), 2)

    def test_crash_and_resume_retains_original_before_map(self):
        self.backend.fail_after, self.backend.crash = 1, True
        path = self.source([entity("person:1"), entity("person:2")])
        writer = self.writer()
        with self.assertRaises(SimulatedCrash):
            writer.apply_file("person", path)
        self.assertEqual(writer._db.execute("SELECT cursor FROM files").fetchone()[0], 0)
        self.assertEqual(self.pending(writer)[0][0], "pending")
        writer.close()
        resumed = self.writer()
        stats = resumed.apply_file("person", path)
        self.assertEqual(stats["new_verified"], 2)
        self.assertEqual(stats["existing_own_batch"], 0)
        self.assertEqual(self.pending(resumed), [("verified", "{}")])

    def test_wrong_readback_remains_pending(self):
        self.endpoints()
        self.backend.corrupt = True
        writer = self.writer()
        with self.assertRaisesRegex(GraphWriteError, "exact expected"):
            writer.apply_file("m01", self.source([edge()]))
        self.assertEqual(writer._db.execute("SELECT cursor,complete FROM files").fetchone(), (0, 0))
        self.assertEqual(self.pending(writer)[0][0], "pending")

    def test_own_existing_edge_must_match_exactly(self):
        self.endpoints()
        self.backend.edges["cooperate"][("person:1", "person:2", 0)] = {
            "weight": 999.0, "props": _json(edge()["props"])}
        writer = self.writer()
        with self.assertRaisesRegex(GraphWriteError, "source snapshot"):
            writer.apply_file("m01", self.source([edge()]))
        self.assertEqual(self.backend.insert_calls, 0)

    def test_snapshot_and_config_mismatch_rejected(self):
        writer = self.writer()
        path = self.source([entity("person:1")])
        writer.apply_file("person", path)
        self.source([entity("person:2")])
        with self.assertRaisesRegex(GraphWriteError, "snapshot hash"):
            writer.apply_file("person", path)
        writer.close()
        with self.assertRaisesRegex(GraphWriteError, "target, batch"):
            self.writer(host="different")

    def test_pending_batch_size_is_bound(self):
        self.backend.fail_after, self.backend.crash = 1, True
        path = self.source([entity("person:1"), entity("person:2")])
        writer = self.writer()
        with self.assertRaises(SimulatedCrash):
            writer.apply_file("person", path, 2)
        with self.assertRaisesRegex(GraphWriteError, "batch identity differs"):
            writer.apply_file("person", path, 1)

    def test_unsupported_conditional_insert_has_no_fallback(self):
        self.backend.unsupported = True
        writer = self.writer()
        with self.assertRaises(GraphWriteError):
            writer.apply_file("person", self.source([entity("person:1")]))
        self.assertEqual(self.backend.insert_calls, 1)
        self.assertEqual(self.backend.vertices["person"], {})
        self.assertTrue(all(" IF NOT EXISTS " in query for query in self.backend.queries if query.startswith("INSERT")))

    def test_input_gates_and_duplicate_identities(self):
        writer = self.writer()
        for kind, record in [
            ("m01", edge(rank=1)), ("m01", edge(src="person:2", dst="person:1")),
            ("m01", edge(dst="person:1")), ("m04", edge()),
            ("m01", edge(weight=float("inf"))), ("m01", edge(weight=True)),
            ("person", entity("person:1", batch="wrong")),
        ]:
            with self.subTest(kind=kind, record=record):
                with self.assertRaises(GraphWriteError):
                    writer._record(kind, record)
        with self.assertRaisesRegex(GraphWriteError, "Duplicate canonical"):
            writer.apply_file("person", self.source([entity("person:1"), entity("person:1")]))
        self.assertEqual(self.backend.insert_calls, 0)

    def test_journal_exclusive_lock(self):
        self.writer()
        with self.assertRaisesRegex(GraphWriteError, "holds this journal"):
            self.writer()


if __name__ == "__main__":
    unittest.main(verbosity=2)
