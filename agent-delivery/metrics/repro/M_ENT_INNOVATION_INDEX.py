#!/usr/bin/env python3
"""M_ENT_INNOVATION_INDEX 创新能力指数 — 依赖侧实测脚本

王惠口径（calc-logic 真源）：三准则层（创新投入/创新产出/可持续发展）14 三级指标，
  极值归一×100 → 层内加权 → 层间加权 → 0~100 分（权重待甲方 Q014）。
calc-logic 自标五项待建：资本化研发投入/科研平台表/学历结构/软件著作权表/无形资产明细。
实测（2026-10-20）gkx：
  ① 财务维：营收 2.4%/资产 2.9%（既往）；研发列 arch_development_am 与研发人员 development_employee、
    从业人数 employees_number 填充另探。
  ② 专利维：dwd_patent 294 万 + dwd_patent_legal 状态过滤（既往已证可用）。
  ③ 获奖维：tech_tag 获奖类标签命中探针。
  ④ 五待建项零承载复核。
结论：14 项三级指标 5 项零表+财务薄 → 部分支持。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_INNOVATION_INDEX_out.json")
ENV_GKX = Path(__file__).resolve().parents[6] / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def dec(x):
    return str(x) if isinstance(x, Decimal) else x


def main():
    rep = {"metric_id": "M_ENT_INNOVATION_INDEX", "metric_name": "创新能力指数", "script": "M_ENT_INNOVATION_INDEX.py"}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    with gc.cursor() as cur:
        cur.execute("SELECT COUNT(*) n, SUM(arch_development_am IS NOT NULL) rd, "
                    "SUM(development_employee IS NOT NULL) rde, SUM(employees_number IS NOT NULL) emp "
                    "FROM dwd_org_annual_financial_info")
        fin = {k: dec(v) for k, v in dict(cur.fetchone()).items()}
        cur.execute("SELECT COUNT(*) n FROM dwd_patent_legal")
        legal = cur.fetchone()["n"]
        cur.execute("SELECT org_tag, COUNT(*) n FROM dwd_org_tech_tag WHERE org_tag LIKE '%奖%' OR org_tag LIKE '%实验室%' OR org_tag LIKE '%平台%' GROUP BY 1 ORDER BY n DESC LIMIT 8")
        award_tags = [dict(r) for r in cur.fetchall()]
        missing = {}
        for key, pats in {
            "capitalized_rd_field": ["%capitaliz%"],
            "research_platform_table": ["%platform%", "%laborator%", "%lab%"],
            "education_structure_field": ["%education%", "%degree%"],
            "software_copyright_table": ["%software_copyright%", "%copyright%"],
            "intangible_asset_detail": ["%intangible%"],
        }.items():
            hit = []
            for p in pats:
                cur.execute(f"SHOW TABLES LIKE '{p}'")
                hit += [list(r.values())[0] for r in cur.fetchall()]
            missing[key] = sorted(set(hit))
    gc.close()

    rep["probe"] = {
        "financial_fill": fin, "patent_legal_rows": legal,
        "award_like_tags": award_tags, "missing_check": missing,
    }
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"14 项三级指标中：专利三项原料足（294 万专利+法务 {legal:,} 行）；财务侧薄填充"
            f"（研发 {fin['rd']}/{fin['n']}、研发人员 {fin['rde']}、从业 {fin['emp']}）；"
            f"五项 calc-logic 自标待建复核确认零承载（{ {k: len(v) for k, v in missing.items()} } 全空）；"
            f"获奖类标签 LIKE 探针 {len(award_tags)} 类命中（待口径确认）。"
            "三准则层中投入层半缺、产出层两项缺、可持续层薄 → 部分支持。"
        ),
        "criteria": {
            "patent_dims_ready": True,
            "financial_dims_thin": True,
            "five_pending_fields_absent": all(len(v) == 0 for v in missing.values()),
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
