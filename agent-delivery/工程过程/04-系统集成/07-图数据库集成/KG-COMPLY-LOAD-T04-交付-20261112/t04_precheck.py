#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T04 · 只读预检（M07/M08/M09 灌数前置 + T10 输入自证）

铁律：
  - 只读。图库只执行 SHOW / MATCH count / DESCRIBE；久新库只执行 SELECT / SHOW。
  - 不 INSERT、不 CREATE、不 SUBMIT、不 ALTER、不 UPDATE、不 DELETE。
  - 凭据只从环境变量读，不写进任何文件。

用法：
  export NEBULA_ADDR=10.50.75.136:9669
  export NEBULA_USER=<环境清单 TRSGraph 行账号>
  export NEBULA_PASS=<口令>
  export DORIS_ADDR=47.93.119.170:29030          # 可省，有默认
  export DORIS_USER=<久新只读账号>                # 缺省则跳过 Doris 部分
  export DORIS_PASS=<口令>
  python3 t04_precheck.py

输出：终端打印 + 生成 T04-预检-实测.md
"""
import os
import sys
from datetime import datetime

# ── 图库（Nebula 协议）──────────────────────────────────────────
SPACE = "demo_gkx_chain"
NEW_TAGS = ["research", "person", "paper", "patent", "project"]
NEW_EDGES = ["belong", "participate", "author_of", "publish", "policy_relate",
             "policy_apply_to", "research_coop", "talent_coop", "service_provide",
             "supply", "parent_sub"]
TECH_TAGS = ["tech_point", "tech_paper", "tech_patent", "tech_institution", "tech_person"]
TECH_EDGES = ["tech_rel", "tech_has_paper", "tech_has_patent", "tech_has_person",
              "tech_has_institution", "tech_path_step"]

# ── 久新 Doris（2026-11-12 唐绍祖答复定案口径：应灌子集数对账，不按源表行数）──────
DORIS_DB = "gkx_technology_analysis_dev"
M08_WHERE = "institution_role_code IS NOT NULL AND institution_role_code != ''"
DORIS_QUERIES = [
    ("M07-定性证据（裁定不建：100%资助署名、参与字段全0）",
     f"SELECT relation_type AS rt, sum(is_lead=1) AS lead1, sum(is_direct_investigator=1) AS inv1, count(*) AS cnt "
     f"FROM {DORIS_DB}.ads_talent_project GROUP BY 1"),
    ("M08-应灌边（裁定 17,426）",
     f"SELECT institution_role_code AS role_code, count(*) AS cnt FROM {DORIS_DB}.ads_project_institution "
     f"WHERE {M08_WHERE} GROUP BY 1"),
    ("M08-行级可灌（机构端点全部能挂画像表 → 应灌=实灌分母）",
     f"SELECT count(*) AS cnt FROM {DORIS_DB}.ads_project_institution a "
     f"JOIN {DORIS_DB}.ads_institution_profile b ON a.institution_id=b.institution_id "
     f"WHERE a.{M08_WHERE}"),
    ("M08-去重端点（项目 17,402 / 机构 1,590）",
     f"SELECT count(*) AS d_project FROM (SELECT project_id FROM {DORIS_DB}.ads_project_institution "
     f"WHERE {M08_WHERE} GROUP BY project_id) t",
     ),
    ("M09-应灌边与去重端点（85,069 / 专利 70,496 / 人才 6,490）",
     f"SELECT count(*) AS cnt, count(DISTINCT patent_id) AS d_patent, count(DISTINCT talent_id) AS d_talent "
     f"FROM {DORIS_DB}.ads_talent_patent"),
    ("主数据-person 全量（100,000）", f"SELECT count(*) AS cnt FROM {DORIS_DB}.ads_talent_profile"),
    ("主数据-research 全量（83,745）", f"SELECT count(*) AS cnt FROM {DORIS_DB}.ads_institution_profile"),
]

out = [f"# T04 预检 · 实测（{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}，只读）", ""]


def nebula_part():
    from nebula3.gclient.net import ConnectionPool
    try:
        from nebula3.Config import Config as NebulaConfig
    except ImportError:
        from nebula3.Config import Configs as NebulaConfig

    addr = os.environ.get("NEBULA_ADDR", "10.50.75.136:9669")
    user, pw = os.environ.get("NEBULA_USER"), os.environ.get("NEBULA_PASS")
    if not user or not pw:
        out.append("## 一、图库：跳过（未设 NEBULA_USER/NEBULA_PASS）\n")
        return
    host, port = addr.split(":")
    pool = ConnectionPool()
    if not pool.init([(host, int(port))], NebulaConfig()):
        out.append(f"## 一、图库：❌ 连不上 {addr}\n")
        return
    sess = pool.get_session(user, pw)
    if not sess.execute(f"USE {SPACE}").is_succeeded():
        out.append(f"## 一、图库：❌ 进不了空间 {SPACE}\n")
        return
    out.append(f"## 一、图库（{addr} / {SPACE}）灌数前基线\n")

    def cnt(nql):
        r = sess.execute(nql)
        if not r.is_succeeded():
            return f"❌ {r.error_msg()}"
        try:
            data = r.as_primitive()  # list[dict]
            first = data[0] if data else {}
            v = next(iter(first.values()), "?") if first else 0
            return 0 if v is None else v
        except Exception:
            return "?"

    out.append("### 1. 新建 5 Tag（应全 0，灌数前照）\n")
    out.append("| Tag | MATCH count |")
    out.append("|---|---:|")
    for t in NEW_TAGS:
        out.append(f"| {t} | {cnt(f'MATCH (v:{t}) RETURN count(v) AS c')} |")

    out.append("\n### 2. 新建 11 Edge（应全 0）\n")
    out.append("| Edge | MATCH count |")
    out.append("|---|---:|")
    for e in NEW_EDGES:
        out.append(f"| {e} | {cnt(f'MATCH ()-[e:{e}]->() RETURN count(e) AS c')} |")

    out.append("\n### 3. 技术点层（T10 输入自证，对照 11-11 T01 复验基线）\n")
    out.append("| 项 | SHOW STATS |")
    out.append("|---|---:|")
    r = sess.execute("SHOW STATS")
    stats = {}
    if r.is_succeeded():
        try:
            data = r.as_primitive()  # list[dict]，t01_verify 同款
        except Exception:
            data = []
        for row in data:
            k, v, c = row.get("Type"), row.get("Name"), row.get("Count")
            if k is not None and v is not None:
                stats[(str(k), str(v))] = c
    for t in TECH_TAGS:
        out.append(f"| Tag {t} | {stats.get(('Tag', t), '?')} |")
    for e in TECH_EDGES:
        out.append(f"| Edge {e} | {stats.get(('Edge', e), '?')} |")
    out.append(f"| Space vertices | {stats.get(('Space', 'vertices'), '?')} |")
    out.append(f"| Space edges | {stats.get(('Space', 'edges'), '?')} |")
    sess.release()
    out.append("")


def doris_part():
    import pymysql
    addr = os.environ.get("DORIS_ADDR", "47.93.119.170:29030")
    user, pw = os.environ.get("DORIS_USER"), os.environ.get("DORIS_PASS")
    if not user or not pw:
        out.append("## 二、久新 Doris：跳过（未设 DORIS_USER/DORIS_PASS，口令线下获取）\n")
        return
    host, port = addr.split(":")
    conn = pymysql.connect(host=host, port=int(port), user=user, password=pw,
                           charset="utf8mb4", connect_timeout=10, read_timeout=600)
    cur = conn.cursor()
    out.append(f"## 二、久新 Doris（{addr} / {DORIS_DB}）构成与端点\n")
    for name, sql in DORIS_QUERIES:
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            out.append(f"### {name}\n")
            out.append("| " + " | ".join(cols) + " |")
            out.append("|" + "---:|" * len(cols))
            for row in rows[:20]:
                out.append("| " + " | ".join(str(x) for x in row) + " |")
            if len(rows) > 20:
                out.append(f"\n（共 {len(rows)} 组，仅列前 20）")
            out.append("")
        except Exception as ex:
            out.append(f"### {name}\n❌ {ex}\n")
    conn.close()


if __name__ == "__main__":
    nebula_part()
    doris_part()
    md = "\n".join(out) + "\n"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "T04-预检-实测.md"), "w") as f:
        f.write(md)
    print(md)
    print("✅ 已生成 T04-预检-实测.md")
