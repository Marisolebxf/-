# GDF 作业 POLICY-C2：把政策正文切成条款，合并进 ADS policy_text_parse。
# 把本文件复制到 GDF 的 Python 节点（人工拷贝或同步均可）。
# 在国内、国际两张平面当日都洗进 policy_base_info 且 success 之后执行。
# 不调用国科信的 HTTP 接口。规则没切开时，才用模型兜底；无密钥或失败不写假条款。
#
# 依赖：Python 3.9+、pymysql。模型可选：
#   LLM_BASE_URL  LLM_API_KEY  LLM_MODEL（默认 glm-5.3-flash）
# 库连接同 policy_c1_industry.py 的 POLICY_MYSQL_* / POLICY_DWD_DB / POLICY_ADS_DB。
#
#   python policy_c2_clauses.py --limit 100
#   python policy_c2_clauses.py --policy-id <id> [--force]
#   python policy_c2_clauses.py --self-check

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime

_CN = "一二三四五六七八九十"
ARTICLE_SPLIT = re.compile(r"(?=第[0-9０-９一二三四五六七八九十百千]+条)")
ARTICLE_HEAD = re.compile(r"^(第[0-9０-９一二三四五六七八九十百千]+条)")
HEADING_SPLIT = re.compile(rf"(?:(?<=^)|(?<=[\n。；;]))\s*(?=(?:（[{_CN}]+）|[{_CN}]+、|\d{{1,2}}[.、]))")
HEADING_HEAD = re.compile(rf"^(?:（[{_CN}]+）|[{_CN}]+、|\d{{1,2}}[.、])")
AMOUNT_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:亿元|万元|元|%|个百分点)")
TARGET_RE = re.compile(r"(?:适用对象|支持对象|申报主体)[:：]?\s*([^。；;\n]{2,40})")
CATEGORIES = ("补贴标准", "准入条件", "扶持措施", "保障机制", "责任主体", "政策目标")


def _split_marked(text: str, splitter: re.Pattern, head: re.Pattern) -> list[tuple[str, str]]:
    out = []
    for part in splitter.split(str(text or "")):
        part = part.strip()
        matched = head.match(part)
        if not matched:
            continue
        body = part[matched.end():].strip()
        if body:
            out.append((matched.group(0).strip(), body[:400]))
    return out


def split_articles(text: str) -> list[tuple[str, str]]:
    raw = str(text or "").strip()
    if not raw:
        return []
    numbered = _split_marked(raw, ARTICLE_SPLIT, ARTICLE_HEAD)
    return numbered or _split_marked(raw, HEADING_SPLIT, HEADING_HEAD)


def pick_category(body: str, amount: str) -> str:
    if any(k in body for k in ("负责", "主管部门", "牵头")):
        return "责任主体"
    if any(k in body for k in ("保障", "监督", "考核")):
        return "保障机制"
    if amount or any(k in body for k in ("补贴", "资助", "奖励", "万元", "亿元")):
        return "补贴标准"
    if any(k in body for k in ("申报", "准入", "资质", "应当", "须")):
        return "准入条件"
    if any(k in body for k in ("目标", "为了", "旨在")):
        return "政策目标"
    return "扶持措施"


def _support(elements: dict) -> str:
    support = elements.get("支持方式")
    if isinstance(support, list):
        return "、".join(str(x).strip() for x in support if str(x).strip())
    return str(support or "").strip()


def classify_article(no: str, body: str, elements: dict) -> dict:
    amount_m = AMOUNT_RE.search(body)
    amount = amount_m.group(0).replace(" ", "") if amount_m else ""
    target_m = TARGET_RE.search(body)
    target = target_m.group(1).strip() if target_m else str(elements.get("适用对象") or "").strip()
    cond = body[:80] if pick_category(body, amount) == "准入条件" else ""
    return {
        "no": no, "category": pick_category(body, amount), "target": target,
        "support_type": _support(elements), "amount": amount, "condition": cond, "excerpt": body[:180],
    }


def elements_of(row: dict) -> dict:
    for key in ("policy_support", "elements"):
        raw = row.get(key)
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str) and raw.strip().startswith("{"):
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict):
                return data
    return {}


def elements_clause(elements: dict) -> dict | None:
    target = str(elements.get("适用对象") or "").strip()
    support = _support(elements)
    cond = str(elements.get("申报条件") or "").strip()
    if not (target or support or cond):
        return None
    if support:
        category = "扶持措施"
    elif cond:
        category = "准入条件"
    else:
        category = "政策目标"
    return {
        "no": "", "category": category, "target": target, "support_type": support,
        "amount": "", "condition": cond[:80], "excerpt": "",
    }


def content_hash(row: dict) -> str:
    raw = f"{row.get('title') or ''}\n{row.get('abstract') or ''}\n{row.get('content') or ''}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def llm_window(row: dict) -> str:
    title = str(row.get("title") or "").strip()
    abstract = str(row.get("abstract") or "").strip()[:400]
    content = str(row.get("content") or "").strip()[:1200]
    return f"{title}\n{abstract}\n{content}".strip()


def accept_llm_item(item: dict, window: str, elements: dict) -> dict | None:
    excerpt = str(item.get("excerpt") or "").strip()
    if len(excerpt) < 4 or excerpt not in window:
        return None
    no = str(item.get("no") or "").strip()
    if no and no not in window:
        no = ""
    amount = str(item.get("amount") or "").strip()
    if amount and amount not in window:
        amount = ""
    category = str(item.get("category") or "").strip()
    if category not in CATEGORIES:
        category = pick_category(excerpt, amount)
    return {
        "no": no, "category": category,
        "target": str(item.get("target") or elements.get("适用对象") or "").strip(),
        "support_type": "", "amount": amount,
        "condition": str(item.get("condition") or "").strip()[:80],
        "excerpt": excerpt[:180],
    }


def llm_clauses(row: dict):
    base = os.environ.get("LLM_BASE_URL", "").strip().rstrip("/")
    key = os.environ.get("LLM_API_KEY", "").strip()
    if not base or not key:
        return None
    window = llm_window(row)
    if not window:
        return None
    url = base if base.endswith("/chat/completions") else f"{base}/chat/completions"
    model = os.environ.get("LLM_MODEL", "").strip() or "glm-5.3-flash"
    body = {
        "model": model,
        "temperature": 0.1,
        "max_tokens": 800,
        "messages": [
            {"role": "system", "content": "你是政策条款抽取助手。只根据给定原文抽取，禁止编造原文没有的句子、金额和条款号。excerpt 必须是原文里的连续片段。"},
            {"role": "user", "content": "从下面政策文本抽出条款。只输出 JSON：{\"clauses\":[{\"no\":\"\",\"category\":\"补贴标准|准入条件|扶持措施|保障机制|责任主体|政策目标\",\"target\":\"\",\"amount\":\"\",\"condition\":\"\",\"excerpt\":\"\"}]}\n没有把握就返回 {\"clauses\":[]}。\n\n" + window},
        ],
    }
    req = urllib.request.Request(
        url, data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.load(resp)
        raw = payload["choices"][0]["message"]["content"]
    except (OSError, ValueError, KeyError, IndexError, urllib.error.URLError) as exc:
        print(f"llm failed: {exc}", file=sys.stderr)
        return []
    data = str(raw or "").strip()
    if data.startswith("```"):
        data = data.strip("`")
        if data.lower().startswith("json"):
            data = data[4:].strip()
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError:
        return []
    if isinstance(parsed, dict):
        parsed = parsed.get("clauses") or parsed.get("items") or []
    items = parsed if isinstance(parsed, list) else []
    return {"clauses": [item for item in items if isinstance(item, dict)], "model_version": f"clause-llm-{model}"}


def structure_one(row: dict, blob: dict, *, force: bool) -> dict | None:
    """返回要写入的条款和 meta。None 表示跳过、不写。"""
    existing = blob.get("clauses") if isinstance(blob.get("clauses"), list) else []
    if existing and not force:
        return None
    elements = elements_of(row)
    articles = split_articles(row.get("content") or "") or split_articles(row.get("abstract") or "")
    digest = content_hash(row)
    if articles:
        return {
            "clauses": [classify_article(no, body, elements) for no, body in articles],
            "meta": {"source": "rule", "content_hash": digest, "llm_tried": False, "model_version": "clause-rule-v1"},
        }
    lifted = elements_clause(elements)
    if lifted is not None:
        return {
            "clauses": [lifted],
            "meta": {"source": "elements", "content_hash": digest, "llm_tried": False, "model_version": "clause-rule-v1"},
        }
    if not str(row.get("content") or row.get("abstract") or row.get("title") or "").strip():
        return None
    meta = blob.get("clause_meta") if isinstance(blob.get("clause_meta"), dict) else {}
    if not force and meta.get("llm_tried") and meta.get("content_hash") == digest:
        return None
    produced = llm_clauses(row)
    if produced is None:
        return None
    if isinstance(produced, dict):
        raw_items = produced.get("clauses") or []
        version = str(produced.get("model_version") or "clause-llm-v1")
    else:
        raw_items, version = list(produced or []), "clause-llm-v1"
    window = llm_window(row)
    grounded = []
    for item in raw_items:
        if isinstance(item, dict):
            clause = accept_llm_item(item, window, elements)
            if clause:
                grounded.append(clause)
    return {
        "clauses": grounded,
        "meta": {"source": "llm", "content_hash": digest, "llm_tried": True, "model_version": version},
    }


def _ident(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]+", name or ""):
        raise SystemExit(f"库名非法: {name!r}")
    return name


def connect():
    import pymysql

    return pymysql.connect(
        host=os.environ["POLICY_MYSQL_HOST"],
        port=int(os.environ.get("POLICY_MYSQL_PORT", "3306")),
        user=os.environ["POLICY_MYSQL_USER"],
        password=os.environ["POLICY_MYSQL_PASSWORD"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def _q(conn, sql, args=()):
    with conn.cursor() as cur:
        cur.execute(sql, args)
        return list(cur.fetchall())


def _x(conn, sql, args=()):
    with conn.cursor() as cur:
        cur.execute(sql, args)


def _blob(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}
    return {}


def assert_no_collision(conn, dwd: str) -> None:
    rows = _q(
        conn,
        f"SELECT policy_id FROM {dwd}.policy_base_info GROUP BY policy_id HAVING COUNT(DISTINCT source_plane)>1 LIMIT 1",
    )
    if rows:
        raise SystemExit(f"policy_id 撞车: {rows[0]['policy_id']}。先停，不改 UK，本脚本不写")


def _attach_parse(conn, ads: str, rows: list[dict]) -> None:
    if not rows:
        return
    ids = [row["policy_id"] for row in rows]
    marks = ",".join(["%s"] * len(ids))
    found = _q(conn, f"SELECT policy_id, structured_elements FROM {ads}.policy_text_parse WHERE policy_id IN ({marks})", ids)
    by_id = {str(item["policy_id"]): item["structured_elements"] for item in found}
    for row in rows:
        row["structured_elements"] = by_id.get(str(row["policy_id"]))


def _needs_work(row: dict, force: bool) -> bool:
    if force:
        return True
    blob = _blob(row.get("structured_elements"))
    clauses = blob.get("clauses") if isinstance(blob.get("clauses"), list) else []
    if clauses:
        return False
    meta = blob.get("clause_meta") if isinstance(blob.get("clause_meta"), dict) else {}
    return not (meta.get("llm_tried") and meta.get("content_hash") == content_hash(row))


def load_rows(conn, dwd: str, ads: str, limit: int, policy_id: str, force: bool) -> list[dict]:
    cols = "policy_id, title, abstract, content, policy_support"
    where = "is_deleted=0 AND IFNULL(is_history,0)=0"
    if policy_id:
        rows = _q(conn, f"SELECT {cols} FROM {dwd}.policy_base_info WHERE policy_id=%s AND {where} LIMIT 1", (policy_id,))
        _attach_parse(conn, ads, rows)
        return rows
    out: list[dict] = []
    last = ""
    while len(out) < limit:
        batch = _q(
            conn,
            f"SELECT {cols} FROM {dwd}.policy_base_info WHERE {where} AND policy_id>%s ORDER BY policy_id LIMIT 200",
            (last,),
        )
        if not batch:
            break
        last = str(batch[-1]["policy_id"])
        _attach_parse(conn, ads, batch)
        for row in batch:
            if not _needs_work(row, force):
                continue
            out.append(row)
            if len(out) >= limit:
                break
    return out


def save(conn, ads: str, pid: str, row: dict, result: dict) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    found = _q(conn, f"SELECT structured_elements FROM {ads}.policy_text_parse WHERE policy_id=%s LIMIT 1", (pid,))
    blob = _blob(found[0]["structured_elements"]) if found else {}
    info = result["meta"]
    blob["clauses"] = result["clauses"]
    blob["clause_meta"] = {"source": info["source"], "content_hash": info["content_hash"], "llm_tried": bool(info["llm_tried"])}
    payload = json.dumps(blob, ensure_ascii=False)
    if found:
        _x(conn, f"UPDATE {ads}.policy_text_parse SET structured_elements=%s, title=%s, model_version=%s, update_time=%s WHERE policy_id=%s", (payload, str(row.get("title") or ""), info["model_version"], now, pid))
    else:
        _x(conn, f"INSERT INTO {ads}.policy_text_parse (policy_id, title, structured_elements, model_version, update_time) VALUES (%s,%s,%s,%s,%s)", (pid, str(row.get("title") or ""), payload, info["model_version"], now))
    conn.commit()


def run(limit: int, policy_id: str, force: bool) -> int:
    dwd = _ident(os.environ.get("POLICY_DWD_DB", "gkxlumenx_dwd"))
    ads = _ident(os.environ.get("POLICY_ADS_DB", "gkxlumenx_ads"))
    conn = connect()
    written = skipped = 0
    try:
        assert_no_collision(conn, dwd)
        for row in load_rows(conn, dwd, ads, limit, policy_id, force):
            pid = str(row["policy_id"])
            result = structure_one(row, _blob(row.get("structured_elements")), force=force)
            if result is None:
                skipped += 1
                continue
            if not result["clauses"] and result["meta"]["source"] == "llm":
                save(conn, ads, pid, row, result)
                print(f"{pid} llm_empty 已记下哈希，不写假条款")
                written += 1
                continue
            if not result["clauses"]:
                skipped += 1
                continue
            save(conn, ads, pid, row, result)
            written += 1
            print(f"{pid} {result['meta']['source']} {len(result['clauses'])}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(f"done written={written} skipped={skipped}")
    return 0


def self_check() -> None:
    text = "第一条 给予补贴100万元。第二条 申报应当具备资质。"
    parts = split_articles(text)
    assert len(parts) == 2 and parts[0][0] == "第一条"
    assert split_articles("一、开展试点工作。")
    assert not split_articles("没有条款标记的一段话")
    clause = classify_article("第一条", "给予补贴100万元。", {})
    assert clause["category"] == "补贴标准" and "100万元" in clause["amount"]
    lifted = elements_clause({"适用对象": "中小企业", "申报条件": "在本市注册"})
    assert lifted and lifted["target"] == "中小企业"
    assert elements_clause({}) is None
    window = "原文里的连续片段"
    assert accept_llm_item({"excerpt": "不在原文", "no": "第一条"}, window, {}) is None
    assert accept_llm_item({"excerpt": "连续片段", "amount": "9元"}, window, {})["amount"] == ""
    row = {"title": "t", "abstract": "", "content": text, "policy_support": "{\"适用对象\":\"企业\"}"}
    got = structure_one(row, {}, force=False)
    assert got and got["meta"]["source"] == "rule" and len(got["clauses"]) == 2
    assert structure_one(row, {"clauses": [{"no": "第一条"}]}, force=False) is None
    print("self-check ok")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLICY-C2 条款结构化")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--policy-id", default="")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.limit < 1 or args.limit > 100:
        print("limit 须在 1 到 100", file=sys.stderr)
        return 2
    if args.self_check:
        self_check()
        return 0
    return run(args.limit, args.policy_id.strip(), args.force)


if __name__ == "__main__":
    raise SystemExit(main())
