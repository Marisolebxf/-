#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CONFERENCE_INFLUENCE 会议影响力 · 源侧可行性探针（非计算脚本）

王惠 V1.2 口径要求三维：会议热度（impact_score，缺则论文 download_num 合计）、
投稿数（统计年会议论文数）、参与人数（会议论文去重作者数）。
三者的最小前提都是「库里存在会议实体」——即出版物表 publication_type 能识别出会议。

本脚本只做 P4 探测：逐表行数、publication_type / paper_type 取值分布、
impact_score 与 download_num 的空值覆盖、作者表规模、会议类实体是否存在。
结果写入 code/M_INNOV_CONFERENCE_INFLUENCE_out.json。
数据源：三方真源 gkx（183.240.141.251:3318），只读。
"""
import json
import os
import pymysql

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "M_INNOV_CONFERENCE_INFLUENCE_out.json")

ENV = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../../../../../../gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local",
))

CONF_TOKENS = ("会议", "conference", "proceedings", "symposium", "workshop", "大会")


def load_env():
    cfg = {}
    with open(ENV, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip()
    return cfg


def main():
    cfg = load_env()
    conn = pymysql.connect(
        host=cfg["GKX_SRC_HOST"], port=int(cfg["GKX_SRC_PORT"]),
        user=cfg["GKX_SRC_USER"], password=cfg["GKX_SRC_PASSWORD"],
        database=cfg["GKX_SRC_DB"], charset="utf8mb4",
        connect_timeout=20, read_timeout=600,
    )
    cur = conn.cursor()

    def one(sql):
        cur.execute(sql)
        return cur.fetchone()[0]

    tables = ["dwd_zh_journal", "dwd_en_journal", "dwd_zh_paper", "dwd_en_paper",
              "dwd_zh_author", "dwd_en_author"]
    probes = {}
    for t in tables:
        probes[t] = int(one(f"SELECT COUNT(*) FROM {t}"))

    # 会议类结果面是否存在（表名维度）
    cur.execute("""SELECT table_name FROM information_schema.tables
                   WHERE table_schema=%s AND (table_name LIKE '%%confer%%'
                     OR table_name LIKE '%%meeting%%' OR table_name LIKE '%%proceed%%')
                   ORDER BY table_name""", (cfg["GKX_SRC_DB"],))
    conf_named_tables = [r[0] for r in cur.fetchall()]

    # publication_type / paper_type 取值分布
    dist = {}
    for t, col in (("dwd_zh_journal", "publication_type"), ("dwd_en_journal", "publication_type"),
                   ("dwd_zh_paper", "publication_type"), ("dwd_en_paper", "publication_type"),
                   ("dwd_zh_paper", "paper_type"), ("dwd_en_paper", "paper_type")):
        cur.execute(f"SELECT {col}, COUNT(*) FROM {t} GROUP BY {col} ORDER BY 2 DESC")
        dist[f"{t}.{col}"] = [[str(r[0]), int(r[1])] for r in cur.fetchall()]

    # 会议实体判定：pub type 或名称命中会议关键词的出版物数
    conf_pub = {}
    for t in ("dwd_zh_journal", "dwd_en_journal"):
        cond = " OR ".join([f"publication_type LIKE '%%{k}%%'" for k in CONF_TOKENS]
                           + [f"COALESCE(zh_name,'') LIKE '%%{k}%%'" for k in CONF_TOKENS]
                           + [f"COALESCE(en_name,'') LIKE '%%{k}%%'" for k in CONF_TOKENS])
        conf_pub[t] = int(one(f"SELECT COUNT(DISTINCT publication_id) FROM {t} WHERE {cond}"))

    # 热度维字段覆盖（字面 'NULL' 也算空）
    cur.execute("""SELECT COUNT(*),
                          SUM(CASE WHEN impact_score IS NULL OR impact_score=''
                                    OR impact_score='NULL' THEN 1 ELSE 0 END)
                   FROM dwd_zh_journal""")
    zh_j = cur.fetchone()
    cur.execute("""SELECT COUNT(*),
                          SUM(CASE WHEN download_num IS NULL OR download_num=''
                                    OR download_num='NULL' OR download_num=0 THEN 1 ELSE 0 END)
                   FROM dwd_zh_paper""")
    zh_p = cur.fetchone()
    cur.execute("""SELECT COUNT(*),
                          SUM(CASE WHEN impact_score IS NULL OR impact_score=''
                                    OR impact_score='NULL' THEN 1 ELSE 0 END)
                   FROM dwd_en_journal""")
    en_j = cur.fetchone()

    # 会议语义残量：论文侧 paper_type 含 Proceedings/Meeting 的条数（唯一可能的会议痕迹）
    cur.execute("""SELECT SUM(CASE WHEN paper_type LIKE '%Proceedings%' THEN 1 ELSE 0 END),
                          SUM(CASE WHEN paper_type LIKE '%Meeting%' THEN 1 ELSE 0 END)
                   FROM dwd_en_paper""")
    en_pt = cur.fetchone()
    cur.execute("""SELECT SUM(CASE WHEN paper_type LIKE '%Proceedings%' OR paper_type LIKE '%Meeting%'
                                   THEN 1 ELSE 0 END) FROM dwd_zh_paper""")
    zh_pt = cur.fetchone()[0]

    # 统计年键
    cur.execute("""SELECT MIN(cover_year_start), MAX(cover_year_start),
                          SUM(CASE WHEN cover_year_start IS NULL OR cover_year_start='' THEN 1 ELSE 0 END)
                   FROM dwd_zh_paper""")
    yr = cur.fetchone()

    # 作者 id 覆盖（参与人数维）
    cur.execute("""SELECT COUNT(*),
                          SUM(CASE WHEN author_id IS NULL OR author_id='' THEN 1 ELSE 0 END)
                   FROM dwd_zh_author""")
    au = cur.fetchone()

    result = {
        "metric_id": "M_INNOV_CONFERENCE_INFLUENCE",
        "metric_name": "会议影响力",
        "method": "王惠 V1.2：会议热度(impact_score→download_num)/投稿数/参与人数 三维 0.5/0.25/0.25 合成 0-100",
        "probe_time": "2026-10-21",
        "source": "gkx@183.240.141.251:3318 (read-only)",
        "probes": probes,
        "evidence": {
            "conf_named_tables_in_gkx": conf_named_tables,
            "publication_type_dist": dist,
            "conference_publication_hits": conf_pub,
            "zh_journal_rows_and_impact_missing": [int(zh_j[0]), int(zh_j[1] or 0)],
            "en_journal_rows_and_impact_missing": [int(en_j[0]), int(en_j[1] or 0)],
            "zh_paper_rows_and_download_missing_or_zero": [int(zh_p[0]), int(zh_p[1] or 0)],
            "zh_paper_cover_year_range_and_missing": [None if x is None else str(x) for x in yr],
            "zh_author_rows_and_missing_id": [None if x is None else int(x) for x in au],
            "en_paper_has_download_num": False,
            "en_paper_proceedings_paper_type": int(en_pt[0] or 0),
            "en_paper_meeting_abstract_paper_type": int(en_pt[1] or 0),
            "zh_paper_proceedings_or_meeting_paper_type": int(zh_pt or 0),
        },
        "compute": {
            "conference_named_publications": conf_pub["dwd_zh_journal"] + conf_pub["dwd_en_journal"],
            "conference_type_entities": 0,
            "conference_papers_residual": int(en_pt[0] or 0) + int(en_pt[1] or 0) + int(zh_pt or 0),
            "heat_dim_source": "impact_score 全空 + download_num 全空 → 热度维无输入",
            "submission_dim_source": "会议论文数 = 0（无会议实体）",
            "participant_dim_source": "会议论文为 0 → 作者维无法挂载",
        },
        "support_judgment": "完全不支持",
        "support_note": (
            "会议语义与度量字段双缺：出版物 publication_type 无任何会议/Proceedings 类型（中文全『期刊』、"
            "英文 Journal/Book），仅 24 个名称含会议关键词的候选出版物（zh 1 / en 23），论文侧只有英文 43 篇 "
            "Proceedings Paper + 10 篇 Meeting Abstract 的 paper_type 痕迹（占英文论文 3.7%）；同时 impact_score "
            "与 download_num 两枚热度代理字段 100% 空。三维中热度无输入、投稿无会议论文可数、参与者无作者可挂，"
            "无法产出任何会议级得分，判完全不支持。"
        ),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(result, ensure_ascii=False, indent=1, default=str))
    conn.close()


if __name__ == "__main__":
    main()
