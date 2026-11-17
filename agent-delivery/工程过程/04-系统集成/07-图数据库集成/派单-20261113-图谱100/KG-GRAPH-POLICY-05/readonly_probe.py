"""Policy audit: explicit read-only statements, credentials only from environment.

Run with pymysql + nebula3-python. Input JSON is a list of
{id, engine: mysql|graph, query}. No host/user/password is saved in evidence.
Graph queries must anchor a Tag; abort on first error (including high watermark).
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import time


def run(jobs, output):
    result = {"task_id": "KG-GRAPH-POLICY-05", "started_at": dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(), "read_only": True, "queries": []}
    mysql = pool = session = None
    try:
        for job in jobs:
            q = job["query"].strip().rstrip(";")
            if ";" in q or not re.match(r"^(SELECT|SHOW|DESCRIBE|MATCH|FETCH)\b", q, re.I):
                raise ValueError("Only single read-only statements are allowed")
            if job["engine"] == "graph" and q.upper().startswith("MATCH") and not re.search(r"\(\w+:\w+\)", q):
                raise ValueError("Graph MATCH requires an explicit Tag anchor")
            entry = {**job, "started_at": dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat()}
            started = time.monotonic()
            try:
                if job["engine"] == "mysql":
                    import pymysql
                    if mysql is None:
                        mysql = pymysql.connect(host=os.environ["POLICY_MYSQL_HOST"], port=int(os.environ["POLICY_MYSQL_PORT"]), user=os.environ["POLICY_MYSQL_USER"], password=os.environ["POLICY_MYSQL_PASSWORD"], charset="utf8mb4", connect_timeout=8, read_timeout=25, write_timeout=8, cursorclass=pymysql.cursors.DictCursor)
                        with mysql.cursor() as cur:
                            cur.execute("SET SESSION MAX_EXECUTION_TIME=20000")
                            cur.execute("START TRANSACTION READ ONLY")
                    with mysql.cursor() as cur:
                        cur.execute(q)
                        entry["rows"] = cur.fetchall()
                elif job["engine"] == "graph":
                    from nebula3.gclient.net import ConnectionPool
                    from nebula3.Config import Config
                    if pool is None:
                        pool = ConnectionPool()
                        config = Config()
                        config.timeout = 25000
                        config.max_connection_pool_size = 1
                        if not pool.init([(os.environ["POLICY_GRAPH_HOST"], int(os.environ["POLICY_GRAPH_PORT"]))], config):
                            raise RuntimeError("Graph connection failed")
                        session = pool.get_session(os.environ["POLICY_GRAPH_USER"], os.environ["POLICY_GRAPH_PASSWORD"])
                        selected = session.execute("USE demo_gkx_chain")
                        if not selected.is_succeeded():
                            raise RuntimeError(str(selected.error_msg()))
                    res = session.execute(q)
                    if not res.is_succeeded():
                        raise RuntimeError(str(res.error_msg()))
                    entry["rows"] = res.as_primitive()
                else:
                    raise ValueError("Unknown engine")
                entry["status"] = "success"
            except Exception as exc:
                # Avoid storing an exception's potentially credential-bearing connection repr.
                entry["status"] = "error"
                entry["error_type"] = type(exc).__name__
                entry["error"] = str(exc)
                for key, val in os.environ.items():
                    if key.startswith("POLICY_") and val and ("PASSWORD" in key or "USER" in key or "HOST" in key):
                        entry["error"] = entry["error"].replace(val, "[redacted]")
                raise
            finally:
                entry["elapsed_seconds"] = round(time.monotonic() - started, 3)
                result["queries"].append(entry)
                Path(output).write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
                print(job["id"], entry["status"], entry["elapsed_seconds"], flush=True)
    finally:
        if mysql:
            mysql.rollback()
            mysql.close()
        if session:
            session.release()
        if pool:
            pool.close()
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("output")
    args = ap.parse_args()
    run(json.loads(Path(args.jobs).read_text(encoding="utf-8")), args.output)
