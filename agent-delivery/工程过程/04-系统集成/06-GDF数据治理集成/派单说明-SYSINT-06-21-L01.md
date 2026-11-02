# 派单说明 · SYSINT-06-21-L01

```text
/goal data-agent
身份：你是数据工程师。本单分析服务机构的加工过程，并把结果落地到 GDF。
强度：ponytail off（定义任务）。
任务：SYSINT-06-21-L01
标题：服务机构：分析加工过程并落地到 GDF
WBS：WBS-06-21
监管人：human:淮政玮。未获开工指令前不认领。开工时 task-claim，claimed_by=agent:data-agent，supervised_by=human:淮政玮。
状态：backlog，未认领。先做 SYSINT-06-21-01-L01，再做 SYSINT-06-21-01-L02。对照 SYSINT-06-15-L01，不代替该贴源叶，也不等它跑通。
仓：派单包写在 gkx-orchestration。不改企业 v4、产业链 v2、政策 v2，不改 06-19 / 06-20 派单包。不改业务仓代码。分支 origin/dev。注册表改动写完立刻 commit + push。未获「提交并推送」前，说明和派单包不要自行 push。
开始时间：2026-11-02。完成日期要求：暂无截至时间。
```

## 目标

分析服务机构的加工过程，并落地到 GDF。

## 先做的子任务

`SYSINT-06-21-01-L01`（WBS-06-21-01）调研现网 demo 与 lumen 里服务机构的数据处理。派单见 [派单说明-SYSINT-06-21-01-L01.md](./派单说明-SYSINT-06-21-01-L01.md)。

`SYSINT-06-21-01-L02`（WBS-06-21-01B）依据上一叶的执行结果，检查 `storage/SVC`，更新文档，并输出完整加工链路和分场景流程图。派单见 [派单说明-SYSINT-06-21-01-L02.md](./派单说明-SYSINT-06-21-01-L02.md)。本叶以这两份结果为输入。

## 要落地的内容

分析写清现有加工，再写成 GDF 能照着做的派单包。缺口写「未闭合」，不编造表，不把 demo 库写成产线已跑通。

1. **加工过程。** 专题流水线到 ADS、入 ES、入图谱串成一条。ADS 已知落点包括 `svc_org_card` 以及一起算的 circle / tech / tags / patent，写明在 `demo_gkxlumenx_*` 还是 `gkxlumenx_*`。入 ES 是 `lumen-etl-es-py` 的作业 `service_org`、索引别名 `gkx_svc_org`。入图谱是 Tag `institution`，边 `participates` / `belongs_to` / `service_provide`。内容运营的服务机构写接口不写 ADS。GDF 不直写图库。
2. **落到 GDF。** 派单包写明 GDF 要建的表、要跑的步骤、谁触发。未在 GDF 建作业、执行结果未回，不写可对端。本叶不执行建表，不灌数。

WBS-06-15 仍是贴源加 Mapping 到 ADS 的实施叶。本叶不代替它。

## 完成

handoff：`agent-delivery/agent-handoffs/SYSINT-06-21-L01.md`。定义任务，不写联调通过。
