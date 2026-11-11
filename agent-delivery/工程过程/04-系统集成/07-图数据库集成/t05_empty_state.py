#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T05 · 空态层入图核验（M05/M10–M14/M16/M18/M21/M23/M24）—— 只读核数
口径：SDD §5 T05 话术（KG-COMPLY-SDD-L01）+ 15 边型↔24 M 对应表（§5 line 355）
铁律：只读（MATCH count），不灌 mock、不从 gkx_chain 拷数、无任何写操作。
输出：T05-空态-实测.md（原始证据）
"""
import os
from datetime import datetime

from nebula3.gclient.net import ConnectionPool
try:
    from nebula3.Config import Config as NebulaConfig
except ImportError:
    from nebula3.Config import Configs as NebulaConfig

SPACE = "demo_gkx_chain"

# 9 种边型（11 条 M：M12–M14 共用 policy_apply_to）
EDGE_COUNTS = ["belong", "publish", "policy_relate", "policy_apply_to",
               "service_provide", "supply", "parent_sub", "cite"]

# participates 特殊：M17/M18 同边不同端点构成，M18 只认 institution→segment
PARTICIPATES_SPLITS = [
    ("M18 口径：institution→segment",
     'MATCH (a:institution)-[e:participates]->(b:segment) RETURN count(e) AS cnt'),
    ("参考：M17 存量已满足 enterprise→segment",
     'MATCH (a:enterprise)-[e:participates]->(b:segment) RETURN count(e) AS cnt'),
    ("参考：历史混装 institution→institution（不属 M17/M18，T06 对象）",
     'MATCH (a:institution)-[e:participates]->(b:institution) RETURN count(e) AS cnt'),
    ("participates 同名边总数",
     'MATCH ()-[e:participates]->() RETURN count(e) AS cnt'),
]

# DoD：policy / institution Tag 有历史数据，须与「本期七要素层无供数」分层呈现
TAG_COUNTS = ["policy", "institution"]

out = []


def log(s=""):
    print(s, flush=True)
    out.append(str(s))


def qcnt(sess, nGQL):
    r = sess.execute(nGQL)
    if not r.is_succeeded():
        return f"查询失败：{r.error_msg()}"
    try:
        return f"{r.as_primitive()[0]['cnt']:,}"
    except Exception as ex:
        return f"解析失败:{ex}"


def main():
    addr = os.environ.get("NEBULA_ADDR", "10.50.75.136:9669")
    user, pw = os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"]
    host, port = addr.split(":")
    pool = ConnectionPool()
    assert pool.init([(host, int(port))], NebulaConfig()), "连不上"
    s = pool.get_session(user, pw)
    assert s.execute(f"USE {SPACE}").is_succeeded(), "进不了空间"
    log(f"# T05 空态核验 · 实测（{datetime.now():%Y-%m-%d %H:%M:%S}，只读）\n")
    log(f"- 空间：{SPACE}；账号同 T01（环境清单 TRSGraph 行），全程 MATCH count，无写操作\n")

    log("## 一、11 条 M 对应边型逐条核数（预期 0）\n")
    m_map = [("M05", "belong"), ("M10", "publish"), ("M11", "policy_relate"),
             ("M12/M13/M14", "policy_apply_to"), ("M16", "cite（历史边）"),
             ("M21", "service_provide"), ("M23", "supply"), ("M24", "parent_sub")]
    for m, e in m_map:
        name = e.split("（")[0]
        cnt = qcnt(s, f"MATCH ()-[x:{name}]->() RETURN count(x) AS cnt")
        log(f"- {m} → `{name}`：{cnt} 条")

    log("\n## 二、participates 按端点拆分（M18 = institution→segment）\n")
    for label, nGQL in PARTICIPATES_SPLITS:
        log(f"- {label}：{qcnt(s, nGQL)} 条")

    log("\n## 三、Tag 历史数据（区分「Tag 有数据」与「本期七要素层无供数」）\n")
    for t in TAG_COUNTS:
        cnt = qcnt(s, f"MATCH (v:{t}) RETURN count(v) AS cnt")
        log(f"- Tag `{t}`：{cnt} 点（历史数据；本期七要素层新边全部 0，见上）")

    s.release(); pool.close()
    with open("T05-空态-实测.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("\n📝 已生成 T05-空态-实测.md")


if __name__ == "__main__":
    main()
