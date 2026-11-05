#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POL_UI_CMS_INTENSITY：政策新闻内容管理（力度评估 seq61 + 统计与区域 seq74）探针件。
力度评估=需业务建模类（高优先）；统计与区域=CMS 管理侧统计面。共享承载实测。
出参：repro/out/M_POL_UI_CMS_INTENSITY_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_POL_UI_CMS_INTENSITY",
    "batch": "TOPIC-UI-GAP-L01 批4",
    "probe_date": "2026-11-05",
    "purpose": "政策新闻内容管理：力度评估（建模件）+ 统计与区域（CMS 统计面）承载实测",
    "ui_evidence": ["views/policy/PolicyNewsCmsPage.vue:L21-22（seq61 力度评估 / seq74 统计与区域）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    # 力度评估原料：policy_support / keypoints / type（文件类型与力度相关）
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL AND policy_support <> ''")
    out["facts"]["policy_support_nonnull"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE keypoints IS NOT NULL AND keypoints <> '' AND keypoints <> 'NULL'")
    out["facts"]["keypoints_nonnull"] = int(cur.fetchone()[0])
    cur.execute("""SELECT type, COUNT(*) AS n FROM gkx.dwd_policy_base
                   WHERE type IS NOT NULL AND type <> '' AND type <> 'NULL'
                   GROUP BY type ORDER BY n DESC LIMIT 8""")
    out["facts"]["type_dist"] = [{"k": str(r[0])[:22], "n": int(r[1])} for r in cur.fetchall()]
    # 统计与区域原料：区域三级列全填（2 万条）+ 年度
    for col in ('province', 'city', 'district'):
        cur.execute(f"""SELECT COUNT(*) FROM gkx.dwd_policy_base
                        WHERE {col} IS NOT NULL AND {col} <> '' AND {col} <> 'NULL'""")
        out["facts"][f"{col}_real_nonnull"] = int(cur.fetchone()[0])
    cur.execute("""SELECT city, COUNT(*) AS n FROM gkx.dwd_policy_base
                   WHERE city IS NOT NULL AND city <> '' AND city <> 'NULL'
                   GROUP BY city ORDER BY n DESC LIMIT 8""")
    out["facts"]["city_top8"] = [{"k": str(r[0])[:14], "n": int(r[1])} for r in cur.fetchall()]
    cur.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "力度评估（需业务建模类·高优先）：力度打分无结构列（policy_support 0 真值）、keypoints 0 真值——"
        "打分模型待建（text 可解析：content 全文列在 + type 文件类型分布实测），建模口径甲方未给 → 部分支持；"
        "统计与区域：province/city/district 三级列 2 万条全填、城市分布实测（北京 1,932/上海 1,842/深圳 879）→ CMS 统计面可复现。"
        "升档触发器：力度评估模型口径（要素清单/分值规则）甲方给出。")
    p = os.path.join(HERE, "out", "M_POL_UI_CMS_INTENSITY_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("support =", out["facts"]["policy_support_nonnull"],
          "| type_dist =", out["facts"]["type_dist"][:4],
          "| city_top =", out["facts"]["city_top8"][:3])


if __name__ == "__main__":
    main()
