# TOPIC-ALGO-GAP-L02 · 专题 vs 算法库差集（A1 成品表回填）

> 格式参考 `templates/handoff-template.md`。spike / 定义类，不写业务代码。  
> **L02**：对照已签收 A1 表1/表2 回填 mapped 的 A1 ID。不覆盖 L01 四人套。不开工展示叶。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | A1 对照回填。L01 冻结为 Round 17 指针快照。MCP 认领后再改文件。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义·差集回填；对照清单与 handoff 必须完整。未用 YAGNI 跳过 D8/D9/D10、可观测、架构铁律（本叶无业务代码）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | A1 表2 / L01 yaml / schema 读原文，禁止 compress 代替精读。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改架构/存储流图 |
| 会签态 | N/A（定义·差集回填） |

## missing 旧→新

**7 → 7。** 改判定行：**无。**

对照 A1 表1 97 叶 `requirement_title` 原文复判后，下列能力仍无专叶，维持 missing（禁止用相邻叶充数）：

| row_id | 旧 | 新 | A1 ID |
|--------|----|----|-------|
| TOPIC-PAN-006 | missing | missing | 空（无产品计数专叶；BASE-95 / DEEP-117 不顶替） |
| TOPIC-PAN-007 | missing | missing | 空（无链级专利计数专叶） |
| TOPIC-DIAG-018 | missing | missing | 空（DEEP-125 瓶颈五维 ≠ 环节健康度） |
| TOPIC-SZ-016 | missing | missing | 空（无全球成功案例叶） |
| TOPIC-POL-005 | missing | missing | 空（政策 9 叶无产业适配性；185/力度/效果不顶替） |
| TOPIC-ELEM-009 | missing | missing | 空（187–190 非贡献路径；191/116 不顶替） |
| TOPIC-COL-006 | missing | missing | 空（191 未列产出相关） |

## mapped 回填

171 行 mapped 全部写入列 12 `A1需规ID`（表1 `requirement_id`）与列 13 `A1指标叶ID`（表2 `metric_id`，含 `TEMP_ALGO_*`）。  
列 14 `metric_id` 保留语义层/B 轨已有 ID；**不把 `TEMP_ALGO_*` 写入列 14**；不编造正式 `M_*`。

A1 表2 正式 `M_*` 仅 11 条且全为企业维。产业链/政策/服务/综合等 mapped 行的 A1指标叶ID 多为 `TEMP_ALGO_*`（未入 seed）。

特例（无页面 `algo_lib_leaf` 或需别名，仍 mapped）：

| row_id | A1需规ID | A1指标叶ID | 理由 |
|--------|----------|------------|------|
| TOPIC-SZ-011～014 | `ALGO-CHAIN-DEEP-118` | `TEMP_ALGO_ALGO-CHAIN-DEEP-118_1` | 深圳四维对比；B 轨已 mapped，对深圳产业链模型叶 |
| TOPIC-ENT-002 | `ALGO-ENT-BASE-97` | `M_ENT_KEY_TOTAL` | `05_seq` |
| TOPIC-ENT-007 | `ALGO-ENT-DEEP-141` | `M_ENT_COMPETITIVENESS_SCORE` | 取数依据标题对竞争力叶 |
| TOPIC-PT-006 | `ALGO-SVC-DEEP-174` | `TEMP_ALGO_ALGO-SVC-DEEP-174_1` | 门户复用 ORG-ANALYSIS 同 metric_id |
| TOPIC-PT-012 | `ALGO-SVC-BASE-101` | `TEMP_ALGO_ALGO-SVC-BASE-101_1` | 同上 |
| TOPIC-ENT-05 页面 | 可填企业维 A1 ID | 列 14 保持原 TEMP/空 | 专题页禁止消费 `M_ENT_*`；列 13 仅对照 |

别名：页面 `#深圳产业要素` / `#深圳产业分布` → `产业链基础指标模型构建`（`ALGO-CHAIN-BASE-95`）。

third_party 10 条中 9 条已填 A1 ID；**`TOPIC-RORG-012` 科研机构技术力**表1 无专叶，A1 ID 保持空（禁止改挂服务机构 174–179；不是 missing）。

回填方法计数：`algo_lib_leaf` 172；`row_override` 4；`05_seq` 1；`text_title` 1；`reuse_same_metric_id` 2。日志：`metrics/request/_work/TOPIC-ALGO-GAP-L02-fill-log.csv`。

## 范围与实现

- 真源（只读）：A1 表1 `metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-requirements.yaml`（97）+ 表2 `…-metrics.yaml`（101：11 `M_*` + 90 `TEMP_ALGO_*`）。
- 底稿：`TOPIC-ALGO-GAP-L01.yaml` + catalog/pages。L02 只加列或补字段。
- 不覆盖 `TOPIC-ALGO-GAP-L01.*`。不改 seed / 矩阵 / 业务代码。
- Round 17 OPEN 指针未回滚（catalog 18 `present`；TOPIC-OPS=`n/a_ops`；TOPIC-DATAREQ=`other_system`）。
- **未开工** `DS-ALGO-GAP-L02`。未改展示 catalog。未改挂 DS-13～16。

## 偏离说明

- A1 表2 对多数非企业叶只有 1 条 `TEMP_ALGO_*`，一叶多 KPI 共用同一 A1指标叶ID。
- xlsx「清单」在 schema 15 列后附 `row_id` / `page_id` 便于对照，不改变 1–15 列顺序。
- catalog 头仍标 `task: TOPIC-ALGO-GAP-L01` / `round: 17`（指针快照真源）；L02 只加 `a1_*` / `l02_note`。

## 产物清单

- `metrics/request/专题系统/TOPIC-ALGO-GAP-L02.yaml`
- `metrics/request/专题系统/TOPIC-ALGO-GAP-L02.xlsx`（清单 / 计数 / 回填清单）
- `metrics/request/专题系统/TOPIC-ALGO-GAP-L02-summary.md`
- `metrics/request/专题系统/TOPIC-ALGO-GAP-L02.md`
- catalog / 有 mapped 的 `pages/*.yaml`：补 A1 字段；`metric_open_status=present` 未改
- 本文件

## 验收证据

- yaml/xlsx 同行：250 行；mapped 171 / missing 7 / third_party 10 / other_system 39 / n/a_ops 23。与 L01 列 11 **零判定差**。
- mapped 171/171 已填 A1需规ID 与 A1指标叶ID。列 14 无 `TEMP_ALGO_*`。未编造 `M_*`。
- missing 7→7；改判定行 0。xlsx 计数 `B12=B5=7`。
- OPEN 指针 18 present 未回滚。L01 四人套 git 未改。无 `DS-ALGO-GAP-L02.yaml`。
- **cicd: skip**。本叶未要求 commit。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本叶无算法代码 |
| 调用链 前端→Java→Python `/internal/*` | ✅ 未越层、未写接口 |
| 图谱 Nebula，禁止 Neo4j | ✅ 未改图谱 |
| 可观测 | ✅ 无业务代码，无漏埋点 |
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
| actual_tokens | 140000（估；source: session_estimate，非 console_precise） |
| model_used | grok-4.6 |
| actual_cost | 0.84 |
| cost_warn | green |
| 口径 | algorithm 默认 in/out 75/25；价表按 B 主力 Sonnet $3 / $15 per M：`140000×(0.75×3+0.25×15)/1e6=0.84` |

## 遗留风险 / 开放项

- 库 missing 7 条仍待 OPEN 贴源 / GDF / 右框，不在本叶开工。
- 展示叶 `DS-ALGO-GAP-L02` 仍 backlog，等本叶签收后由 coordinator 升 ready。
- `TEMP_ALGO_*` 入 seed 走 B 轨 / `SEED-TYPE-L01`，本叶不假装已入库。
- 父单 `TOPIC-DS-METRIC-GAP-L01` 收口仍等 L02 两叶齐。
