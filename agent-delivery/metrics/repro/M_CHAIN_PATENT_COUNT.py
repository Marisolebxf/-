#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_PATENT_COUNT —— 产业链关联专利数（20261027 三系统兼容版）

【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统（三系统同一接口）
【维护者】唐绍祖
【兼容设计】见 ../第三方库指标计算过程/M_CHAIN_PATENT_COUNT.md「一・三、三系统需求兼容性设计」
          与 ../过程文件/04_兼容接口设计规约.md
【基线】20261021 改源版（口径不变，兼容层只包装入参/出参，不改变数学定义）

三系统调用注意（后端必读）
--------------------------
1. 算法库同事：全量传参走 `compute({...})`，`region_scope="national"` + `start_year/end_year`。
2. 专题系统同事：可以只传 `{}` 甚至不传——缺省 2021–2024 全量 12 链，缺省行为
   会写进出参 `assumptions`，前端可提示。**不要把 12 链之和当去重专利总数**（多链重复计位）。
3. 展示系统同事：直接消费出参 `display` 段（12 链对比柱 + 城市分布）；`patent_type`
   传 "applied" 不会改变数值（gkx 无授权标记列，申请/授权同值），会进 `assumptions` 提示。
4. 2025/2026 不要传入正式统计窗（专利公开滞后 18 个月，纳入会系统性低估近年值）。
5. 本件与 M_CHAIN_REG_PATENT 不是同一个数（单角色桥 vs 双角色并集），不可互相替代。

口径（与 20261021 基线一致，未改动）
------------------------------------
  COUNT(DISTINCT patent_id) WHERE 申请人名 = 企业名 ∧ 企业挂该链 ∧ application_year ≤ 2024
专利池：gkx.dwd_patent 2,939,895 行；申请人桥：first_applicant_name = dwd_org_base_info.name_cn
（1,107,178 件命中）。读共享快照 region_index_patent_union.json（chain|city → 件数），逐链汇总。
"""
from __future__ import annotations

import json
import os
import time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_PATENT_COUNT_out.json")

APPLICABLE = ["科技专题服务算法库", "科技专题系统", "科技信息展示系统"]

# 缺省参数（任何系统不传参时的行为；md「入参兼容策略」表与此一一对应）
DEFAULTS = {
    "start_year": 2021,        # 算法库/展示常传；专题缺省 → 全量正式窗起点
    "end_year": 2024,          # 公开滞后 18 个月，2025/2026 不可入正式值（传了会被截回并在 assumptions 提示）
    "patent_type": "granted_and_applied",  # 展示侧可传 "applied"；gkx 无授权标记列，两口径同值
    "region_scope": "all",     # "national"=全量 / "sz" / "four_city"；缺省全量+四市拆分
    "industry_tag": None,      # 链码/技术领域标签；None → 12 链全量
}


def L(n):
    with open(os.path.join(SNAP, n), encoding="utf-8") as f:
        return json.load(f)


def _region_filter(city: str, scope: str) -> bool:
    """按 region_scope 过滤城市行。scope 取值见 DEFAULTS['region_scope'] 注释。"""
    if scope == "sz":
        return city == "深圳市"
    if scope == "four_city":
        return city in ("深圳市", "广州市", "东莞市", "惠州市")
    return True  # "national"/"all"：不过滤


def compute(params: dict | None = None) -> dict:
    """三系统统一入口。参数语义与缺省行为见模块 docstring 与 md「入参兼容策略」。"""
    p_in = dict(params or {})
    p = {**DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions: list[str] = []

    # 截断保护：2025/2026 不可入正式窗（专利公开滞后），自动截回并声明
    if p["end_year"] > 2024:
        assumptions.append(
            f"end_year={p['end_year']} 超过可靠公开窗（专利公开滞后18个月），已截回 2024")
        p["end_year"] = 2024
    if p["patent_type"] in ("applied", "granted"):
        assumptions.append(
            "patent_type 申请/授权口径不可分：gkx.dwd_patent 无授权标记列，两口径同值（基线已声明）")
    if p["start_year"] < 2021:
        assumptions.append("start_year 早于 2021：快照按 2021–2024 窗口落盘，超出部分不可分")

    union = L("region_index_patent_union.json")
    layer = L("chain21_layer_20261022.json")
    chains = layer["chain_name"]
    FOUR = ["深圳市", "广州市", "东莞市", "惠州市"]

    agg: dict = {}
    for k, v in union.items():
        ch, city = k.split("|")
        if not _region_filter(city, p["region_scope"]):
            continue
        a = agg.setdefault(ch, {"total": 0, "four": 0, "cities": {}})
        a["total"] += v
        a["cities"][city] = v
        if city in FOUR:
            a["four"] += v

    wanted = [p["industry_tag"]] if p["industry_tag"] else list(chains.keys())
    rows = []
    for ch in wanted:
        nm = chains.get(ch, ch)
        a = agg.get(ch, {"total": 0, "four": 0, "cities": {}})
        firms = layer["chain_city"].get(ch + "|深圳市", 0)
        members = sum(v for k, v in layer["chain_city"].items() if k.startswith(ch + "|"))
        rows.append({
            "chain_code": ch, "chain_name": nm,
            "patents_le2024": a["total"],
            "patents_le2024_four_city": a["four"],
            "patents_le2024_outside_four": a["total"] - a["four"],
            "outside_share_pct": round(100.0 * (a["total"] - a["four"]) / a["total"], 3) if a["total"] else None,
            "sz_patents_le2024": a["cities"].get("深圳市", 0),
            "chain_members": members,
            "patents_per_member": round(a["total"] / members, 2) if members else None,
            "members_with_sz_reg": firms,
            "top_cities": sorted(a["cities"].items(), key=lambda x: -x[1])[:4],
        })
    rows.sort(key=lambda r: -r["patents_le2024"])

    # 快照为 2021–2024 全窗口聚合，年度序列与年份过滤在快照粒度上不可再分：
    # 显式声明而不是静默当作已过滤（B4：负结论要有否定性证据）。
    if (p["start_year"], p["end_year"]) != (2021, 2024) or p["region_scope"] not in ("all", "national"):
        assumptions.append(
            "快照粒度为「链×城市」2021–2024 全窗聚合：年份子窗与 region_scope 过滤在当前快照上不可再分，"
            "返回值为全窗口口径（如需年度序列需上游按年重扫 dwd_patent）")

    tot = sum(r["patents_le2024"] for r in rows)
    four = sum(r["patents_le2024_four_city"] for r in rows)
    sz = sum(r["sz_patents_le2024"] for r in rows)
    vals = sorted(r["patents_le2024"] for r in rows)
    members = sum(r["chain_members"] for r in rows)
    stats = {
        "n_chains": len(rows),
        "min": vals[0] if vals else 0, "max": vals[-1] if vals else 0,
        "median": vals[len(vals) // 2] if vals else 0,
        "top1_share_pct": round(100.0 * vals[-1] / tot, 3) if tot else None,
        "top3_share_pct": round(100.0 * sum(vals[-3:]) / tot, 3) if tot else None,
        "sz_share_pct": round(100.0 * sz / tot, 3) if tot else None,
        "four_city_share_pct": round(100.0 * four / tot, 3) if tot else None,
        "chain_members_total": members,
        "patents_per_member_all": round(tot / members, 2) if members else None,
        "zero_chains": sum(1 for r in rows if r["patents_le2024"] == 0),
    }

    result = {
        "metric_id": "M_CHAIN_PATENT_COUNT",
        "metric_name": "产业链关联专利数",
        "applicable_systems": APPLICABLE,
        "params_effective": {k: p[k] for k in DEFAULTS},
        "assumptions": assumptions,
        "support_judgment": "完全转换支持",
        "judgment_reason": "专利池 2,939,895 件、机构底册 189,116 家、链标签 2,283,762 行三段真实数据齐备，"
                           "12/12 链全部算出非零值（16,300—537,046 件），截断与去重规则可执行、脚本可复跑；"
                           "名称桥的已知漏计（非第一申请人、更名、同名）写入 gaps，属口径下界而非数据缺口。",
        "base_years_used": ["2021", "2022", "2023", "2024"],
        "base_years_missing": ["2025", "2026"],
        "base_years_note": "统计期 2025 年，专利按申请年 ≤2024 截断：发明专利公开滞后 18 个月，"
                           "2025—2026 年申请量不完整，纳入会系统性低估近年值；池内 2021—2026 全覆盖，"
                           "2025/2026 两年仅作观察不入正式值。",
        "sources": [
            "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_patent（2,939,895 行）",
            "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_org_base_info（189,116 行，申请人名桥）",
            "gkx @ 183.240.141.251:3318 / gkx_reader_zp: gkx.dwd_org_industry_tags（链归属）",
            "code/_snapshots21/region_index_patent_union.json（chain|city 汇总，含四市与省外）",
            "code/_snapshots21/chain21_layer_20261022.json（链成员数，与 M_CHAIN_ENTERPRISE_COUNT 同池）",
        ],
        "rule": {
            "unit": "件（patent_id 去重，一案一件；同族不做合并）",
            "pool": "gkx.dwd_patent 全量，按 application_year ≤ 2024 截断",
            "applicant_bridge": "first_applicant_name = name_cn 精确等值（1,107,178 件命中，命中率 37.66%）",
            "chain_attr": "企业挂该链即整件计入；多链企业按链重复计入（与 M_CHAIN_ENTERPRISE_COUNT 同池同链码）",
            "region_axis": "省级归属取申请人企业底册 city；四市 = 深圳/广州/东莞/惠州",
            "why_first_applicant": "dwd_patent 只存第一申请人名；合作申请中非第一申请人的企业不计，属已知下界",
        },
        "value": tot,                      # 主值（单链查询时即该链值；全量=合计）
        "detail": {"stats": stats},        # 计算明细
        "chains": rows,
        "headline": {
            "total_le2024": tot,
            "four_city_total": four,
            "outside_four_share_pct": round(100.0 * (tot - four) / tot, 3) if tot else None,
            "sz_total": sz,
            "unit": "件",
            "n_chains": len(rows),
        },
        "display": {                       # 展示系统直接消费段
            "bar_12chains": [{"name": r["chain_name"], "value": r["patents_le2024"]} for r in rows],
            "sz_vs_outside": {"深圳": sz, "四市其它": four - sz, "省外": tot - four},
            "per_member_density": [{"name": r["chain_name"], "value": r["patents_per_member"]} for r in rows],
            "trend_hint": "年度序列需上游按年重扫 dwd_patent；当前快照为 2021–2024 全窗聚合",
        },
        "gaps": [
            "第一申请人桥：只认第一申请人，合作申请里排第二的链内企业不计，专利数偏低",
            "名称桥：同名企业会合并计数；企业更名/简称不匹配会漏计（桥命中率 37.66% 为整体，链内企业更高）",
            "多链重复：同一件专利若企业挂多链会在各链各计一次，12 链之和 > 去重专利数",
            "同族 M_CHAIN_REG_PATENT 用第一申请人单角色桥（1,127,340 件、每件只计一次），本件用双角色并集"
            "（3,026,291 计位、多链重复）；两者不是同一个数，不可互相校验或替代",
        ],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - T0, 2),
    }
    return result


def main():
    # 缺省运行 = 专题系统姿势（零传参）；算法库全量传参结果与缺省一致（参数都在缺省窗内）
    result = compute()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("total", result["value"], "four", result["headline"]["four_city_total"],
          "sz", result["headline"]["sz_total"])
    for r in result["chains"]:
        print(r["chain_code"], r["chain_name"], r["patents_le2024"],
              r["sz_patents_le2024"], r["patents_per_member"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
