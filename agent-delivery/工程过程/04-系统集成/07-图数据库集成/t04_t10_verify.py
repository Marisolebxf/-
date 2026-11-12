#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T04/T10 交付核验（只读）——白鑫凤代核，2026-11-12
T04：对账单数字 vs 图内实测；T10 由 JSON 侧核（不连图）。
铁律：只读 MATCH count / 抽样 props，无任何写操作。
"""
import os
from datetime import datetime

from nebula3.gclient.net import ConnectionPool
try:
    from nebula3.Config import Config as NebulaConfig
except ImportError:
    from nebula3.Config import Configs as NebulaConfig

SPACE = "demo_gkx_chain"

CHECKS = [
    ("M08 participate: research→project 应17,426",
     'MATCH (a:research)-[e:participate]->(b:project) RETURN count(e) AS cnt', "17,426"),
    ("M09 author_of 总数 应85,069",
     'MATCH ()-[e:author_of]->() RETURN count(e) AS cnt', "85,069"),
    ("M09 方向抽验 person→patent（应等于总数）",
     'MATCH (a:person)-[e:author_of]->(b:patent) RETURN count(e) AS cnt', "85,069"),
    ("Tag person 应100,000",
     'MATCH (v:person) RETURN count(v) AS cnt', "100,000"),
    ("Tag research 应83,745",
     'MATCH (v:research) RETURN count(v) AS cnt', "83,745"),
    ("Tag patent 应70,496",
     'MATCH (v:patent) RETURN count(v) AS cnt', "70,496"),
    ("Tag project 应17,402",
     'MATCH (v:project) RETURN count(v) AS cnt', "17,402"),
    ("Tag paper 应0",
     'MATCH (v:paper) RETURN count(v) AS cnt', "0"),
    ("存量不动 cooperate 应94,824",
     'MATCH ()-[e:cooperate]->() RETURN count(e) AS cnt', "94,824"),
    ("存量不动 participates 应213,500",
     'MATCH ()-[e:participates]->() RETURN count(e) AS cnt', "213,500"),
    ("存量不动 depends_on 应1,073",
     'MATCH ()-[e:depends_on]->() RETURN count(e) AS cnt', "1,073"),
    ("批号抽验 author_of props（看 comply 批号）",
     'MATCH ()-[e:author_of]->() WITH e LIMIT 1 RETURN e.props AS p', None),
    ("批号抽验 participate props",
     'MATCH ()-[e:participate]->() WITH e LIMIT 1 RETURN e.props AS p', None),
]


def fmt(v):
    return f"{v:,}" if isinstance(v, int) else str(v)


def main():
    addr = os.environ.get("NEBULA_ADDR", "10.50.75.136:9669")
    user, pw = os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"]
    host, port = addr.split(":")
    pool = ConnectionPool()
    assert pool.init([(host, int(port))], NebulaConfig()), "连不上"
    s = pool.get_session(user, pw)
    assert s.execute(f"USE {SPACE}").is_succeeded()
    print(f"# T04 交付核验 · 只读实测（{datetime.now():%Y-%m-%d %H:%M:%S}）\n")
    npass = 0
    for label, gql, expect in CHECKS:
        r = s.execute(gql + ";")
        if not r.is_succeeded():
            print(f"❌ {label}｜查询失败：{r.error_msg()}")
            continue
        try:
            val = list(r.as_primitive()[0].values())[0]
        except Exception as ex:
            print(f"❌ {label}｜解析失败 {ex}")
            continue
        if expect is None:
            print(f"ℹ️  {label}｜{val}")
        else:
            ok = fmt(val) == expect if isinstance(val, int) else str(val) == expect
            npass += ok
            print(f"{'✅' if ok else '❌'} {label}｜实测 {fmt(val)}")
    print(f"\n对账项通过：{npass}/{sum(1 for c in CHECKS if c[2])}")
    s.release(); pool.close()


if __name__ == "__main__":
    main()
