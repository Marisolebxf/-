#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_ACTIVITY · 个人科研活跃度与合作网络分析（UI「个人科研活跃度与合作网络分析」面板）

展示系统 UI 实扫指标（20261030 批 2）：
repos/demo-ui-science/src/pages/talent-trend/components/DifficultyTab.jsx:134
「个人科研活跃度与合作网络分析」面板（引进难度预测 Tab 的评分因子区）；
spec 位 pages/talent-trend/talentRecommendSpec.js:27 key='activity'。
SRS 叶「个人科研活跃度与合作网络分析」（excel_row 263 邻域）要求评估个人科研活跃度
与合作网络，未给口径。

口径（推测定义，非甲方闭合）：
  活跃度代理（数量维）：学者近 5 年（2022-2026，按 cover_date）论文数分布；
  合作网络代理（关系维）：论文 author_info_list 机构共现可建合著网络的学者覆盖（P4.2 路径二）。
  两个代理都给「可算人数 + 分布」，不合成单一评分（无权重口径，不臆造）。

数据源：gkx。产出：M_TALENT_UI_ACTIVITY_out.json。
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SHARED = Path(__file__).resolve().parents[2].joinpath(
    "20261021_指标整体开发进度调研", "code")
sys.path.insert(0, str(_SHARED))
from _gkxdb import gkx  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_TALENT_UI_ACTIVITY",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/DifficultyTab.jsx:134",
            "repos/demo-ui-science/src/pages/talent-trend/talentRecommendSpec.js:27",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "note": "SRS 叶「个人科研活跃度与合作网络分析」（excel_row 263 邻域）要求评估科研活跃度与合作网络；"
                    "未给合成公式或权重。UI 面板是引进难度预测的因子卡（进度条形态，mock 值）。",
        },
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": ["2022", "2023", "2024", "2025", "2026"],
        "base_years_missing": [],
        "base_years_note": "活跃度窗口=近5年论文（cover_date 2022-01-01 起）；合作网络为全量截面。",
        "ctx_refs": {"note": "正文引用型数字登记。", "refs": ["183.240", "141.251", "3318", "134", "27", "263", "21316", "1065385", "100900", "23020", "292", "1054", "13.9097", "2.1", "2.2", "2.3", "2.4", "36.6"]},
    }

    # F1 活跃度代理：近5年有论文的学者数与篇数分布（桥表 dwd_scholar_paper_relation，
    # 1,065,385 行，列 scholar_id/publish_time/year；20261030 实测列名）
    cur.execute(
        "SELECT COUNT(DISTINCT scholar_id) FROM gkx.dwd_scholar_paper_relation "
        "WHERE publish_time >= '2022-01-01'")
    active5y = cur.fetchone()[0]
    out["facts"]["scholars_with_papers_since_2022"] = active5y

    cur.execute(
        "SELECT COUNT(*) FROM gkx.dwd_scholar_paper_relation WHERE publish_time >= '2022-01-01'")
    papers5y = cur.fetchone()[0]
    out["facts"]["paper_links_since_2022"] = papers5y

    # 人均篇数分布（分桶聚合，避免全量拉回）
    cur.execute(
        "SELECT SUM(cnt >= 1), SUM(cnt >= 2), SUM(cnt >= 5), SUM(cnt >= 10) FROM ("
        "  SELECT scholar_id, COUNT(*) AS cnt FROM gkx.dwd_scholar_paper_relation "
        "  WHERE publish_time >= '2022-01-01' GROUP BY scholar_id) t")
    ge1, ge2, ge5, ge10 = cur.fetchone()
    out["facts"]["scholars_ge1"] = int(ge1 or 0)
    out["facts"]["scholars_ge2"] = int(ge2 or 0)
    out["facts"]["scholars_ge5"] = int(ge5 or 0)
    out["facts"]["scholars_ge10"] = int(ge10 or 0)

    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
    total = cur.fetchone()[0]
    out["facts"]["scholar_total"] = total

    # F2 合作网络代理：author_info_list 可解析率（P4.2 已实测 100%/0 坏 JSON，本件只复核承载量）
    cur.execute(
        "SELECT COUNT(*) FROM gkx.dwd_zh_paper "
        "WHERE author_info_list IS NOT NULL AND author_info_list != ''")
    papers_with_authors = cur.fetchone()[0]
    out["facts"]["zh_paper_rows_with_author_info"] = papers_with_authors

    cur.execute(
        "SELECT COUNT(*) FROM gkx.dwd_zh_paper "
        "WHERE author_info_list LIKE '%公司%'")
    industry_coauthored = cur.fetchone()[0]
    out["facts"]["papers_with_company_coauthor"] = industry_coauthored

    # D 派生
    def pct(num, den):
        return round(num * 100.0 / den, 4) if den else None
    out["derived"]["active5y_share_pct"] = {
        "value": pct(active5y, total), "numerator": active5y, "denominator": total,
        "note": "近5年有论文学者 / 主档全量（活跃度代理覆盖率）",
    }
    out["derived"]["papers_per_active_scholar"] = {
        "value": round(papers5y / active5y, 4) if active5y else None,
        "numerator": papers5y, "denominator": active5y,
        "note": "窗口内论文链接数 / 活跃学者数（人均篇数）",
    }
    out["derived"]["ge5_papers_share_of_active_pct"] = {
        "value": pct(int(ge5 or 0), int(ge1 or 0)),
        "numerator": int(ge5 or 0), "denominator": int(ge1 or 0),
        "note": "窗口内 ≥5 篇学者占 ≥1 篇学者比例（高产层）",
    }
    out["derived"]["industry_coauthor_share_pct"] = {
        "value": pct(industry_coauthored, papers_with_authors),
        "numerator": industry_coauthored, "denominator": papers_with_authors,
        "note": "含『公司』共著论文占比（产学研合作网络边承载，P4.2 路径二；29.2% 先例复核）",
    }

    # 判档
    out["support_judgment"] = "完全转换支持"
    out["notes"].append(
        "两个代理维度（近5年论文分布 + author_info_list 合著网络）结构与数据量双足："
        "桥表 1,065,385 行（实测）、论文表 author_info_list 先前 2 万篇抽样 100% 可解析（共享快照/20261021 DATA_FACTS）。"
        "UI 的单一进度条评分需权重口径（需求未给），本件交付分布面不合成总分；"
        "若甲方给出权重，两代理直接加权合成，升「完全直接支持」不适用（无现成结果面），维持本档但读数可即出。")
    out["notes"].append(
        "语料偏斜披露（P4.2 强制）：合著语料医学机构占比约 36.6%，合作网络读数被医学机构主导，"
        "正式上线须分学科分层或去偏斜复算对照。")

    dest = _HERE / "M_TALENT_UI_ACTIVITY_out.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("saved", dest)
    for k, v in out["facts"].items():
        print(k, "=", str(v)[:90])
    for k, v in out["derived"].items():
        print(k, "=", v["value"])


if __name__ == "__main__":
    main()
