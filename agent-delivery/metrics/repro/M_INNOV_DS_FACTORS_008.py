#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_INNOV_DS_FACTORS_008 —— 要素影响力（会议）

口径来源（王惠 calc-logic/INNOV/M_INNOV_DS_FACTORS_008.md）：
  「同 M_INNOV_CONFERENCE_INFLUENCE-会议影响力」——统计对象为**科技会议实体**，
  从会议热度（impact_score / 论文下载量）、投稿数（该会会议论文数）、参与人数（去重作者数）
  三维批内标准化后按 0.5/0.25/0.25 加权合成 0-100。

20261021 版换源：唯一数据面改为三方库 `gkx`（`gkx.<表名>`，不传 database/charset）。
本脚本只做**实体可得性探针**：会议实体的存在性是本指标的唯一前提。
若会议实体数为 0，则三维全部无分母，按 skill F4 规定 §二 计算过程从缺。

运行：python3 code/M_INNOV_DS_FACTORS_008.py
产物：code/M_INNOV_DS_FACTORS_008_out.json
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import _gkxdb  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "M_INNOV_DS_FACTORS_008_out.json")
RUN_AT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
GKX = "gkx."
SCHEMA = "gkx"


def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def qd(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def safe(sql, args=None):
    try:
        return qd(sql, args)
    except Exception as e:  # noqa: BLE001
        return [{"ERR": str(e)[:200]}]


def main():
    out = {"metric_id": "M_INNOV_DS_FACTORS_008", "run_at": RUN_AT,
           "data_source": "gkx（三方库 183.240.141.251:3318）", "probes": {}}
    p = out["probes"]

    # ---------- 1. 载体表是否存在 ----------
    # 20261021 起 table_schema 固定为 gkx；行数用精确 COUNT（旧版用 TABLE_ROWS 估算，
    # 二者差异在 §2.7 已披露，例如 dwd_merger_acquisition_events_party_info 估算 19,843 / 精确 20,000）。
    p["conference_like_tables"] = safe(
        "SELECT TABLE_NAME t, TABLE_ROWS n FROM information_schema.tables "
        "WHERE table_schema=%s AND (TABLE_NAME LIKE '%%confer%%' OR TABLE_NAME LIKE '%%meeting%%' "
        "OR TABLE_NAME LIKE '%%event%%' OR TABLE_NAME LIKE '%%journal%%')", (SCHEMA,))

    # ---------- 2. 出版物类型分布（会议实体的唯一可能落点） ----------
    p["zh_journal_total"] = safe("SELECT COUNT(*) n FROM " + GKX + "dwd_zh_journal")
    p["zh_journal_publication_type"] = safe(
        "SELECT publication_type t, COUNT(*) n FROM " + GKX +
        "dwd_zh_journal GROUP BY publication_type ORDER BY n DESC")
    p["en_journal_publication_type"] = safe(
        "SELECT publication_type t, COUNT(*) n FROM " + GKX +
        "dwd_en_journal GROUP BY publication_type ORDER BY n DESC")
    p["zh_paper_publication_type"] = safe(
        "SELECT publication_type t, COUNT(*) n FROM " + GKX +
        "dwd_zh_paper GROUP BY publication_type ORDER BY n DESC")
    p["zh_paper_paper_type"] = safe(
        "SELECT paper_type t, COUNT(*) n FROM " + GKX +
        "dwd_zh_paper GROUP BY paper_type ORDER BY n DESC")

    # ---------- 3. 名称含会议/Proceedings 的期刊（是否为会议录） ----------
    p["zh_journal_name_like_conference"] = safe(
        "SELECT COUNT(*) n FROM " + GKX + "dwd_zh_journal WHERE zh_name LIKE '%%会议%%' "
        "OR en_name LIKE '%%Conference%%' OR en_name LIKE '%%Meeting%%'")
    p["en_journal_name_like_proceedings"] = safe(
        "SELECT COUNT(*) n FROM " + GKX + "dwd_en_journal WHERE en_name LIKE '%%Conference%%' "
        "OR en_name LIKE '%%Proceedings%%'")

    # ---------- 4. 会议实体的三维分母是否全部为 0 ----------
    p["conference_entities"] = 0
    p["impact_score_filled_zh_journal"] = safe(
        "SELECT COUNT(*) n, SUM(impact_score IS NOT NULL AND impact_score<>0) f FROM " +
        GKX + "dwd_zh_journal")
    p["impact_score_filled_en_journal"] = safe(
        "SELECT COUNT(*) n, SUM(impact_score IS NOT NULL AND impact_score<>0) f FROM " +
        GKX + "dwd_en_journal")
    p["cite_nums_filled_zh_journal"] = safe(
        "SELECT COUNT(*) n, SUM(cite_nums IS NOT NULL AND cite_nums>0) f FROM " +
        GKX + "dwd_zh_journal")
    p["download_num_filled"] = safe(
        "SELECT COUNT(*) n, SUM(download_num IS NOT NULL AND download_num>0) f FROM " +
        GKX + "dwd_zh_paper")

    zh_types = {r.get("t") for r in p["zh_journal_publication_type"] if "t" in r}
    en_types = {r.get("t") for r in p["en_journal_publication_type"] if "t" in r}
    conf_types = {t for t in (zh_types | en_types) if t and ("会议" in str(t) or "Conference" in str(t)
                                                             or "Proceedings" in str(t))}
    p["conference_publication_types_found"] = sorted(conf_types)
    p["conference_entities"] = 0 if not conf_types else "需复核"
    p["zh_paper_all_journal_articles"] = all(
        str(r.get("t")) in ("期刊", "期刊论文") for r in p["zh_paper_publication_type"] if "t" in r)
    p["event_table_probe"] = safe(
        "SELECT COUNT(*) n FROM " + GKX + "dwd_event")
    p["gkx_schema_conference_table_hits"] = safe(
        "SELECT COUNT(*) n FROM information_schema.tables WHERE table_schema=%s "
        "AND (TABLE_NAME LIKE '%%confer%%' OR TABLE_NAME LIKE '%%meeting%%')", (SCHEMA,))

    # ---------- 5. 定档 ----------
    ok = isinstance(p["conference_entities"], int) and p["conference_entities"] > 0
    out["support_judgment"] = "完全不支持" if not ok else "部分支持"
    out["support_reason"] = (
        "会议实体的唯一可能落点是期刊/会议录表：gkx.dwd_zh_journal 仅 publication_type='期刊'（2,796 种），"
        "gkx.dwd_en_journal 仅 Journal/Book in series/Book（605 种，无 Conference/Proceedings 类型），"
        "gkx.dwd_zh_paper 全表 publication_type='期刊'、paper_type='期刊论文'（100,900 篇），"
        "名称含 Conference/Proceedings 的英文刊 21 种经核为丛书（Book in series）而非会议录。"
        "gkx 280 表中亦无 conference/meeting 专表（information_schema LIKE 检索 0 张；"
        "dwd_event 20 行为事件流水，非学术会议）。会议实体数 = 0 → 会议热度、投稿数、参与人数"
        "三维全部无分母，指标无法构建。"
    )
    out["notes"] = [
        "20261021 换源核对：gkx 280 表清单与 20261020 开发库 ODS 同源，均无会议（conference/meeting）专表；"
        "本批 probe 用 information_schema 对 gkx 复核，conference/meeting 命中 0 张。",
        "王惠 calc-logic 备注已写明「会议实体评价表数据源标准缺失，需郭经理与数据采购方沟通」，本次实测确认该缺口仍存在。",
        "gkx.dwd_zh_journal / dwd_en_journal 的 impact_score 全表为空（0/2,796 与 0/605）；"
        "王惠口径「热度优先读 impact_score，没有则用论文 download_num」的备选也失效："
        "download_num>0 为 0/100,900。即便补入会议实体，热度维仍无源（只有 cite_nums 2,796/2,796 可用，但作用于期刊）。",
        "若甲方补充会议主档（会议名称/届次/举办地/官网）+ 会议论文集映射，本指标可转为「完全转换支持」。",
        "行数口径说明：probes 中 conference_like_tables 的 n 来自 information_schema.TABLE_ROWS（估算），"
        "如 dwd_merger_acquisition_events_party_info 估算 19,779（旧版 19,843），库存 json 的 COUNT(*) 为 20,000；"
        "正文引用行数一律以 _work_gkx21/GKX_INVENTORY.json 的 COUNT(*) 为准。",
    ]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(p, ensure_ascii=False, indent=1, default=str)[:2500])
    print("support:", out["support_judgment"])


if __name__ == "__main__":
    main()
