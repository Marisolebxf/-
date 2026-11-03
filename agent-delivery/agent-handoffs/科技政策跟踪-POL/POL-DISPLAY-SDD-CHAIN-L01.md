# POL-DISPLAY-SDD-CHAIN-L01 · 科技政策跟踪调用链与边界

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 总控已授权。调研父单 handoff 已落盘。本叶只写调用链，不等签收 |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、自建 L3、`/display/v1` 与 Job 边界。

## 范围

写清展示政策页的调用链：前端 → `gkxlumen-display` 的 `/display/v1/policy/**` →（同步经自建 `gkxlumen-element` 读 ADS；Job 经 `gkxlumen-topic-async-service` 进入 Python `/internal/*`）。按页标明哪些区块同步读 ADS，哪些走 Job。推演与布局推荐分键。写明与专题政策、门户政策扶持、第 6 项 GDF、第 7 项读图的边界，这些范围不新开实现任务。

不写 OpenAPI 字段表、DTO、枚举。不写说明书正文。不改调研分册、WBS、注册表、lumen / demo。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/调用链与边界.md`

## L06 裁定

`E-E7-POLICY-M1-L06` 不是展示实现路径。其 DoD（展示消费 `/topic/v1/policy`）与 A1、详设第 5 卷冲突。展示七页只走 `/display/v1/policy/**`。不把该单改成展示联调单。`L07` 停在专题侧，不是展示签收门。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-DISPLAY-SDD-CHAIN-L01-SEQ` |
| 图 diff | 新增一条展示政策链：同步边到 element / ADS，Job 边到 async-service 再进 `/internal/*`。禁止边：`/topic/v1/policy`、专题 Python 门面、本叶新开的 GDF 与读图任务 |
| 会签态 | 本叶新图。源文件未见 frontmatter，记 `draft`。不自填绿 |
| 说明 | 图在产物第 1 节 |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |

## 修改内容

- 新增 `sdd/调用链与边界.md`
- 新增本 handoff

未 commit，未 push。

## 遗留

- 资源路径清单在 `POL-DISPLAY-SDD-INPUT-L01`
- 分区块 501 明细在 `POL-DISPLAY-SDD-METRIC-L01`
- 三叶齐后才由 `POL-DISPLAY-SDD-L01` 合成说明书
- `gkx_show_service` 仍是骨架。政策算法在注册前保持 501
- 第 7 项独立读图任务号：未见
