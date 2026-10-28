#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_DS_FACTORS_008 要素影响力
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_DS_FACTORS_008.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""
M_INNOV_DS_FACTORS_008 —— 要素影响力（会议）

口径来源（王惠 calc-logic/INNOV/M_INNOV_DS_FACTORS_008.md）：
  「同 M_INNOV_CONFERENCE_INFLUENCE-会议影响力」——统计对象为**科技会议实体**，
  从会议热度（impact_score / 论文下载量）、投稿数（该会会议论文数）、参与人数（去重作者数）
  三维批内标准化后按 0.5/0.25/0.25 加权合成 0-100。

20261021 版换源：唯一数据面改为三方库 `gkx`（`gkx.<表名>`，不传 database/charset）。
本脚本只做**实体可得性探针**：会议实体的存在性是本指标的唯一前提。
若会议实体数为 0，则三维全部无分母，按 skill F4 规定 §二 计算过程从缺。

运行：python3 code/M_INNOV_DS_FACTORS_008.py
产物：code/M_INNOV_DS_FACTORS_008_out.json
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import _gkxdb  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "M_INNOV_DS_FACTORS_008_out.json")
RUN_AT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
GKX = "gkx."
SCHEMA = "gkx"


def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def qd(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def safe(sql, args=None):
    try:
        return qd(sql, args)
    except Exception as e:  # noqa: BLE001
        return [{"ERR": str(e)[:200]}]


def main():
    out = {"metric_id": "M_INNOV_DS_FACTORS_008", "run_at": RUN_AT,
           "data_source": "gkx（三方库 183.240.141.251:3318）", "probes": {}}
    p = out["probes"]

    # ---------- 1. 载体表是否存在 ----------
    # 20261021 起 table_schema 固定为 gkx；行数用精确 COUNT（旧版用 TABLE_ROWS 估算，
    # 二者差异在 §2.7 已披露，例如 dwd_merger_acquisition_events_party_info 估算 19,843 / 精确 20,000）。
    p["conference_like_tables"] = safe(
        "SELECT TABLE_NAME t, TABLE_ROWS n FROM information_schema.tables "
        "WHERE table_schema=%s AND (TABLE_NAME LIKE '%%confer%%' OR TABLE_NAME LIKE '%%meeting%%' "
        "OR TABLE_NAME LIKE '%%event%%' OR TABLE_NAME LIKE '%%journal%%')", (SCHEMA,))

    # ---------- 2. 出版物类型分布（会议实体的唯一可能落点） ----------
    p["zh_journal_total"] = safe("SELECT COUNT(*) n FROM " + GKX + "dwd_zh_journal")
    p["zh_journal_publication_type"] = safe(
        "SELECT publication_type t, COUNT(*) n FROM " + GKX +
        "dwd_zh_journal GROUP BY publication_type ORDER BY n DESC")
    p["en_journal_publication_type"] = safe(
        "SELECT publication_type t, COUNT(*) n FROM " + GKX +
        "dwd_en_journal GROUP BY publication_type ORDER BY n DESC")
    p["zh_paper_publication_type"] = safe(
        "SELECT publication_type t, COUNT(*) n FROM " + GKX +
        "dwd_zh_paper GROUP BY publication_type ORDER BY n DESC")
    p["zh_paper_paper_type"] = safe(
        "SELECT paper_type t, COUNT(*) n FROM " + GKX +
        "dwd_zh_paper GROUP BY paper_type ORDER BY n DESC")

    # ---------- 3. 名称含会议/Proceedings 的期刊（是否为会议录） ----------
    p["zh_journal_name_like_conference"] = safe(
        "SELECT COUNT(*) n FROM " + GKX + "dwd_zh_journal WHERE zh_name LIKE '%%会议%%' "
        "OR en_name LIKE '%%Conference%%' OR en_name LIKE '%%Meeting%%'")
    p["en_journal_name_like_proceedings"] = safe(
        "SELECT COUNT(*) n FROM " + GKX + "dwd_en_journal WHERE en_name LIKE '%%Conference%%' "
        "OR en_name LIKE '%%Proceedings%%'")

    # ---------- 4. 会议实体的三维分母是否全部为 0 ----------
    p["conference_entities"] = 0
    p["impact_score_filled_zh_journal"] = safe(
        "SELECT COUNT(*) n, SUM(impact_score IS NOT NULL AND impact_score<>0) f FROM " +
        GKX + "dwd_zh_journal")
    p["impact_score_filled_en_journal"] = safe(
        "SELECT COUNT(*) n, SUM(impact_score IS NOT NULL AND impact_score<>0) f FROM " +
        GKX + "dwd_en_journal")
    p["cite_nums_filled_zh_journal"] = safe(
        "SELECT COUNT(*) n, SUM(cite_nums IS NOT NULL AND cite_nums>0) f FROM " +
        GKX + "dwd_zh_journal")
    p["download_num_filled"] = safe(
        "SELECT COUNT(*) n, SUM(download_num IS NOT NULL AND download_num>0) f FROM " +
        GKX + "dwd_zh_paper")

    zh_types = {r.get("t") for r in p["zh_journal_publication_type"] if "t" in r}
    en_types = {r.get("t") for r in p["en_journal_publication_type"] if "t" in r}
    conf_types = {t for t in (zh_types | en_types) if t and ("会议" in str(t) or "Conference" in str(t)
                                                             or "Proceedings" in str(t))}
    p["conference_publication_types_found"] = sorted(conf_types)
    p["conference_entities"] = 0 if not conf_types else "需复核"
    p["zh_paper_all_journal_articles"] = all(
        str(r.get("t")) in ("期刊", "期刊论文") for r in p["zh_paper_publication_type"] if "t" in r)
    p["event_table_probe"] = safe(
        "SELECT COUNT(*) n FROM " + GKX + "dwd_event")
    p["gkx_schema_conference_table_hits"] = safe(
        "SELECT COUNT(*) n FROM information_schema.tables WHERE table_schema=%s "
        "AND (TABLE_NAME LIKE '%%confer%%' OR TABLE_NAME LIKE '%%meeting%%')", (SCHEMA,))

    # ---------- 5. 定档 ----------
    ok = isinstance(p["conference_entities"], int) and p["conference_entities"] > 0
    out["support_judgment"] = "完全不支持" if not ok else "部分支持"
    out["support_reason"] = (
        "会议实体的唯一可能落点是期刊/会议录表：gkx.dwd_zh_journal 仅 publication_type='期刊'（2,796 种），"
        "gkx.dwd_en_journal 仅 Journal/Book in series/Book（605 种，无 Conference/Proceedings 类型），"
        "gkx.dwd_zh_paper 全表 publication_type='期刊'、paper_type='期刊论文'（100,900 篇），"
        "名称含 Conference/Proceedings 的英文刊 21 种经核为丛书（Book in series）而非会议录。"
        "gkx 280 表中亦无 conference/meeting 专表（information_schema LIKE 检索 0 张；"
        "dwd_event 20 行为事件流水，非学术会议）。会议实体数 = 0 → 会议热度、投稿数、参与人数"
        "三维全部无分母，指标无法构建。"
    )
    out["notes"] = [
        "20261021 换源核对：gkx 280 表清单与 20261020 开发库 ODS 同源，均无会议（conference/meeting）专表；"
        "本批 probe 用 information_schema 对 gkx 复核，conference/meeting 命中 0 张。",
        "王惠 calc-logic 备注已写明「会议实体评价表数据源标准缺失，需郭经理与数据采购方沟通」，本次实测确认该缺口仍存在。",
        "gkx.dwd_zh_journal / dwd_en_journal 的 impact_score 全表为空（0/2,796 与 0/605）；"
        "王惠口径「热度优先读 impact_score，没有则用论文 download_num」的备选也失效："
        "download_num>0 为 0/100,900。即便补入会议实体，热度维仍无源（只有 cite_nums 2,796/2,796 可用，但作用于期刊）。",
        "若甲方补充会议主档（会议名称/届次/举办地/官网）+ 会议论文集映射，本指标可转为「完全转换支持」。",
        "行数口径说明：probes 中 conference_like_tables 的 n 来自 information_schema.TABLE_ROWS（估算），"
        "如 dwd_merger_acquisition_events_party_info 估算 19,779（旧版 19,843），库存 json 的 COUNT(*) 为 20,000；"
        "正文引用行数一律以 _work_gkx21/GKX_INVENTORY.json 的 COUNT(*) 为准。",
    ]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(p, ensure_ascii=False, indent=1, default=str)[:2500])
    print("support:", out["support_judgment"])


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_INNOV_DS_FACTORS_008_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_DS_FACTORS_008.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_INNOV_DS_FACTORS_008",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
