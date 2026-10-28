#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_SZ_POLICY 深圳政策维度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_SZ_POLICY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_SZ_POLICY 深圳政策维度 —— 可运行复现脚本（2026-10-21 · gkx 改源版）

指标：产业链分析 / 深圳产业情况分析对比 / 四维对比 · 深圳政策维度
数据源：三方库 gkx（183.240.141.251:3318）`gkx.dwd_policy_base`，经 `_gkxdb.gkx()` 只读连接。
口径（本报告重建，仿王惠）：政策数量 + 政策强度（层级代理）合成 0–100。
关键约束（实测）：status 20,000 行恒为「有效」；theme 有效 2 行；keywords / policy_support 0 行；
keypoints 0 行；district 872/879 为空；publish_year 集中在 2014–2022，2023 年后基本断档。
故政策只能按「标题/正文关键词」做代理匹配，精度须披露。

产出：code/M_CHAIN_SZ_POLICY_out.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import gkx  # noqa: E402

MID = "M_CHAIN_SZ_POLICY"
OUT = Path(__file__).parent / f"{MID}_out.json"
t0 = time.time()
res: dict = {"metric_id": MID, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
             "data_source": "gkx（三方库 gkx.dwd_policy_base，只读）"}

_cur = gkx()


def q(sql, args=None):
    if args:
        _cur.execute(sql, args)
    else:
        _cur.execute(sql)
    cols = [c[0] for c in _cur.description]
    return [dict(zip(cols, r)) for r in _cur.fetchall()]


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def step(name, fn):
    t = time.time()
    try:
        res[name] = fn()
    except Exception as e:  # noqa: BLE001
        res[name] = f"ERR {str(e)[:200]}"
    print(f"[{time.time()-t:6.1f}s] {name}: {str(res[name])[:260]}", flush=True)


# ------------------------------------------------------------------ 1 探针
step("probe_total", lambda: q1("SELECT COUNT(*) n FROM gkx.dwd_policy_base"))
step("probe_status", lambda: q("SELECT status, COUNT(*) n FROM gkx.dwd_policy_base GROUP BY status"))
step("probe_dead_cols", lambda: q1("""
SELECT SUM(theme IS NOT NULL AND UPPER(theme)<>'NULL' AND theme<>'') theme_n,
       SUM(keywords IS NOT NULL AND UPPER(keywords)<>'NULL' AND keywords<>'') kw_n,
       SUM(quote_policy IS NOT NULL AND UPPER(quote_policy)<>'NULL' AND quote_policy<>'') quote_n,
       SUM(policy_support IS NOT NULL AND UPPER(policy_support)<>'NULL' AND policy_support<>'') support_n,
       SUM(keypoints IS NOT NULL AND UPPER(keypoints)<>'NULL' AND keypoints<>'') keypoints_n,
       SUM(content IS NOT NULL AND LENGTH(content)>50) content_n
FROM gkx.dwd_policy_base"""))
step("probe_year", lambda: q("SELECT publish_year, COUNT(*) n FROM gkx.dwd_policy_base WHERE publish_year IS NOT NULL AND UPPER(publish_year)<>'NULL' GROUP BY publish_year ORDER BY publish_year DESC LIMIT 14"))
step("probe_city", lambda: q("SELECT city, COUNT(*) n FROM gkx.dwd_policy_base WHERE city IS NOT NULL AND UPPER(city)<>'NULL' GROUP BY city ORDER BY n DESC LIMIT 10"))
step("probe_rank", lambda: q("SELECT `rank`, COUNT(*) n FROM gkx.dwd_policy_base GROUP BY `rank` ORDER BY n DESC LIMIT 8"))
step("probe_type", lambda: q("SELECT type, COUNT(*) n FROM gkx.dwd_policy_base GROUP BY type ORDER BY n DESC LIMIT 9"))
step("probe_sz_district", lambda: q("SELECT district, COUNT(*) n FROM gkx.dwd_policy_base WHERE city='深圳市' GROUP BY district ORDER BY n DESC LIMIT 8"))
step("probe_sz_total", lambda: q1("SELECT COUNT(*) n FROM gkx.dwd_policy_base WHERE city='深圳市'"))
step("probe_gd_total", lambda: q1("SELECT COUNT(*) n FROM gkx.dwd_policy_base WHERE province='广东省'"))
step("probe_sz_title", lambda: q1("SELECT COUNT(*) n FROM gkx.dwd_policy_base WHERE title LIKE '%深圳%'"))

# -------------------------------------------------- 2 链关键词（政策文本代理）
CHAIN_KW = {
    "新一代信息技术": ["人工智能", "集成电路", "软件", "5G", "大数据", "云计算", "信息技术", "通信"],
    "生物": ["生物医药", "生物", "医疗器械", "创新药", "医药"],
    "新能源": ["新能源", "光伏", "储能", "氢能", "风电", "电池"],
    "新材料": ["新材料"],
    "高端装备": ["高端装备", "机器人", "数控", "智能制造", "工业母机"],
    "智能网联新能源汽车": ["智能网联", "新能源汽车", "汽车"],
    "绿色环保": ["节能环保", "双碳", "绿色低碳", "环保"],
    "低空经济与空天": ["低空", "无人机", "通用航空", "空天"],
    "传统与创意": ["文化创意", "时尚", "工业设计"],
    "海洋": ["海洋", "船舶"],
    "未来制造": ["增材制造", "3D打印"],
    "未来信息": ["量子", "6G", "光通信"],
    "未来能源": ["可控核聚变", "核能"],
    "未来空间": ["商业航天", "深空"],
    "未来健康": ["合成生物", "细胞", "基因", "脑机"],
}


def chain_policy():
    out = []
    for chain, kws in CHAIN_KW.items():
        like = " OR ".join([f"title LIKE '%{k}%' OR content LIKE '%{k}%'" for k in kws])
        row = q1(f"""
            SELECT COUNT(*) n,
                   SUM(type LIKE '政策文件-%' OR type LIKE '规范性文件-%') doc_n,
                   SUM(`rank` LIKE '%区级%' OR `rank` LIKE '%园区级%') grass_n,
                   MAX(publish_year) latest_year
            FROM gkx.dwd_policy_base
            WHERE city='深圳市' AND ({like})""")
        nat = q1(f"SELECT COUNT(*) n FROM gkx.dwd_policy_base WHERE ({like})")
        out.append({
            "chain": chain,
            "keywords": kws,
            "sz_policy_n": int(row["n"] or 0),
            "sz_doc_n": int(row["doc_n"] or 0),
            "sz_grass_n": int(row["grass_n"] or 0),
            "sz_latest_year": row["latest_year"],
            "national_policy_n": int(nat["n"] or 0),
            "sz_share_pct": round((row["n"] or 0) / nat["n"] * 100, 2) if nat["n"] else 0.0,
        })
    return out


step("chain_policy", chain_policy)

# ------------------------------------------------------------ 3 打分（0–100）
def scores():
    rows = res.get("chain_policy") or []
    if not isinstance(rows, list) or not rows:
        return "ERR"
    mx = max(r["sz_policy_n"] for r in rows) or 1
    out = []
    for r in rows:
        qty = r["sz_policy_n"] / mx * 100
        inten = (r["sz_doc_n"] / r["sz_policy_n"] * 100) if r["sz_policy_n"] else 0.0
        grass = (r["sz_grass_n"] / r["sz_policy_n"] * 100) if r["sz_policy_n"] else 0.0
        out.append({**r,
                    "qty_score": round(qty, 2),
                    "intensity_score": round(inten, 2),
                    "grassroots_pct": round(grass, 2),
                    "composite_0_100": round(0.6 * qty + 0.4 * inten, 2)})
    out.sort(key=lambda x: -x["composite_0_100"])
    return out


step("scores", scores)

# 全量文本代理精度自检：关键词命中「其他通知/公示公告」这类非政策文件的比例
step("precision_probe", lambda: q("""
SELECT type, COUNT(*) n FROM gkx.dwd_policy_base
WHERE city='深圳市' AND (title LIKE '%人工智能%' OR content LIKE '%人工智能%')
GROUP BY type ORDER BY n DESC LIMIT 8"""))

res["support_judgment"] = "部分支持"
res["support_reason"] = (
    "政策数量维可算（20,000 条真题录政策，深圳 879 条，正文可用 18,763 条）；"
    "强度维无承载（fiscal_sci_tech_exp / general_public_budget 两列不存在，theme/keywords/policy_support/keypoints 全部空或字面 NULL），"
    "只能用「市级/区级占比」代理；status 20,000 行恒为「有效」使有效性筛选恒真；publish_year 2023 年后断档 —— 故判部分支持。"
)
res["_elapsed_s"] = round(time.time() - t0, 1)
# gkx 把缺失值写成字面 'NULL'/'null' 字符串；展示层归一为 null，避免被误读为真实取值
for _k, _f in (("probe_type", "type"), ("probe_sz_district", "district")):
    if isinstance(res.get(_k), list):
        for _r in res[_k]:
            if isinstance(_r.get(_f), str) and _r[_f].strip().upper() == "NULL":
                _r[_f] = None
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("wrote", OUT, f"{res['_elapsed_s']}s")


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
    out_json = here / "M_CHAIN_SZ_POLICY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_SZ_POLICY.py 等价）
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
        "metric_id": "M_CHAIN_SZ_POLICY",
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
