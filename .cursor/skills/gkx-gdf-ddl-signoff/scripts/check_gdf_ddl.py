"""GDF 派单包签收自检。只读。退出码 0 才是通过。不打印口令。"""
import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PACK_ROOT = ROOT / "agent-delivery" / "data" / "GDF" / "派单包"
STORE_ROOT = ROOT / "agent-delivery" / "data" / "data-design" / "storage"

DIMS = {
    "policy": ("政策", "POLICY"),
    "ent": ("企业", "ENT"),
    "chain": ("产业链", "CHAIN"),
    "svc": ("服务机构", "SVC"),
}
OBSOLETE = ("禁止当现行", "已被", "已作废")
SQL_FENCE = re.compile(r"```sql\s*(.*?)```", re.S | re.I)
CREATE_RE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`[^`]+`\s*\.\s*)?`([^`]+)`\s*\((.*)\)\s*(.*)",
    re.S | re.I,
)


def dimension_from_task(task_id):
    upper = task_id.upper()
    if "POLICY" in upper:
        return "policy"
    if "CHAIN" in upper or "产业" in task_id:
        return "chain"
    if "SVC" in upper or "服务机构" in task_id:
        return "svc"
    if "ENT" in upper or "企业" in task_id:
        return "ent"
    sys.exit("无法从任务 ID 判断维度")


def latest_pack(dim):
    folder, _storage = DIMS[dim]
    base = PACK_ROOT / folder
    found = []
    for path in base.glob("GDF-*-WORKPACK-v*"):
        if not path.is_dir():
            continue
        readme = path / "README.md"
        head = readme.read_text(encoding="utf-8")[:400] if readme.exists() else ""
        if any(mark in head for mark in OBSOLETE):
            continue
        version = int(re.search(r"-v(\d+)$", path.name, re.I).group(1))
        found.append((version, path))
    if not found:
        for path in base.glob("GDF-*-WORKPACK"):
            if not path.is_dir():
                continue
            readme = path / "README.md"
            head = readme.read_text(encoding="utf-8")[:400] if readme.exists() else ""
            if any(mark in head for mark in OBSOLETE):
                continue
            found.append((0, path))
    if not found:
        sys.exit(f"没有现行派单包：{base}")
    return max(found)[1]


def sql_blocks(root):
    blocks = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for body in SQL_FENCE.findall(text):
            if re.search(r"CREATE\s+TABLE", body, re.I):
                blocks.append((path, body))
    return blocks


def split_items(body):
    items, buf, depth = [], [], 0
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            items.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        items.append(tail)
    return [item for item in items if item]


def norm_type(text):
    text = text.replace("`", "")
    return re.sub(r"\s+", " ", text.strip().lower())


def parse_create(sql):
    match = CREATE_RE.search(sql)
    if not match:
        return None
    schema_match = re.search(
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`([^`]+)`\s*\.\s*`([^`]+)`",
        sql,
        re.I,
    )
    schema = schema_match.group(1).lower() if schema_match else ""
    name, cols_raw, tail = match.group(1), match.group(2), match.group(3)
    columns, indexes = [], []
    for item in split_items(cols_raw):
        head = item.lstrip().lower()
        if head.startswith(("primary key", "unique key", "key ", "constraint", "index ")):
            indexes.append(norm_type(item))
            continue
        col = re.match(
            r"`([^`]+)`\s+([a-zA-Z0-9(),]+)(.*)",
            item,
            re.S,
        )
        if not col:
            continue
        rest = col.group(3)
        comment = re.search(r"COMMENT\s+'([^']*)'", rest, re.I)
        columns.append(
            (
                col.group(1).lower(),
                norm_type(col.group(2)),
                "not null" if re.search(r"\bNOT NULL\b", rest, re.I) else "null",
                norm_type(comment.group(1)) if comment else "",
            )
        )
    table_comment = re.search(r"COMMENT\s*=\s*'([^']*)'|COMMENT\s+'([^']*)'", tail, re.I)
    comment = ""
    if table_comment:
        comment = norm_type(table_comment.group(1) or table_comment.group(2) or "")
    charset = re.search(r"CHARSET\s*=\s*(\w+)|CHARACTER\s+SET\s+(\w+)", tail, re.I)
    collate = re.search(r"COLLATE\s*=\s*(\w+)", tail, re.I)
    return {
        "schema": schema,
        "columns": tuple(columns),
        "indexes": tuple(sorted(indexes)),
        "comment": comment,
        "charset": (charset.group(1) or charset.group(2) or "").lower() if charset else "",
        "collate": (collate.group(1) if collate else "").lower(),
    }


def collect(root):
    tables = {}
    for path, sql in sql_blocks(root):
        parsed = parse_create(sql)
        if not parsed:
            continue
        name = CREATE_RE.search(sql).group(1).lower()
        parsed["path"] = str(path.relative_to(ROOT))
        tables[name] = parsed
    return tables


def same(left, right):
    keys = ("columns", "indexes", "comment", "charset", "collate")
    return all(left[key] == right[key] for key in keys)


def diff_line(name, left, right):
    if left["columns"] != right["columns"]:
        return f"{name} 列或注释不一致"
    if left["indexes"] != right["indexes"]:
        return f"{name} 索引不一致"
    if left["comment"] != right["comment"] or left["charset"] != right["charset"] or left["collate"] != right["collate"]:
        return f"{name} 表注释或排序规则不一致"
    return f"{name} 不一致"


def live_signature(cursor, schema, table):
    cursor.execute(
        """
        SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
        ORDER BY ORDINAL_POSITION
        """,
        (schema, table),
    )
    rows = cursor.fetchall()
    if not rows:
        return None
    columns = tuple(
        (name.lower(), norm_type(col_type), "null" if nullable == "YES" else "not null", norm_type(comment or ""))
        for name, col_type, nullable, comment in rows
    )
    cursor.execute(
        """
        SELECT INDEX_NAME, NON_UNIQUE, SEQ_IN_INDEX, COLUMN_NAME
        FROM information_schema.STATISTICS
        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
        ORDER BY INDEX_NAME, SEQ_IN_INDEX
        """,
        (schema, table),
    )
    grouped = {}
    unique = {}
    for index_name, non_unique, _seq, column_name in cursor.fetchall():
        grouped.setdefault(index_name, []).append(column_name)
        unique[index_name] = non_unique
    indexes = []
    for index_name, cols in grouped.items():
        cols_sql = ", ".join(f"`{col}`" for col in cols)
        if index_name == "PRIMARY":
            indexes.append(norm_type(f"primary key ({cols_sql})"))
        elif unique[index_name] == 0:
            indexes.append(norm_type(f"unique key `{index_name}` ({cols_sql})"))
        else:
            indexes.append(norm_type(f"key `{index_name}` ({cols_sql})"))
    cursor.execute(
        """
        SELECT TABLE_COMMENT, TABLE_COLLATION
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
        """,
        (schema, table),
    )
    table_comment, collation = cursor.fetchone()
    charset = "utf8mb4" if (collation or "").startswith("utf8mb4") else ((collation or "").split("_", 1)[0])
    return {
        "columns": columns,
        "indexes": tuple(sorted(indexes)),
        "comment": norm_type(table_comment or ""),
        "charset": charset.lower(),
        "collate": (collation or "").lower(),
    }


def connect():
    password = os.environ.get("GKX_LUMEN_MYSQL_PASSWORD") or os.environ.get("MYSQL_PWD")
    if not password:
        return None, "未设置 GKX_LUMEN_MYSQL_PASSWORD，库未核对"
    try:
        import pymysql
    except ImportError:
        return None, "未安装 pymysql，库未核对"
    host = os.environ.get("GKX_LUMEN_MYSQL_HOST", "10.50.11.76")
    port = int(os.environ.get("GKX_LUMEN_MYSQL_PORT", "3306"))
    user = os.environ.get("GKX_LUMEN_MYSQL_USER", "gkxlumenx")
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, connect_timeout=8)
    except Exception as exc:
        return None, f"连库失败：{exc.__class__.__name__}"
    return conn, ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task")
    parser.add_argument("--dimension", choices=sorted(DIMS))
    args = parser.parse_args()
    dim = args.dimension or (dimension_from_task(args.task) if args.task else sys.exit("需要 --task 或 --dimension"))
    pack = latest_pack(dim)
    _folder, storage = DIMS[dim]
    store = STORE_ROOT / storage / "stores" / "mysql"
    md_tables = collect(store)
    pack_tables = collect(pack)
    failures = []
    names = sorted(set(md_tables) | set(pack_tables))
    if not names:
        failures.append("dwd.md/ads.md 与派单包都没有 CREATE TABLE")
    for name in names:
        if name not in md_tables:
            failures.append(f"{name} 在派单包有建表语句，dwd.md/ads.md 没有，不能算从 md 复制")
        elif name not in pack_tables:
            failures.append(f"{name} 在 dwd.md/ads.md 有建表语句，派单包未包含")
        elif not same(md_tables[name], pack_tables[name]):
            failures.append("派单包与 md " + diff_line(name, md_tables[name], pack_tables[name]))
        else:
            print(f"文件一致 {name}")
    conn, reason = connect()
    if conn is None:
        failures.append(reason)
    else:
        cur = conn.cursor()
        for name, spec in sorted(md_tables.items()):
            schema = spec["schema"]
            if schema.startswith("demo_"):
                pairs = [(schema, schema[len("demo_") :])]
            elif schema.startswith("gkxlumenx_"):
                pairs = [("demo_" + schema, schema)]
            else:
                pairs = [("demo_gkxlumenx_dwd", "gkxlumenx_dwd")]
                failures.append(f"{name} 建表语句未写库名，按 DWD 层核对")
            for demo_schema, lumen_schema in pairs:
                for label, live_schema in (("demo", demo_schema), ("lumen", lumen_schema)):
                    live = live_signature(cur, live_schema, name)
                    if live is None:
                        failures.append(f"{label} 库 {live_schema}.{name} 未建表")
                        continue
                    if not same(spec, live):
                        failures.append(f"{label} {live_schema} 与 md " + diff_line(name, spec, live))
                    else:
                        print(f"库一致 {live_schema}.{name}")
        conn.close()
    print(f"派单包 {pack.relative_to(ROOT)}")
    print(f"结构真源 {store.relative_to(ROOT)}")
    if failures:
        print("不通过")
        for item in failures:
            print(f"- {item}")
        return 1
    print("通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
