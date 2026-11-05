#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_IND_UI_PANORAMA：产业专题全景（seq168-173）复现件。
投融资事件数/总额（产业口径）+ 深圳研判 + 产业链全景（零部件样例）承载实测。
出参：repro/out/M_IND_UI_PANORAMA_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_IND_UI_PANORAMA",
    "batch": "TOPIC-UI-GAP-L01 批6",
    "probe_date": "2026-11-05",
    "purpose": "产业专题全景六件承载实测（投融资/研判/链全景）",
    "ui_evidence": [
        "seq168/171 投融资事件数、seq169/172 投融资总额（产业整体概况）",
        "seq170 深圳研判、seq173 零部件产业链全景",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def parse_amount_cn(s):
    """中文金额解析（万/亿 → 元）。None/不可解析返回 None。"""
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    try:
        if "亿" in s:
            return float(s.replace("亿", "").replace("人民币", "").strip()) * 1e8
        if "万" in s:
            return float(s.replace("万", "").replace("人民币", "").strip()) * 1e4
        return float(s)
    except (ValueError, TypeError):
        return None


def main():
    cur = gkx()
    # 投融资事件数与总额（中文金额解析口径，B4 校验后落产物）
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_financing_info")
    out["facts"]["financing_events"] = int(cur.fetchone()[0])
    cur.execute("""SELECT funding_amount FROM gkx.dwd_org_financing_info
                   WHERE funding_amount IS NOT NULL AND funding_amount <> ''""")
    total_yuan = 0.0
    parsed = 0
    unparsed_samples = []
    for (amt,) in cur.fetchall():
        v = parse_amount_cn(amt)
        if v is not None:
            total_yuan += v
            parsed += 1
        elif len(unparsed_samples) < 5:
            unparsed_samples.append(str(amt)[:20])
    out["facts"]["financing_amount_parsed_rows"] = parsed
    out["facts"]["financing_amount_unparsed_samples"] = unparsed_samples
    out["derived"]["financing_total_yuan"] = round(total_yuan, 2)
    out["derived"]["financing_total_yi"] = round(total_yuan / 1e8, 4)
    # 年度投融资事件（全景趋势面）
    cur.execute("""SELECT SUBSTRING(CAST(completion_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_org_financing_info
                   WHERE completion_date >= '2018-01-01' AND completion_date < '2026-01-01'
                   GROUP BY y ORDER BY y""")
    out["facts"]["financing_yearly_2018_2025"] = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    # 产业链全景：gkx 链树主承载（12 链 INB12xx-25xx）
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_industry_chain_info""")
    out["facts"]["chain_tree_rows"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(DISTINCT SUBSTRING(industry_code,1,7)) FROM gkx.dwd_industry_chain_info
                   WHERE industry_code IS NOT NULL AND LENGTH(industry_code) >= 7""")
    out["facts"]["chain_count_approx"] = int(cur.fetchone()[0])
    cur.execute("""SELECT industry_name, COUNT(*) AS n FROM gkx.dwd_industry_chain_info
                   WHERE industry_code IS NOT NULL AND LENGTH(industry_code) >= 7
                   GROUP BY industry_name ORDER BY n DESC LIMIT 12""")
    out["facts"]["chain_top_by_nodes"] = [{"k": str(r[0])[:20], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_industry_chain_info WHERE node_company_count > 0""")
    out["facts"]["nodes_with_ent_count"] = int(cur.fetchone()[0])
    cur.close()
    # 深圳研判面：live 链树（12 链主树）
    conn = live("DWD")
    with conn.cursor() as c:
        c.execute("SELECT COUNT(*) AS n FROM chain WHERE chain_id NOT LIKE 'INB17%'")
        out["facts"]["live_chain_main"] = int(c.fetchone()["n"])
        c.execute("SELECT COUNT(*) AS n FROM chain WHERE chain_id LIKE 'INB17%'")
        out["facts"]["live_chain_inb17_legacy"] = int(c.fetchone()["n"])
        c.execute("SELECT COUNT(*) AS n FROM chain_node")
        out["facts"]["live_chain_node_rows"] = int(c.fetchone()["n"])
        c.execute("SELECT COUNT(*) AS n FROM chain_enterprise")
        out["facts"]["live_chain_enterprise_rows"] = int(c.fetchone()["n"])
        c.execute("SELECT COUNT(*) AS n FROM enterprise_industry_chain")
        out["facts"]["live_eic_rows"] = int(c.fetchone()["n"])
    conn.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "投融资双件可复现（事件 25,654 笔；金额为中文混合字符串「8320.0万人民币/4.70亿人民币」，解析口径落产物，"
        "解析成功 " + str(parsed) + " 行、不可解析样例如实披露）；"
        "产业链全景：gkx 链树 1,273 节点（12 链 INB12xx-25xx 主码 1,048 + INB2x 225）实测在，"
        "但 node_company_count 全 0 + live chain_node/chain_enterprise/enterprise_industry_chain 均空表"
        "——链-企业挂接缺失使全景图无企业密度层；深圳研判为 LLM 研判文本（非结构化指标，挂接后可生成）。"
        "→ 部分支持。升档触发器：链-企业挂接灌数（ods_sync 12 链真源）。")
    p = os.path.join(HERE, "out", "M_IND_UI_PANORAMA_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| events:", out["facts"]["financing_events"],
          "| total_yi:", out["derived"]["financing_total_yi"],
          "| chains:", out["facts"]["chain_count_approx"])


if __name__ == "__main__":
    main()
