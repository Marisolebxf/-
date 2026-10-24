#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_PAPER_PATENT_CNT 技术点论文量 / 专利量 —— gkx 口径重建（20261022）。

只连 gkx；专利侧聚合读 code/_snapshots21/patent_*_20261021.json（一次全表扫描产物，
见 PATENT_SCAN_LEDGER.md）。

四段实测：
  1 计数面   论文 100,900（dwd_zh_paper，DOI 全唯一）、专利 2,939,895（dwd_patent）
  2 技术点面 gkx 无 tech_domain / technology_id 实体表（280 张表全名扫描）
  3 主体桥   论文 author_info_list.institution ↔ 专利 first_applicant_name 精确同名
  4 标题桥   专利 title_en 抽样 200 × 论文 en_name 抽样 30,000 的字符二元组 Dice 匹配率
判据阈值（Dice>=0.6 视为可对齐）**本件自定义、待甲方确认**。
产物：code/M_TECH_PAPER_PATENT_CNT_out.json
"""
from __future__ import annotations

import collections
import json
import re
import statistics
import time
from pathlib import Path

import pymysql

M = "M_TECH_PAPER_PATENT_CNT"
CODE = Path(__file__).resolve().parent
SNAP = CODE / "_snapshots21"
GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)

DICE_TH = 0.6       # 本件自定义、待甲方确认
DICE_STRONG = 0.75  # 同上（强匹配线）
N_PAT_TITLE = 200
N_PAPER_TITLE = 30000
PAGE = 10000
BASE = [2021, 2022, 2023, 2024]


def gkx():
    last = None
    for i in range(5):
        try:
            c = pymysql.connect(**GKX)
            with c.cursor() as cur:
                cur.execute("SET NAMES utf8mb4")
                cur.execute("SET SESSION max_execution_time=180000")
            return c
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (2 ** i))
    raise RuntimeError(f"gkx connect failed: {last!r}")


def q(sql, args=None, cap=180000):
    last = None
    for i in range(4):
        try:
            c = gkx()
            try:
                with c.cursor() as cur:
                    cur.execute(f"SET SESSION max_execution_time={cap}")
                    cur.execute(sql, args or ())
                    cols = [d[0] for d in cur.description] if cur.description else []
                    return [dict(zip(cols, r)) for r in cur.fetchall()]
            finally:
                c.close()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2.0 * (2 ** i))
    raise RuntimeError(f"query failed: {last!r} :: {sql[:120]}")


def num(v):
    if v is None:
        return 0
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def load(p):
    return json.load(open(p, encoding="utf-8"))


const = load(SNAP / "tech5_constants_20261022.json")
ipc_year = load(SNAP / "patent_ipc4_year_20261021.json")
by_name = load(SNAP / "patent_ipc4_by_name_20261021.json")
paper_panel = load(SNAP / "papers_city_year_gkx21.json")
# 2026-10-23 加：全表口径的年度分布（与 2,939,895 同源，来自按 dwd_id 分块流式累加的
# patent_panel_innov 快照）。本件原先只记 IPC 非空的 2,009,365，别的件拿它去除全表总量
# 就会混基（看板件真踩过：68.3482% vs 真实 82.4752%）。把两个数并列写进产物，
# 让「哪个是 IPC 子集、哪个是全表」在数据层就分得开，不靠正文解释。
panel = load(SNAP / "patent_panel_innov_20261021.json")
full_year = {str(y): int(panel["year_all"].get(str(y), 0)) for y in BASE}
full_window = sum(full_year.values())

# ---------- 1. 计数面 ----------
paper = q("""SELECT COUNT(*) n, COUNT(DISTINCT doi) doi_u,
                    SUM(en_name IS NOT NULL AND en_name<>'') en_fill,
                    SUM(zh_name IS NOT NULL AND zh_name<>'') zh_fill,
                    SUM(author_info_list IS NOT NULL AND author_info_list<>'') auth_fill,
                    MIN(cover_year_start) y0, MAX(cover_year_start) y1
             FROM gkx.dwd_zh_paper""")[0]
paper_n = num(paper["n"])
pat_n = const["patent_rows"]
pat_ipc = const["patent_with_ipc"]

cls = q("""SELECT COUNT(*) n, COUNT(DISTINCT id) ids,
                  SUM(keywords IS NOT NULL AND keywords<>'') kw_fill,
                  SUM(scope IS NOT NULL AND scope<>'') scope_fill
           FROM gkx.dwd_zh_paper_classification""")[0]
ptitle = q("""SELECT COUNT(*) n,
                     SUM(title_en IS NOT NULL AND title_en<>'') en_fill,
                     SUM(title_trans_cn IS NOT NULL AND title_trans_cn<>'') cn_fill
              FROM gkx.dwd_patent_title""")[0]

nat = collections.defaultdict(dict)
for ipc4, y, n, org in ipc_year:
    nat[ipc4][int(y)] = int(n)
pat_year = {str(y): sum(v.get(y, 0) for v in nat.values()) for y in BASE}

paper_year = {str(y): int(n) for y, n in paper_panel["year_all"].items()}
paper_year_rows = {y: paper_year.get(str(y), 0) for y in range(2015, 2027)}

# ---------- 2. 技术点实体面 ----------
tables = [r["TABLE_NAME"] for r in q(
    "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='gkx'")]
kw_tables = {kw: [t for t in tables if kw in t.lower()]
             for kw in ("domain", "technology", "tech_point", "techpoint", "subject",
                        "discipline", "industry", "ipc")}
tech_cols = q("""SELECT TABLE_NAME t, COLUMN_NAME c FROM information_schema.COLUMNS
                 WHERE TABLE_SCHEMA='gkx'
                   AND (COLUMN_NAME LIKE '%%technolog%%' OR COLUMN_NAME LIKE '%%tech_point%%'
                        OR COLUMN_NAME LIKE '%%tech_domain%%')""")

# ---------- 3. 主体桥：论文机构 ↔ 专利申请人 ----------
def norm_name(s: str) -> str:
    s = re.sub(r"[（(].*?[)）]", "", s)
    s = re.sub(r"\s+", "", s)
    return s.strip()


pat_applicant = collections.Counter()
for ipc4, nm, c in by_name:
    if nm:
        pat_applicant[norm_name(nm)] += int(c)
pat_set = set(pat_applicant)

inst_paper = collections.Counter()
inst_inst_total = 0
paper_org_hit = 0
offset = 0
while offset < paper_n:
    rows = q("""SELECT pk_id, author_info_list FROM gkx.dwd_zh_paper
                ORDER BY pk_id LIMIT %s OFFSET %s""", (PAGE, offset), cap=240000)
    if not rows:
        break
    for r in rows:
        s = r["author_info_list"]
        if not s:
            continue
        try:
            arr = json.loads(s)
        except Exception:  # noqa: BLE001
            continue
        seen = set()
        hit = False
        for a in arr:
            raw = (a.get("institution") or "").strip()
            if not raw:
                continue
            for part in re.split(r"[;；]", raw):
                part = norm_name(part)
                if not part or part in seen:
                    continue
                seen.add(part)
                inst_paper[part] += 1
                inst_inst_total += 1
                if part in pat_set:
                    hit = True
        if hit:
            paper_org_hit += 1
    offset += PAGE

inst_set = set(inst_paper)
inst_hit = inst_set & pat_set
inst_hit_instances = sum(inst_paper[k] for k in inst_hit)

top_bridge = []
for nm in sorted(inst_hit, key=lambda x: -inst_paper[x])[:20]:
    top_bridge.append({
        "org": nm,
        "paper_cnt": inst_paper[nm],
        "patent_cnt": pat_applicant[nm],
    })

# ---------- 4. 标题桥：Dice 匹配率 ----------
pat_titles = q("""SELECT pn, title_en FROM gkx.dwd_patent_title
                  WHERE title_en IS NOT NULL AND title_en<>'' AND dwd_id %% 70 = 0
                  ORDER BY dwd_id LIMIT %s""", (N_PAT_TITLE,), cap=120000)
paper_titles = [r["en_name"] for r in q(
    """SELECT en_name FROM gkx.dwd_zh_paper
       WHERE en_name IS NOT NULL AND en_name<>'' ORDER BY pk_id LIMIT %s""",
    (N_PAPER_TITLE,), cap=240000) if r["en_name"]]


def bigrams(s: str):
    s = re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    return [s[i:i + 2] for i in range(len(s) - 1)]


index = collections.defaultdict(list)
for i, t in enumerate(paper_titles):
    for g in set(bigrams(t)):
        index[g].append(i)


def best_dice(title):
    """字符二元组 Dice 的最佳匹配（候选截断 40 篇，按数据定序）。

    2026-10-23 修：原实现遍历 `set(bigrams(title))` 累加，再用 `cnt.most_common(40)`
    取候选——同票时候选顺序由 set 的迭代序（=PYTHONHASHSEED）决定，于是**同一个样本
    每次跑出的中位数不同**：实测 0.5593 / 0.5596 / 0.5639 / 0.5603，90 分位 0.6325—0.6351，
    ≥0.6 命中 58—59 条。已发布的正文数字（0.5593）只是其中一次跑的结果，重跑即变。
    改为：按 bigram 字典序累加、同票按论文下标升序截断，整条计算链只由数据决定。
    确定性验证：3 个 PYTHONHASHSEED（0/1/12345）四次指纹相同（见 _work_gkx21/probe_dice_determinism.py）。
    """
    mb = set(bigrams(title))
    if len(mb) < 2:
        return 0.0, None
    cnt = collections.Counter()
    for g in sorted(mb):
        for j in index.get(g, ()):
            cnt[j] += 1
    best, bj = 0.0, None
    for j, _ in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:40]:
        vb = set(bigrams(paper_titles[j]))
        inter = len(mb & vb)
        d = 2 * inter / (len(mb) + len(vb)) if (mb or vb) else 0.0
        if d > best:
            best, bj = d, j
    return best, bj


dices = []
for r in pat_titles:
    d, _ = best_dice(r["title_en"])
    dices.append(round(d, 4))
dices_sorted = sorted(dices)
median_d = round(statistics.median(dices_sorted), 4) if dices_sorted else None
ge_th = sum(1 for d in dices if d >= DICE_TH)
ge_strong = sum(1 for d in dices if d >= DICE_STRONG)
n_dice = len(dices)

# 反向验证：随机配对基线。若「最佳匹配」与随机配对差别不大，说明命中只是通用词。
import random
random.seed(20261022)
ctrl = []
for i, r in enumerate(pat_titles):
    j = random.randrange(len(paper_titles))
    mb, vb = set(bigrams(r["title_en"])), set(bigrams(paper_titles[j]))
    inter = len(mb & vb)
    ctrl.append(round(2 * inter / (len(mb) + len(vb)), 4) if (mb or vb) else 0.0)
ctrl_median = round(statistics.median(sorted(ctrl)), 4) if ctrl else None
ctrl_p90 = round(sorted(ctrl)[int(0.9 * (len(ctrl) - 1))], 4) if ctrl else None

# ---------- 5. 领域级侧计数（专利侧可做，论文侧无域键） ----------
dom_total = {d: sum(v.get(y, 0) for y in BASE) for d, v in nat.items()}
top_dom = [{"ipc4": d, "patent_cnt_2021_2024": t,
            "share_pct": round(t / sum(dom_total.values()) * 100, 3)}
           for d, t in sorted(dom_total.items(), key=lambda kv: -kv[1])[:15]]

criteria = {
    "direct_structure": "否（技术点实体表与双侧结果表均不在 gkx）",
    "direct_data": "否（无技术点粒度计数结果可读）",
    "dependency_structure": "部分（论文表、专利表、专利标题表在库；技术点实体表与学科—IPC 对照表不在库）",
    "dependency_data": "部分（双侧总量足：论文 100,900、专利 2,939,895；但专利标题仅 20,361 行覆盖 0.693%，标题可对齐率低于阈值）",
}

out = {
    "metric_id": M,
    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "domain_mapping_version": const["domain_mapping_version"],
    "patent_dedup_key": const["patent_dedup_key"],
    "paper_dedup_key": "doi（dwd_zh_paper 100,900 行，COUNT(DISTINCT doi)=100,900，无重复）",
    "base_years_used": const["base_years_used"],
    "base_years_missing": const["base_years_missing"],
    "base_years_note": const["base_years_note"],
    "constants_ref": "code/_snapshots21/tech5_constants_20261022.json",
    "support_judgment": "部分支持",
    "judgment_reason": f"两侧计数都能算（论文 {paper_n:,} / 专利 {pat_n:,}），但需求要求按 technology_id 输出技术点粒度："
                       f"gkx 无技术点实体表；主体桥精确同名覆盖 {round(len(inst_hit)/len(inst_set)*100,2)}% 的论文机构、"
                       f"{round(paper_org_hit/paper_n*100,2)}% 的论文；标题桥 0.75 以上命中 {ge_strong}/{n_dice}，"
                       f"上限 {round(max(dices),4) if dices else None} 低于强匹配线"
                       "——技术点粒度对齐不成立，只能交付机构级双计数与双侧总量。",
    "counts": {
        "paper_rows": paper_n,
        "paper_doi_distinct": num(paper["doi_u"]),
        "paper_en_name_fill": num(paper["en_fill"]),
        "paper_en_name_fill_pct": round(num(paper["en_fill"]) / paper_n * 100, 2),
        "paper_author_fill": num(paper["auth_fill"]),
        "paper_year_min": str(paper["y0"]), "paper_year_max": str(paper["y1"]),
        "patent_rows": pat_n,
        "patent_with_ipc": pat_ipc,
        "patent_with_ipc_pct": round(pat_ipc / pat_n * 100, 2),
        "patent_title_rows": num(ptitle["n"]),
        "patent_title_coverage_pct": round(num(ptitle["n"]) / pat_n * 100, 3),
        "patent_title_en_fill": num(ptitle["en_fill"]),
        "patent_title_cn_fill": num(ptitle["cn_fill"]),
    },
    "paper_axis": {
        "rows_declared": int(paper_panel["rows_declared"]),
        "year_counts_2015_2026": paper_year_rows,
        "classification_rows": num(cls["n"]),
        "classification_coverage_pct": round(num(cls["n"]) / paper_n * 100, 2),
        "classification_keywords_fill": num(cls["kw_fill"]),
        "classification_scope_fill": num(cls["scope_fill"]),
        "classification_note": "dwd_zh_paper_classification 有 scope（中图分类）与 keywords，"
                                f"但只覆盖 {num(cls['n'])}/{paper_n} 篇（{round(num(cls['n'])/paper_n*100,2)}%），"
                                "且 scope 是图书分类号，不是 IPC，无官方对照表可连",
    },
    "patent_axis": {
        "year_totals_2021_2024": pat_year,
        "total_2021_2024": sum(pat_year.values()),
        "domains_total": len(dom_total),
        "top_domains": top_dom,
    },
    # 2026-10-23 加：基期专利总量的**两个口径**，并列存放，避免再次混基。
    "patent_window_caliber": {
        "ipc_nonnull_window_total": sum(pat_year.values()),
        "ipc_nonnull_year_totals": pat_year,
        "all_rows_window_total": full_window,
        "all_rows_year_totals": full_year,
        "all_rows_total": pat_n,
        "ipc_share_of_window_pct": round(sum(pat_year.values()) / full_window * 100, 4),
        "ipc_nonnull_share_of_all_pct": round(sum(pat_year.values()) / pat_n * 100, 4),
        "all_rows_share_of_all_pct": round(full_window / pat_n * 100, 4),
        "rule": ("`ipc_nonnull_window_total`（IPC 非空行，2021—2024）只能与同为 IPC 非空的分母相除，"
                 "用于领域结构；`all_rows_window_total`（全表行，2021—2024）才能与全表总量 "
                 "`all_rows_total` 相除，用于时间占比。两者互换即混基："
                 "2,009,365 / 2,939,895 = 68.3482% 是错的，正确近四年占比是 2,424,684 / 2,939,895 = 82.4752%。"
                 "IPC 标注率则是 2,009,365 / 2,424,684 = 82.87%（分子分母同为窗口内，分子多一层 IPC 非空）。"),
    },
    "tech_point_face": {
        "gkx_tables_total": len(tables),
        "keyword_table_hits": kw_tables,
        "tech_columns": tech_cols,
        "verdict": "无 tech_domain / technology_id / tech_point 表，也无任何列名含 technolog/tech_point；"
                   "技术点粒度不可作为输出坐标，只能退到 IPC4（专利侧）与机构（两侧共有，且仅精确同名子集）",
    },
    "org_bridge": {
        "paper_institutions_distinct": len(inst_set),
        "paper_institution_instances": inst_inst_total,
        "patent_applicants_distinct": len(pat_set),
        "exact_overlap_institutions": len(inst_hit),
        "institution_coverage_pct": round(len(inst_hit) / len(inst_set) * 100, 2),
        "instance_coverage_pct": round(inst_hit_instances / inst_inst_total * 100, 2),
        "paper_with_patent_org": paper_org_hit,
        "paper_coverage_pct": round(paper_org_hit / paper_n * 100, 2),
        "normalization": "去括号内容 + 去空白后精确同名；不做同义词/别名合并（无机构主数据）",
        "top20": top_bridge,
    },
    "title_bridge": {
        "patent_sample": n_dice,
        "patent_sample_rule": "dwd_patent_title 中 title_en 非空的 dwd_id 对 70 取模为 0，按 dwd_id 取前 200 条",
        "paper_sample": len(paper_titles),
        "paper_sample_rule": f"dwd_zh_paper 中 en_name 非空的按 pk_id 取前 {N_PAPER_TITLE} 条"
                             f"（占英文题名 {num(paper['en_fill'])} 条的 "
                             f"{round(len(paper_titles)/num(paper['en_fill'])*100, 2)}%）",
        "metric": "字符二元组 Dice 系数，正则化后小写、非字母数字折为空格",
        "threshold_dice": DICE_TH,
        "threshold_strong": DICE_STRONG,
        "threshold_note": "阈值本件自定义、待甲方确认：需求未给标题对齐判据，0.6/0.75 取自文献计量常用经验线",
        "median_best_dice": median_d,
        "p90_best_dice": round(dices_sorted[int(0.9 * (n_dice - 1))], 4) if dices else None,
        # 2026-10-23 补：正文引用了「最高 0.6829」，但它此前只存在于 verdict 字符串里，
        # 没有独立数值键 —— md_vs_out 因此记一笔未命中。上限是本件判「不可用」的关键证据之一
        # （上限低于强匹配线 0.75），必须能被单独引用与复核。
        "max_best_dice": round(max(dices), 4) if dices else None,
        "ge_threshold": ge_th,
        "ge_strong": ge_strong,
        "match_rate_pct": round(ge_th / n_dice * 100, 2) if n_dice else None,
        "strong_rate_pct": round(ge_strong / n_dice * 100, 2) if n_dice else None,
        "control_random_median": ctrl_median,
        "control_random_p90": ctrl_p90,
        "control_note": "反向验证：同一批专利标题与随机论文标题配对的 Dice 中位数与 90 分位",
        "verdict": f"标题不能承担论文—专利对齐：最佳匹配中位 {median_d}、0.75 以上 {ge_strong}/{n_dice}，"
                   f"而随机配对中位 {ctrl_median}——0.6 命中（{ge_th}/{n_dice}）是通用技术词带来的，"
                   f"不是同一篇文献；上限 {round(max(dices),4) if dices else None} 仍低于强匹配线 {DICE_STRONG}",
    },
    "criteria": criteria,
    "missing_sources": [
        "技术点实体表（technology_id）：gkx 无，需求的技术点粒度无坐标",
        "学科—IPC 对照表：gkx 无，论文侧无法映射到专利侧分类号",
        "专利标题全量：仅 20,361/2,939,895 = 0.693%，标题对齐即便可行也只覆盖极小子集",
        "机构主数据（统一社会信用代码）：两侧均为自由文本，只能精确同名",
        "论文关键词全量：仅 20,048/100,900 = 19.87% 有 classification 行",
    ],
    "notes": [
        "论文侧没有 IPC / 学科码列，专利侧没有论文标识列——两侧不存在共同实体键",
        "专利侧计数读一次性全表扫描缓存，不对宽表做行级多字段聚合",
    ],
}

print(json.dumps({"paper": paper_n, "patent": pat_n, "inst_cov_pct": out["org_bridge"]["institution_coverage_pct"],
                  "paper_cov_pct": out["org_bridge"]["paper_coverage_pct"],
                  "median_dice": median_d, "match_rate_pct": out["title_bridge"]["match_rate_pct"],
                  "support": out["support_judgment"]}, ensure_ascii=False))

with open(CODE / f"{M}_out.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(f"[OK] wrote {M}_out.json")
