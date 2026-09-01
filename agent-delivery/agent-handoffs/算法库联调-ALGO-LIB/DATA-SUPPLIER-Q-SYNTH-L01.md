# DATA-SUPPLIER-Q-SYNTH-L01 · 综合维 SYNTH — 从指标抽三方问题

> 定义·文档叶。先拆跨维依赖（ENT/CHAIN/POLICY/久新不重问），再出综合维现行待回复 + 一日日志 + sidecar。未改 seed、未改 D3 枚举、未写业务仓代码、未 live 再探库。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 监管人确认「继续综合维」后 MCP claim → in_progress。 |

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

对照派单包 `DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md`、`question/README.md` 与 ENT 已交清单：

1. `SYNTH-SUPPLIER-QUESTIONS.md` 写成「现行待回复」滚动表 + 「分析日志」`## 2026-09-01`（含跨维依赖表）。
2. 8 题只问综合域独有入站：合作边、参与机构 JSON、人才流动缺表、联合专利多权利人、区域资金/空间、GRAPHAPI 落表。
3. third_party 问落表+主键（P1-3）；MODEL 只问入参键（协同边、资金/空间）；MIXED seq 182–191 跳过。
4. sidecar upsert 12 条卡住的 SYNTH `metric_id`（`as_of=2026-09-01`，`domain=SYNTH`，`summary`≤80 字）。
5. 未改 seed、未改绿 D3。

## DoD 对照

| 项 | 结果 |
|----|------|
| 先拆跨维依赖（吃 ENT/CHAIN 上游的不重问）再出题 | ✅ 区划码/INB/专利码走 ENT；政策走 POLICY；人才/机构走久新；链目录走 CHAIN |
| 产出综合维（SYNTH）现行待回复 + 一日日志 + sidecar | ✅ 8 题；`## 2026-09-01`；sidecar 12 条 |
| third_party 问落表+主键；MODEL 只问入参键；MIXED 跳过 | ✅ P1-3；P0/P1 入参键；182–191 跳过 |
| 不改 seed、不改绿 D3 | ✅ |
| handoff + cost | ✅ 见下 |

## 偏离说明

无范围偏离。入站依据 = `gkx_schema_ddl.sql` + METRIC-OPEN，未探库行数。sidecar 一 metric 一 `q_id`：P0-2 / P0-3 / P2-1 的卡住指标与 P0-1 同批（`RELATION_INPUT` 等），未再拆行；`M_SYNTH_VIT_*` 入参全是跨维，sidecar 未挂，进度表那些行仍回落 `d3_gap`。DS-21/23 无入站 `dwd_*`，未编造题。

## 产物清单

- `agent-delivery/data/third-party-source/question/综合维度/SYNTH-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/综合维度/README.md`
- `agent-delivery/data/third-party-source/question/README.md`（综合目录行）
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`（SYNTH 12 条）
- 本 handoff

## 验收证据

- 现行表 8 行 Q-id：`SYNTH-P0-1`…`SYNTH-P0-4`、`SYNTH-P1-1`…`SYNTH-P1-3`、`SYNTH-P2-1`。
- 分析日志写明跨维不重问与 MIXED/二次 RANK/甲方权重跳过。
- sidecar `domain: SYNTH` 12 keys；`summary` 均 ≤80 字。
- 未触碰 seed / 矩阵 YAML / 业务仓 / 导出脚本。
- 会签通过：综合维供应方问题清单可对外转发（定义叶，无前后端联调代码）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未写 Java/Python 算法 |
| 2 调用链 | ✅ 未越层 |
| 3 图谱 NebulaGraph | ✅ GRAPHAPI 只问是否有入站快照；未引入 Neo4j、未请对方 hang |
| 4 可观测性 | N/A（文档叶） |
| 5 CI/CD | skip / 未 push（文档仓） |
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
| actual_tokens | 42000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 0.7 |
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

- `agent-delivery/data/third-party-source/question/综合维度/SYNTH-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/综合维度/README.md`
- `agent-delivery/data/third-party-source/question/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`
- 本文件

## 遗留风险 / 开放项

- 项目–机构关联表是否「一项目多机构」未用 live COUNT 验证。
- 编排仓文档尚未 commit。
