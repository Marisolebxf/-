#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T01 补建结构执行（本项目燕大侧唯一一次授权写操作）
授权链：唐绍祖 2026-11-10 确认内容（16 条 CREATE、无 ALTER）
      → 徐滕强 2026-11-11 授权"你们可以直接建"（执行人由 DBA 改为燕大，聊天记录为凭）
范围铁律：只执行下列 16 条语句；只碰 demo_gkx_chain；无任何 ALTER；不写任何数据。
输出：终端打印 + 生成 T01-建表执行-实测.md（执行证据）
"""
import os
import time
from datetime import datetime

from nebula3.gclient.net import ConnectionPool
try:
    from nebula3.Config import Config as NebulaConfig
except ImportError:
    from nebula3.Config import Configs as NebulaConfig

SPACE = "demo_gkx_chain"  # 只碰 demo 空间，绝不碰 gkx_chain

# 与《T01-缺口清单-交付版》v3 §6 逐条一致（唐绍祖 2026-11-10 确认版）
STMTS = [
    # Tag（5 个）
    "CREATE TAG IF NOT EXISTS research (name string, props string)",
    "CREATE TAG IF NOT EXISTS person   (name string, props string)",
    "CREATE TAG IF NOT EXISTS paper    (name string, props string)",
    "CREATE TAG IF NOT EXISTS patent   (name string, props string)",
    "CREATE TAG IF NOT EXISTS project  (name string, props string)",
    # Edge（11 种）
    "CREATE EDGE IF NOT EXISTS belong          (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS participate     (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS author_of       (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS publish         (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS policy_relate   (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS policy_apply_to (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS research_coop   (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS talent_coop     (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS service_provide (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS supply          (weight double, props string)",
    "CREATE EDGE IF NOT EXISTS parent_sub      (weight double, props string)",
]

NEW_TAGS = ["research", "person", "paper", "patent", "project"]
NEW_EDGES = ["belong", "participate", "author_of", "publish", "policy_relate",
             "policy_apply_to", "research_coop", "talent_coop", "service_provide",
             "supply", "parent_sub"]

out = []


def log(s=""):
    print(s, flush=True)
    out.append(str(s))


def q(sess, nGQL):
    r = sess.execute(nGQL)
    return r.is_succeeded(), (r.error_msg() if not r.is_succeeded() else "")


def main():
    addr = os.environ.get("NEBULA_ADDR", "10.50.75.136:9669")
    user, pw = os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"]
    host, port = addr.split(":")
    pool = ConnectionPool()
    assert pool.init([(host, int(port))], NebulaConfig()), "连不上"
    s = pool.get_session(user, pw)

    log(f"# T01 补建结构执行记录 · {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    log(f"- 空间：{SPACE}（仅此空间）")
    log("- 授权：唐绍祖 2026-11-10 确认内容；徐滕强 2026-11-11 授权燕大直接执行")
    log("- 范围：仅下列 16 条 CREATE（IF NOT EXISTS），无 ALTER、无数据写入\n")

    ok, err = q(s, f"USE {SPACE}")
    assert ok, f"进不了空间 {SPACE}: {err}"
    log(f"## 一、执行 {len(STMTS)} 条 CREATE\n")
    n_ok = 0
    for stmt in STMTS:
        ok, err = q(s, stmt + ";")
        mark = "✅" if ok else f"❌ {err}"
        log(f"- {mark} `{stmt}`")
        n_ok += ok
    log(f"\n成功 {n_ok}/{len(STMTS)}。\n")
    if n_ok != len(STMTS):
        log("!! 有失败语句，中止后续步骤，先查原因。")
        s.release(); pool.close()
        with open("T01-建表执行-实测.md", "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        return

    log("## 二、等两个心跳（约 45 秒）让结构生效\n")
    time.sleep(45)

    ok, err = q(s, "SUBMIT JOB STATS;")
    log(f"- SUBMIT JOB STATS：{'✅ 已提交' if ok else '❌ ' + err}（统计异步刷新，供 SHOW STATS 用）\n")

    log("## 三、即时复核（SHOW + DESCRIBE，只读）\n")
    for nGQL in ["SHOW TAGS;", "SHOW EDGES;"]:
        r = s.execute(nGQL)
        if r.is_succeeded():
            try:
                names = [row[0].as_string() for row in r]
            except Exception:
                names = [str(row) for row in r]
            log(f"- `{nGQL}` → {len(names)} 个：{', '.join(names)}")

    log("")
    for t in NEW_TAGS:
        r = s.execute(f"DESCRIBE TAG {t};")
        if r.is_succeeded():
            try:
                cols = [(row[0].as_string(), row[1].as_string()) for row in r]
            except Exception:
                cols = [(str(row)) for row in r]
            log(f"- DESCRIBE TAG {t} → {cols}")
        else:
            log(f"- DESCRIBE TAG {t} ❌ {r.error_msg()}")
    for e in NEW_EDGES:
        r = s.execute(f"DESCRIBE EDGE {e};")
        if r.is_succeeded():
            try:
                cols = [(row[0].as_string(), row[1].as_string()) for row in r]
            except Exception:
                cols = [(str(row)) for row in r]
            log(f"- DESCRIBE EDGE {e} → {cols}")
        else:
            log(f"- DESCRIBE EDGE {e} ❌ {r.error_msg()}")

    s.release(); pool.close()
    with open("T01-建表执行-实测.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("\n📝 已生成 T01-建表执行-实测.md（执行证据，复验时与核对清单同版提交）")


if __name__ == "__main__":
    main()
