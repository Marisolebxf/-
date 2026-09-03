# DATA-SUPPLIER-Q-ENT-L01 · 企业维 — 从细稿/指标抽三方问题

> 定义·文档叶。回收 COVER-STAT 细稿缺口，按入站 `dwd_*` 表.列聚类成企业维现行待回复 + 一日日志 + sidecar。未改 seed、未改 D3 枚举、未写业务仓代码、未 live 再探库。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 监管人确认「认领ent」后 MCP claim → in_progress。 |

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

对照派单包 `DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md`、`question/README.md` 与 COVER-STAT 细稿 `metrics/calc-logic/ENT/`：

1. `ENT-SUPPLIER-QUESTIONS.md` 写成「现行待回复」滚动表 + 「分析日志」`## 2026-09-01`。
2. 11 题按入站 `dwd_*` 列聚类（P0×7 / P1×3 / P2×1）；draft 标「随口径修订」。
3. sidecar upsert 25 条卡住的 STAT 原料 `metric_id`（`as_of=2026-09-01`，`domain=ENT`，`summary`≤80 字）。
4. MIXED / 二次 `<- metric:` / CMS-only / 甲方 Q-* / `related_entities` / 项目 DWD·ADS 不进对外清单。
5. 未改 seed、未改绿 D3。

## DoD 对照

| 项 | 结果 |
|----|------|
| 回收 COVER-STAT 细稿缺口，按 `dwd_*` 表.列聚类成企业维现行待回复 | ✅ 11 题；见 ENT-SUPPLIER-QUESTIONS.md |
| 追加一日分析日志；sidecar upsert；draft 标「随口径修订」 | ✅ `## 2026-09-01`；sidecar 25 条 ENT |
| 本批 STAT/COMPUTE 为主，MIXED 跳过；不问 related_entities/甲方 Q | ✅ COMPUTE 二次不另开题；MIXED 跳过 |
| 不改 seed、不改绿 D3 | ✅ |
| handoff + cost | ✅ 见下 |

## 偏离说明

无范围偏离。本叶未再探库（沿用细稿 2026-08-27～31 live `gkx` 探针）。`metric-registry` 本会话不可用，D1 快照记 n/a，未打开 seed/矩阵 YAML。`M_ENT_PATENT_GRANT_COUNT` sidecar 挂 P0-6（名称→码）；授权枚举在 P1-1，进度表只显示一条 summary。

2026-09-03 订正（监管人确认，不扩范围）：ENT-P0-3 不再把 `dwd_org_sc_info` 写成证照；ENT-P1-4 问句去掉项目 DWD 加宽。

## 产物清单

- `agent-delivery/data/third-party-source/question/企业维度/ENT-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/企业维度/README.md`
- `agent-delivery/data/third-party-source/question/README.md`（企业目录行）
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`（ENT 25 条）
- 本 handoff

## 验收证据

- 现行表 11 行 COVER-STAT 题 + 补题 `ENT-P1-4`（无 metric_id，不进 sidecar）。
- 分析日志：`2026-09-01` 首批、`2026-09-02` P1-4、`2026-09-03` P0-3/P1-4 问句订正。
- sidecar `domain: ENT` 25 keys；`summary` 均 ≤80 字；`M_ENT_SUPPLIER_COUNT` as_of=2026-09-03。
- 未触碰 seed / 矩阵 YAML / 业务仓 / 导出脚本。
- 会签通过：监管人 `human:徐滕强` 2026-09-03 确认内容可对外（先用订正后的 P0-3，勿发「证照」旧句）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未写 Java/Python 算法 |
| 2 调用链 | ✅ 未越层 |
| 3 图谱 NebulaGraph | ✅ 未引入 Neo4j |
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
| actual_tokens | 48000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 0.8 |
| cost_warn | green |

## CI/CD（必填）

- 分支：`origin/dev`
- commit：`8fe86d14`（首批清单+sidecar）；`41855e2f`（P1-4）；本轮订正另记
- pipeline URL / ID：skip（设计/文档，无业务 CI）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/data/third-party-source/question/企业维度/ENT-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/企业维度/README.md`
- `agent-delivery/data/third-party-source/question/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`
- 本文件

## 遗留风险 / 开放项

- 探针日期为 2026-08-27～31，对方回复前行数可能漂移（资讯表已在 P1-2 点名）。
- 淮政玮 / 郭万迎汇总对外前勿单独改 D3。
- 编排仓文档尚未 commit。
