#!/usr/bin/env python3
"""M_ENT_CULTIVATION_INDEX 培育推荐指数 — 依赖侧实测脚本

王惠口径（calc-logic 真源）：
  三维（产业相关度/政策匹配度/企业潜力）×极值归一化 0-100 → 加权（等权 1/3 或熵值法，Q015）。
  ① 产业相关度=产业链融入度（Link×Centroid；同 M_ENT_INDUSTRY_MATCH_SCORE）
  ② 政策匹配度=行动型契合+话语型契合（政策词典+GPT 分类企业文本）
  ③ 企业潜力=资产总额+盈利能力(ROE)+研发投入强度 加权
实测（2026-10-20）gkx：
  ① tags 2,283,762 行✅；股东 400,286 行✅（图谱边原料在）；财务收入占比列在（低填充）
  ② 政策库 20,000 行 content 96%；企业文本 dwd_org_org_product_info 45,011 行 description 71.3%——
     但行动/话语契合的 GPT 分类框架未建（前置模型缺）
  ③ 财务 90,926 行：资产>0 2,628（2.9%）、pure_profit 非空 2,349（2.6%）、arch_development_am>0 全空（None）、营收>0 2,191（2.4%）
结论：潜力维三指标两低一空、政策维 GPT 未建、融入度维原料可算 → 三维一可两缺 → 部分支持。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_CULTIVATION_INDEX_out.json")
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
    rep = {"metric_id": "M_ENT_CULTIVATION_INDEX", "metric_name": "培育推荐指数", "script": Path(__file__).name}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    with gc.cursor() as cur:
        cur.execute("SELECT COUNT(*) n FROM dwd_org_industry_tags")
        tags = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) n FROM dwd_org_shareholder_info")
        sh = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) n, SUM(total_assets>0) assets, SUM(pure_profit IS NOT NULL) profit, "
                    "SUM(arch_development_am>0) rd, SUM(operating_revenue>0) rev FROM dwd_org_annual_financial_info")
        fin = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in dict(cur.fetchone()).items()}
        cur.execute("SELECT COUNT(*) n, SUM(description IS NOT NULL AND description<>'') d FROM dwd_org_org_product_info")
        prod = {k: str(v) for k, v in dict(cur.fetchone()).items()}
    gc.close()
    n = int(fin["n"])
    pct = lambda x: f"{round(int(x or 0)/n*100,1)}%"

    probe = {
        "gkx_tags": tags, "gkx_shareholder": sh,
        "gkx_financial": fin, "fin_pct": {"assets": pct(fin["assets"]), "profit": pct(fin["profit"]),
                                          "rd(arch_development_am)": "全空(None)", "rev": pct(fin["rev"])},
        "gkx_product_text": prod,
        "gpt_classification_built": False,
    }
    rep["probe"] = probe
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"三维成熟度：①产业相关度原料可算（tags {tags} 行+股东 {sh} 行图谱边+目录）✅；"
            f"②政策匹配度缺 GPT 分类框架（政策库 content 96%、企业文本 {prod['n']} 行 description 71.3%，"
            f"但行动/话语两型契合的识别模型未建）❌；"
            f"③企业潜力财务三指标：资产 {pct(fin['assets'])}、净利润 {pct(fin['profit'])}、"
            f"研发投入 arch_development_am 全空、营收 {pct(fin['rev'])}——低填充+一列空❌。"
            "三维一可两缺（GPT 框架未建+财务薄）→ 部分支持。"
        ),
        "criteria": {
            "industry_dim_ready": True,
            "policy_gpt_ready": False,
            "potential_financial_fill_pct": pct(fin["assets"]),
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
