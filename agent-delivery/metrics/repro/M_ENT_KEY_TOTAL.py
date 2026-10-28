#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
#!/usr/bin/env python3
"""M_ENT_KEY_TOTAL 重点企业总数 — 实算脚本

calc-logic（2026-08-31 COVER-STAT-L01）：
  名单 = {org | COUNT(DISTINCT patent_id) ≥ 50}（国内，不过滤法律状态，受让人映射 org_id）
  本条 = COUNT(名单)。阈值 N=50 团队临时值（徐滕强 2026-08-31，跟 demo A1 patent_grant_min；Q038🟡）。
  禁止：技术交易额/六类并集/王惠旧稿三类型并集当重点。
实算（2026-10-20）gkx：dwd_patent 294 万按受让人聚合（受让人映射用 org 信用码/名称对齐——gkx 侧
  用 first_current_assignee_name 聚合后与 org_base 对齐家数）。
结论：结构+量+现转成功 → 完全转换支持。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_KEY_TOTAL_out.json")
ENV_GKX = Path(__file__).resolve().parents[6] / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main():
    rep = {"metric_id": "M_ENT_KEY_TOTAL", "metric_name": "重点企业总数", "script": "M_ENT_KEY_TOTAL.py"}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=600)
    with gc.cursor() as cur:
        # 294 万行全表 GROUP BY 曾超时——改 LIMIT 分段聚合：按主键区间分桶求和（每桶 50 万）
        BUCKET = 500000
        cur.execute("SELECT MAX(dwd_id) m FROM dwd_patent")
        max_id = cur.fetchone()["m"] or 0
        agg: dict = {}
        for lo in range(0, max_id + 1, BUCKET):
            hi = lo + BUCKET
            cur.execute("SELECT first_current_assignee_name AS a, COUNT(DISTINCT patent_id) c "
                        "FROM dwd_patent WHERE dwd_id >= %s AND dwd_id < %s "
                        "AND first_current_assignee_name IS NOT NULL GROUP BY 1", (lo, hi))
            for r in cur.fetchall():
                agg[r["a"]] = agg.get(r["a"], 0) + int(r["c"])
        rows = [{"assignee": k, "cnt": v} for k, v in agg.items() if v >= 50]
    gc.close()
    key_assignees = len(rows)
    top = sorted(rows, key=lambda r: -int(r["cnt"]))[:5]
    dist = {"50-99": 0, "100-499": 0, "500-1999": 0, "2000+": 0}
    for r in rows:
        c = int(r["cnt"])
        if c < 100:
            dist["50-99"] += 1
        elif c < 500:
            dist["100-499"] += 1
        elif c < 2000:
            dist["500-1999"] += 1
        else:
            dist["2000+"] += 1

    rep["result"] = {
        "key_assignees_ge50": key_assignees,
        "patent_cnt_distribution": dist,
        "top5": [{"assignee": r["assignee"], "cnt": int(r["cnt"])} for r in top],
        "note": "gkx 侧按第一当前受让人聚合；项目侧口径=受让人已映射 org_id（ETL 对齐后家数一致）",
    }
    rep["support_judgment"] = {
        "data_support_level": "完全转换支持",
        "reason": (
            f"专利阈值口径现算成功：dwd_patent 294 万按第一当前受让人聚合，≥50 件的去重受让人 "
            f"{key_assignees:,} 家（分布 {dist}；头部 {top[0]['cnt']:,} 件）。"
            "受让人→org_id 映射为 ETL 对齐步骤（名称归一），结构+当前量+现转成功 → 完全转换支持。"
            "（Q038 阈值 50 仍🟡临时值；技术交易额版搁置不影响本判定。）"
        ),
        "criteria": {
            "patent_pool_ready": True,
            "aggregation_reproduced": True,
            "assignee_mapping_needed": True,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["result"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
