#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_OUTPUT_SCALE · 技术规模（成果侧可算 / 应用侧无承载）

seed 口径原文（20261016 版《M_TECH_OUTPUT_SCALE.md》§一 抄录）：
  「选定时间窗内该技术的成果与应用体量（内部默认不含资金投入——投入走 M_TECH_INVEST_AMOUNT）。
    ADS 读面计数/加总。**禁止用论文量、专利量或技术交易额冒充「技术规模」专名**。」

这条「禁止冒充」是本文的判档主线：
  - 成果侧：本库只有专利（2,939,895）与论文（100,900）两类成果，二者都在禁止之列；
  - 应用侧：产品数 / 产值 / 装机量 / 交易金额——本库**没有任何承载表**，
    `dwd_patent_transfer` 22,809 行**无金额列**且仅 534 行能回连主表。
因此本脚本输出的是**技术点专利体量代理**（`patent_volume_proxy`），
不以「技术规模」专名对外发布；支持度判 **部分支持**（成果侧可算，应用侧永久缺）。

输出：code/M_TECH_OUTPUT_SCALE_out.json
"""
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _tech5_common as T  # noqa: E402

t0 = time.time()
b = T.graph_bundle()
full = T.ipc4_full_stats()
proof = T.probe()
raw = T.load_json("tech5_ipc4_stats.json", []) or []

nodes = [r["node"] for r in b["rows"]]
rows = []
for r in b["rows"]:
    f = full.get(r["node"])
    rows.append({
        "node": r["node"],
        "n_patents": f["n"] if f else None,
        "n_inv": f["inv"] if f else None,
        "n_um": f["um"] if f else None,
        "n_design": f["des"] if f else None,
        "n_granted": f["granted"] if f else None,
        "n_applicants": f["n_appl"] if f else None,
        "degree": r["degree"],
        "patents_in_graph": r["patents_in_graph"],
    })

known = [r for r in rows if r["n_patents"]]
unknown = [r["node"] for r in rows if not r["n_patents"]]
tot = sum(r["n_patents"] for r in known)
for r in known:
    r["share_pct"] = round(100 * r["n_patents"] / tot, 4)
known.sort(key=lambda r: -r["n_patents"])
cum = 0.0
for i, r in enumerate(known, 1):
    cum += r["share_pct"]
    r["rank"] = i
    r["cum_share_pct"] = round(cum, 4)

# ---- 五档：按件数绝对阈值（可跨期比较，不做相对分位，避免「每期都有第一名」）----
BANDS = [(20000, "S1 超大（≥2万件）"), (5000, "S2 大（5千–2万）"),
         (1000, "S3 中（1千–5千）"), (200, "S4 小（200–1千）"), (0, "S5 长尾（<200）")]
for r in known:
    for th, lab in BANDS:
        if r["n_patents"] >= th:
            r["band"] = lab
            break
band_dist = {lab: sum(1 for r in known if r["band"] == lab) for _, lab in BANDS}

# ---- 集中度：CR10 / CR50 / HHI / Gini ----
shares = [r["n_patents"] / tot for r in known]
hhi = round(sum(s * s for s in shares) * 10000, 1)
srt = sorted(r["n_patents"] for r in known)
n = len(srt)
cumv = 0
gini_num = 0
for i, v in enumerate(srt, 1):
    gini_num += (2 * i - n - 1) * v
gini = round(gini_num / (n * sum(srt)), 4)

# ---- 按 IPC 部（A–H）汇总（仅 378 节点宇宙）----
SEC_NAME = {"A": "人类生活必需", "B": "作业运输", "C": "化学冶金", "D": "纺织造纸",
            "E": "固定建筑", "F": "机械工程", "G": "物理", "H": "电学"}
sec = {}
for r in known:
    k = r["node"][0]
    d = sec.setdefault(k, {"section": k, "name": SEC_NAME.get(k, ""), "n_nodes": 0,
                           "n_patents": 0, "n_inv": 0, "n_granted": 0, "top_node": None, "_top": -1})
    d["n_nodes"] += 1
    d["n_patents"] += r["n_patents"]
    d["n_inv"] += r["n_inv"]
    d["n_granted"] += r["n_granted"]
    if r["n_patents"] > d["_top"]:
        d["_top"], d["top_node"] = r["n_patents"], r["node"]
for k, d in sec.items():
    d.pop("_top")
    d["share_pct"] = round(100 * d["n_patents"] / tot, 3)
    d["inv_share"] = round(d["n_inv"] / d["n_patents"], 4)
    d["grant_rate"] = round(d["n_granted"] / d["n_patents"], 4)
sec_rows = sorted(sec.values(), key=lambda x: -x["n_patents"])

# ---- 三层对账（把「节点宇宙」与「主表总量」的差额逐层摊开）----
patent = proof.get("patent") or {}
rows_total = int(patent.get("rows") or 0)
ipc_filled = int(patent.get("ipc_filled") or 0)
sum_579 = sum(r[1] for r in raw)
recon = {
    "dwd_patent_rows": rows_total,
    "main_ipc_filled": ipc_filled,
    "main_ipc_rate": round(ipc_filled / rows_total, 4) if rows_total else None,
    "no_ipc_rows": rows_total - ipc_filled,
    "sum_ipc4_codes_in_stats": sum_579,
    "residual_after_codes": ipc_filled - sum_579,
    "sum_378_graph_nodes": tot,
    "graph_node_share_of_main_ipc": round(tot / ipc_filled, 4) if ipc_filled else None,
    "note": ("主表 294 万 → 主分类 IPC 非空 242 万（82.35%）→ 579 个 IPC4 码合计 242.0 万 → "
             f"378 个共类网节点合计 {tot}（占主分类专利 "
             f"{round(tot / ipc_filled * 100, 2)}%）。差额来自无 IPC 的 {rows_total - ipc_filled} 件"
             "与共类网 n≥50 且成边阈值过滤。"),
}

# ---- 第二把尺：关键词计数（独立于 IPC 的另一条路径，用于交叉校验）----
kw_p = T.load_json("tech5_kw_patent.json", {}) or {}
kw_x = {}
for did, d in T.DOMAINS.items():
    kws = {k.split("_")[-1]: v for k, v in kw_p.items() if k.startswith(f"p_{did}_")}
    ipc_nodes = {code: (full[code]["n"] if code in full else None) for code in d["ipc"]}
    ipc_total = sum(v for v in ipc_nodes.values() if v) or None
    best = max(kws.items(), key=lambda kv: kv[1]) if kws else ("", 0)
    kw_x[did] = {
        "name": d["name"], "ipc": d["ipc"], "ipc_counts": ipc_nodes,
        "kw_counts": kws, "kw_total_upper_bound": sum(kws.values()),
        "ipc_total": ipc_total,
        "best_single_term": {"term": best[0], "n": best[1],
                             "ratio_vs_ipc": round(best[1] / ipc_total, 3) if ipc_total else None},
        "ratio_kw_over_ipc": (round(sum(kws.values()) / ipc_total, 3) if ipc_total else None),
    }
# 只有 D-BIO / D-IC 两域自带 IPC 映射，ratio 才有意义
kw_check = {k: v for k, v in kw_x.items() if v["ipc_total"]}

# ---- 应用体量 / 交易体量：为什么不能算 ----
tr = proof.get("transfer") or {}
app_side = {
    "product_count": "无承载表（无产品库/型号库）",
    "output_value_产值": "无承载表",
    "installed_base_装机量": "无承载表",
    "transaction_amount_技术交易额": {
        "table": tr.get("table"), "rows": tr.get("rows"),
        "has_amount_column": tr.get("has_amount_column"),
        "join_to_patent_main": tr.get("join_to_patent_pn"),
        "verdict": (f"表内无金额列；且 {tr.get('rows')} 行中仅 {tr.get('join_to_patent_pn')} 行"
                    f"（{round((tr.get('join_to_patent_pn') or 0) / (tr.get('rows') or 1) * 100, 2)}%）"
                    "能回连 dwd_patent.pn，主体多为境外受让方 → 技术交易额不可算"),
    },
    "paper_count": {"rows": (proof.get("paper") or {}).get("rows"),
                    "verdict": "seed 明令禁止以论文量冒充技术规模；且论文侧关键词命中仅百量级"},
}

# ---- 时间窗事实：增长/环比为何不给 ----
window = {
    "apdt_year_min": patent.get("apdt_year_min"), "apdt_year_max": patent.get("apdt_year_max"),
    "year_dist": patent.get("year_dist"),
    "prev5_sum_in_snapshot": sum(r[4] for r in raw),
    "recent5_sum_in_snapshot": sum(r[3] for r in raw),
    "verdict": ("专利表只有 2021–2026 单窗口：快照里 prev5（上一个五年）合计为 0，"
                "任何环比/增长率都会除以 0；2025/2026 的低值是公开滞后截断，不是规模萎缩"),
}

top = known[0]
out = {
    "metric_id": "M_TECH_OUTPUT_SCALE",
    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "object_universe": "IPC4 技术点（378 个共类网节点，与 M_INNOV_DS_02_PATH_002 同宇宙）",
    "proxy_name": "patent_volume_proxy（技术点专利体量）",
    "proxy_disclaimer": ("seed 明令禁止以专利量冒充「技术规模」专名；本产物只作体量代理，"
                        "对外命名须写「技术点专利规模」，不得写「技术规模」"),
    "nodes_total": len(nodes),
    "nodes_with_volume": len(known),
    "nodes_without_volume": unknown,
    "total_patents_in_nodes": tot,
    "band_distribution": band_dist,
    "concentration": {
        "cr10_pct": round(sum(r["n_patents"] for r in known[:10]) / tot * 100, 3),
        "cr50_pct": round(sum(r["n_patents"] for r in known[:50]) / tot * 100, 3),
        "hhi": hhi, "gini": gini,
        "top1": {"node": top["node"], "n": top["n_patents"], "share_pct": top["share_pct"]},
    },
    "volume_stats": T.stats([r["n_patents"] for r in known]),
    "section_rollup": sec_rows,
    "reconciliation": recon,
    "keyword_crosscheck": kw_check,
    "all_keyword_domains": kw_x,
    "application_side_blockers": app_side,
    "data_window_finding": window,
    "top20": known[:20],
    "bottom10": known[-10:],
    "support_judgment": "部分支持",
    "support_reason": (
        f"成果侧可算：378 个技术点中 {len(known)} 个有专利体量，合计 {tot} 件，"
        f"CR10 {round(sum(r['n_patents'] for r in known[:10]) / tot * 100, 1)}%、HHI {hhi}，"
        f"分布非退化（{band_dist}）。但 seed 定义的「应用体量」四类承载（产品/产值/装机/交易额）"
        "全部缺失，且 seed 明文禁止以专利量冒名——故只能判部分支持。"
    ),
    "elapsed_sec": round(time.time() - t0, 2),
}

(HERE / "M_TECH_OUTPUT_SCALE_out.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")

print(json.dumps({k: out[k] for k in ("nodes_total", "nodes_with_volume", "total_patents_in_nodes",
                                      "band_distribution", "concentration", "volume_stats",
                                      "reconciliation", "keyword_crosscheck", "support_judgment",
                                      "elapsed_sec")}, ensure_ascii=False, indent=1))
print("\nsections:", [(s["section"], s["n_nodes"], s["n_patents"], s["share_pct"]) for s in sec_rows])
print("\ntop10:", [(r["node"], r["n_patents"], r["share_pct"]) for r in known[:10]])
