# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(r"d:\work\gkx-lumen\gkx-orchestration\agent-delivery\qa\total-set\KJXXZSXT\fp-split-run")
d = json.loads((p / "_inventory.json").read_text(encoding="utf-8"))
core = {
    "科技发展态势",
    "科技政策跟踪",
    "科技人才态势",
    "科技数据资源",
    "科技知识图谱",
    "科技成果展示",
    "科技服务全景",
}
pol = "政策对比功能升级（核增需求）"
lines = [
    "# 五级任务队列（展示系统）",
    "",
    "状态：`pending` / `running` / `done` / `blocked` / `skipped`",
    "金样：**T27** 技术创新力指标展示。全量等监管人指令再开。",
    "范围锁定：七模块 589 + 政策对比核增 17 = **606 六级**。学习类核增 skipped。",
    "",
    "| ID | 三级 | 四级 | 五级 | 六级数 | 状态 |",
    "|---|---|---|---|---:|---|",
]
n_in = n_skip = 0
for t in d["tasks"]:
    if t["l3"] in core or t["l3"] == pol:
        st = "running（金样）" if t["id"] == "T27" else "pending"
        n_in += 1
    else:
        st = "skipped（学习类核增，六级为 /）"
        n_skip += 1
    lines.append(
        f"| {t['id']} | {t['l3']} | {t['l4']} | {t['l5']} | {t['l6_count']} | {st} |"
    )
(p / "01-task-list.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("in_scope_l5", n_in, "skipped_l5", n_skip)
