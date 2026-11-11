#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T01 · 只读核对 demo_gkx_chain 结构 vs 已签收 DDL（KG-7ELEM-SCHEMA-DDL-L01）

铁律：
  - 只读。只执行 SHOW TAGS / SHOW EDGES / DESCRIBE / SHOW STATS。
  - 不 INSERT、不 CREATE、不 SUBMIT、不 ALTER。
  - 凭据只从环境变量读，不写进任何文件。

用法：
  export NEBULA_ADDR=10.50.75.136:9669
  export NEBULA_USER=<线下申请的只读账号>
  export NEBULA_PASS=<口令>
  python3 t01_verify.py

输出：终端打印核对结果 + 生成 T01-缺口清单-实测.md
"""
import os
import sys
from datetime import datetime

from nebula3.gclient.net import ConnectionPool
try:  # 新旧版本类名兼容（本机装的是老版 Config）
    from nebula3.Config import Config as NebulaConfig
except ImportError:
    from nebula3.Config import Configs as NebulaConfig

SPACE = "demo_gkx_chain"

# ── 标准答案：带属性版（唐绍祖 2026-11-10 确认、徐滕强 2026-11-11 授权执行后的目标结构）──
# Tag: {名: [(属性, 类型), ...]}
EXPECTED_TAGS = {
    "enterprise": [("name", "string"), ("node_type", "string"), ("enterprise_code", "string"),
                   ("chain_role", "string"), ("weight", "double"), ("props", "string")],
    "segment":    [("name", "string"), ("segment_key", "string"), ("chain_id", "string"),
                   ("chain_stage", "string"), ("weight", "double"), ("props", "string")],
    "research":   [("name", "string"), ("props", "string")],   # 2026-11-11 建成（带属性版）
    "paper":      [("name", "string"), ("props", "string")],
    "patent":     [("name", "string"), ("props", "string")],
    "project":    [("name", "string"), ("props", "string")],
    "person":     [("name", "string"), ("props", "string")],
    "institution":[("name", "string"), ("institution_type", "string"),
                   ("weight", "double"), ("props", "string")],
    "policy":     [("name", "string"), ("weight", "double"), ("props", "string")],
}

EXPECTED_EDGES = {
    "cooperate":       [],   # 基准空属性；图内多列见 ACCEPTED_DRIFT（评审裁定保留不重建）
    "belong":          [("weight", "double"), ("props", "string")],
    "cite":            [("weight", "double"), ("props", "string")],
    "participate":     [("weight", "double"), ("props", "string")],   # 注意：无 s，与 participates 是两种边
    "author_of":       [("weight", "double"), ("props", "string")],
    "publish":         [("weight", "double"), ("props", "string")],
    "policy_relate":   [("weight", "double"), ("props", "string")],
    "policy_apply_to": [("weight", "double"), ("props", "string")],
    "depends_on":      [("dependency_type", "string"), ("weight", "double"), ("props", "string")],
    "participates":    [],   # 企业/服务机构 → 产业链环节；多列见 ACCEPTED_DRIFT
    "research_coop":   [("weight", "double"), ("props", "string")],
    "talent_coop":     [("weight", "double"), ("props", "string")],
    "service_provide": [("weight", "double"), ("props", "string")],
    "supply":          [("weight", "double"), ("props", "string")],
    "parent_sub":      [("weight", "double"), ("props", "string")],
}

# 评审（2026-11-09）裁定保留、不重建的已知属性漂移：图内比基准多的列
ACCEPTED_DRIFT = {
    "cooperate":    {"props", "weight"},
    "participates": {"chain_role", "chain_score", "participation_depth", "props"},
}

# DDL 外、图内预期会有的（技术点层等，不算缺口，只记录）
KNOWN_EXTRAS_NOTE = "技术点层（tech_point/tech_paper/tech_patent/tech_institution/tech_person）、chain 等历史结构"


def rows(result):
    """把 nebula3 结果转成 (列名列表, [[值, ...], ...])；兼容老版 as_primitive"""
    if result is None or not result.is_succeeded():
        return [], []
    try:
        data = result.as_primitive()  # list[dict]，值已是 python 原生类型
    except Exception:
        data = None
    if data:
        keys = list(data[0].keys())
        return keys, [[("" if row.get(k) is None else str(row.get(k))) for k in keys] for row in data]
    return list(result.keys()), []


def describe_map(sess, kind, name):
    """DESCRIBE TAG/EDGE x → {字段: 类型}"""
    r = sess.execute(f"DESCRIBE {kind} {name}")
    if not r.is_succeeded():
        return None
    m = {}
    for row in rows(r)[1]:
        if row and row[0] not in ("", "None"):
            m[row[0]] = row[1]
    return m


def main():
    addr = os.environ.get("NEBULA_ADDR", "10.50.75.136:9669")
    user = os.environ.get("NEBULA_USER")
    pw = os.environ.get("NEBULA_PASS")
    if not user or not pw:
        print("❌ 未设置 NEBULA_USER / NEBULA_PASS（凭据线下申请，不落盘）")
        sys.exit(1)

    host, port = addr.split(":")
    config = NebulaConfig()
    pool = ConnectionPool()
    if not pool.init([(host, int(port))], config):
        print("❌ 连不上图库，检查网络/地址")
        sys.exit(1)
    sess = pool.get_session(user, pw)
    if not sess.execute(f"USE {SPACE}").is_succeeded():
        print(f"❌ 进不了空间 {SPACE}（账号权限或空间名问题）：{sess.execute(f'USE {SPACE}').error_msg()}")
        sys.exit(1)
    print(f"✅ 已连入 {addr} / {SPACE}（只读模式）\n")

    # 1) 现有 Tag / Edge
    tag_rows = rows(sess.execute("SHOW TAGS"))[1]
    edge_rows = rows(sess.execute("SHOW EDGES"))[1]
    actual_tags = {r[0] for r in tag_rows if r and r[0] not in ("Name", "")}
    actual_edges = {r[0] for r in edge_rows if r and r[0] not in ("Name", "")}

    report = [f"# T01 结构复验 · 实测（{datetime.now():%Y-%m-%d %H:%M}，16 条补建语句执行后）",
              f"\n目标：{addr} / {SPACE}；对照：带属性版目标结构（唐绍祖 2026-11-10 确认内容、徐滕强 2026-11-11 授权执行）\n"]

    # 2) Tag 比对
    report.append("## 1. Tag（DDL 9 个）\n\n| Tag | 状态 | 差异 |\n|---|---|---|")
    missing_tags, drift = [], []
    for t, props in EXPECTED_TAGS.items():
        if t not in actual_tags:
            missing_tags.append(t)
            report.append(f"| {t} | ❌ 缺失 | 需 DBA 补建 |")
            continue
        dm = describe_map(sess, "TAG", t) or {}
        want = {p: ty for p, ty in props}
        extra = set(dm) - set(want) - {"_vid"}
        lack = set(want) - set(dm)
        typedrift = {p for p in set(want) & set(dm) if want[p] != dm[p]}
        if not extra and not lack and not typedrift:
            report.append(f"| {t} | ✅ 一致 | |")
        else:
            drift.append(t)
            report.append(f"| {t} | ⚠ 属性漂移 | 多:{sorted(extra) or '-'} 少:{sorted(lack) or '-'} 类型差:{sorted(typedrift) or '-'} |")

    # 3) Edge 比对
    report.append("\n## 2. Edge（DDL 15 种）\n\n| Edge | 状态 | 差异 |\n|---|---|---|")
    missing_edges = []
    accepted = []
    for e, props in EXPECTED_EDGES.items():
        if e not in actual_edges:
            missing_edges.append(e)
            report.append(f"| {e} | ❌ 缺失 | 需 DBA 补建 |")
            continue
        dm = describe_map(sess, "EDGE", e) or {}
        want = {p: ty for p, ty in props}
        extra = set(dm) - set(want)
        lack = set(want) - set(dm)
        typedrift = {p for p in set(want) & set(dm) if want[p] != dm[p]}
        if not extra and not lack and not typedrift:
            report.append(f"| {e} | ✅ 一致 | |")
        elif not lack and not typedrift and extra == ACCEPTED_DRIFT.get(e, set()):
            accepted.append(e)   # 评审 2026-11-09 裁定保留的已知漂移
            report.append(f"| {e} | ✅ 已裁定保留 | 多列 {sorted(extra)}（历史写入所需，不重建） |")
        else:
            drift.append(e)
            report.append(f"| {e} | ⚠ 属性漂移 | 多:{sorted(extra) or '-'} 少:{sorted(lack) or '-'} 类型差:{sorted(typedrift) or '-'} |")

    # 4) 图内多余结构（记录，不算缺口）
    extras_t = sorted(actual_tags - set(EXPECTED_TAGS))
    extras_e = sorted(actual_edges - set(EXPECTED_EDGES))
    report.append("\n## 3. DDL 之外的既有结构（历史/技术点层，只记录不处理）\n")
    report.append(f"- Tag：{extras_t}\n- Edge：{extras_e}\n\n（预期含 {KNOWN_EXTRAS_NOTE}）")

    # 5) 建议 DBA 执行的语句
    report.append("\n## 4. 建议 DBA 执行的补建语句（逐条，均 IF NOT EXISTS）\n\n```sql")
    for t in missing_tags:
        props = ", ".join(f"{p} {ty}" for p, ty in EXPECTED_TAGS[t])
        report.append(f"CREATE TAG IF NOT EXISTS {t} ({props});" if props else f"CREATE TAG IF NOT EXISTS {t} ();")
    for e in missing_edges:
        props = ", ".join(f"{p} {ty}" for p, ty in EXPECTED_EDGES[e])
        report.append(f"CREATE EDGE IF NOT EXISTS {e} ({props});" if props else f"CREATE EDGE IF NOT EXISTS {e} ();")
    report.append("```\n")

    # 6) 可选基线（SHOW STATS 读的是最近一次统计，不主动触发 SUBMIT）
    r = sess.execute("SHOW STATS")
    if r.is_succeeded():
        report.append("## 5. 基线（SHOW STATS，对照 2026-11-07 实测）\n\n```\n"
                      + "\n".join(" | ".join(row) for row in rows(r)[1]) + "\n```")

    # 汇总
    if not missing_tags and not missing_edges and not drift:
        verdict = ("- 结论：**9 Tag + 15 Edge 全部存在且属性一致**（2 处已裁定保留漂移不计），结构补建复验通过。\n"
                   "- 证据同版归档：本文件 + T01-建表执行-实测.md + T01-补列-实测.md。\n"
                   "- 下一步：T01 按登记册验收流程关闭，T02–T04 解阻。\n")
    else:
        verdict = ("- 下一步：本清单交 human:唐绍祖 确认内容 → 报 human:徐滕强 → 授权执行补建语句 → 复验本脚本。\n")
    summary = (f"\n## 汇总\n\n- 缺 Tag：{len(missing_tags)} 个 → {missing_tags}\n"
               f"- 缺 Edge：{len(missing_edges)} 种 → {missing_edges}\n"
               f"- 属性漂移（未裁定）：{drift or '无'}；已裁定保留：{accepted or '无'}\n"
               + verdict)
    report.append(summary)

    out = "\n".join(report)
    print(out)
    with open("T01-复验-实测.md", "w", encoding="utf-8") as f:
        f.write(out)
    print(f"\n📝 已生成 T01-复验-实测.md（复验证据，与建表执行记录同版归档）。")
    sess.release()
    pool.close()


if __name__ == "__main__":
    main()
