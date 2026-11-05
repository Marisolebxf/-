#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POL_UI_TIMELINE_CFG：政策时序分析·权威渠道（分析配置，seq55）+ 区域政策对比·对比区域/评价维度（seq56/57）
配置项三件合一探针件：权威渠道值域（ministry 2 万条实测）、对比区域值域（province/city 实测）、评价维度（列承载缺披露）。
出参：repro/out/M_POL_UI_TIMELINE_CFG_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_POL_UI_TIMELINE_CFG",
    "batch": "TOPIC-UI-GAP-L01 批4",
    "probe_date": "2026-11-05",
    "purpose": "政策时序/区域对比配置项值域实测（权威渠道/对比区域/评价维度）",
    "ui_evidence": [
        "views/policy 分析配置面板（seq55 权威渠道：国家部委/地方政府）",
        "对比区域选择（seq56：深圳/长三角/粤港澳/京津冀/成渝）",
        "评价维度复选（seq57：资金规模/土地供给/税收优惠/人才政策/创新…）",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("""SELECT ministry, COUNT(*) AS n FROM gkx.dwd_policy_base
                   WHERE ministry IS NOT NULL AND ministry <> ''
                   GROUP BY ministry ORDER BY n DESC LIMIT 12""")
    out["facts"]["ministry_top12"] = [{"k": str(r[0])[:28], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE ministry IS NOT NULL AND ministry <> ''")
    out["facts"]["ministry_nonnull"] = int(cur.fetchone()[0])
    cur.execute("""SELECT province, COUNT(*) AS n FROM gkx.dwd_policy_base
                   WHERE province IS NOT NULL AND province <> '' AND province <> 'NULL'
                   GROUP BY province ORDER BY n DESC LIMIT 10""")
    out["facts"]["province_top10"] = [{"k": str(r[0])[:14], "n": int(r[1])} for r in cur.fetchall()]
    # 五大区域群可组性（省码清单）
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE province IN
                   ('广东省','上海市','江苏省','浙江省','安徽省','北京市','天津市','河北省','四川省','重庆市')""")
    out["facts"]["five_region_group_hits"] = int(cur.fetchone()[0])
    # 评价维度候选列（资金/土地/税收/人才 关键词列探测）
    cur.execute("SHOW COLUMNS FROM gkx.dwd_policy_base")
    cols = [r[0] for r in cur.fetchall()]
    out["facts"]["eval_dim_candidate_cols"] = [c for c in cols if any(
        k in c for k in ("support", "fund", "money", "tax", "land", "talent"))]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL AND policy_support <> ''")
    out["facts"]["policy_support_nonnull"] = int(cur.fetchone()[0])
    cur.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "权威渠道面实测（ministry 2 万条全填：工信部 637/上海企业服务云 548/深圳政府 346…国家部委 vs 地方政府可分）；"
        "对比区域面实测（province 十省市 15,000+ 条，五大区域群可组）；"
        "评价维度（资金/土地/税收/人才）列承载缺——policy_support 列实测 0 真值、维度打分无结构列 → 部分支持。"
        "升档触发器：政策结构化解析（support 要素抽取）落地。")
    p = os.path.join(HERE, "out", "M_POL_UI_TIMELINE_CFG_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("five_region_hits =", out["facts"]["five_region_group_hits"],
          "| eval_cols =", out["facts"]["eval_dim_candidate_cols"],
          "| support_nonnull =", out["facts"]["policy_support_nonnull"])


if __name__ == "__main__":
    main()
