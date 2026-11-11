"""T03 native Nebula conditional writer with resumable, verified batches.

The caller supplies credentials in memory. SQLite stores target configuration,
input hashes and batch evidence, never credentials. No schema changes are made.
"""

from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path
import sqlite3
import time


SPACE = "demo_gkx_chain"
BATCH = "comply-2026-11-11-t03"
VERSION = "1"
KINDS = {
    "person": ("person", None, None),
    "research": ("research", None, None),
    "m01": ("cooperate", "person", "person"),
    "m02": ("cooperate", "research", "research"),
    "m04": ("belong", "person", "research"),
}
PREFIXES = {"person": "person:", "research": "inst:"}
COUNTERS = (
    "source_records", "new_verified", "existing_own_batch", "existing_other_batch",
    "concurrent_other_batch", "missing_source", "missing_target", "missing_endpoint_records",
    "batch_owned_verified", "batches_verified", "write_attempts",
)


class GraphWriteError(RuntimeError):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _digest(value):
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for data in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(data)
    return digest.hexdigest()


def _cast(value):
    if hasattr(value, "is_null") and (value.is_null() or value.is_empty()):
        return None
    result = value.cast() if hasattr(value, "cast") else value
    if isinstance(result, bytes):
        return result.decode("utf-8")
    if isinstance(result, dict):
        return {_cast(key): _cast(item) for key, item in result.items()}
    return result


def _owner(properties):
    try:
        value = json.loads(properties.get("props") or "null")
    except (TypeError, ValueError):
        return None
    return value.get("batch") if isinstance(value, dict) else None


class GraphWriter:
    def __init__(self, host, port, user, password, space, journal_path):
        if space != SPACE:
            raise GraphWriteError("T03 is restricted to demo_gkx_chain.")
        self.host, self.port, self.space = host, int(port), space
        self._user, self._password = user, password
        self._pool = self._session = self._lock = self._db = None
        self._checked = False
        self._known_vertices = {tag: set() for tag in PREFIXES}
        self._journal = Path(journal_path)
        self._journal.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._acquire_lock()
            self._db = sqlite3.connect(self._journal, timeout=10)
            self._db.execute("PRAGMA synchronous=FULL")
            self._db.executescript("""
                CREATE TABLE IF NOT EXISTS settings (name TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS files (
                    kind TEXT PRIMARY KEY, sha256 TEXT NOT NULL, size INTEGER NOT NULL,
                    source_path TEXT NOT NULL, cursor INTEGER NOT NULL DEFAULT 0,
                    line INTEGER NOT NULL DEFAULT 0, complete INTEGER NOT NULL DEFAULT 0,
                    counts TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS batches (
                    kind TEXT NOT NULL, start INTEGER NOT NULL, finish INTEGER NOT NULL,
                    line_finish INTEGER NOT NULL, request_sha256 TEXT NOT NULL,
                    state TEXT NOT NULL, prior TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0,
                    summary TEXT, PRIMARY KEY (kind, start)
                );
            """)
            config = _json({"version": VERSION, "host": host, "port": self.port,
                            "space": space, "batch": BATCH, "rank": 0})
            old = self._db.execute("SELECT value FROM settings WHERE name='config'").fetchone()
            if old and old[0] != config:
                raise GraphWriteError("Journal target, batch or writer version differs from this run.")
            self._db.execute("INSERT OR IGNORE INTO settings VALUES ('config', ?)", (config,))
            self._db.commit()
            self._connect()
        except BaseException:
            self.close()
            raise

    def _acquire_lock(self):
        self._lock = self._journal.with_name(self._journal.name + ".lock").open("a+b")
        if os.name == "nt":
            import msvcrt
            if self._lock.tell() == 0:
                self._lock.write(b"0")
                self._lock.flush()
            self._lock.seek(0)
            try:
                msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                raise GraphWriteError("Another process holds this journal.") from None
        else:
            import fcntl
            try:
                fcntl.flock(self._lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise GraphWriteError("Another process holds this journal.") from None

    def _connect(self):
        from nebula3.Config import Config
        from nebula3.gclient.net import ConnectionPool
        config = Config()
        config.max_connection_pool_size = 1
        config.timeout = 120000
        self._pool = ConnectionPool()
        try:
            if not self._pool.init([(self.host, self.port)], config):
                raise GraphWriteError("Graph connection initialization failed.")
            self._session = self._pool.get_session(self._user, self._password)
            self._query("USE " + SPACE + ";")
        except GraphWriteError:
            raise
        except Exception as exc:
            raise GraphWriteError("Graph connection failed (" + type(exc).__name__ + ").") from None

    def _query(self, statement):
        try:
            result = self._session.execute(statement)
        except Exception as exc:
            raise GraphWriteError("Graph request failed (" + type(exc).__name__ + ").") from None
        if not result.is_succeeded():
            code = result.error_code()
            raise GraphWriteError("Graph statement failed with code " + str(code) + ".", code)
        return [[_cast(value) for value in result.row_values(i)] for i in range(result.row_size())]

    def preflight(self):
        schemas = {}
        for category, names, required in (
            ("TAG", ("person", "research"), {"name": "string", "props": "string"}),
            ("EDGE", ("cooperate", "belong"), {"weight": "double", "props": "string"}),
        ):
            for name in names:
                rows = self._query("DESCRIBE " + category + " `" + name + "`;")
                fields = {str(row[0]): str(row[1]).lower() for row in rows}
                if any(fields.get(key) != value for key, value in required.items()):
                    raise GraphWriteError("Required fields or types are missing from " + name + ".")
                schemas[name] = fields
        self._checked = True
        return {"host": self.host, "port": self.port, "space": self.space, "schemas": schemas}

    @staticmethod
    def _vid(value, tag):
        if not isinstance(value, str) or not value.startswith(PREFIXES[tag]):
            raise GraphWriteError("Input VID does not match its declared Tag.")
        if len(value) == len(PREFIXES[tag]) or len(value.encode("utf-8")) > 80:
            raise GraphWriteError("Input VID is empty or exceeds the approved byte length.")
        return value

    def _record(self, kind, record):
        tag, source_tag, target_tag = KINDS[kind]
        props = record.get("props")
        if isinstance(props, str):
            props = json.loads(props)
        if not isinstance(props, dict) or props.get("batch") != BATCH:
            raise GraphWriteError("Every input record must carry the fixed T03 props.batch.")
        props_text = _json(props)
        if source_tag is None:
            vid = self._vid(record.get("id"), tag)
            name = record.get("name")
            if not isinstance(name, str):
                raise GraphWriteError("An entity name must be a string.")
            return {"id": vid, "name": name, "props": props_text}
        source = self._vid(record.get("src"), source_tag)
        target = self._vid(record.get("dst"), target_tag)
        rank = record.get("rank", 0)
        if isinstance(rank, bool) or rank != 0:
            raise GraphWriteError("The approved canonical T03 rank is zero.")
        if source_tag == target_tag and source >= target:
            raise GraphWriteError("Canonical undirected pairs require src < dst and no self-loop.")
        weight = record.get("weight")
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or not math.isfinite(weight):
            raise GraphWriteError("An edge weight must be a finite number.")
        return {"src": source, "dst": target, "rank": 0, "weight": float(weight), "props": props_text}

    @staticmethod
    def _key(record):
        return record["id"] if "id" in record else _json([record["src"], record["dst"], record["rank"]])

    @staticmethod
    def _expected(record):
        names = ("name", "props") if "id" in record else ("weight", "props")
        return {key: record[key] for key in names}

    def _fetch_vertices(self, tag, vids):
        vids = sorted(set(vids))
        if not vids:
            return {}
        statement = (
            "MATCH (v:`" + tag + "`) WHERE id(v) IN " + _json(vids) +
            " RETURN id(v) AS vid, v." + tag + ".name AS name, v." + tag + ".props AS props;"
        )
        found = {}
        for vid, name, props in self._query(statement):
            if vid in found or vid not in vids:
                raise GraphWriteError("Vertex identity fetch returned duplicate or unexpected data.")
            found[vid] = {"name": name, "props": props}
        self._known_vertices[tag].update(found)
        return found

    def _fetch(self, kind, records):
        tag, source_tag, _ = KINDS[kind]
        if source_tag is None:
            return self._fetch_vertices(tag, [record["id"] for record in records])
        values = ",".join(_json(record["src"]) + "->" + _json(record["dst"]) + "@0" for record in records)
        statement = (
            "FETCH PROP ON `" + tag + "` " + values +
            " YIELD src(edge) AS src, dst(edge) AS dst, rank(edge) AS rank, properties(edge) AS attrs;"
        )
        allowed = {self._key(record) for record in records}
        found = {}
        for source, target, rank, attrs in self._query(statement):
            key = _json([source, target, rank])
            if key in found or key not in allowed or not isinstance(attrs, dict):
                raise GraphWriteError("Edge identity fetch returned duplicate or unexpected data.")
            if "weight" not in attrs or "props" not in attrs:
                raise GraphWriteError("Edge identity fetch omitted required properties.")
            found[key] = {"weight": attrs["weight"], "props": attrs["props"]}
        return found

    def _endpoint_presence(self, kind, records):
        _, source_tag, target_tag = KINDS[kind]
        if source_tag is None:
            return {}
        wanted = {}
        for record in records:
            wanted.setdefault(source_tag, set()).add(record["src"])
            wanted.setdefault(target_tag, set()).add(record["dst"])
        for tag, vids in wanted.items():
            self._fetch_vertices(tag, vids - self._known_vertices[tag])
        return {self._key(record): (record["src"] in self._known_vertices[source_tag], record["dst"] in self._known_vertices[target_tag])
                for record in records}

    def _insert(self, kind, records):
        if not records:
            return
        name, source_tag, _ = KINDS[kind]
        if source_tag is None:
            values = [_json(r["id"]) + ":(" + _json(r["name"]) + "," + _json(r["props"]) + ")" for r in records]
            statement = "INSERT VERTEX IF NOT EXISTS `" + name + "`(name,props) VALUES "
        else:
            values = [_json(r["src"]) + "->" + _json(r["dst"]) + "@0:(" + _json(r["weight"]) + "," + _json(r["props"]) + ")" for r in records]
            statement = "INSERT EDGE IF NOT EXISTS `" + name + "`(weight,props) VALUES "
        self._query(statement + ",".join(values) + ";")

    def _prepare(self, kind, records):
        current = self._fetch(kind, records)
        endpoints = self._endpoint_presence(kind, records)
        prior = {}
        for record in records:
            key = self._key(record)
            if key in endpoints and not all(endpoints[key]):
                prior[key] = {"state": "missing_endpoint", "source": endpoints[key][0], "target": endpoints[key][1]}
            elif key in current:
                prior[key] = {"state": "existing", "digest": _digest(current[key]), "own": _owner(current[key]) == BATCH}
            else:
                prior[key] = {"state": "new"}
        return prior

    def _verify(self, kind, records, prior, observed):
        stats = Counter(source_records=len(records), batches_verified=1)
        for record in records:
            key = self._key(record)
            old = prior[key]
            if old["state"] == "missing_endpoint":
                stats["missing_endpoint_records"] += 1
                stats["missing_source"] += not old["source"]
                stats["missing_target"] += not old["target"]
                continue
            if key not in observed:
                raise GraphWriteError("A submitted or preexisting identity is absent on readback.")
            value = observed[key]
            if old["state"] == "existing":
                if _digest(value) != old["digest"]:
                    raise GraphWriteError("A preexisting record changed while verifying this batch.")
                if old["own"] and KINDS[kind][1] is not None and value != self._expected(record):
                    raise GraphWriteError("A preexisting T03 edge differs from this source snapshot.")
                stats["existing_own_batch" if old["own"] else "existing_other_batch"] += 1
                stats["batch_owned_verified"] += old["own"]
            elif _owner(value) == BATCH:
                if value != self._expected(record):
                    raise GraphWriteError("A new T03 record differs from its exact expected values.")
                stats["new_verified"] += 1
                stats["batch_owned_verified"] += 1
            else:
                stats["existing_other_batch"] += 1
                stats["concurrent_other_batch"] += 1
        return {key: stats[key] for key in COUNTERS}

    def _apply_batch(self, kind, records, start, finish, line_finish):
        request_hash = _digest(records)
        entry = self._db.execute(
            "SELECT finish,line_finish,request_sha256,state,prior FROM batches WHERE kind=? AND start=?",
            (kind, start),
        ).fetchone()
        if entry:
            if entry[:3] != (finish, line_finish, request_hash) or entry[3] != "pending":
                raise GraphWriteError("Pending batch identity differs; restore the original input and batch size.")
            prior = json.loads(entry[4])
            # A missing endpoint batch has not submitted those edge identities.
            # Revalidate just those records after an operator restores the Tags;
            # never replace the original before-map of already writable records.
            missing_records = [record for record in records
                               if prior[self._key(record)]["state"] == "missing_endpoint"]
            if missing_records:
                prior.update(self._prepare(kind, missing_records))
                with self._db:
                    self._db.execute("UPDATE batches SET prior=?,summary=NULL WHERE kind=? AND start=?",
                                     (_json(prior), kind, start))
        else:
            prior = self._prepare(kind, records)
            with self._db:
                self._db.execute("INSERT INTO batches(kind,start,finish,line_finish,request_sha256,state,prior) VALUES(?,?,?,?,?,'pending',?)",
                                 (kind, start, finish, line_finish, request_hash, _json(prior)))
        missing = [value for value in prior.values() if value["state"] == "missing_endpoint"]
        if missing:
            audit = {"failure": "missing_endpoint", "missing_endpoint_records": len(missing),
                     "missing_source": sum(not value["source"] for value in missing),
                     "missing_target": sum(not value["target"] for value in missing)}
            with self._db:
                self._db.execute("UPDATE batches SET summary=? WHERE kind=? AND start=?", (_json(audit), kind, start))
            raise GraphWriteError("Typed edge endpoints are missing; the batch remains pending without advancing its cursor.")
        for attempt in range(3):
            with self._db:
                self._db.execute("UPDATE batches SET attempts=attempts+1 WHERE kind=? AND start=?", (kind, start))
            try:
                current = self._fetch(kind, records)
                writable = [record for record in records if prior[self._key(record)]["state"] == "new" and self._key(record) not in current]
                self._insert(kind, writable)
                observed = self._fetch(kind, records)
                summary = self._verify(kind, records, prior, observed)
                if KINDS[kind][1] is None:
                    self._known_vertices[KINDS[kind][0]].update(observed)
                attempts = self._db.execute("SELECT attempts FROM batches WHERE kind=? AND start=?", (kind, start)).fetchone()[0]
                summary["write_attempts"] = attempts
                stored = json.loads(self._db.execute("SELECT counts FROM files WHERE kind=?", (kind,)).fetchone()[0])
                totals = Counter(stored)
                totals.update(summary)
                with self._db:
                    self._db.execute("UPDATE batches SET state='verified',summary=?,prior='{}' WHERE kind=? AND start=?", (_json(summary), kind, start))
                    self._db.execute("UPDATE files SET cursor=?,line=?,counts=? WHERE kind=?", (finish, line_finish, _json(dict(totals)), kind))
                return
            except GraphWriteError as error:
                if error.code in (-1004, -1009) or attempt == 2:
                    raise
                time.sleep(0.25 * (attempt + 1))
                self._disconnect()
                self._connect()

    def apply_file(self, kind, path, batch_size=500):
        if kind not in KINDS or not isinstance(batch_size, int) or not 1 <= batch_size <= 1000:
            raise GraphWriteError("Select an approved kind and a batch size between 1 and 1000.")
        if not self._checked:
            self.preflight()
        path = Path(path).resolve()
        digest, size = _file_hash(path), path.stat().st_size
        entry = self._db.execute("SELECT sha256,size,cursor,line,complete FROM files WHERE kind=?", (kind,)).fetchone()
        if entry:
            if entry[:2] != (digest, size):
                raise GraphWriteError("Input snapshot hash or size changed for this journal kind.")
            if entry[4]:
                return self.counts()[kind]
            cursor, line = entry[2:4]
        else:
            with self._db:
                self._db.execute("INSERT INTO files(kind,sha256,size,source_path,counts) VALUES(?,?,?,?,?)",
                                 (kind, digest, size, str(path), _json({key: 0 for key in COUNTERS})))
            cursor, line = 0, 0
        with path.open("rb") as source:
            source.seek(cursor)
            while True:
                start = source.tell()
                records = []
                while len(records) < batch_size:
                    raw = source.readline()
                    if not raw:
                        break
                    line += 1
                    if raw.strip():
                        records.append(self._record(kind, json.loads(raw)))
                if not records:
                    break
                if len({self._key(record) for record in records}) != len(records):
                    raise GraphWriteError("Duplicate canonical identities occur inside an input batch.")
                self._apply_batch(kind, records, start, source.tell(), line)
                total = self.counts()[kind]
                if total["batches_verified"] % 20 == 0:
                    print(kind, "verified", total["source_records"], "new", total["new_verified"], "existing", total["existing_own_batch"] + total["existing_other_batch"], flush=True)
        if _file_hash(path) != digest:
            raise GraphWriteError("The input file changed during writing; its journal is not complete.")
        with self._db:
            self._db.execute("UPDATE files SET complete=1 WHERE kind=?", (kind,))
        return self.counts()[kind]

    def counts(self):
        result = {kind: dict(json.loads(stats), completed=bool(complete), snapshot_sha256=digest)
                  for kind, stats, complete, digest in self._db.execute("SELECT kind,counts,complete,sha256 FROM files ORDER BY kind")}
        for kind, summary in self._db.execute("SELECT kind,summary FROM batches WHERE state='pending' AND summary IS NOT NULL"):
            audit = json.loads(summary)
            if audit.get("failure") == "missing_endpoint":
                for key in ("missing_endpoint_records", "missing_source", "missing_target"):
                    result[kind][key] += audit[key]
        return result

    def _disconnect(self):
        if self._session is not None:
            try:
                self._session.release()
            except Exception:
                pass
            self._session = None
        if self._pool is not None:
            self._pool.close()
            self._pool = None

    def close(self):
        try:
            self._disconnect()
        finally:
            self._password = None
            if self._db is not None:
                self._db.close()
                self._db = None
            if self._lock is not None:
                self._lock.close()
                self._lock = None
