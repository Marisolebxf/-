# DATA-SUPPLIER-Q-CHAIN-L01 · 产业链维 — 从指标抽三方问题

> 定义·文档叶。按入站 `dwd_*` 表.列聚类成产业链维现行待回复 + 一日日志 + sidecar。未改 seed、未改 D3 枚举、未写业务仓代码。首批 cap 20；定义类，无 ponytail 行。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:李伟` |
| claim_type | `pull` |
| 说明 | 进度表专题维度 Owner=李伟；2026-09-02 认领 → `in_progress` 后按 `gkx-supplier-q-daily` 跑首批。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | N/A（定义·文档类） |
| 说明 | 派单包：definition **禁止** ponytail 行。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓文档 + 只读探库，未走 Headroom。 |

## 范围与实现

对照派单包 `DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md`、`question/README.md` 与 `gkx-supplier-q-daily`（当日 cap 20）：

1. 新建 `CHAIN-SUPPLIER-QUESTIONS.md`：现行待回复 7 题 + 分析日志 `## 2026-09-02`；`human:李伟` 点头后落盘现行表。
2. 本维题：`CHAIN-P0-1`（缺上下游/`position`）、`CHAIN-P0-2`（缺 `dwd_org_industry_chain_dtl`）、`CHAIN-P0-3`（INB 链/环节 VID）、`CHAIN-P0-4`（缺资讯 `heat_score`）、`CHAIN-P1-1`（缺链–专利表）、`CHAIN-P1-2`（资讯 `industry_code` JSON）、`CHAIN-P2-1`（`is_deleted` 过滤）。
3. 跨维复用、不重复开号：`ENT-P0-2` / `ENT-P2-1` / `ENT-P0-6`；sidecar 中 4 条 MODEL `q_id` 指向 `ENT-P0-2`。
4. sidecar upsert 20 条（`as_of=2026-09-02`，`domain=CHAIN`，`summary`≤80 字）。
5. live `gkx` 只读探针（`is_deleted=0`）：`dwd_industry_chain_info`=1273；`dwd_org_industry_tags`=19029；`dwd_industry_chain_news_info`=12291；确认无 `dwd_org_industry_chain_dtl` / `dwd_org_industry_chain_pat_dtl`。
6. MIXED / 甲方 QC01–QC11·Q053 / 项目 ADS·Nebula / `pending_cosign` DEEP·BASE（等唐绍祖入参）不进对外清单。
7. 未改 seed、未改绿 D3。

## DoD 对照

| 项 | 结果 |
|----|------|
| 产出产业链维现行待回复 + 至少一日日志 + sidecar 概要 | ✅ 7 题；`## 2026-09-02`；sidecar 20 |
| 按入站 `dwd_*` 聚类；GRAPH 只问 INB/稳定码；MIXED 跳过 | ✅ |
| `/goal` 本批 metric_id 清单不超范围 | ✅ cap 20 |
| 不改 seed、不改绿 D3；不问甲方 Q | ✅ |
| handoff + cost | ✅ 见下 |

## 偏离说明

无范围偏离。本叶按 Owner 确认收口 **首批** handoff；CHAIN 域其余指标（含 DEEP/BASE/`pending_cosign`）未扫完，续跑另开日切或另叶，**不**把全库 99+ 条一次做完。

## 产物清单

- `agent-delivery/data/third-party-source/question/产业链维度/CHAIN-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/产业链维度/README.md`
- `agent-delivery/data/third-party-source/question/README.md`（产业链目录行）
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`（CHAIN 20 条）
- 本 handoff

## 验收证据

- 现行表 7 行：`CHAIN-P0-1` … `CHAIN-P2-1`。
- 分析日志含本批 20 metric_id、跳过清单、跨维复用、live 行数。
- sidecar `domain: CHAIN` 20 keys；其中 4 条 `q_id=ENT-P0-2`；`summary` 均 ≤80 字。
- 未触碰 seed / 矩阵 YAML / 业务仓 / 导出脚本。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未写 Java/Python 算法 |
| 2 调用链 | ✅ 未越层 |
| 3 图谱 NebulaGraph | ✅ GRAPH 只问入站 INB/稳定码；禁名称猜点 |
| 4 可观测性 | N/A（文档叶） |
| 5 CI/CD | skip / 文档仓 |
| 6 demo2 merge | ✅ 未 merge 进 lumen |
| 7 共享聚合 | ✅ 未改 Java、未直连 nGQL |
| 8 数据策略 | ✅ 只问入站 `dwd_*`；只读 live `gkx` |
| 9 D8 | N/A |
| 10 D9 | ✅ sidecar ≠ 8 件套；未改 D3 枚举 |
| 11 D10 | N/A |
| 12 D12 | ✅ 未调 demo 服务、未写业务仓 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000 |
| model_used | Cursor Grok 4.5 |
| actual_cost | 1.60 |
| cost_warn | green |

## CI/CD（必填）

- 分支：`dev`（编排仓）
- commit：本 handoff 落盘时未要求 push
- pipeline URL / ID：skip（设计/文档）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A（文档 + 只读探库）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A

## 涉及文件

- `agent-delivery/data/third-party-source/question/产业链维度/CHAIN-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/产业链维度/README.md`
- `agent-delivery/data/third-party-source/question/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`
- 本文件

## 遗留风险 / 开放项

- DEEP/BASE/`GRAPH_102_1`/`103_1`/`GLOBAL_CASE_MATCH` 等 `pending_cosign`：等唐绍祖入参清单后再问。
- CHAIN 域其余未进本批的指标：续日 `gkx-supplier-q-daily` 或另叶。
- 对方书面回复前，以 live 抽样 + 映射明细为准；`position` 缺口与 Q053（INB 已冻）勿混成甲方口径题。
