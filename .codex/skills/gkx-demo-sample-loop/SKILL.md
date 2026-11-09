---
name: gkx-demo-sample-loop
description: >
  展示系统演示样本满足循环：先有《合规演示用例》，再只读线上库对照其中可演的行；缺口分类后建数据、查询或算法子任务，直到样本满足。
  Use when the user says 演示样本满足, 演示样本满足任务LOOP, 按 LOOP 跑, 演示样本验收, 样本没对上, or gkx-demo-sample-loop.
  未授权不建单、不改库、不改代码。
---

# 演示样本满足循环

步骤真源在 `agent-delivery/产品实现规程.md`：§4.1 SDD，§6.4 合规演示用例，§6.5 循环。改流程先改规程。Cursor 技能只保留入口：

- `.cursor/skills/gkx-demo-sample-loop/SKILL.md`
- `.cursor/skills/gkx-demo-sample-loop/演示样本满足任务LOOP.md`

讨论流程时不建单。口令「按 LOOP 跑」才按真源执行一轮。

一轮结束回写该模块 LOOP 计划开头的状态行。通过、阻塞、交给人、子任务签收都要写。只改状态行。没回写就不算收尾。

样本满足、子任务都已签收或本轮没有子任务、状态行已回写之后，验收单改为 `done`。没收尾不改 `done`。写法在规程 §6.5。
