# DATA-SUPPLIER-Q-POLICY-L01 · 政策维 — 三方问题清单按日结构 + sidecar

> 定义·文档叶。把政策现稿改成「现行待回复 + 按日日志」，用 35 条 kit 回看挂 metric、缺列才补问法，sidecar 回填卡住的指标。未改 seed、未改 D3 枚举、未写业务仓代码、未 live 再探库、未改进度导出脚本。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 父会话已认领并开工；本叶不重复认领、不把状态改成 integration/done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | N/A（定义·文档类） |
| 说明 | 定义类任务不压文档完整性。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓文档，未走 Headroom。 |

## 范围与实现

对照派单包 `DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md` §0–§6、`question/README.md` 与 `/goal`：

1. `POLICY-SUPPLIER-QUESTIONS.md` 改为「现行待回复」滚动表 + 「分析日志」`## 2026-09-01`。
2. 保留原 11 条抽样结论；Q-id 改为 `POLICY-P0-1`…`POLICY-P2-3`。
3. MCP `metric-query` domain=POLICY `fields=full` 回看 35 条；按入站 `dwd_*` 表.列聚类挂 metric；二次/CMS-only 跳过。
4. sidecar upsert 25 条卡住的 metric_id（`as_of=2026-09-01`，`domain=POLICY`，`summary`≤80 字）。
5. 未把 QPOL-01 等甲方题写成供应方题；未问 `related_entities`。

## DoD 对照

| 项 | 结果 |
|----|------|
| POLICY-SUPPLIER-QUESTIONS.md 改为「现行待回复 + 按日日志」，保留 2026-09-01 抽样结论 | ✅ 11 题保留；日志写清类型计数与抽样 |
| 用方法回看政策 seed STAT/COMPUTE/GRAPH/MODEL，补题不另开文件 | ✅ 35 条 kit；缺列只在 P1-1 写明无 pedigree，未新开文件 |
| sidecar upsert 本批 metric_id summary≤80 字 | ✅ 25 条；同一 q_id 多 metric |
| MIXED 跳过；不问 related_entities/甲方 Q；不改 seed/不改绿 D3 | ✅ MIXED=0；QPOL 仍甲方；备注明确不发 related_entities |
| handoff + cost | ✅ 见下 |

## 偏离说明

无。未改 `export_feishu_metric_board.py`（PROGRESS-L01）。未 live 再探库（沿用现稿 2026-09-01 抽样）。

## 产物清单

- `agent-delivery/data/third-party-source/question/政策维度/POLICY-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/政策维度/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`（POLICY 25 条）
- 本 handoff

## 验收证据

- 现行表 11 行 Q-id：`POLICY-P0-1`…`POLICY-P0-4`、`POLICY-P1-1`…`POLICY-P1-4`、`POLICY-P2-1`…`POLICY-P2-3`。
- 分析日志：STAT 12 / COMPUTE 1 / GRAPH 4 / MODEL 18；入站 47050 行 `dwd_policy_base`；验收 live `gkx`。
- 跳过二次 5 + CMS-only 2；TIMESERIES / NATIONAL_DIST / SZ_DIST 列已在 DDL、未另开题。
- sidecar `metrics` 25 keys，非空对象。
- 未触碰 seed / 矩阵 YAML / 业务仓 / 导出脚本。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未写 Java/Python 算法 |
| 2 调用链 | ✅ 未越层 |
| 3 图谱 NebulaGraph | ✅ GRAPH 只问入站稳定码/引用 id；未引入 Neo4j |
| 4 可观测性 | N/A（文档叶） |
| 5 CI/CD | skip / 未 push（文档仓） |
| 6 demo2 merge | ✅ 未 merge 进 lumen |
| 7 共享聚合 | ✅ 未改 Java、未直连 nGQL |
| 8 数据策略 | ✅ 只问入站 `dwd_*`；未伪 full |
| 9 D8 | N/A |
| 10 D9 | ✅ sidecar ≠ 8 件套；D3 ≠ 8 件套；未改 D3 枚举 |
| 11 D10 | N/A |
| 12 D12 | ✅ 未调 demo 服务、未写业务仓 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ~55000（估：35 条 kit + 细稿回看 + 清单改写；非整会话精确计数） |
| model_used | Cursor Grok 4.6 |
| actual_cost | ~0.25 USD（文档叶档粗算；Grok 4.6 未列入 `budget-estimate.md` pricing 表） |
| cost_warn | green |

## CI/CD（必填）

- 分支：`dev`（编排仓；本叶按指令 **未 commit / 未 push**）
- commit：无
- pipeline URL / ID：skip（设计/文档）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/data/third-party-source/question/政策维度/POLICY-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/政策维度/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`
- 本文件

## 遗留风险 / 开放项

- 算法库叶 kit 仍 `pending_ods` / `pending_cosign`：入参列主要来自已落地 calc-logic + 入站 DDL + 2026-09-01 抽样，不是 8 件套 formula。
- sidecar 25 条；二次/CMS-only 与无抽样缺口的 3 条 STAT 不进索引，进度表那些行仍回落 `d3_gap`（PROGRESS 接线后）。
- 父会话收口：本叶不 `task-update-status` 到 integration/done。
