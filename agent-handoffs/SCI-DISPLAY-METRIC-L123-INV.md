# SCI-DISPLAY-METRIC-L123-INV · 科技信息展示系统 §1.1.1.1 原始需求指标盘点

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:王惠` |
| claim_type | `coordinator_dispatch` |
| 说明 | 定义任务；给人审后不得自行改 YAML |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |
| 说明 | 产品定义完整性优先，不以缩代码为目标 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 bid / 血缘 / calc-logic / 客户决策清单精读，禁止 compress 代替 |

## 范围与实现

- 仅展示系统 `bid-reference/科技信息展示系统和科技专题服务系统.md` **§1.1.1.1**（含 §1.1.1.1.4 七大模块）**全量**指标盘点，不限于「影响力」。
- 「影响力按要素分列」是统称拆行的**方法示例**，不是本单重点；同等规则用于创新价值、科技发展指标分维、湾区子指标等。
- 专题系统对应章 + 算法库 + ENT/POLICY/CHAIN/SYNTH/SVC/TNIE 已有 YAML 与 `calc-logic/ENT/` 只作口径引用。
- **未**注册 8 件套、**未**改 YAML、**未**写 SQL、**未**编正式 `metric_id`。
- 未把专题功能点扩进展示；未从 Demo/USM 倒推新指标。

## 偏离说明

- 无 `exact_cite`：专题已登记指标与展示原文「名称+对象」均未完全一致，一律 `analog_cite` 或 `none`。
- `POLICY`：**该域无** `metric-readiness-matrix-POLICY.yaml`（有 seed + `metric-spec-POLICY.yaml`）。
- `calc-logic/` 仅 ENT 入仓；其它域 handoff/盘点已写「无 calc-logic」。
- 科技指数分类/权重不新建决策项，沿用 `Q-TINDEX-02` / `Q-TINDEX-03`。

## 产物清单

1. `agent-handoffs/产品整体定义/科技信息展示系统-指标盘点/SCI-DISPLAY-METRIC-L123-INV.md`（七大模块覆盖 + 总表为主；§4 为统称分列方法示例；专题引用对照 + 未定义待甲方）
2. 本地 Excel（**不进仓**）：`C:\Users\25456\gkx-local-drafts\SCI-DISPLAY-METRIC-L123-INV.xlsx`（列与总表对齐，含 `d1_def_status`）
3. `agent-delivery/客户决策清单跟踪表.md` 新增 §2.ah：`Q069` `Q070` `Q071`（🟡）
4. 本 handoff

## 验收证据（对照 DoD）

- [x] 七大模块均有覆盖结论（智库/交流/传播写明原文无独立统计指标名）
- [x] 总表覆盖展示原文抽到的统计/评估指标，不以影响力为筛选
- [x] 统称类（影响力仅为示例）无单行交差；原文出现对象有分列行或显式「原文该处不涉及」
- [x] 可引用指标已查 ENT 及其它已有域；cite 三态无空
- [x] analog_cite 均有差异 + pending_ref；exact_cite 0 条故无改写专题 definition
- [x] L2/L3 无执行人自补（仅原文举例）
- [x] 给人审：`human:王惠`；本单不改 YAML

盘点行数：总表 112（主交付）；其中影响力相关 44 行仅作 §4 分列示例；analog_cite 20；missing_in_source 56。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | N/A 本文档 |
| 调用链 / Nebula / 可观测 | N/A |
| D8 Design | N/A |
| D9 8 件套 | 遵守：本单只盘点，不注册；后续 data-agent 正式化 |
| D10 | N/A |
| D12 demo/lumen | 未改业务仓 |
| 范围 ±10% | 只盘点不扩功能点 |
| 业务口径不替甲方拍板 | 新 🟡 Q069–Q071 |

## CI/CD（必填）

- 分支：`dev`（编排仓文档）
- commit：提交本 handoff / 盘点 MD / 决策清单后回填
- pipeline：`cicd: skip`（definition）
- 部署 / K8s：N/A
- 验证：文档路径存在；Excel 仅本地

## 可观测性（建议）

- N/A

## 开放项

- `Q069` 展示侧统称指标如何按原文对象分列（影响力仅为示例）及公式/对象
- `Q070` 展示创新/竞争力/投入产出等 vs 专题 analog 边界
- `Q071` 主题举例子指标与分列行是否同一计数（科学/技术影响力为该方法的一例）
- 既有：`Q014` `QPOL-02` `Q-SYNTH-*` `Q-TINDEX-02/03` `QC05`

## 下一步

王惠审过盘点稿 → coordinator 派 **data-agent** 按 `metrics/README.md` §2.1–2.2 正式化（Excel 底稿不进仓）。本单保持不改 YAML。

## 涉及文件

- `agent-handoffs/产品整体定义/科技信息展示系统-指标盘点/SCI-DISPLAY-METRIC-L123-INV.md`
- `agent-delivery/客户决策清单跟踪表.md`
- `agent-handoffs/SCI-DISPLAY-METRIC-L123-INV.md`
