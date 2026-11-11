#!/usr/bin/env python3
"""Offline T03 source-export regressions; no SQL driver or database is needed."""

import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch


sys.dont_write_bytecode = True
SOURCE_PATH = Path(__file__).with_name("kg_comply_t03_source.py")
SPEC = importlib.util.spec_from_file_location("t03_source_under_test", SOURCE_PATH)
source = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(source)
ORIGINAL_INSPECT = source._inspect


def fixture():
    people = [{"talent_id": key, "name": key, "email": "excluded@example.invalid", "data_version": 1}
              for key in ("t1", "t2", "t3")]
    institutions = [{"institution_id": key, "name": key, "institution_type_id": kind, "data_version": 1}
                    for key, kind in (("i1", "education"), ("i2", "healthcare"), ("i3", "company"))]
    collaborators = []
    for left, right, score, papers in (("t1", "t2", 7, 5), ("t1", "t3", None, None)):
        for first, second in ((left, right), (right, left)):
            row = {field: None for field in source.M01_FIELDS}
            row.update(talent_id=first, collaborator_talent_id=second, co_paper_count=papers,
                       co_patent_count=2, collaboration_score=score, data_version=1)
            collaborators.append(row)
    experiences = []
    values = [
        ("t1", "i1", "e1", 2, 2010, 2020, None, "A"),
        ("t1", "i1", "e2", 2, 2021, None, 0, "B"),
        ("t2", "i2", "e3", 2, 2024, 2026, None, "C"),
        ("t3", "i2", "e4", 2, 2018, 2025, 1, "D"),
        ("t1", "i3", "e5", 2, 2015, 2020, None, "Excluded company"),
        ("t1", "i2", "e6", 1, 2005, 2009, None, "Excluded education"),
    ]
    for talent, institution, experience, kind, start, end, current, position in values:
        experiences.append(dict(talent_id=talent, institution_id=institution, experience_id=experience,
                                experience_type=kind, start_year=start, end_year=end, is_current=current,
                                institution_type_id="education", position=position, position_en=None,
                                data_version=1))
    return {"person": people, "research": institutions, "m01": collaborators, "m04": experiences}


def source_metadata(rows):
    result = {}
    for key, records in rows.items():
        fields = {field for record in records for field in record}
        fields.add("update_time")
        result[key] = {"table": source.TABLES[key], "columns": sorted(fields), "row_count": len(records),
                       "max_data_version": 1, "min_update_time": "2026-11-11T00:00:00",
                       "max_update_time": "2026-11-11T00:00:00"}
    return result


class SourceSelfcheck(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="t03-source-selfcheck-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.rows = fixture()
        self.metadata = source_metadata(self.rows)
        self.queries = []
        metadata_patch = patch.object(source, "_inspect", side_effect=lambda conn: copy.deepcopy(self.metadata))
        stream_patch = patch.object(source, "_stream", side_effect=self.stream)
        metadata_patch.start()
        stream_patch.start()
        self.addCleanup(metadata_patch.stop)
        self.addCleanup(stream_patch.stop)

    def stream(self, conn, query, parameters=None):
        """Small independent source fixture with assertions on the SQL contract."""
        self.queries.append(query)
        self.assertNotIn("ads_institution_collaboration_yearly", query)
        if source.TABLES["m01"] in query:
            self.assertIn("WHERE talent_id < collaborator_talent_id", query)
            self.assertNotIn("OFFSET", query)
            limit = int(re.search(r"LIMIT (\d+)", query).group(1))
            rows = sorted((copy.deepcopy(row) for row in self.rows["m01"]
                           if row["talent_id"] < row["collaborator_talent_id"]),
                          key=lambda row: (row["talent_id"], row["collaborator_talent_id"]))
            if parameters is not None:
                self.assertEqual(parameters[0], parameters[1])
                self.assertIn("talent_id > %s", query)
                self.assertIn("collaborator_talent_id > %s", query)
                rows = [row for row in rows if (row["talent_id"], row["collaborator_talent_id"]) >
                        (parameters[0], parameters[2])]
            return iter(rows[:limit])
        if source.TABLES["m04"] in query:
            self.assertIn("WHERE experience_type = 2", query)
            return iter(copy.deepcopy([row for row in self.rows["m04"] if row["experience_type"] == 2]))
        for key in ("person", "research"):
            if source.TABLES[key] in query:
                fields = re.findall(r"`([^`]+)`", query.split(" FROM ")[0])
                id_field = "talent_id" if key == "person" else "institution_id"
                return iter([{field: row.get(field) for field in fields}
                             for row in sorted(self.rows[key], key=lambda row: row[id_field])])
        self.fail("Unexpected source query")

    def export(self, name="snapshot"):
        target = self.directory / name
        manifest = source.export_snapshot(object(), target)
        records = {key: [json.loads(line) for line in (target / (key + ".jsonl")).read_text(encoding="utf-8").splitlines()]
                   for key in source.FILES}
        return target, manifest, records

    def test_full_export_mirrors_and_work_stints(self):
        target, manifest, records = self.export()
        self.assertEqual(len(records["person"]), 3)
        self.assertEqual(len(records["research"]), 3)  # Company master data is retained.
        self.assertNotIn("email", records["person"][0]["props"])
        self.assertEqual(len(records["m01"]), 2)
        self.assertEqual(records["m01"][0]["weight"], 7)
        self.assertEqual(records["m01"][1]["weight"], 0)
        self.assertIsNone(records["m01"][1]["props"]["collaboration_score"])
        work = records["m04"][0]["props"]
        self.assertEqual(work["stint_count"], 2)
        self.assertEqual(work["source_experience_ids"], ["e1", "e2"])
        self.assertEqual(work["positions"], ["A", "B"])
        self.assertEqual((work["first_start_year"], work["last_end_year"]), (2010, 2020))
        self.assertTrue(work["is_current"])
        self.assertEqual(work["source_is_current_counts"], {"NULL": 1, "0": 1})
        self.assertTrue(records["m04"][1]["props"]["is_current"])  # Ends in the cutoff year.
        self.assertFalse(records["m04"][2]["props"]["is_current"])  # Source value 1 remains auditable.
        self.assertEqual(manifest["quality"], {"m04_work_rows": 5, "m04_company_rows": 1,
                                             "m04_eligible_rows": 4, "m04_grouped_pairs": 3})
        for key, rows in records.items():
            self.assertEqual(manifest["files"][key]["rows"], len(rows))
            self.assertEqual(manifest["files"][key]["sha256"], source._sha256(target / (key + ".jsonl")))
            self.assertTrue(all(record["props"]["batch"] == source.BATCH for record in rows))
        self.assertEqual(manifest["source"], manifest["source_after"])

    def test_completed_cache_reuses_without_streaming(self):
        target, manifest, _ = self.export()
        self.queries.clear()
        self.assertEqual(source.export_snapshot(object(), target), manifest)
        self.assertEqual(self.queries, [])

    def test_checksum_corruption_rejected(self):
        target, _, _ = self.export()
        with (target / "m01.jsonl").open("a", encoding="utf-8") as handle:
            handle.write("{}\n")
        with self.assertRaisesRegex(source.SourceExportError, "checksum"):
            source.export_snapshot(object(), target)

    def test_partial_snapshot_rejected(self):
        target = self.directory / "partial"
        target.mkdir()
        (target / "person.jsonl").write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(source.SourceExportError, "incomplete"):
            source.export_snapshot(object(), target)

    def test_source_change_prevents_manifest_publication(self):
        changed = copy.deepcopy(self.metadata)
        changed["m04"]["max_data_version"] = 2
        target = self.directory / "changed"
        with patch.object(source, "_inspect", side_effect=[copy.deepcopy(self.metadata), changed]):
            with self.assertRaisesRegex(source.SourceExportError, "changed during export"):
                source.export_snapshot(object(), target)
        self.assertFalse(target.exists())
        self.assertFalse(target.with_name(target.name + ".lock").exists())

    def test_missing_entity_endpoint_fails_closed(self):
        self.rows["m01"][0]["collaborator_talent_id"] = "t9"
        with self.assertRaisesRegex(source.SourceExportError, "endpoint"):
            self.export()
        self.assertFalse((self.directory / "snapshot").exists())

    def test_missing_required_field_fails_closed(self):
        self.metadata["m01"]["columns"].remove("collaboration_score")
        with self.assertRaisesRegex(source.SourceExportError, "Missing columns"):
            self.export()

    def test_repeated_experience_key_fails_closed(self):
        self.rows["m04"].append(copy.deepcopy(self.rows["m04"][0]))
        with self.assertRaisesRegex(source.SourceExportError, "repeated talent/experience"):
            self.export()

    def test_m01_keyset_pages_preserve_same_left_id(self):
        with patch.object(source, "M01_PAGE_SIZE", 1):
            _, manifest, records = self.export()
        self.assertEqual([(row["src"], row["dst"]) for row in records["m01"]],
                         [("person:t1", "person:t2"), ("person:t1", "person:t3")])
        self.assertEqual(manifest["files"]["m01"]["rows"], 2)
        self.assertEqual(sum(source.TABLES["m01"] in query for query in self.queries), 3)

    def test_source_error_details_are_bounded_and_redacted(self):
        message = source._safe_source_error(Exception(2013, "Lost connection; password=abc token=xyz mysql://u:p@db " + "x" * 500))
        self.assertIn("code=2013", message)
        self.assertIn("Lost connection", message)
        self.assertNotIn("abc", message)
        self.assertNotIn("xyz", message)
        self.assertNotIn("u:p", message)
        self.assertLessEqual(len(message.split("detail=", 1)[1]), 300)

    def test_scope_v2_never_inspects_or_exports_m02(self):
        self.assertEqual(source.FILES, ("person", "research", "m01", "m04"))
        self.assertEqual(set(source.TABLES), set(source.FILES))
        self.assertIn("v2-scope832923ec", source.RULES_VERSION)
        self.assertFalse(hasattr(source, "_m02"))
        # Exercise actual metadata SQL generation as well as the streamed export.
        def metadata_query(conn, query):
            self.assertNotIn("ads_institution_collaboration_yearly", query)
            self.queries.append(query)
            if query.startswith("SHOW COLUMNS"):
                return [{"Field": "data_version"}, {"Field": "update_time"}]
            return [{"row_count": 1, "max_data_version": 1,
                     "min_update_time": None, "max_update_time": None}]
        with patch.object(source, "_fetch_all", side_effect=metadata_query):
            self.assertEqual(set(ORIGINAL_INSPECT(object())), set(source.FILES))
        target, manifest, records = self.export()
        self.assertEqual(set(manifest["files"]), set(source.FILES))
        self.assertEqual(set(manifest["source"]), set(source.FILES))
        self.assertNotIn("m02", manifest["weight_mapping"])
        self.assertIn("T02", manifest["skipped_relations"]["M02"])
        self.assertIn("T02", manifest["skipped_relations"]["M19"])
        self.assertFalse((target / "m02.jsonl").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
