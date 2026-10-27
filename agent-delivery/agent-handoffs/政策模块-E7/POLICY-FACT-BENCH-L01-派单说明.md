# 派单说明 · 政策事实落点

> 日期：2026-10-27
> 任务：`POLICY-FACT-BENCH-L01`（已建，状态 `ready`，本说明不认领、不开工）
> WBS：`WBS-06-03J`（[WBS.md](../../工程过程/04-系统集成/06-GDF数据治理集成/WBS.md)）
> 监管人：`human:淮政玮`
> 执行：`agent:frontend-agent`，协作 `agent:algorithm-agent`
> Epic：`E-PLATFORM-P1`。强度：ponytail full

清单真源是 [POLICY-METRIC-FACT-GAP-L01.md](./POLICY-METRIC-FACT-GAP-L01.md)。35 条的标签以该文件为准：已有表 10、缺表 1、口径 24。本叶不改那份判定，不把 QPOL 改绿。

## 顺序

先改 `demo-algo-ent-analysis`，再改 `demo-ui-system-test`。demo 人工自检通过并写进 handoff 之前，不改任何 lumen 仓。

```text
demo-algo 两个接口  →  demo-ui-system-test 事实落点页  →  人工自检
  →  再迁 lumen 展示页和专题页
```

## 页面

挂在 `demo-ui-system-test` 政策菜单，标题「事实落点」。35 条都列出。24 条口径单独成组。每条给出 `metric_id`、中文名、标签（已有表 / 缺表 / 口径），并链到 `metrics/calc-logic/POLICY/{metric_id}.md`。

每条两个按钮：

- 「创建相关的事实表」：按该文档里的事实落点，在 demo 库补齐本指标要写的表。已有表的只核对，不另造第二张。
- 「mock符合条件的数据到事实表」：只插入本按钮自己的批次，按该文档的计算逻辑算出这一条，写入 demo ADS。结果标明临时口径。

算出的数可以进展示页和专题页。这些页沿用已有的「待甲方确认」角标，不新造一套标记。

## 库

只写 `demo_gkxlumenx_ods` / `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`。`is_live("policy")` 为真时两个按钮都拒绝。不写供应方库 `gkx`，不写正式 `gkxlumenx_*`。

mock 只删本按钮先前写入的批次，不调用会清空五张分布表的全量重算。

缺表只有 `M_POLICY_SUPPORT_STRENGTH`：事实是一条政策的政策标识、扶持方式、金额。权重不进表。demo 按钮可以在 demo ODS 建这张事实并写入临时口径。这不构成 `WBS-06-03H` 的点头，产线空表仍归 `GDF-POLICY-MT-SUPPORT-L01`。

## 不做

- 不代替 `WBS-06-03` 的跑通，本叶不是可对端。
- 不打开 `WBS-06-03G`。本页 mock 不是政策包灌数，不向政策包 ODS 写。
- 不改 `metrics/calc-logic`、就绪度、QPOL。
- 不把 `lumen-ui-topic` 指到 demo 服务。
- 迁 lumen 时调用链仍是前端 → Java → Python `/internal/*`。

## 认领

```text
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师。算法接口由同一叶里的 algorithm-agent 协作完成，页面在接口可调用之后再接。
强度：ponytail full
监管人：human:淮政玮
执行：agent:frontend-agent
协作：agent:algorithm-agent
任务：POLICY-FACT-BENCH-L01
仓：先 ${GKX_ROOT}/repos/demo-algo-ent-analysis 与 ${GKX_ROOT}/repos/demo-ui-system-test。人工自检写进 handoff 之前不改 lumen。
认领：claimed_by=agent:frontend-agent，supervised_by=human:淮政玮。

目标：按本派单说明做事实落点页。35 条、24 条口径、两个按钮、计算逻辑只引用指标库原文。出数标明临时口径，展示页和专题页能读到。
验收：demo 上点一条已有表、一条口径、以及扶持这一条缺表，各自能出数；自检记录写入 handoff；然后再迁 lumen。
不做：不改缺口清单的标签，不把 03H 标成已点头，不打开 03G，不写供应方库。
```

完工 handoff：`agent-handoffs/政策模块-E7/POLICY-FACT-BENCH-L01.md`。`ponytail: full`。
