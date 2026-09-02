# DATA-SUPPLIER-Q-SVC-L01 · 服务机构维 — 从指标抽三方问题

> 定义·文档叶。按入站 `dwd_*` 表.列聚类成产业服务维现行待回复 + 一日日志 + sidecar。未改 seed、未改 D3 枚举、未写业务仓代码、未 live 探库。定义类，无 ponytail 行。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:侯佳伟` |
| supervised_by | `human:侯佳伟` |
| claim_type | `pull` |
| 说明 | 2026-09-01 已认领并 push；本叶开工转 `in_progress`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | N/A（定义·文档类） |
| 说明 | 派单包：definition **禁止** ponytail 行。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓文档，未走 Headroom。 |

## 范围与实现

对照派单包 `DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md`、`question/README.md` 与 `gkx-supplier-q-daily`（当日 cap 20）：

1. `SVC-SUPPLIER-QUESTIONS.md` 写成「现行待回复」+ 分析日志 `## 2026-09-02`。
2. 本维独有 4 题：`SVC-P0-1`（高校/院所码）、`SVC-P0-2`（从业人数）、`SVC-P1-1`（服务–服务边）、`SVC-P1-2`（成立日/首次服务）。
3. 区划 / INB 环节 / 主键跟企业维 `ENT-P0-1` / `ENT-P0-2` / `ENT-P2-1`，不在 SVC 现行表重复开号；sidecar 仍 upsert，`q_id` 指向 ENT。
4. sidecar upsert 20 条（`as_of=2026-09-02`，`domain=SVC`，`summary`≤80 字）。
5. MIXED / CMS-only / UNKNOWN 旧 ID / 甲方 Q-SVC-* / Q-SVCCHAIN-* / 项目 ADS 不进对外清单。
6. 未改 seed、未改绿 D3。MODEL 18 条与 GRAPH 112/113 留待下一批。

## DoD 对照

| 项 | 结果 |
|----|------|
| 按 `dwd_*` 表.列聚类成本维现行待回复 | ✅ 4 题；跨维 3 题复用 ENT |
| 追加一日分析日志；sidecar upsert；draft 标「随口径修订」 | ✅ `## 2026-09-02`；sidecar 20 条 SVC |
| 本批 STAT/GRAPH；MIXED 跳过；不问 related_entities/甲方 Q | ✅ |
| 不改 seed、不改绿 D3 | ✅ |
| handoff + cost | ✅ 见下 |

## 偏离说明

无范围偏离。本叶未探库（无 `gkx-mysql-raw/.env.local`）。`metric-registry` MCP 本会话未挂载，改用与 MCP 同文的 `scripts/lib/metric-registry-lib.mjs` `queryMetrics`（未打开 seed/矩阵 YAML 作答）。叶未标 `done`（MODEL 批次未做）。

## 产物清单

- `agent-delivery/data/third-party-source/question/服务机构维度/SVC-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/服务机构维度/README.md`
- `agent-delivery/data/third-party-source/question/README.md`（服务机构目录行）
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`（SVC 20 条）
- 本 handoff

## 验收证据

- 现行表 4 行：`SVC-P0-1` `SVC-P0-2` `SVC-P1-1` `SVC-P1-2`。
- 分析日志含跳过清单与跨维复用表。
- sidecar `domain: SVC` 20 keys；`summary` 均 ≤80 字。
- 未触碰 seed / 矩阵 YAML / 业务仓 / 导出脚本。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未写 Java/Python 算法 |
| 2 调用链 | ✅ 未越层 |
| 3 图谱 NebulaGraph | ✅ GRAPH 只问入站稳定码；禁名称猜点 |
| 4 可观测性 | N/A（文档叶） |
| 5 CI/CD | skip / 文档仓 |
| 6 demo2 merge | ✅ 未 merge 进 lumen |
| 7 共享聚合 | ✅ 未改 Java、未直连 nGQL |
| 8 数据策略 | ✅ 只问入站 `dwd_*` |
| 9 D8 | N/A |
| 10 D9 | ✅ sidecar ≠ 8 件套；未改 D3 枚举 |
| 11 D10 | N/A |
| 12 D12 | ✅ 未调 demo 服务、未写业务仓 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 72000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 1.20 |
| cost_warn | green |

## CI/CD（必填）

- 分支：`dev`（编排仓）
- commit：本 handoff 落盘时未要求 push
- pipeline URL / ID：skip（设计/文档）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A

## 涉及文件

- `agent-delivery/data/third-party-source/question/服务机构维度/SVC-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/服务机构维度/README.md`
- `agent-delivery/data/third-party-source/question/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`
- 本文件

## 遗留风险 / 开放项

- 无 live 空值率；对方回复前以细稿/ENT 探针为准。
- MODEL 18 + `M_SVC_GRAPH_112_1` / `113_1` 未进本批（cap 20）。
- 服务机构 vs 企业圈定仍是甲方 Q-SVC-001/010，未改写成供应方题。
