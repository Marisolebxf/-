# DS-ALGO-GAP-L02 · 展示 vs 算法库差集（A1 成品表回填）

> 格式参考 `templates/handoff-template.md`。spike / 定义类，不写业务代码。  
> **L02**：对照已签收 A1 表1/表2 回填 mapped 的 A1 ID。不覆盖 L01 四人套。消费专题 L02 missing 7 条，不重列。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | A1 对照回填。L01 冻结为 Round 18 指针快照。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义·差集回填；对照清单与 handoff 必须完整。未用 YAGNI 跳过 D8/D9/D10、可观测、架构铁律（本叶无业务代码）。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | A1 表2 / L01 yaml / 专题 L02 结论读原文，禁止 compress 代替精读。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改架构/存储流图 |
| 会签态 | N/A（定义·差集回填） |

## missing 旧→新

**70 → 70。** 改判定行：**无。**

对照 A1 表1 97 叶复判后，L01 主清单 70 条仍无专叶。禁止用相邻叶 / seq 116 图谱 API / 区域指数顶替。专题 7 条不重列；`M_POLICY_INDUSTRY_FIT` 仅 also_in。

## mapped 回填

204 行 mapped 全部写入列 12 `A1需规ID` 与列 13 `A1指标叶ID`（含 `TEMP_ALGO_*`）。  
列 14 `metric_id` 保留语义层/B 轨已有 ID；不把 `TEMP_ALGO_*` 写入列 14；不编造正式 `M_*`。

门户 6 条 B 轨小节名（`#产业市场规模` 等）不是表1 标题，落到 `ALGO-CHAIN-BASE-95` / `TEMP_ALGO_ALGO-CHAIN-BASE-95_1`。

third_party 16 条中 14 条已填；`DS-CHAIN-OV-009/010` 投融资保持 third_party、A1 ID 空（缺口说明禁止改 mapped）。

## 范围与实现

- 真源（只读）：A1 表1 97 + 表2 101；专题 L02 missing 7。
- 底稿：`DS-ALGO-GAP-L01.yaml` + catalog/pages。L02 只加列或补字段。
- 不覆盖 `DS-ALGO-GAP-L01.*`。不改 seed / 矩阵 / 业务代码。
- Round 18 OPEN 指针未回滚。DS-13～16 仍缺 OPEN，未改挂 `TOPIC-TALENT`。

## 偏离说明

- A1 表2 对多数非企业叶只有 1 条 `TEMP_ALGO_*`，一叶多 KPI 共用同一 A1指标叶ID。
- xlsx「清单」在 schema 15 列后附 `row_id` / `page_id`。
- catalog 头仍标 Round 18；L02 只给 pages 补 A1 字段。

## 产物清单

- `metrics/request/展示系统/DS-ALGO-GAP-L02.yaml`
- `metrics/request/展示系统/DS-ALGO-GAP-L02.xlsx`
- `metrics/request/展示系统/DS-ALGO-GAP-L02-summary.md`
- 本文件
- pages：补 A1 字段；`metric_open_status` 未改
- `agent-handoffs/算法库联调-ALGO-LIB/DS-ALGO-GAP-L02.md`

## 验收证据

- yaml/xlsx 同行：930 行；mapped 204 / missing items 71 / 主清单 70 / third_party 16 / other_system 336 / n/a_ops 303。与 L01 列 11 **零判定差**。
- mapped 204/204 已填 A1需规ID 与 A1指标叶ID。列 14 无 `TEMP_ALGO_*`。未编造 `M_*`。
- missing 70→70；改判定行 0。
- DS-13～16 catalog 仍 missing。L01 四人套未被覆盖。
- **cicd: skip**。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本叶无算法代码 |
| 调用链 前端→Java→Python `/internal/*` | ✅ 未越层、未写接口 |
| 图谱 Nebula，禁止 Neo4j | ✅ 未改图谱 |
| 可观测 | ✅ 无业务代码 |
| CI/CD | ✅ skip（定义·文档） |
| 共享聚合 / ADS | ✅ 未改 Java/前端 |
| D8 Design | ✅ 无 UI |
| D9 8 件套 | ✅ 不发明正式 `M_*` 进 seed；`TEMP_ALGO_*` 只进列 13 |
| D10 交互规范 | ✅ 无 UI |
| D12 demo/lumen 隔离 | ✅ 只改编排仓 |

## CI/CD（必填）

- 分支：编排仓 `dev`（本叶未要求 commit / push）
- commit：无
- pipeline URL / ID：N/A
- 部署：N/A
- **cicd: skip**

## 可观测性

- N/A（无服务、无埋点变更）

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 160000（估；source: session_estimate，非 console_precise） |
| model_used | grok-4.6 |
| actual_cost | 0.96 |
| cost_warn | green |
| 口径 | algorithm 默认 in/out 75/25；价表按 B 主力 Sonnet $3 / $15 per M：`160000×(0.75×3+0.25×15)/1e6=0.96` |

## 遗留风险 / 开放项

- 库 missing 70 条仍待 T0-X 四桶会，不在本叶开工。
- 投融资两行 third_party 无 A1 ID。
- `TEMP_ALGO_*` 入 seed 走 B 轨 / `SEED-TYPE-L01`，本叶不假装已入库。
- 父单 `TOPIC-DS-METRIC-GAP-L01` 本会话同步收口索引。
