# GDF 作业 POLICY-C2：把政策正文切成条款，合并进 ADS policy_text_parse。
#
# ═══ 修改版 v2（2026-10-30）═══
# 基于客户原件 policy_c2_clauses.py（sha256 0a4f49d6...）改造，业务逻辑未动。
# 改动清单见同目录《修改记录.md》。摘要：
#   S1 跳过判定补上 content_hash 比对（原件算了 hash 却没用，导致正文改了也不重算）
#   S2 无 LLM 密钥也留痕（llm_unavailable），避免每天重撞同一批
#   S3 新增 --max-rounds 脚本内循环 + no_progress 保护 + --deadline-sec
#   S4 退出码显式化（1 保留给未捕获异常）
#   S5 --force 必须配 --policy-id，防止全表重烧模型
#   S6 self-check 覆盖新逻辑
# ════════════════════════════
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
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta

_CN = "一二三四五六七八九十"
ARTICLE_SPLIT = re.compile(r"(?=第[0-9０-９一二三四五六七八九十百千]+条)")
ARTICLE_HEAD = re.compile(r"^(第[0-9０-９一二三四五六七八九十百千]+条)")
HEADING_SPLIT = re.compile(rf"(?:(?<=^)|(?<=[\n。；;]))\s*(?=(?:（[{_CN}]+）|[{_CN}]+、|\d{{1,2}}[.、]))")
HEADING_HEAD = re.compile(rf"^(?:（[{_CN}]+）|[{_CN}]+、|\d{{1,2}}[.、])")
AMOUNT_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:亿元|万元|元|%|个百分点)")
TARGET_RE = re.compile(r"(?:适用对象|支持对象|申报主体)[:：]?\s*([^。；;\n]{2,40})")
CATEGORIES = ("补贴标准", "准入条件", "扶持措施", "保障机制", "责任主体", "政策目标")
JOB = "c2"
STATE_TABLE = "script_state"
RETRY_DEGRADED_MIN = 60
RETRY_FAILED_MIN = 60
RETRY_NO_MATCH_DAYS = 30
MAX_TRY = 5


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
    """返回要写入的条款和 meta。None 表示跳过、不写。

    v2 改动（S1）：原件算了 content_hash 也存进 clause_meta，但判定时只看「有没有 clauses」，
    导致正文改了也不重算。现在改为：clauses 存在 **且** content_hash 相同才跳过。
    旧数据（有 clauses 但没有 clause_meta.content_hash）保守跳过——不做全量重算，
    避免升级瞬间把 4 万条全烧一遍模型；其指纹由状态表在下次运行时补齐。
    """
    existing = blob.get("clauses") if isinstance(blob.get("clauses"), list) else []
    digest = content_hash(row)
    meta0 = blob.get("clause_meta") if isinstance(blob.get("clause_meta"), dict) else {}
    if existing and not force:
        prev_hash = meta0.get("content_hash")
        if not prev_hash or prev_hash == digest:
            return None
        # 到这里说明正文/标题/摘要变了，继续往下重算
    elements = elements_of(row)
    articles = split_articles(row.get("content") or "") or split_articles(row.get("abstract") or "")
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
        # S2 补：原件这里 return None，什么痕迹都不留 → 无正文的行每趟重复入选。
        # 改为返回 empty 标记，由 run() 写状态表。
        return {"clauses": [], "meta": {"source": "empty", "content_hash": digest,
                                        "llm_tried": False, "model_version": "clause-empty"}}
    meta = blob.get("clause_meta") if isinstance(blob.get("clause_meta"), dict) else {}
    if not force and meta.get("llm_tried") and meta.get("content_hash") == digest:
        return None
    produced = llm_clauses(row)
    if produced is None:
        # S2：未配 LLM_BASE_URL/LLM_API_KEY（或调用不可用）时原件直接 return None，
        # 结果库里什么都没留，下一轮又被选中 → 每天重撞同一批。
        # 现在返回一个只写状态表、不写 ADS 的标记，让 run() 记 llm_unavailable。
        # 不写 clause_meta.llm_tried，避免给 ADS 留下「试过模型」的假标记。
        return {"clauses": [], "meta": {"source": "llm_unavailable", "content_hash": digest,
                                        "llm_tried": False, "model_version": "clause-llm-unavailable"}}
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


# ─────────────── 以下为修改版新增（S1/S2 状态表）───────────────

def sql_content_hash(alias: str = "p") -> str:
    """与 content_hash() 等价的 MySQL 表达式（title\nabstract\ncontent，NULL 变空串）。
    不能用 CONCAT_WS：它遇 NULL 会连分隔符一起跳过，与 Python 口径不一致。"""
    return ("LEFT(SHA2(CONCAT(IFNULL({a}.title,''),CHAR(10),IFNULL({a}.abstract,''),"
            "CHAR(10),IFNULL({a}.content,'')),256),16)").format(a=alias)


def state_table_exists(conn, dwd: str) -> bool:
    rows = _q(conn, "SELECT 1 AS ok FROM information_schema.TABLES "
                    "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s LIMIT 1", (dwd, STATE_TABLE))
    return bool(rows)


def save_state(conn, dwd: str, policy_id: str, src_hash: str, status: str,
               batch_id: str, note: str = "", retry_min: int = 0,
               retry_days: int = 0, terminal: bool = False) -> None:
    now = datetime.now().replace(microsecond=0)
    next_try = None
    if not terminal:
        if retry_min:
            next_try = now + timedelta(minutes=retry_min)
        elif retry_days:
            next_try = now + timedelta(days=retry_days)
    prev = _q(conn, f"SELECT try_count, content_hash FROM {dwd}.{STATE_TABLE} "
                    f"WHERE job=%s AND policy_id=%s LIMIT 1", (JOB, policy_id))
    try_count = (int(prev[0]["try_count"]) + 1) if prev else 1
    if prev and str(prev[0]["content_hash"]) != src_hash:
        try_count = 1
    if try_count >= MAX_TRY and not terminal:
        terminal = True
        next_try = None
        note = (note + f" | 达重试上限{MAX_TRY}转终态").strip(" |")
    _x(conn,
       f"INSERT INTO {dwd}.{STATE_TABLE} "
       f"(job, policy_id, content_hash, status, batch_id, tried_at, next_try_at, try_count, note) "
       f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
       f"ON DUPLICATE KEY UPDATE content_hash=VALUES(content_hash), status=VALUES(status), "
       f"batch_id=VALUES(batch_id), tried_at=VALUES(tried_at), next_try_at=VALUES(next_try_at), "
       f"try_count=VALUES(try_count), note=VALUES(note)",
       (JOB, policy_id, src_hash, status, batch_id,
        now.strftime("%Y-%m-%d %H:%M:%S"),
        next_try.strftime("%Y-%m-%d %H:%M:%S") if next_try else None,
        try_count, note[:500]))
    conn.commit()


def check_env() -> None:
    """C2 只硬要求 MySQL；LLM 缺失不失败（规则路径仍能产出）。"""
    for key in ("POLICY_MYSQL_HOST", "POLICY_MYSQL_USER", "POLICY_MYSQL_PASSWORD"):
        if not os.environ.get(key, "").strip():
            raise SystemExit(f"环境变量缺失：{key}")

# ─────────────── 新增结束 ───────────────


def _attach_parse(conn, ads: str, rows: list[dict]) -> None:
    if not rows:
        return
    ids = [row["policy_id"] for row in rows]
    marks = ",".join(["%s"] * len(ids))
    found = _q(conn, f"SELECT policy_id, structured_elements FROM {ads}.policy_text_parse WHERE policy_id IN ({marks})", ids)
    by_id = {str(item["policy_id"]): item["structured_elements"] for item in found}
    for row in rows:
        row["structured_elements"] = by_id.get(str(row["policy_id"]))


def _attach_state(conn, dwd: str, rows: list[dict]) -> None:
    """S1 补：把状态表挂到行上。C2 的增量原来只看 ADS 有没有条款，
    导致「规则切不开 + 无模型」的行在 ADS 里什么都没有，下一趟又被选中。"""
    if not rows:
        return
    ids = [row["policy_id"] for row in rows]
    marks = ",".join(["%s"] * len(ids))
    found = _q(conn, f"SELECT policy_id, content_hash, status, next_try_at "
                     f"FROM {dwd}.{STATE_TABLE} WHERE job=%s AND policy_id IN ({marks})",
               tuple([JOB] + ids))
    by_id = {str(r["policy_id"]): r for r in found}
    for row in rows:
        row["_state"] = by_id.get(str(row["policy_id"]))


def _state_skip(row: dict, force: bool) -> bool:
    """状态表判定：指纹相同且未到重试时间 → 跳过。"""
    if force:
        return False
    st = row.get("_state")
    if not isinstance(st, dict) or not st:
        return False
    if str(st.get("content_hash") or "") != content_hash(row):
        return False          # 内容变了，必须重算
    nxt = st.get("next_try_at")
    if nxt is None:
        return True           # 终态
    try:
        return bool(nxt > datetime.now())
    except TypeError:
        return True


def _needs_work(row: dict, force: bool) -> bool:
    if force:
        return True
    blob = _blob(row.get("structured_elements"))
    clauses = blob.get("clauses") if isinstance(blob.get("clauses"), list) else []
    if clauses:
        return False
    meta = blob.get("clause_meta") if isinstance(blob.get("clause_meta"), dict) else {}
    return not (meta.get("llm_tried") and meta.get("content_hash") == content_hash(row))


def load_rows(conn, dwd: str, ads: str, limit: int, policy_id: str, force: bool,
              cursor: str = "") -> list[dict]:
    cols = "policy_id, title, abstract, content, policy_support"
    where = "is_deleted=0 AND IFNULL(is_history,0)=0"
    if policy_id:
        rows = _q(conn, f"SELECT {cols} FROM {dwd}.policy_base_info WHERE policy_id=%s AND {where} LIMIT 1", (policy_id,))
        _attach_parse(conn, ads, rows)
        _attach_state(conn, dwd, rows)
        return rows
    out: list[dict] = []
    last = cursor
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
        _attach_state(conn, dwd, batch)
        for row in batch:
            if _state_skip(row, force):
                continue
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


def run(limit: int, policy_id: str, force: bool,
        max_rounds: int = 1, deadline_sec: int = 0) -> int:
    dwd = _ident(os.environ.get("POLICY_DWD_DB", "gkxlumenx_dwd"))
    ads = _ident(os.environ.get("POLICY_ADS_DB", "gkxlumenx_ads"))
    conn = connect()
    agg = {"rounds": 0, "processed": 0, "written": 0, "skipped": 0, "failed": 0}
    stopped = "max_rounds"
    batch_id = datetime.now().strftime("%Y%m%d%H%M%S")
    t0 = time.time()
    try:
        if not state_table_exists(conn, dwd):
            print(f"缺状态表 {dwd}.{STATE_TABLE}，请先建表（见 sql/script_state.sql）。脚本不建表。",
                  file=sys.stderr)
            return 4
        assert_no_collision(conn, dwd)
        cursor = ""
        for r in range(1, max_rounds + 1):
            rows = load_rows(conn, dwd, ads, limit, policy_id, force, cursor)
            if not rows:
                stopped = "exhausted"
                break
            round_written = round_skipped = 0
            for row in rows:
                pid = str(row["policy_id"])
                digest = content_hash(row)
                result = structure_one(row, _blob(row.get("structured_elements")), force=force)

                if result is None:
                    # 已处理且内容未变：跳过，不重复写状态
                    round_skipped += 1
                    cursor = pid
                    continue

                source = result["meta"]["source"]

                if source == "llm_unavailable":
                    # S2：只写状态表，不碰 ADS
                    print(f"{pid} llm_unavailable 未配模型，已记状态")
                    save_state(conn, dwd, pid, digest, "llm_unavailable", batch_id,
                               note="未配置 LLM_BASE_URL/LLM_API_KEY", terminal=True)
                    round_skipped += 1
                    cursor = pid
                    continue

                if source == "empty":
                    save_state(conn, dwd, pid, digest, "empty", batch_id,
                               note="无正文/摘要/标题", terminal=True)
                    print(f"{pid} empty 无正文，已记状态")
                    round_skipped += 1
                    cursor = pid
                    continue

                if not result["clauses"]:
                    if source == "llm":
                        # 有密钥但模型返回空：保留原件行为（写 ADS 记下哈希，避免重复调模型）
                        save(conn, ads, pid, row, result)
                        save_state(conn, dwd, pid, digest, "no_match", batch_id,
                                   note="模型返回空条款", terminal=True)
                        print(f"{pid} llm_empty 已记下哈希，不写假条款")
                    else:
                        save_state(conn, dwd, pid, digest, "empty", batch_id,
                                   note="无正文可切", terminal=True)
                        print(f"{pid} empty 已记状态")
                    round_skipped += 1
                    cursor = pid
                    continue

                save(conn, ads, pid, row, result)
                save_state(conn, dwd, pid, digest, "done", batch_id,
                           note=f"{source} 条款 {len(result['clauses'])} 条", terminal=True)
                round_written += 1
                cursor = pid
                print(f"{pid} {source} {len(result['clauses'])}")

            agg["rounds"] = r
            agg["processed"] += len(rows)
            agg["written"] += round_written
            agg["skipped"] += round_skipped
            if round_written == 0 and round_skipped == len(rows):
                stopped = "no_progress"
                break
            if deadline_sec and time.time() - t0 > deadline_sec:
                stopped = "deadline"
                break
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("done rounds={rounds} processed={processed} written={written} "
          "skipped={skipped} stopped={stopped} batch={batch_id}".format(batch_id=batch_id, stopped=stopped, **agg))
    return 0 if stopped == "exhausted" else 7


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
    assert structure_one(row, {"clauses": [{"no": "第一条"}]}, force=False) is None, \
        "有条款且无指纹（旧数据）须保守跳过，不做全量重算"
    # S1 新增：指纹不同 → 必须重算
    changed = structure_one(row, {"clauses": [{"no": "第一条"}],
                                 "clause_meta": {"content_hash": "deadbeefdeadbeef"}}, force=False)
    assert changed is not None and changed["meta"]["source"] == "rule", \
        "正文变了必须重算，不能被『已有条款』挡住"
    # S1 新增：指纹相同 → 跳过
    same = structure_one(row, {"clauses": [{"no": "第一条"}],
                              "clause_meta": {"content_hash": content_hash(row)}}, force=False)
    assert same is None, "指纹相同须跳过（省 token 的关键）"
    # S2 新增：无密钥须返回 llm_unavailable 标记，而不是 None
    bare = {"title": "无条款标记的政策", "abstract": "", "content": "这是一段没有条款标记的正文。", "policy_support": ""}
    import os as _os
    saved = {k: _os.environ.pop(k, None) for k in ("LLM_BASE_URL", "LLM_API_KEY")}
    try:
        got_bare = structure_one(bare, {}, force=False)
        assert got_bare is not None and got_bare["meta"]["source"] == "llm_unavailable", \
            "无密钥须留痕，不能静默返回 None"
    finally:
        for k, v in saved.items():
            if v is not None: _os.environ[k] = v
    assert "CONCAT_WS" not in sql_content_hash("p"), "SQL 指纹不能使用 CONCAT_WS"
    print("self-check ok")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLICY-C2 条款结构化")
    parser.add_argument("--limit", type=int, default=100,
                        help="单轮批大小，1~100（既有约束，未变）")
    parser.add_argument("--max-rounds", type=int, default=1,
                        help="脚本内循环轮数上限，默认 1 = 原行为。C2 可能调模型，建议 5 以内")
    parser.add_argument("--deadline-sec", type=int, default=0,
                        help="软超时（秒），到期优雅退出。建议设为平台 Job 超时的 80%%")
    parser.add_argument("--policy-id", default="")
    parser.add_argument("--force", action="store_true",
                        help="重算；必须配 --policy-id，防止全表重烧模型")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.limit < 1 or args.limit > 100:
        print("limit 须在 1 到 100", file=sys.stderr)
        return 2
    if args.max_rounds < 1:
        print("max-rounds 须 >= 1", file=sys.stderr)
        return 2
    if args.deadline_sec < 0:
        print("deadline-sec 须 >= 0", file=sys.stderr)
        return 2
    if args.force and not args.policy_id.strip():
        print("--force 必须配 --policy-id：全表重烧模型请勿用 --force", file=sys.stderr)
        return 2
    if args.self_check:
        self_check()
        return 0
    try:
        check_env()
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 3
    return run(args.limit, args.policy_id.strip(), args.force,
               max_rounds=args.max_rounds, deadline_sec=args.deadline_sec)


if __name__ == "__main__":
    raise SystemExit(main())
