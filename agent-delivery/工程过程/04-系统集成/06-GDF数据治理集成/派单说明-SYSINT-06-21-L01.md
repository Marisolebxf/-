# 派单说明 · SYSINT-06-21-L01

```text
/goal data-agent
身份：你是数据工程师。本单只梳理服务机构的加工链路，不写作业，不建表，不灌数。
强度：ponytail off（定义任务）。
任务：SYSINT-06-21-L01
标题：服务机构：梳理专题跑通到 ADS、入 ES、入图谱的完整加工链路
WBS：WBS-06-21
监管人：human:淮政玮。未获开工指令前不认领。开工时 task-claim，claimed_by=agent:data-agent，supervised_by=human:淮政玮。
状态：backlog，未认领。先做子任务 SYSINT-06-21-01-L01。对照 SYSINT-06-15-L01，不代替该叶，也不等该叶跑通。
仓：只写 gkx-orchestration。说明放在本目录或 handoff。不改企业 v4、产业链 v2、政策 v2，不改 06-19 / 06-20 派单包。分支 origin/dev。注册表改动写完立刻 commit + push。未获「提交并推送」前，说明文档不要自行 push。
开始时间：2026-11-02。完成日期要求：暂无截至时间。
```

## 先做的子任务

`SYSINT-06-21-01-L01`（WBS-06-21-01）调研现网 demo 与 lumen 里服务机构的数据处理。本叶的链路说明以那份调研为输入。派单见 [派单说明-SYSINT-06-21-01-L01.md](./派单说明-SYSINT-06-21-01-L01.md)。

## 要梳理的链路

一条说明写完下面三段，并串成同一条链路。缺口写「未闭合」，不编造表，不把 demo 库写成产线已跑通。

1. **到 ADS。** 现有专题侧服务机构流水线已经灌到 ADS 的部分：库、表、作业、谁触发。已知落点包括 `svc_org_card` 以及和它一起算的 circle / tech / tags / patent。写明这些表现在在 `demo_gkxlumenx_*` 还是 `gkxlumenx_*`。内容运营的服务机构写接口不写 ADS，不要把它写成加工链路。
2. **入 ES。** `lumen-etl-es-py` 的作业 `service_org`，索引别名 `gkx_svc_org`。写明源表、触发方式和与 ADS 的先后。
3. **入图谱。** 现有落点：Tag `institution`；边 `participates`（服务机构到产业链环节）、`belongs_to`（服务机构到产业）、`service_provide`（服务机构到企业）。写明谁写图、写哪个 space。GDF 不直写图库。

WBS-06-15 仍是贴源加 Mapping 到 ADS 的实施叶。本叶的说明给它当输入，不新建派单包，不建 GDF 作业，不执行建表，不写可对端。

## 完成

handoff：`agent-delivery/agent-handoffs/SYSINT-06-21-L01.md`。定义任务，不写联调通过。
