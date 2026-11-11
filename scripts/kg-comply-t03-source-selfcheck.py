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
    yearly = []
    for left, right, year, count in (("i1", "i2", 2015, 2), ("i1", "i2", 2018, 3),
                                     ("i1", "i2", 2026, 5), ("i1", "i2", 2014, 900),
                                     ("i1", "i3", 2024, 100)):
        for first, second in ((left, right), (right, left)):
            row = {field: None for field in source.M02_COUNTS}
            row.update(institution_id=first, collaborator_institution_id=second, statistics_year=year,
                       institution_type_id="education", collaborator_institution_type_id="education",
                       co_paper_count=count, collaboration_strength=0.75, data_version=1)
            yearly.append(row)
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
    return {"person": people, "research": institutions, "m01": collaborators,
            "m02": yearly, "m04": experiences}


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

    def stream(self, conn, query):
        """Small independent source fixture with assertions on the SQL contract."""
        self.queries.append(query)
        if "GROUP BY" in query:
            return iter(self.aggregate_yearly(query))
        if source.TABLES["m01"] in query:
            self.assertIn("WHERE talent_id < collaborator_talent_id", query)
            return iter(sorted((copy.deepcopy(row) for row in self.rows["m01"]
                                if row["talent_id"] < row["collaborator_talent_id"]),
                               key=lambda row: (row["talent_id"], row["collaborator_talent_id"])))
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

    def aggregate_yearly(self, query):
        for clause in ("y.institution_id < y.collaborator_institution_id", "p1.institution_type_id",
                       "p2.institution_type_id", "BETWEEN 2015 AND 2026",
                       "COUNT(DISTINCT y.statistics_year)",
                       "GROUP BY y.institution_id, y.collaborator_institution_id"):
            self.assertIn(clause, query)
        self.assertNotRegex(query, r"SUM\([^)]*(strength|rank|fwci|shared_author_count)")
        types = {row["institution_id"]: row["institution_type_id"] for row in self.rows["research"]}
        groups = {}
        for row in self.rows["m02"]:
            left, right, year = row["institution_id"], row["collaborator_institution_id"], row["statistics_year"]
            if left >= right or not 2015 <= year <= 2026 or "company" in (types.get(left), types.get(right)):
                continue
            groups.setdefault((left, right), []).append(row)
        result = []
        for (left, right), records in sorted(groups.items()):
            years = {row["statistics_year"] for row in records}
            row = dict(institution_id=left, collaborator_institution_id=right,
                       institution_type_id=types.get(left), institution_type_max=types.get(left),
                       collaborator_institution_type_id=types.get(right),
                       collaborator_institution_type_max=types.get(right),
                       first_year=min(years), latest_year=max(years), year_count=len(years),
                       source_year_rows=len(records))
            for field in source.M02_COUNTS:
                values = [record.get(field) for record in records if record.get(field) is not None]
                row[field] = sum(values) if values else None
            result.append(row)
        return result

    def export(self, name="snapshot"):
        target = self.directory / name
        manifest = source.export_snapshot(object(), target)
        records = {key: [json.loads(line) for line in (target / (key + ".jsonl")).read_text(encoding="utf-8").splitlines()]
                   for key in source.FILES}
        return target, manifest, records

    def test_full_export_mirrors_years_and_work_stints(self):
        target, manifest, records = self.export()
        self.assertEqual(len(records["person"]), 3)
        self.assertEqual(len(records["research"]), 3)  # Company master data is retained.
        self.assertNotIn("email", records["person"][0]["props"])
        self.assertEqual(len(records["m01"]), 2)
        self.assertEqual(records["m01"][0]["weight"], 7)
        self.assertEqual(records["m01"][1]["weight"], 0)
        self.assertIsNone(records["m01"][1]["props"]["collaboration_score"])
        self.assertEqual(len(records["m02"]), 1)
        institution = records["m02"][0]
        self.assertEqual(institution["weight"], 10)
        self.assertEqual(institution["props"]["year_count"], 3)
        self.assertEqual((institution["props"]["first_year"], institution["props"]["latest_year"]), (2015, 2026))
        self.assertEqual(institution["props"]["collaborator_institution_type_id"], "healthcare")
        self.assertIsNone(institution["props"]["co_project_count"])
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
        changed["m02"]["max_data_version"] = 2
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

    def test_repeated_canonical_pair_year_fails_closed(self):
        self.rows["m02"].append(copy.deepcopy(self.rows["m02"][0]))
        with self.assertRaisesRegex(source.SourceExportError, "pair/year identity"):
            self.export()


if __name__ == "__main__":
    unittest.main(verbosity=2)
