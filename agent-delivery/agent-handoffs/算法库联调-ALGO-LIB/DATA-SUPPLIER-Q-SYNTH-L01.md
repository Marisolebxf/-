# DATA-SUPPLIER-Q-SYNTH-L01 · 综合维 SYNTH — 从指标抽三方问题

> 定义·文档叶。先拆跨维依赖（ENT/CHAIN/POLICY 不重问；科研机构挂 SYNTH-P0-5，不等 ORG-P0-1），再出综合维现行待回复 + 按日日志 + sidecar。未改 seed、未改 D3 枚举、未写业务仓代码、未 live 再探库。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 2026-09-01 开工；2026-09-02 改挂科研机构；2026-09-03 监管人「synth继续做」续切。 |

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

1. `SYNTH-SUPPLIER-QUESTIONS.md`：现行待回复滚动表 + 日志 `## 2026-09-01` / `09-02` / `09-03`。
2. 对外 10 题：合作边、参与机构 JSON、人才流动缺表、联合专利多权利人、科研机构类型码、区域资金/空间、GRAPHAPI 落表、**展示侧图谱分析/算法结果落表（P1-4）**、项目–学者主键。
3. third_party 问落表+主键（P1-3 / P1-4）；MODEL 只问入参键或复用跨维题；MIXED 182–191 与 `ELEM_CONTRIB` 跳过。
4. sidecar：`domain=SYNTH` **31** 条（12 协同/要素/GRAPHAPI + 14×P1-4 + 2 要素复用 + 3 活力跨维）。`summary`≤80 字。
5. 未改 seed、未改绿 D3。

## DoD 对照

| 项 | 结果 |
|----|------|
| 先拆跨维依赖（吃 ENT/CHAIN 上游的不重问）再出题 | ✅ 区划码/INB/专利码走 ENT；政策走 POLICY；链目录走 CHAIN；科研机构 SYNTH-P0-5；人才专题不开口 |
| 产出综合维（SYNTH）现行待回复 + 一日日志 + sidecar | ✅ 10 题；三日日志；sidecar 31 |
| third_party 问落表+主键；MODEL 只问入参键；MIXED 跳过 | ✅ P1-3/P1-4；入参键或跨维复用；182–191 + CONTRIB 跳过 |
| 不改 seed、不改绿 D3 | ✅ |
| handoff + cost | ✅ 见下 |

## 偏离说明

无范围偏离。入站依据 = kit `source_tables` + DDL/METRIC-OPEN，未探库行数。sidecar 一 metric 一 `q_id`：活力三条挂 `ENT-P0-1`（跨维原料，综合不另开列）；领域指数挂 `ENT-P0-2`。DS-21/23 十四条共挂 P1-4（同一类缺表 `pending_ods`）。二次 RANK / 甲方权重无 sidecar。

## 产物清单

- `agent-delivery/data/third-party-source/question/综合维度/SYNTH-SUPPLIER-QUESTIONS.md`
- `agent-delivery/data/third-party-source/question/综合维度/README.md`
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`（SYNTH 31 条）
- 本 handoff

## 验收证据

- 现行表 10 行：`SYNTH-P0-1`…`P0-5`、`P1-1`…`P1-4`、`P2-1`。
- 分析日志写明跨维不重问与 MIXED/二次 RANK/甲方权重跳过。
- sidecar `domain: SYNTH` 31 keys；`summary` 均 ≤80 字。
- 未触碰 seed / 矩阵 YAML / 业务仓 / 导出脚本。
- 会签通过：综合维供应方问题清单可对外转发（先用含 P1-4 的现行表）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未写 Java/Python 算法 |
| 2 调用链 | ✅ 未越层 |
| 3 图谱 NebulaGraph | ✅ GRAPHAPI / DS 只问是否有入站快照；未引入 Neo4j、未请对方 hang |
| 4 可观测性 | N/A（文档叶） |
| 5 CI/CD | skip（设计/文档） |
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
| actual_tokens | 78000 |
| model_used | grok-4.6 |
| actual_cost | 1.15 |
| cost_warn | green |

## CI/CD（必填）

- 分支：`origin/dev`
- commit：`8fe86d14`（首批）；`79637409`（P0-5）；本轮 2026-09-03 P1-4 另记
- pipeline URL / ID：skip（设计/文档，无业务 CI）
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
- `agent-delivery/data/third-party-source/question/source-gap-index.yaml`
- 本文件

## 遗留风险 / 开放项

- 项目–机构关联表是否「一项目多机构」未用 live COUNT 验证。
- MIXED 182–191 / `ELEM_CONTRIB` 等唐绍祖拆类型后再开题。
- 游标内可出的本波类型已切完；后续只跟供应方回复或口径修订，不扫新 cap。
