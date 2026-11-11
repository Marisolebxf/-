"""Read-only source export for the approved T03 batch.

The caller supplies an authenticated PyMySQL connection. Exported node IDs and
edge endpoints are complete target VIDs, and all edges have rank zero. This
module never connects to or writes to the graph database.
"""

from collections import Counter
from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import sys
import uuid


DATABASE = "gkx_technology_analysis_dev"
BATCH = "comply-2026-11-11-t03"
RULES_VERSION = "t03-tang-four-relations-20261111-v1"
FILES = ("person", "research", "m01", "m02", "m04")
TABLES = {
    "person": "ads_talent_profile",
    "research": "ads_institution_profile",
    "m01": "ads_talent_collaborator",
    "m02": "ads_institution_collaboration_yearly",
    "m04": "ads_talent_experience",
}
NAMES = ("name_zh", "name", "name_en", "name_original")
PROFILE_FIELDS = (
    "name", "name_zh", "name_en", "name_original", "institution_type_id",
    "country_code", "country_name", "province", "province_name", "city", "city_name",
    "current_institution", "current_institution_ids", "primary_topic_id",
    "paper_count", "patent_count", "project_count", "talent_count", "cited_by_count",
    "data_version", "update_time",
)
M01_FIELDS = (
    "talent_id", "collaborator_talent_id", "co_paper_count", "co_project_count",
    "co_patent_count", "first_collaboration_year", "latest_collaboration_year",
    "collaboration_score", "score_version", "metrics_as_of_date", "data_version",
)
M02_COUNTS = (
    "co_paper_count", "cross_author_co_paper_count", "multi_affiliation_paper_count",
    "co_paper_cited_by_count", "open_access_co_paper_count", "co_patent_count",
    "co_patent_family_count", "co_project_count",
)
M04_FIELDS = (
    "talent_id", "experience_id", "experience_type", "institution_id",
    "institution_type_id", "start_year", "end_year", "is_current", "position",
    "position_en", "data_version",
)


class SourceExportError(Exception):
    """A source export failure whose message is safe to display."""


def _now():
    return datetime.now(timezone.utc).isoformat()


def _log(message):
    print(message, file=sys.stderr, flush=True)


def _json_default(value):
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.decode("utf-8")
    raise TypeError("Unsupported source scalar type: {}".format(type(value).__name__))


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False, default=_json_default)


def _sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sql_table(table):
    return "`{}`.`{}`".format(DATABASE, table)


def _identifier(value):
    if not isinstance(value, str) or not value or value != value.strip():
        raise SourceExportError("A source business ID is empty or contains surrounding whitespace.")
    return value


def _number(value, field):
    if value is None:
        return 0.0
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise SourceExportError("Invalid numeric source field: {}.".format(field)) from None
    if isinstance(value, bool) or not math.isfinite(result) or result < 0:
        raise SourceExportError("Invalid numeric source field: {}.".format(field))
    return result


def _fetch_all(conn, query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            fields = [column[0] for column in cursor.description]
            return [row if isinstance(row, dict) else dict(zip(fields, row)) for row in cursor.fetchall()]
    except Exception as error:
        raise SourceExportError("Source metadata request failed ({}).".format(type(error).__name__)) from None


def _stream(conn, query):
    import pymysql.cursors

    try:
        with conn.cursor(pymysql.cursors.SSCursor) as cursor:
            cursor.execute(query)
            fields = [column[0] for column in cursor.description]
            for row in cursor:
                yield dict(zip(fields, row))
    except SourceExportError:
        raise
    except Exception as error:
        raise SourceExportError("Source streaming request failed ({}).".format(type(error).__name__)) from None


def _inspect(conn):
    result = {}
    for key, table in TABLES.items():
        schema = _fetch_all(conn, "SHOW COLUMNS FROM {};".format(_sql_table(table)))
        columns = [row["Field"] for row in schema]
        if not {"data_version", "update_time"}.issubset(columns):
            raise SourceExportError("Missing data_version/update_time in {}.".format(table))
        summary = _fetch_all(conn, (
            "SELECT COUNT(*) AS row_count, MAX(data_version) AS max_data_version, "
            "MIN(update_time) AS min_update_time, MAX(update_time) AS max_update_time FROM {};"
        ).format(_sql_table(table)))[0]
        result[key] = {
            "table": table, "columns": columns,
            "row_count": int(summary["row_count"]),
            "max_data_version": summary["max_data_version"],
            "min_update_time": summary["min_update_time"],
            "max_update_time": summary["max_update_time"],
        }
    return result


def _require(source, fields):
    missing = set(fields) - set(source["columns"])
    if missing:
        raise SourceExportError("Missing columns in {}: {}.".format(source["table"], ", ".join(sorted(missing))))


def _select(fields):
    return ", ".join("`{}`".format(field) for field in fields)


def _base_props(table, record_id):
    return {"batch": BATCH, "source_table": table, "source_record_id": record_id}


def _entities(conn, source, id_field, prefix):
    _require(source, (id_field,))
    fields = [id_field] + [field for field in PROFILE_FIELDS if field in source["columns"]]
    if not any(field in fields for field in NAMES):
        raise SourceExportError("No supported name column in {}.".format(source["table"]))
    if prefix == "inst:":
        _require(source, ("institution_type_id",))
    query = "SELECT {} FROM {} ORDER BY `{}`;".format(_select(fields), _sql_table(source["table"]), id_field)
    for row in _stream(conn, query):
        business_id = _identifier(row[id_field])
        name = next((row[field] for field in NAMES if row.get(field)), "")
        props = _base_props(source["table"], business_id)
        props.update(row)
        yield {"id": prefix + business_id, "name": name, "props": props}


def _m01(conn, source):
    _require(source, M01_FIELDS)
    query = (
        "SELECT {} FROM {} WHERE talent_id < collaborator_talent_id "
        "ORDER BY talent_id, collaborator_talent_id;"
    ).format(_select(M01_FIELDS), _sql_table(source["table"]))
    for row in _stream(conn, query):
        source_id = _identifier(row["talent_id"])
        target_id = _identifier(row["collaborator_talent_id"])
        if source_id >= target_id:
            raise SourceExportError("M01 returned a noncanonical or self-loop pair.")
        props = _base_props(source["table"], _json([source_id, target_id]))
        props.update(row)
        props.update(match_method="coauthor", m_number="M01", weight_field="collaboration_score")
        yield {"src": "person:" + source_id, "dst": "person:" + target_id,
               "rank": 0, "weight": _number(row["collaboration_score"], "collaboration_score"), "props": props}


def _m02(conn, source):
    required = (
        "institution_id", "collaborator_institution_id", "statistics_year",
        "institution_type_id", "collaborator_institution_type_id", "co_paper_count",
    )
    _require(source, required)
    counts = [field for field in M02_COUNTS if field in source["columns"]]
    select = [
        "y.institution_id", "y.collaborator_institution_id",
        "MIN(p1.institution_type_id) AS institution_type_id",
        "MAX(p1.institution_type_id) AS institution_type_max",
        "MIN(p2.institution_type_id) AS collaborator_institution_type_id",
        "MAX(p2.institution_type_id) AS collaborator_institution_type_max",
        "MIN(y.statistics_year) AS first_year", "MAX(y.statistics_year) AS latest_year",
        "COUNT(DISTINCT y.statistics_year) AS year_count", "COUNT(*) AS source_year_rows",
    ] + ["SUM(y.`{0}`) AS `{0}`".format(field) for field in counts]
    query = (
        "SELECT {} FROM {} y "
        "LEFT JOIN {profile} p1 ON p1.institution_id = y.institution_id "
        "LEFT JOIN {profile} p2 ON p2.institution_id = y.collaborator_institution_id "
        "WHERE y.institution_id < y.collaborator_institution_id "
        "AND COALESCE(p1.institution_type_id, 'unknown') <> 'company' "
        "AND COALESCE(p2.institution_type_id, 'unknown') <> 'company' "
        "AND y.statistics_year BETWEEN 2015 AND 2026 "
        "GROUP BY y.institution_id, y.collaborator_institution_id "
        "ORDER BY y.institution_id, y.collaborator_institution_id;"
    ).format(", ".join(select), _sql_table(source["table"]), profile=_sql_table(TABLES["research"]))
    for row in _stream(conn, query):
        source_id = _identifier(row["institution_id"])
        target_id = _identifier(row["collaborator_institution_id"])
        if "company" in (row["institution_type_id"], row["collaborator_institution_type_id"]):
            raise SourceExportError("M02 company filtering did not match the source profiles.")
        if source_id >= target_id or row["source_year_rows"] != row["year_count"]:
            raise SourceExportError("M02 source pair/year identity is not unique.")
        if (row["institution_type_id"] != row.pop("institution_type_max") or
                row["collaborator_institution_type_id"] != row.pop("collaborator_institution_type_max")):
            raise SourceExportError("M02 institution types change across years; resolve the source conflict.")
        props = _base_props(source["table"], _json([source_id, target_id]))
        props.update(row)
        props.update(match_method="coauthor", m_number="M02", weight_field="SUM(co_paper_count)",
                     aggregation="Annual base counts summed after selecting one mirror side; directional strengths and ranks are not summed.")
        yield {"src": "inst:" + source_id, "dst": "inst:" + target_id,
               "rank": 0, "weight": _number(row["co_paper_count"], "co_paper_count"), "props": props}


def _year(value):
    if value is None:
        return None
    try:
        result = int(value)
    except (TypeError, ValueError):
        raise SourceExportError("A source experience year is invalid.") from None
    if result < 1 or result > 9999:
        raise SourceExportError("A source experience year is outside the supported range.")
    return result


def _m04(conn, source, quality, research_types):
    _require(source, M04_FIELDS)
    query = (
        "SELECT {} FROM {} WHERE experience_type = 2 "
        "ORDER BY talent_id, institution_id, experience_id;"
    ).format(_select(M04_FIELDS), _sql_table(source["table"]))
    groups = {}
    seen_experiences = set()
    for row in _stream(conn, query):
        quality["m04_work_rows"] += 1
        talent_id = _identifier(row["talent_id"])
        institution_id = _identifier(row["institution_id"])
        experience_id = _identifier(row["experience_id"])
        if institution_id not in research_types:
            raise SourceExportError("M04 refers to an institution absent from the full source profile.")
        institution_type = research_types[institution_id]
        if institution_type == "company":
            quality["m04_company_rows"] += 1
            continue
        quality["m04_eligible_rows"] += 1
        experience_key = (talent_id, experience_id)
        if experience_key in seen_experiences:
            raise SourceExportError("M04 contains a repeated talent/experience source key.")
        seen_experiences.add(experience_key)
        key = (talent_id, institution_id)
        group = groups.setdefault(key, {
            "institution_type_id": institution_type, "source_institution_types": set(), "experience_ids": [],
            "start_years": [], "end_years": [], "positions": set(), "positions_en": set(),
            "is_current": False, "source_is_current": Counter(),
        })
        group["source_institution_types"].add(row["institution_type_id"])
        start_year, end_year = _year(row["start_year"]), _year(row["end_year"])
        if start_year is not None:
            group["start_years"].append(start_year)
        if end_year is not None:
            group["end_years"].append(end_year)
        group["is_current"] |= end_year is None or end_year >= 2026
        group["experience_ids"].append(experience_id)
        group["source_is_current"]["NULL" if row["is_current"] is None else str(row["is_current"])] += 1
        for field in ("position", "position_en"):
            if row[field]:
                group["positions" if field == "position" else "positions_en"].add(row[field])
    quality["m04_grouped_pairs"] = len(groups)
    for (talent_id, institution_id), group in sorted(groups.items()):
        props = _base_props(source["table"], _json([talent_id, institution_id]))
        props.update({
            "talent_id": talent_id, "institution_id": institution_id,
            "institution_type_id": group["institution_type_id"], "m_number": "M04",
            "source_institution_type_ids": sorted(group["source_institution_types"], key=lambda value: "" if value is None else str(value)),
            "experience_type": 2, "match_method": "employment_history_aggregated",
            "stint_count": len(group["experience_ids"]),
            "source_experience_ids": sorted(group["experience_ids"]),
            "first_start_year": min(group["start_years"]) if group["start_years"] else None,
            "last_end_year": max(group["end_years"]) if group["end_years"] else None,
            "positions": sorted(group["positions"]), "positions_en": sorted(group["positions_en"]),
            "is_current": group["is_current"],
            "is_current_rule": "ANY(end_year IS NULL OR end_year >= 2026), T03 ruling dated 2026-11-11",
            "source_is_current_counts": dict(group["source_is_current"]),
            "weight_field": "No strength defined by the ruling; 0 is used.",
        })
        yield {"src": "person:" + talent_id, "dst": "inst:" + institution_id,
               "rank": 0, "weight": 0.0, "props": props}


def _write_records(path, rows, entity_ids=None):
    count = 0
    previous = None
    with path.open("w", encoding="utf-8", newline="\n") as target:
        for record in rows:
            key = (record["id"],) if "id" in record else (record["src"], record["dst"], record["rank"])
            if entity_ids is not None and (record["src"] not in entity_ids or record["dst"] not in entity_ids):
                raise SourceExportError("An exported edge endpoint is absent from the full source entity population.")
            if previous is not None and key <= previous:
                raise SourceExportError("Source export keys are repeated or out of order in {}.".format(path.name))
            target.write(_json(record) + "\n")
            count += 1
            previous = key
            if count % 100000 == 0:
                _log("T03 source {}: {} records".format(path.name, count))
    _log("T03 source {} completed: {} records".format(path.name, count))
    return {"filename": path.name, "rows": count, "bytes": path.stat().st_size, "sha256": _sha256(path)}


def _resume(out_dir, source, exporter_sha):
    with (out_dir / "manifest.json").open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    if (manifest.get("status") != "complete" or manifest.get("format_version") != 1 or
            manifest.get("rules_version") != RULES_VERSION or manifest.get("batch") != BATCH or
            manifest.get("exporter_sha256") != exporter_sha or manifest.get("source") != json.loads(_json(source)) or
            manifest.get("source_after") != manifest.get("source")):
        raise SourceExportError("Existing T03 snapshot does not match this source/rule version; use a fresh directory.")
    for name in FILES:
        info = manifest["files"][name]
        path = out_dir / (name + ".jsonl")
        if info.get("filename") != path.name or not path.is_file() or _sha256(path) != info.get("sha256"):
            raise SourceExportError("Existing T03 snapshot checksum verification failed.")
    _log("Reusing verified complete T03 source snapshot.")
    return manifest


def export_snapshot(conn, out_dir: Path) -> dict:
    """Export approved source data, or reuse a complete matching snapshot.

    Metadata probes read COUNT and MAX(data_version) once per source table.
    Large exports use SSCursor. A sibling staging directory is renamed only
    after all files and the complete manifest have been written successfully.
    """
    out_dir = Path(out_dir)
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    started_at = _now()
    exporter_sha = _sha256(Path(__file__))
    source = _inspect(conn)
    if (out_dir / "manifest.json").is_file():
        return _resume(out_dir, source, exporter_sha)
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SourceExportError("T03 source snapshot is incomplete; use a fresh output directory.")
    lock_path = out_dir.with_name(out_dir.name + ".lock")
    try:
        lock = lock_path.open("x", encoding="utf-8")
    except FileExistsError:
        raise SourceExportError("Another T03 source exporter owns this snapshot directory.") from None
    stage = out_dir.with_name(out_dir.name + ".partial-" + uuid.uuid4().hex)
    try:
        lock.write(_now())
        lock.close()
        stage.mkdir()
        quality = Counter()
        files = {
            "person": _write_records(stage / "person.jsonl", _entities(conn, source["person"], "talent_id", "person:")),
            "research": _write_records(stage / "research.jsonl", _entities(conn, source["research"], "institution_id", "inst:")),
        }
        entity_ids = set()
        research_types = {}
        for name in ("person", "research"):
            with (stage / (name + ".jsonl")).open(encoding="utf-8") as handle:
                for line in handle:
                    record = json.loads(line)
                    entity_ids.add(record["id"])
                    if name == "research":
                        research_types[record["props"]["institution_id"]] = record["props"]["institution_type_id"]
        streams = {"m01": _m01(conn, source["m01"]), "m02": _m02(conn, source["m02"]),
                   "m04": _m04(conn, source["m04"], quality, research_types)}
        for name, rows in streams.items():
            files[name] = _write_records(stage / (name + ".jsonl"), rows, entity_ids)
        for name in ("person", "research"):
            if files[name]["rows"] != source[name]["row_count"]:
                raise SourceExportError("The full {} population changed during export.".format(name))
        source_after = _inspect(conn)
        if _json(source_after) != _json(source):
            raise SourceExportError("Source count/version/update-time metadata changed during export; use a fresh snapshot.")
        manifest = {
            "format_version": 1, "status": "complete", "rules_version": RULES_VERSION,
            "batch": BATCH, "space": "demo_gkx_chain", "source_database": DATABASE,
            "exporter_sha256": exporter_sha, "source": source, "source_after": source_after,
            "started_at": started_at, "finished_at": _now(), "files": files,
            "quality": dict(quality), "all_exported_edge_endpoints_in_source_profiles": True,
            "institution_type_authority": "ads_institution_profile for both endpoints; experience type values also preserved for audit",
            "physical_edge_policy": "One canonical physical edge per M01/M02 pair; M04 is person to research; rank=0.",
            "weight_mapping": {"m01": "collaboration_score; NULL -> 0, original NULL preserved",
                               "m02": "SUM(co_paper_count) after mirror deduplication and year/company filtering; all-NULL -> 0",
                               "m04": "0; no numeric strength prescribed"},
            "skipped_relations": {"M03": "Company endpoints are outside M03; no rows exported.",
                                  "M19": "Same evidence as M02; research_coop remains empty.",
                                  "M20": "Same evidence as M01; talent_coop remains empty."},
            "consistency": "Ordered read-only exports with source version/count probes; source-side transactional snapshot is not provided.",
        }
        with (stage / "manifest.json").open("w", encoding="utf-8", newline="\n") as target:
            target.write(_json(manifest) + "\n")
        if out_dir.exists():
            out_dir.rmdir()
        stage.replace(out_dir)
        return json.loads(_json(manifest))
    finally:
        lock.close()
        lock_path.unlink(missing_ok=True)
