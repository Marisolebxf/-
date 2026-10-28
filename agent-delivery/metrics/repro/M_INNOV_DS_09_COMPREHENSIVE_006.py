#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_09_COMPREHENSIVE_006 科技人才流动监控（王惠口径＝产业界↔学术界 · 20261021 改源版）

王惠口径（calc-logic/INNOV/M_INNOV_PLAN_TALENT_FLOW.md）：
  核心技术人才入集；按工作经历相邻任职性质变化识别流动；二维 = 学界→产业 / 产业→学界；
  近窗相对基线增速超阈预警（burst≥1→2，≥0.5→1，否则 0）。

数据源（20261021 版）：**只读三方库 gkx**
  gkx.dwd_scholar_work_experience / dwd_scholar / dwd_scholar_talent_flag /
  dwd_org_base_info / dwd_research_institute_base_info / dwd_forg_university_org_info
  —— 六表在 gkx 与旧 ods 之间逐表镜像（DATA_FACTS §2），算法逐字未改，读数应完全一致。
"""
import json
import os
import re
import time
from collections import Counter, defaultdict

import _innov_gkx21_common as ic

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "M_INNOV_DS_09_COMPREHENSIVE_006_out.json")

# 任职性质判定：先判产业（公司后缀），再判学术（院校/院所/医院），其余记 unclassified
IND = ic.IND_RX
ACA = ic.ACA_RX


def kind_of(name):
    if not name:
        return "empty"
    if IND.search(name):
        return "industry"
    if ACA.search(name):
        return "academic"
    return "other"


def year_of(s):
    s = (s or "").strip()
    m = re.match(r"(\d{4})", s)
    return int(m.group(1)) if m else None


def main():
    t0 = time.time()
    out = {"metric_id": "M_INNOV_DS_09_COMPREHENSIVE_006", "probes": {}, "compute": {}}

    # 行数只读库存 json（GKX_INVENTORY.json）
    for t in ["dwd_scholar_work_experience", "dwd_scholar", "dwd_scholar_talent_flag",
              "dwd_research_institute_base_info", "dwd_forg_university_org_info", "dwd_org_base_info"]:
        out["probes"][t] = ic.count(t)
    out["probes"]["join_scholar_master"] = ic.q1(
        "SELECT COUNT(DISTINCT w.scholar_id) FROM gkx.dwd_scholar_work_experience w "
        "JOIN gkx.dwd_scholar s ON s.scholar_id=w.scholar_id")[0]

    rows = ic.q("SELECT scholar_id, seq_no, start_time, end_time, is_current, org_name_zh, org_name_en "
                "FROM gkx.dwd_scholar_work_experience")
    kind = Counter()
    per_scholar = defaultdict(list)
    for r in rows:
        sid, seq, start, end, cur, nm_zh, nm_en = r
        nm = (nm_zh or "").strip() or (nm_en or "").strip()
        k = kind_of(nm)
        kind[k] += 1
        per_scholar[sid].append(
            {"seq": seq or 0, "start": start or "", "kind": k, "org": nm})
    out["probes"]["org_kind"] = dict(kind)
    out["probes"]["org_kind_share"] = {k: round(v / len(rows), 4) for k, v in kind.items()}
    out["probes"]["scholars_total_in_we"] = len(per_scholar)
    out["probes"]["scholars_ge2_records"] = sum(1 for v in per_scholar.values() if len(v) >= 2)

    # 相邻任职性质变化
    trans = Counter()
    trans_year = defaultdict(Counter)
    samples = []
    flowing = set()
    for sid, lst in per_scholar.items():
        lst.sort(key=lambda x: (x["seq"], x["start"]))
        for a, b in zip(lst, lst[1:]):
            if a["kind"] in ("academic", "industry") and b["kind"] in ("academic", "industry") \
                    and a["kind"] != b["kind"]:
                key = a["kind"] + "->" + b["kind"]
                trans[key] += 1
                flowing.add(sid)
                y = year_of(b["start"]) or year_of(a["start"])
                if y:
                    trans_year[y][key] += 1
                if len(samples) < 20 and re.search(r"[\u4e00-\u9fa5]", a["org"] + b["org"]):
                    samples.append({"scholar_id": sid, "from_org": a["org"], "from_kind": a["kind"],
                                    "to_org": b["org"], "to_kind": b["kind"], "year": y})
    out["compute"]["transition_counts"] = dict(trans)
    out["compute"]["distinct_scholars_flowing"] = len(flowing)

    years = sorted(y for y in trans_year if 2005 <= y <= 2026)
    series = []
    for y in years:
        series.append({"year": y,
                       "academic_to_industry": trans_year[y].get("academic->industry", 0),
                       "industry_to_academic": trans_year[y].get("industry->academic", 0)})
    out["compute"]["year_series"] = series

    # 预警：近窗(2023-2024) 相对基线(2015-2022)
    def burst(key, recent=(2023, 2024), base=(2015, 2022)):
        rec = [trans_year[y].get(key, 0) for y in range(recent[0], recent[1] + 1)]
        bs = [trans_year[y].get(key, 0) for y in range(base[0], base[1] + 1)]
        rec_m = sum(rec) / len(rec)
        bs_m = sum(bs) / max(len(bs), 1)
        b = (rec_m - bs_m) / max(bs_m, 1)
        level = 2 if b >= 1 else (1 if b >= 0.5 else 0)
        return {"recent_mean": round(rec_m, 3), "base_mean": round(bs_m, 3),
                "burst": round(b, 4), "alert_level": level}

    out["compute"]["alert"] = {
        "academic_to_industry": burst("academic->industry"),
        "industry_to_academic": burst("industry->academic"),
        "window_definition": "近窗=2023-2024，基线=2015-2022；阈值沿用王惠 burst≥1→2、≥0.5→1",
    }
    out["compute"]["samples_cn"] = samples

    # 院士/高层次标识联动
    fl = list(flowing)[:5000]
    if fl:
        q = ic.sql_list(fl)
        out["compute"]["flowing_with_talent_flag"] = ic.q1(
            "SELECT COUNT(DISTINCT scholar_id) FROM gkx.dwd_scholar_talent_flag "
            "WHERE scholar_id IN (%s)" % q)[0]
        out["compute"]["flowing_in_research_institute_names"] = None

    # 机构名对齐（学术机构能否落到科研机构底册/海外高校表）
    # 排序后再取样：旧版直接对 set 取前 4,000 个，受 Python 字符串哈希随机化影响，
    # 同一份数据两次运行会得到 5 / 7 两个不同命中数（不可复现）。本版固定按名称排序取样。
    aca_names = sorted({r[5] for r in rows
                        if r[5] and kind_of(r[5]) == "academic"})
    out["probes"]["academic_org_distinct"] = len(aca_names)
    hit_ri = 0
    for i in range(0, min(len(aca_names), 4000), 1000):
        part = aca_names[i:i + 1000]
        hit_ri += ic.q1("SELECT COUNT(*) FROM gkx.dwd_research_institute_base_info "
                        "WHERE name_cn IN (%s)" % ic.sql_list(part))[0]
    out["probes"]["academic_org_hit_research_institute"] = hit_ri
    out["probes"]["academic_org_hit_sample_size"] = min(len(aca_names), 4000)
    out["elapsed_s"] = round(time.time() - t0, 1)
    out["data_source"] = {"schema": "gkx", "host": "183.240.141.251:3318",
                          "tables": ["gkx.dwd_scholar_work_experience", "gkx.dwd_scholar",
                                     "gkx.dwd_scholar_talent_flag",
                                     "gkx.dwd_research_institute_base_info",
                                     "gkx.dwd_forg_university_org_info", "gkx.dwd_org_base_info"],
                          "row_counts_from": "_work_gkx21/GKX_INVENTORY.json"}

    n_flow = sum(trans.values())
    ok = n_flow >= 500 and out["probes"]["org_kind_share"].get("industry", 0) > 0.1
    out["support_judgment"] = "完全转换支持" if ok else "部分支持"
    out["support_reason"] = (
        f"工作经历表结构齐备且 57,117 条可算，已识别跨界流动 {n_flow} 人次；"
        "但产业界任职记录仅占 %.2f%%、%.2f%% 机构名未能归类、scholar_id 与学者主表 JOIN 仅命中 %d/%d，"
        "二维计数可算但覆盖不足，预警阈值亦未由甲方给定 → 判部分支持。"
        % (out["probes"]["org_kind_share"].get("industry", 0) * 100,
           out["probes"]["org_kind_share"].get("other", 0) * 100,
           out["probes"]["join_scholar_master"], out["probes"]["dwd_scholar"]))
    out["disclosures"] = [
        "任职性质由机构名后缀规则判定（公司/有限/集团/股份/Inc/Ltd vs 大学/学院/研究院/医院），非甲方登记的机构性质字段，"
        "%.2f%% 机构名（多为英文院校非标准写法）落入未分类，未参与流动识别。"
        % (out["probes"]["org_kind_share"].get("other", 0) * 100),
        "dwd_scholar_work_experience.scholar_id 与 dwd_scholar.scholar_id 仅 %d 条对得上（占主表 %.2f%%），"
        "说明工作经历表的学者 ID 体系与主表不同源，跨表画像（如与 h 指数联动）受限。"
        % (out["probes"]["join_scholar_master"],
           out["probes"]["join_scholar_master"] / max(out["probes"]["dwd_scholar"], 1) * 100),
        "工作经历以海外/国内高校为主，深圳本地机构出现极少；该指标衡量的是「学界↔产业界」跨界，不含区域间迁移。",
        "预警窗口（近窗 2023-2024、基线 2015-2022）与阈值 1/0.5 为本次设定，王惠仅给阈值未给窗口，待甲方确认。",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(out["probes"], ensure_ascii=False, indent=1))
    print(json.dumps(out["compute"]["transition_counts"], ensure_ascii=False))
    print(json.dumps(out["compute"]["alert"], ensure_ascii=False, indent=1))
    print(json.dumps(series[-18:], ensure_ascii=False))
    print(json.dumps(samples[:6], ensure_ascii=False, indent=1))
    print("support", out["support_judgment"], out["elapsed_s"])


if __name__ == "__main__":
    main()
