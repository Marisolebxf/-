#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T01 补列实测 · VID 前缀抽查 + 边端点方向抽样（只读）
铁律：只执行 MATCH / SHOW 类只读查询，无任何写操作。
输出：终端打印 + 生成 T01-补列-实测.md（原始证据）
"""
import os
import sys
from datetime import datetime

from nebula3.gclient.net import ConnectionPool
try:
    from nebula3.Config import Config as NebulaConfig
except ImportError:
    from nebula3.Config import Configs as NebulaConfig

SPACE = "demo_gkx_chain"
PREFIXES = ["ent:", "seg:", "inst:", "person:", "paper:", "patent:", "proj:", "policy:", "svc:", "tp:"]
# 现存全部 Tag（DDL 内 4 + DDL 外技术点层/历史 6）
TAGS = ["enterprise", "segment", "institution", "policy",
        "chain", "tech_point", "tech_paper", "tech_patent", "tech_institution", "tech_person"]
# 现存全部 15 种边（DDL 内 4 + DDL 外 11）
EDGES = ["cooperate", "cite", "depends_on", "participates",
         "tech_rel", "tech_has_paper", "tech_has_patent", "tech_has_institution",
         "tech_has_person", "tech_path_step", "supplies", "belongs_to", "support", "apply_to", "regulate"]

out = []


def log(s=""):
    print(s, flush=True)
    out.append(str(s))


def q(sess, nGQL):
    r = sess.execute(nGQL)
    if not r.is_succeeded():
        return None, r.error_msg()
    try:
        return r.as_primitive(), None
    except Exception as ex:
        return None, f"解析失败:{ex}"


def main():
    addr = os.environ.get("NEBULA_ADDR", "10.50.75.136:9669")
    user, pw = os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"]
    host, port = addr.split(":")
    pool = ConnectionPool()
    assert pool.init([(host, int(port))], NebulaConfig()), "连不上"
    s = pool.get_session(user, pw)
    assert s.execute(f"USE {SPACE}").is_succeeded(), "进不了空间"
    log(f"# T01 补列实测 · {datetime.now():%Y-%m-%d %H:%M:%S}（只读）\n")

    # ── 一、每个现存 Tag：VID 前缀分布（GROUP BY）+ 20 条样例 ──
    log("## 一、Tag → VID 前缀分布\n")
    for t in TAGS:
        data, err = q(s, f'MATCH (v:{t}) RETURN left(id(v), 5) AS p5, count(*) AS c')
        if err:
            log(f"- {t}: 前缀分布查询失败（{err}），改抽样")
            data, err = q(s, f'MATCH (v:{t}) RETURN id(v) AS vid LIMIT 20')
            if err:
                log(f"  抽样也失败：{err}\n")
                continue
            from collections import Counter
            cnt = Counter(str(r["vid"]).split(":")[0] + ":" for r in data)
            log(f"  抽样20条前缀：{dict(cnt)}\n")
            continue
        dist = {r["p5"]: r["c"] for r in data}
        log(f"- **{t}**（{sum(dist.values()):,} 点）：{dist}")
        sample, err = q(s, f'MATCH (v:{t}) RETURN id(v) AS vid LIMIT 3')
        if not err and sample:
            log(f"  样例：{[r['vid'] for r in sample]}")
    log()

    # ── 二、10 个目标前缀的存在性（在对应 Tag 内查；未知宿主的做全图查） ──
    log("## 二、目标 VID 前缀存在性\n")
    for p in PREFIXES:
        n = len(p)  # ent:→4, paper:→6
        host_tags = {"ent:": "enterprise", "seg:": "segment", "inst:": "institution",
                     "policy:": "policy", "tp:": "tech_point"}.get(p)
        if host_tags:
            data, err = q(s, f'MATCH (v:{host_tags}) WHERE left(id(v), {n}) == "{p}" RETURN id(v) AS vid LIMIT 3')
            where = f"（在 {host_tags} 内）"
        else:
            data, err = q(s, f'MATCH (v) WHERE left(id(v), {n}) == "{p}" RETURN id(v) AS vid LIMIT 3')
            where = "（全图）"
        if err:
            log(f"- `{p}`：查询失败 {where}：{err}")
        elif data:
            log(f"- `{p}`：存在 {where}，样例 {[r['vid'] for r in data[:3]]}")
        else:
            log(f"- `{p}`：未见 {where}（对应 Tag 未建或无数据）")
    log()

    # ── 三、15 种现存边：端点方向抽样（各 20 条） ──
    log("## 三、边端点方向抽样（各 20 条）\n")
    for e in EDGES:
        data, err = q(s, f'MATCH (v)-[e:{e}]->(v2) RETURN tags(v) AS st, tags(v2) AS dt, '
                        f'id(v) AS sv, id(v2) AS dv LIMIT 20')
        if err:
            log(f"- **{e}**：查询失败：{err}")
            continue
        if not data:
            log(f"- **{e}**：无数据（0 条）")
            continue
        from collections import Counter
        combo = Counter((str(r["st"]), str(r["dt"])) for r in data)
        log(f"- **{e}**（抽样{len(data)}条）：")
        for (st, dt), c in combo.most_common():
            log(f"    {st} → {dt} ：{c} 条")
        log(f"    样例：{data[0]['sv']} -[{e}]-> {data[0]['dv']}")
    log()

    # ── 四、T06 输入：depends_on / participates 全量端点拆分 ──
    log("## 四、全量端点拆分（T06 输入）\n")
    for e in ["depends_on", "participates"]:
        data, err = q(s, f'MATCH (v)-[e:{e}]->(v2) RETURN tags(v) AS st, tags(v2) AS dt, count(*) AS c')
        if err:
            log(f"- **{e}**：全量拆分查询失败：{err}")
            continue
        log(f"- **{e}** 全量端点构成：")
        for r in data:
            log(f"    {r['st']} → {r['dt']} ：{r['c']:,} 条")
    log()

    s.release(); pool.close()
    with open("T01-补列-实测.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("\n📝 已生成 T01-补列-实测.md")


if __name__ == "__main__":
    main()
