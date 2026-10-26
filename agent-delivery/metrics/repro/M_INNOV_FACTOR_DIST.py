#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_FACTOR_DIST · 科创要素分布比例（INNOV / DS-01-FACTORS）。

数据面：`gkx`（三方库）+ §2 授权缓存。
  - 专利年/国别/IPC：`_snapshots21/patent_panel_innov_20261021.json`（全量 2,939,895 行）
    → **本脚本不向 `dwd_patent` 发任何聚合 SQL**；
  - 论文/期刊/学者/机构/项目/成果行数：`gkx` 小表 COUNT（均 <10 万行）；
  - 机构省市分布：`_snapshots21/base_20261021.json`（189,116 行全量底册）。

输出：code/M_INNOV_FACTOR_DIST_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FACTS = HERE / "_snapshots21" / "innov21_facts_20261021.json"
OUT = HERE / "M_INNOV_FACTOR_DIST_out.json"

COUNTRY_CN = {"China": "CN", "WO": "WO", "Hong Kong": "HK",
              "Japan": "JP", "Taiwan Province": "TW", "Macao": "MO"}


def share_rows(rows, key="n"):
    total = sum(r[key] for r in rows)
    out = []
    for r in rows:
        item = dict(r)
        item["pct"] = round(float(r[key]) / float(total) * 100, 2) if total else None
        out.append(item)
    return total, out


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    tc = {k: v["rows"] for k, v in f["table_counts"].items()}
    pat = f["patent"]
    py = {int(k): v for k, v in f["paper_year"].items()}
    jy = {int(k): v for k, v in f["project_year"].items()}

    # ---------- 1. 类型结构 ----------
    counts = {
        "论文": tc["dwd_zh_paper"] + tc["dwd_en_paper"],
        "期刊": tc["dwd_zh_journal"] + tc["dwd_en_journal"],
        "专利": int(pat["rows"]),
        "专家学者": tc["dwd_scholar"],
        "组织机构": tc["dwd_org_base_info"] + tc["dwd_research_institute_base_info"] + tc["dwd_forg_base_info"],
        "课题/项目": tc["dwd_zh_project"] + tc["dwd_en_project"],
        "成果（代理）": int(f["project_output"]["total_outputs"]),
    }
    total_types, type_share = share_rows([{"type": k, "n": v} for k, v in counts.items()])

    # ---------- 2. 年度结构（2021–2026） ----------
    years = list(range(2021, 2027))
    year_rows = []
    for y in years:
        year_rows.append({"year": y, "论文": py.get(y, 0), "专利": int(pat["year"].get(str(y), 0)),
                          "项目": jy.get(y, 0)})
    for label in ("论文", "专利", "项目"):
        s = sum(r[label] for r in year_rows)
        for r in year_rows:
            r[f"{label}_pct"] = round(float(r[label]) / float(s) * 100, 2) if s else None

    # ---------- 3. 地域结构：机构底册 ----------
    base = f["base"]
    region_rows = [{"province": "广东省", "city": c, "n": n,
                    "pct": round(n / base["rows"] * 100, 3)}
                   for c, n in base["city_counts"].items()]

    # ---------- 4. 地域结构：专利受理国 ----------
    country_rows = [{"c": COUNTRY_CN.get(k, k), "raw": k, "n": v}
                    for k, v in sorted(pat["country"].items(), key=lambda x: -x[1])]
    total_country, country_share = share_rows(country_rows)

    # ---------- 5. 学科结构：中文论文中图分类 ----------
    disc_total, disc_share = share_rows([{"s": s, "n": n} for s, n in f["discipline"]])

    # ---------- 6. 技术结构：专利 IPC 部类 ----------
    ipc_total, ipc_share = share_rows([{"s": s, "n": n} for s, n in pat["ipc_section"].items()])

    out = {
        "metric_id": "M_INNOV_FACTOR_DIST",
        "name": "科创要素分布比例",
        "domain": "INNOV / DS-01-FACTORS",
        "formula_owner": "AI-20261016（需求只给功能口径，无公式；本报告按类型/年度/地域/学科/技术五维给占比）",
        "generated_at": time.strftime("%Y-%m-%d"),
        "source_db": "gkx",
        "source_detail": {
            "专利": "patent_panel_innov_20261021.json（全量 2,939,895 行，零专利 SQL）",
            "机构底册": "base_20261021.json（189,116 行）",
            "其余": "gkx 小表聚合（论文 100,900 / 项目 58,453 / 学者 21,316 / 政策 20,000）",
        },
        "probes": {
            "type_counts": counts,
            "table_counts": tc,
            "patent_panel_rows": int(pat["rows"]),
            "patent_year_coverage": sorted(int(k) for k in pat["year"]),
        },
        "compute": {
            "type_structure": {"total": total_types, "rows": type_share,
                               "missing": "会议（gkx 无会议主表；zh/en 论文与期刊表的 publication_type 均无「会议」）"},
            "year_structure_2021_2026": {
                "rows": year_rows,
                "note": "专利仅 2021–2026 有 apdt_year；2017–2020 零行，不得把缺失年份当 0；"
                        "2026 为残年（采集止于 2026-10，且公开滞后），不与 2025 做同比；"
                        "项目 2022 年后严重截断（58/6 条），年结构不可解释。",
            },
            "region_structure_org": {
                "total": base["rows"], "guangdong_pct": base["guangdong_pct"],
                "rows": region_rows[:12],
                "method": "base_20261021.json 全量底册（189,116 行，非采样）；47 个重名已在底册侧按 org_id 去重",
            },
            "region_structure_patent_country": {"total": total_country, "rows": country_share},
            "region_structure_scholar": f["scholar_city"],
            "discipline_structure_paper": {
                "total": disc_total, "rows": disc_share[:15],
                "coverage": f"{disc_total:,} / {tc['dwd_zh_paper']:,} 篇"
                            f"（{disc_total / tc['dwd_zh_paper'] * 100:.2f}%）有中图分类",
            },
            "tech_structure_patent_ipc": {"total": ipc_total, "rows": ipc_share},
        },
        "samples": type_share,
        "support_judgment": "部分支持",
        "support_basis": (
            "类型、年度、地域（机构/专利受理国）、学科（中图分类）、技术（IPC 部类）五个维度均可产出占比，"
            "分母来自 gkx 真表或全量面板缓存；但「会议」无主表导致类型结构缺 1 类，成果只能用项目产出聚合代理，"
            "机构地域 99.82% 集中在广东（深圳都市圈四市 99.82%）、不能当全国分布，"
            "论文分类仅覆盖 19.87%——始终有依赖维不足，判部分支持。"
        ),
        "notes": [
            "专利占可计要素总量的 85.52%，类型结构会被专利数量碾压；页面应提供「去专利」或按类内归一视图。",
            "机构地域分布来自 189,116 行全量底册（非采样），广东 99.82%（深圳 50.55%、广州 26.23%、东莞 17.76%、惠州 5.28%），不能解释为全国/全球分布。",
            "专利受理国 96.90% 为 CN、3.06% 为 WO，海外仅 1,055 件；该分布反映数据采集范围，不反映全球创新格局。",
            "中文论文中图分类中「医药、卫生」占 47.73%（9,569/20,048），语料医学偏重；按学科做分布会被医学主导，须给剔除医疗类的对照。",
            "会议要素缺失、成果为聚合计数（awards_count 全为 0），类型结构与分布比例均无法覆盖需求列举的全部 9 类。",
            "英文论文 1,387 篇、英文期刊 605 种，英文侧占比在任何维度都不具代表性。",
            "专利年度维只覆盖 2021–2026（六期，2026 为残年）；2017–2020 在 gkx.dwd_patent 中零行，任何跨 2020 之前的年度占比都不能用本库构造。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({"saved": OUT.name, "type_total": total_types,
                      "type_rows": type_share, "years": year_rows,
                      "ipc": ipc_share, "support": out["support_judgment"]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
