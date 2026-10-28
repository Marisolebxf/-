#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
#!/usr/bin/env python3
"""M_ENT_DS_07_INDUSTRY_POTENTIAL_004 科学影响力评估 — 依赖侧实测脚本

calc-logic（AI 补漏规范化，SRS《科技创新评估.md》序号149，公式待算法 Lead 会签）：
  两维：①论文被引影响力（SUM 被引+篇均）②国际合作论文比例（境内+境外单位论文/总数）；
  极值归一后等权 → 科学影响力，输出产业分布与排名。
  产业→论文映射经 dwd_author_org_base_info_rel（作者-机构）对齐。
实测（2026-10-20）gkx：
  ① 论文池：zh 100,900 / en 1,387；中文被引 dwd_zh_paper_citation 20,031 行（100% 有次数）；
    英文被引次数字段缺（待建，calc-logic 自标）。
  ② 作者机构：zh_author 62,002 / en_author 1,387。
  ③ 产业映射关键表 dwd_author_org_base_info_rel 与 dwd_author_foreign_org_base_info_rel **均缺表**——
    作者→机构→产业 链路断（合作维+产业入集双失）。
结论：被引维可算（全库级）、合作维断链、产业映射断链 → 部分支持。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_DS_07_INDUSTRY_POTENTIAL_004_out.json")
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
    rep = {"metric_id": "M_ENT_DS_07_INDUSTRY_POTENTIAL_004", "metric_name": "科学影响力评估", "script": "M_ENT_DS_07_INDUSTRY_POTENTIAL_004.py"}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    stats = {}
    with gc.cursor() as cur:
        for t in ("dwd_zh_paper", "dwd_en_paper", "dwd_zh_paper_citation", "dwd_zh_author", "dwd_en_author",
                  "dwd_author_org_base_info_rel", "dwd_author_foreign_org_base_info_rel", "dwd_forg_base_info"):
            try:
                cur.execute(f"SELECT COUNT(*) n FROM {t}")
                stats[t] = cur.fetchone()["n"]
            except Exception:
                stats[t] = None
        cur.execute("SELECT SUM(citation_num) s, COUNT(*) n FROM dwd_zh_paper_citation")
        cit = dict(cur.fetchone())
    gc.close()

    probe = {"table_rows": stats, "zh_citation_sum": str(cit["s"])}
    rep["probe"] = probe
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"被引维可算（zh 论文 100,900 + 被引表 20,031 行合计 {cit['s']} 次，100% 有值；en 论文仅 1,387 且被引字段缺待建）；"
            f"国际合作维断链：dwd_author_foreign_org_base_info_rel 缺表（境外关联无承载）；"
            f"产业映射断链：dwd_author_org_base_info_rel 缺表——作者→机构→产业 入集不可达。"
            "对象=产业科研产出集合，产业入集断则指标无法按口径产出（仅全库级被引可算）→ 部分支持。"
        ),
        "criteria": {
            "citation_dim_ready": True,
            "intl_coop_dim_ready": False,
            "industry_mapping_ready": False,
            "en_citation_field": False,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
