# TOPIC-ALGO-GAP-L02 · 专题 vs 算法库差集（A1 成品表回填）

> 格式参考 `templates/handoff-template.md`。spike / 定义类，不写业务代码。  
> **L02**：对照已签收 A1 表1/表2 回填 mapped 的 A1 ID。不覆盖 L01 四人套。不开工展示叶。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | A1 对照回填。L01 冻结为 Round 17 指针快照。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义·差集回填；对照清单与 handoff 必须完整。未用 YAGNI 跳过 D8/D9/D10、可观测、架构铁律（本叶无业务代码）。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | A1 表2 / L01 yaml / schema 读原文，禁止 compress 代替精读。 |

## missing 旧→新

**7 → 7。** 改判定行：**无**。

A1 97 叶逐条复判后，下列能力仍无专叶，维持 missing（禁止用相邻叶充数）：

| row_id | 旧 | 新 | A1 ID |
|--------|----|----|-------|
| TOPIC-PAN-006 | missing | missing | 空（无产品计数专叶） |
| TOPIC-PAN-007 | missing | missing | 空（无链级专利计数专叶） |
| TOPIC-DIAG-018 | missing | missing | 空（瓶颈叶 ≠ 环节健康度） |
| TOPIC-SZ-016 | missing | missing | 空（无全球成功案例叶） |
| TOPIC-POL-005 | missing | missing | 空（无产业适配性叶） |
| TOPIC-ELEM-009 | missing | missing | 空（无贡献路径专叶） |
| TOPIC-COL-006 | missing | missing | 空（191 未列产出相关） |

## mapped 回填

171 行 mapped 全部写入 `A1需规ID`（表1 `requirement_id`）与 `A1指标叶ID`（表2 `metric_id`，含 `TEMP_ALGO_*`）。  
列 14 `metric_id` 保留语义层/B 轨已有 ID；不把 `TEMP_ALGO_*` 写入列 14；不编造正式 `M_*`。

特例（无页面 `algo_lib_leaf`，仍 mapped）：

| row_id | A1需规ID | A1指标叶ID | 理由 |
|--------|----------|------------|------|
| TOPIC-SZ-011～014 | `ALGO-CHAIN-DEEP-118` | `TEMP_ALGO_ALGO-CHAIN-DEEP-118_1` | 深圳四维对比；B 轨已有，对 深圳产业链模型叶 |
| TOPIC-PT-006 | `ALGO-SVC-DEEP-174` | `TEMP_ALGO_ALGO-SVC-DEEP-174_1` | 门户复用 ORG-ANALYSIS 同 metric_id |
| TOPIC-PT-012 | `ALGO-SVC-BASE-101` | `TEMP_ALGO_ALGO-SVC-BASE-101_1` | 同上 |

third_party 10 条中 9 条已填；`TOPIC-RORG-012` 科研机构技术力无对应叶，ID 空（不是 missing）。

## 范围与实现

- 真源：A1 表1 97 + 表2 101。底稿 L01 yaml/catalog/pages，只加列或补字段。
- 不覆盖 `TOPIC-ALGO-GAP-L01.*`。不改 seed / 矩阵。不回滚 OPEN 指针。
- 未开工 `DS-ALGO-GAP-L02`。

## 偏离说明

- A1 表2 对多数非企业叶只有 1 条 `TEMP_ALGO_*`，一叶多 KPI 共用同一 A1指标叶ID。
- 深圳 `#深圳产业要素` / `#深圳产业分布` 别名落到 `ALGO-CHAIN-BASE-95`。

## 产物清单

- `metrics/request/专题系统/TOPIC-ALGO-GAP-L02.yaml` / `-summary.md` / `.xlsx` / 本文件
- catalog / pages：补 `A1需规ID` / `A1指标叶ID`；`metric_open_status=present` 未改
- `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-ALGO-GAP-L02.md`

## 验收证据

- missing 7→7；mapped 171/171 已填 A1需规ID。
- 列 14 无 `TEMP_ALGO_*`。未编造 `M_*`。
- OPEN 指针 18 present 未回滚。L01 四人套未改。
- **cicd: skip**。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本叶无算法代码 |
| 调用链 | ✅ 未越层 |
| Nebula | ✅ 未改图谱 |
| D9 不发明正式 `M_*` 进 seed | ✅ |
| CI/CD | ✅ skip |
| D12 | ✅ 只改编排仓 |

## CI/CD（必填）

- 分支：编排仓 `dev`（本叶未要求 commit）
- **cicd: skip**

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 140000（估） |
| model_used | grok-4.6 |
| actual_cost | 0.84 |
| cost_warn | green |

正式 handoff：`agent-handoffs/算法库联调-ALGO-LIB/TOPIC-ALGO-GAP-L02.md`。
