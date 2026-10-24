#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_DS_16_TALENT_RECRUIT_013 —— 高精度成本模型构建。

需求：构建人才引进的高精度成本模型（招聘成本、薪酬包、安家/搬迁、机会成本），
      支撑「引进一个人要花多少钱」的测算。
判定：**完全不支持**。成本模型的因变量（薪酬 / 引进总成本）在全库不存在：
  1. 列名含 salary/wage/compensation/payroll/remuneration/income/cost 的 37 列、7 张表，
     逐列核对后**没有一列是人力成本**：34 列是 `dwd_main_business_composition_*` 的
     分部收入/分部成本（企业财务口径，且含 4 张 _bak 备份表），另 1 列是
     `dwd_en_journal.layout_cost`（期刊排版费）。0 列薪酬、0 列安家费、0 列猎头费。
  2. `dwd_org_recruit_info` 7,981,643 行有 job_title / job_description / work_place /
     release_date / hiring_number，**没有薪资字段**——招聘侧给不出价格。
  3. `dwd_scholar` 21,316 行只有 paper_nums / citation_nums / h_index / reference_nums，
     无薪酬、无职级、无合同。
  4. 财务表：`dwd_org_annual_financial_info` 90,926 行，employees 非空 3,184 行、
     revenue 非空 2,193 行；`dwd_org_stock_finance_info` 40,239 行研发费用非空 19,695 行
     ——这些是**企业**口径的营收/研发/员工数，只能做「人均研发费用」这种宏观代理，
     不能落到「引进某人的薪酬包」。
  5. 没有个人—项目—经费的关联表，机会成本（放弃原职位收入）无法测算。

因此不产出成本数值——产出即造数。只落证据与最小可行替代口径（企业人均研发费用）。
零 SQL：读 `code/_snapshots21/zero_source_probe_20261022.json` 与 `talent22_probe`。
产物：`code/M_TALENT_DS_16_TALENT_RECRUIT_013_out.json`。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DS_16_TALENT_RECRUIT_013"
PROBE = HERE / "_snapshots21" / "zero_source_probe_20261022.json"
PROBE2 = HERE / "_snapshots21" / "talent22_probe_20261022.json"


def main() -> None:
    p = json.loads(PROBE.read_text(encoding="utf-8"))
    p2 = json.loads(PROBE2.read_text(encoding="utf-8"))
    sal = p["columns"]["salary_cost"]
    items = sal["items"]
    hr_like = [x for x in items if any(k in x["column"] for k in
                                       ("salary", "wage", "pay", "remun", "compens"))]
    finance = p2["dwd_org_annual_financial_info"]
    stock = p2["dwd_org_stock_finance_info"]

    payload = {
        "metric": METRIC,
        "title": "高精度成本模型构建",
        "support_judgment": "完全不支持",
        "support_reason": (
            "成本模型的因变量不存在：37 个 cost/income 列全部是企业分部财务或期刊排版费，"
            "0 列薪酬/安家费/猎头费；798 万条招聘记录无薪资字段；学者主档无薪酬职级。"
            "只能做「企业人均研发费用」这类宏观代理，无法落到个人引进成本，故完全不支持。"
        ),
        "dimensions": [
            {"dim": "薪酬包（年薪/签字费/绩效）", "verdict": "无",
             "evidence": "salary|wage|compensation|payroll|remuneration 命中 0 列（37 列 cost 全部为企业财务口径）",
             "needed": "接入招聘平台薪资字段、个税/社保缴纳基数或企业薪酬调研"},
            {"dim": "安家费 / 搬迁 / 住房补贴", "verdict": "无",
             "evidence": "无 relocation/housing/settlement/allowance 类字段；政策表只有补贴政策文本，无个人领取记录",
             "needed": "接入人才补贴申领明细（对象级）"},
            {"dim": "猎头 / 招聘过程成本", "verdict": "无",
             "evidence": "`dwd_org_recruit_info` 7,981,643 行，字段仅 job_title/job_description/work_place/release_date/hiring_number",
             "needed": "接入招聘费用台账（渠道费、猎头费率、面试成本）"},
            {"dim": "机会成本（放弃原职位收入）", "verdict": "无",
             "evidence": "无个人历史薪酬、无个人—项目—经费关联",
             "needed": "需要个人历年收入或原单位薪酬等级"},
            {"dim": "宏观代理：企业人均研发费用", "verdict": "弱",
             "evidence": f"stock_finance 40,239 行研发费用非空 {stock['rd_nonnull']:,}；annual_financial 员工数非空 {finance['employees_nonnull']:,}",
             "needed": "只能算企业层面的人均研发投入，不能代表引进个人的成本"},
        ],
        "evidence": {
            "salary_cost_columns": sal["n_columns"], "salary_cost_tables": sal["n_tables"],
            "hr_like_columns": len(hr_like),
            "salary_cost_items": items,
            "recruit_rows": p2["dwd_org_recruit_info"]["rows"],
            "recruit_columns": ["org_id", "name_cn", "job_title", "job_description",
                                "work_place", "release_date", "hiring_number", "data_source"],
            "annual_financial": finance, "stock_finance": stock,
            "scholar_columns": ["paper_nums", "citation_nums", "h_index", "reference_nums"],
        },
        "no_score_declaration": (
            "本件不输出人均引进成本、不输出成本分档。因变量（薪酬/总成本）为 0 字段；"
            "用「企业人均研发费用」冒充个人引进成本会把 8 位数企业研发预算摊到个人头上，量级错 2—3 个数量级。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("无基期：成本因变量不存在，财务表虽有 period（198912—202603），"
                            "但那是企业报表期，不是人才引进成本的时间序列。"),
        "probes": {"sql_count": 0, "probe_sql_total": p.get("sql_count"),
                   "probe_snapshot": "_snapshots21/zero_source_probe_20261022.json",
                   "source": "gkx @ 183.240.141.251:3318"},
        "reused_from": ("code/_snapshots21/zero_source_probe_20261022.json + "
                        "code/_snapshots21/talent22_probe_20261022.json"),
    }
    C.write(METRIC, payload)
    print("judgment", payload["support_judgment"])
    print("salary cols", sal["n_columns"], "tables", sal["n_tables"], "hr_like", len(hr_like))
    print("recruit rows", p2["dwd_org_recruit_info"]["rows"], "stock rd", stock["rd_nonnull"])


if __name__ == "__main__":
    main()
