# DS-ALGO-GAP-L02 · 展示 vs 算法库差集（A1 成品表回填）

> 格式参考 `templates/handoff-template.md`。spike / 定义类，不写业务代码。  
> **L02**：对照已签收 A1 表1/表2 回填 mapped 的 A1 ID。不覆盖 L01 四人套。消费专题 L02。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | A1 对照回填。L01 冻结为 Round 18 指针快照。MCP 认领后再改文件。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义·差集回填；对照清单与 handoff 必须完整。未用 YAGNI 跳过 D8/D9/D10、可观测、架构铁律（本叶无业务代码）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | A1 表2 / L01 yaml / 专题 L02 / schema 读原文，禁止 compress 代替精读。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改架构/存储流图 |
| 会签态 | N/A（定义·差集回填） |

## missing 旧→新

**70 → 70。** 改判定行：**无。**

A1 97 叶复判后，展示主清单 70 条仍无专叶。专题 L02 missing 7 条不重列。`M_POLICY_INDUSTRY_FIT` 仅 also_in。禁止为好看改 mapped。禁止编造正式 `M_*`。

## mapped 回填

204/204 mapped 已填 `A1需规ID` / `A1指标叶ID`。列 14 无 `TEMP_ALGO_*`。  
门户 B 轨小节名落到 `ALGO-CHAIN-BASE-95`。third_party 14/16 已填；投融资两行保持空。

回填日志：`metrics/request/_work/DS-ALGO-GAP-L02-fill-log.csv`。

## 范围与实现

- 真源：A1 双表 + `TOPIC-ALGO-GAP-L02`。
- 不覆盖 `DS-ALGO-GAP-L01.*`。不改 seed / 矩阵。不回滚 OPEN。DS-13～16 未改挂人才 OPEN。

## 偏离说明

- 一叶多 KPI 共用同一 `TEMP_ALGO_*` A1指标叶ID。
- catalog 仍 Round 18；pages 只补 A1 字段。

## 产物清单

- `metrics/request/展示系统/DS-ALGO-GAP-L02.yaml` / `.xlsx` / `-summary.md` / `.md`
- pages 补 A1；catalog OPEN 未改
- 本文件

## 验收证据

- 930 行；mapped 204/204 已填 A1；missing 70→70；列 11 与 L01 零判定差。
- DS-13～16 仍 missing OPEN。未改挂 `TOPIC-TALENT`。
- **cicd: skip**。本叶未要求 commit。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 调用链 | ✅ 未越层 |
| 图谱 Nebula | ✅ |
| 可观测 | ✅ 无业务代码 |
| CI/CD | ✅ skip |
| 共享聚合 / ADS | ✅ |
| D8 / D10 | ✅ 无 UI |
| D9 | ✅ 不发明 `M_*` 进 seed |
| D12 | ✅ 只改编排仓 |

## CI/CD（必填）

- 分支：编排仓 `dev`
- commit：无
- **cicd: skip**

## 可观测性

- N/A

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 160000（估；source: session_estimate） |
| model_used | grok-4.6 |
| actual_cost | 0.96 |
| cost_warn | green |

## 遗留风险 / 开放项

- missing 70 待 T0-X。SEED-TYPE / OPEN 贴源 / GDF 不在本叶。
- 父单索引已同步写 `TOPIC-DS-METRIC-GAP-L01`。
