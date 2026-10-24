#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_185_1 区域产业创新政策综合评价模型 —— gkx 重建版（20261022）。

王惠口径：三维（创新政策数量 / 政策类型 / 政策效果）。
  D1 数量：城市内有效政策去重数；
  D2 类型：覆盖的政策类型数 / 王惠四类词表（科研扶持、成果转化、产业促进、人才引进）；
  D3 效果：实施时效性 + 政策可见度。

本版相对旧版（`_quarantine/20261022_demo_helper/code/M_SYNTH_185_1.py`）：
  1. 旧版 `_b6_engine.conn()` 连演示库；本脚本零数据库连接，只读 `_snapshots21/`。
  2. 评价集从「深/京/沪/广」改为「深/广/莞/惠」，理由见 184 同款说明。
  3. **D2 被迫改口径**：gkx 的 `dwd_policy_base.type` 是**文件体裁**（通知/办法/意见…），
     不是王惠的四类主题；主题字段 `theme` 在 20,000 行里 19,998 行为 0。故 D2 改为
     「文件体裁覆盖度」，并明确它**不是**王惠的四类政策类型。
  4. **D3 整维不可算**：`implementation_date` / `expire_date` 20,000 行**全部为
     `'0000-00-00'`**（不是 NULL、不是空串，所以 `IS NOT NULL` 与非空判断都会误判成
     「100% 有值」）；`link` 20,000 行全部非空、`status` 20,000 行全部为「有效」，
     两个子项在四市之间**零区分度**。旧版把 D3 记为「时效子项缺、可见度单子项可算」，
     实际可见度也是常数 1.0，等同于不可算——本版如实把它整维踢出指数。

输出：`code/M_SYNTH_185_1_out.json`
"""
from __future__ import annotations

import collections
import json
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
import _synth18x_common as S  # noqa: E402

METRIC = "M_SYNTH_185_1"

# 全库出现的非空 type 值（gkx 实测 13 个，来自探针 policy_type_status）
TYPE_VOCAB = [
    "其他通知", "政策文件-管理办法/实施方案", "公示公告", "申报通知",
    "政策文件-指导意见", "政策文件-规划纲要", "政策文件-其他文件",
    "规范性文件-规范条例", "政策文件-政策指南", "规范性文件-部门规章",
    "政策解读", "规范性文件-法律法规", "政策文件-评定标准",
]

DIMS = collections.OrderedDict([
    ("D1_政策数量", ["市级有效政策存量"]),
    ("D2_政策类型", ["文件体裁覆盖度"]),
    ("D3_政策效果", ["实施时效性", "政策可见度"]),
])

SUB_UNAVAILABLE = {
    "实施时效性": "implementation_date / expire_date 全表 20,000 行**全部为 '0000-00-00'**"
             "（零日期占位符），既不是 NULL 也不是空串，因此 `IS NOT NULL`、"
             "`<> ''`、`TRIM()<>''` 三种写法都会把它当有效值；"
             "以 2026-10-22 为基准日代入窗口，四市 1,212 条政策的在效数全部为 0",
    "政策可见度": "link 列 20,000 行全部非空（含四市 1,212 行），四市可见度都是 100%，"
             "极值归一后整列无定义——常数不是「高」，是「测不出差异」",
    "政策主题类型": "王惠四类（科研扶持/成果转化/产业促进/人才引进）在库内无对应字段；"
              "theme 列 19,998/20,000 行为 0，keypoints 为 'NULL' 占位",
}


def main():
    pol = S.policy_stats()
    pubyear = S.policy_pubyear()

    raw = {
        "市级有效政策存量": {c: pol["n"].get(c, 0) for c in S.CITIES},
        "文件体裁覆盖度": {c: round(min(pol["kinds"].get(c, 0) / len(TYPE_VOCAB), 1.0) * 100, 2)
                     for c in S.CITIES},
        "实施时效性": {c: None for c in S.CITIES},
        "政策可见度": {c: None for c in S.CITIES},
    }
    zd = S.q("policy_zero_dates")[0]
    aid = {
        "政策类型数_原始": {c: pol["kinds"].get(c, 0) for c in S.CITIES},
        "link非空数": {c: pol["link"].get(c, 0) for c in S.CITIES},
        "implementation零日期数": {c: pol["impl"].get(c, 0) for c in S.CITIES},
        "expire零日期数": {c: pol["expire"].get(c, 0) for c in S.CITIES},
        "在效政策数_基准日20261022": {c: pol["inforce"].get(c, {}).get("inforce", 0)
                              for c in S.CITIES},
        "全表": {"n": int(zd[0]), "impl_zero_date": int(zd[1]), "expire_zero_date": int(zd[2]),
               "status_有效": int(zd[3]), "link空": int(zd[4]), "link非空": int(zd[5])},
    }

    # D1 用批内 min-max；D2 用固定词表分母（覆盖率，不再二次归一，避免「覆盖度被拉成 0/100」）
    norm = {"市级有效政策存量": S.mm(raw["市级有效政策存量"]),
            "文件体裁覆盖度": dict(raw["文件体裁覆盖度"]),
            "实施时效性": {c: None for c in S.CITIES},
            "政策可见度": {c: None for c in S.CITIES}}

    dim_scores = collections.OrderedDict()
    for d, subs in DIMS.items():
        dim_scores[d] = {c: S.wmean([norm[s].get(c) for s in subs]) for c in S.CITIES}

    n_dims = {c: sum(1 for d in DIMS if dim_scores[d][c] is not None) for c in S.CITIES}
    MIN_DIMS = 2
    index = {c: (S.wmean([dim_scores[d][c] for d in DIMS]) if n_dims[c] >= MIN_DIMS else None)
             for c in S.CITIES}
    rank = sorted([c for c in S.CITIES if index[c] is not None], key=lambda x: -index[x])

    # ---- 敏感性：三条替代口径（全现算）----
    d2_mm = S.mm(raw["文件体裁覆盖度"])
    sensitivity = {
        "只留数量维_D1": dim_scores["D1_政策数量"],
        "只留类型维_D2": dim_scores["D2_政策类型"],
        "类型维改批内min-max": {c: S.wmean([dim_scores["D1_政策数量"][c], d2_mm[c]])
                       for c in S.CITIES},
    }

    # ---- 全表结构分布：从落盘 20,000 行快照现算（不查库）----
    rows_all = S.policy_rows_all()
    by_city = collections.Counter(r["city"] for r in rows_all)
    by_rank = collections.Counter(x for r in rows_all for x in json.loads(r["rank"] or "[]"))
    by_type = collections.Counter(r["type"] for r in rows_all)
    table_distribution = {
        "by_city_top12": [[k, v] for k, v in by_city.most_common(12)],
        "city_null_national": by_city.get("NULL", 0),
        "by_rank": [[k, v] for k, v in by_rank.most_common()],
        "by_type_top8": [[k, v] for k, v in by_type.most_common(8)],
        "by_level": [[str(k), v] for k, v in sorted(
            collections.Counter(r.get("level") for r in S.policy_base_all()).items(),
            key=lambda x: -x[1])],
        "note": "rank=行政层级（省级/市级/国家级/区级/空/园区级）；level 是同一套层级的数字编码"
                "（3/2/4/1/0），两者不是政策效力等级，不得拿来做力度加权",
    }

    out = {
        "metric_id": METRIC,
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "gkx @ 183.240.141.251:3318（gkx_reader_zp 只读），经 _snapshots21/ 落盘快照读取；"
                  "本脚本零数据库连接",
        "evaluation_set": S.CITIES,
        "stat_year": "存量（四市 publish_date 止于 2022，未按年截断；2021—2024 截断口径会把广州政策池从 325 条砍到 39 条）",
        "raw": raw,
        "aux": aid,
        "norm_0_100": norm,
        "dim_scores": dim_scores,
        "n_dims_available": n_dims,
        "min_dims_for_index": MIN_DIMS,
        "index_0_100": {c: (round(index[c], 1) if index[c] is not None else None)
                        for c in S.CITIES},
        "rank": rank,
        "type_vocab": TYPE_VOCAB,
        "type_vocab_n": len(TYPE_VOCAB),
        "sensitivity": sensitivity,
        "table_distribution": table_distribution,
        "sub_unavailable": SUB_UNAVAILABLE,
        "coverage": {
            "policy_rows_total": pol["total_rows"],
            "policy_rows_4city": sum(pol["n"].values()),
            "policy_rows_national": pol["total_rows"] - sum(pol["n"].values()),
            "city_share_pct": round(sum(pol["n"].values()) / pol["total_rows"] * 100, 2),
            "publish_year_max": max((max(v) for v in pubyear.values() if v), default=None),
            "huizhou_rows": pol["n"].get("惠州市", 0),
            "dongguan_rows": pol["n"].get("东莞市", 0),
        },
        "params": {
            "normalization_D1": "批内 min-max（四城，含库内 0 记录的惠州）",
            "normalization_D2": "固定词表分母（13 个体裁值），不做二次归一",
            "index": "三维等权；实际只有 D1/D2 可算，可算维数 2 达到出指数的下限",
            "effect_dim": "整维剔除，不补 0、不用可见度冒充",
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "数量维在四市都有真实读数（深 879 / 广 325 / 莞 8 / 惠 0 条），类型维可用文件体裁覆盖度"
            "代理（深 11 / 广 10 / 莞 4 / 惠 0 类）；但效果维整维不可算：时间戳两列 20,000 行全是 "
            "'0000-00-00' 零日期，link 与 status 在四市是常数、零区分度；且王惠的四类政策主题在库内"
            "无字段（theme 19,998/20,000 为 0）。三维里一维整缺、一维只能代理，"
            "不满足『完全转换支持』的结构+数据双条件，判部分支持"),
        "note": "惠州 0 条是「库内无记录」，不是「惠州没有政策」；东莞 8 条同样处于采集边缘，"
                "其得分不具备城市间比较意义，MD §三 已单列披露。旧版读数（含京沪）来自演示库，"
                "与本版不可直接比较。",
    }
    out.update(S.base_block(
        list(range(1992, 2023)),
        [2023, 2024, 2025, 2026],
        "政策表是**存量表**：四市 1,212 条公告的 publish_date 全部落在 1992—2022"
        "（深圳最早 2000、广州最早 1992、东莞仅 2020—2022 共 8 条、惠州 0 条），"
        "base_years_used 列的是库存量实际覆盖的发布年。2023—2026 进 missing 不是「有数据但缺值」："
        "2023/2025/2026 全表零行，2024 只有 1 条北京记录（『平谷区便民咨询服务电话』）属脏数据，"
        "四市一条都没有，故这四年不进任何分母。另：publish_date 有 3 条零日期 '0000-00-00'，"
        "单独掷出不计年；`implementation_date` / `expire_date` 则是全表 20,000 行全为零日期"
        "（范围谓词实测 impl_zero=20000 / exp_zero=20000），不构成任何可用基期，"
        "`IS NOT NULL` 会把它们误报成 20,000 行有值，本版按零值处理。"))
    S.write_out(METRIC, out)
    print("index", out["index_0_100"], "rank", rank)


if __name__ == "__main__":
    main()
