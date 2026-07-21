# 派单包：ENT-MOD-RISK-METRIC-OPEN-L01

- **派单方**：coordinator（补生成 · webhook confirm 未落盘 git）
- **时间**：2026-07-21
- **双 Agent 分工**：
  - **`algorithm-agent`**：供应链 / 痛难点 **8 个 metric** 口径、公式、DEMO 阈值与算法边界（不替甲方闭合 Q017/Q018）
  - **`data-agent`**：ODS→DWD→ADS 贴源存在性 + `pending_hint` catalog
- **监管人**：human:唐绍祖（语义 Owner 临时代行 §1.4.1）
- **Sprint**：2026-W30 stretch
- **上游**：`ENT-MOD-RISK-PACK-L01` ✅ done（核心产品包已冻结为 V1 输入）
- **confirm**：`dispatch_confirmed_by=human:唐绍祖` · trigger=`def-pack-unlock-mo-ux`

## 1. 目标

闭合 Track-MS 五件套 **#4 指标语义 + #5 开放项**，支撑风险洞察两种模式：

1. **供应链关系分析（E-28）** — ⓘ MetricSpecCard + ⚠️ PendingBadge（Q017）
2. **企业发展痛难点识别（E-29）** — 同上（Q018）

Wave0 / Demo 允许 🧪 Mock + 🟡 团队临时默认；**不得**把临时阈值写成甲方已确认。

## 2. 范围

### 2.1 TRACE 真源（关键数字）

`TRACE-ENT-RISK.yaml` v1.0：

| 项 | 值 |
|----|-----|
| `metrics_required` | **8** |
| `metrics_mapped` | **8**（均为 `registered_pending_semantic_review`） |
| `open_questions` | **Q017**、**Q018** |
| `gaps` | GAP-RISK-Q017 / GAP-RISK-Q018 / GAP-RISK-V1 |

**metric 清单**：

| metric_id | 叶子 | 开放项 |
|-----------|------|--------|
| `M_ENT_SUPPLIER_COUNT` | E-28 | Q017 |
| `M_ENT_CORE_SUPPLIER_COUNT` | E-28 | Q017 |
| `M_ENT_NODE_CENTRALITY` | E-28 | Q017 |
| `M_ENT_SUPPLY_CHAIN_RISK` | E-28 | Q017 |
| `M_ENT_RELATION_STRENGTH` | E-28 | Q017 |
| `M_ENT_PAINPOINT_COUNT` | E-29 | Q018 |
| `M_ENT_PAINPOINT_SEVERITY` | E-29 | Q018 |
| `M_ENT_PAINPOINT_GAP` | E-29 | Q018 |

**algorithm-agent**：

- 对照算法库真源（`科技专题服务算法库.md` 供应链 / 痛难点模型章节）与 PACK 四件套，写清每个 metric 的 **definition / formula / 单位 / DEMO 临时阈值**
- 明确 **前端不计算** 官方风险等级、中心性、痛难点严重度（architecture_constraints）
- Q017/Q018：登记临时默认（TRACE 已有）+ 会签栏；**不替何老师/甲方拍板正式阈值**

**data-agent**：

- 逐 metric 做 ODS→DWD→ADS 字段存在性（`gkx_schema_ddl.sql`、企业域设计 v1）
- 产出 `ENT-RISK-data-gap-catalog.yaml`（含 ≥80 字 `pending_hint`）
- 同步/引用 `客户决策清单跟踪表.md` 中 Q017、Q018

### 2.2 联合产出

| 文件 | 说明 |
|------|------|
| `METRIC-OPEN-ENT-RISK-核对记录.md` | #4/#5 适用性、指标矩阵、PDR-05/06 自检、唐绍祖会签 |
| `agent-handoffs/产品整体定义/E-28_E-29-风险洞察/ENT-RISK-data-gap-catalog.yaml` | UI 缺口文案真源 |
| `cfg_metric-ENT-seed.yaml` | 风险 8 指标 8 件套补全 |
| `TRACE-ENT-RISK.yaml` | open_questions / gaps 与 catalog 一致（不伪闭合 Q017/Q018） |

### 2.3 禁止

- 替甲方闭合 Q017/Q018 正式阈值或评级规则
- 修改 demo / Java / Python 实现（属 V1-HIFI / V2 / ALGO leaf）
- 新增 Neo4j 或让前端直连图库 / Python

## 3. Definition of Done

1. **METRIC-OPEN-ENT-RISK-核对记录.md** + **ENT-RISK-data-gap-catalog.yaml**
2. **cfg_metric-ENT-seed.yaml** 风险相关 8 条更新
3. catalog 中至少 **3 条** `pending_hint` ≥80 字（含表名/字段/Mock 说明）
4. TRACE 与客户决策清单 Q017/Q018 引用一致
5. handoff：`ENT-MOD-RISK-METRIC-OPEN-L01.md` + cost 四字段
6. 唐绍祖 §1.4.1 会签

## 4. 下游

| 任务 | 关系 |
|------|------|
| `ENT-MOD-RISK-V1-HIFI` | 消费 catalog 挂 ⓘ / ⚠️；可并行 |
| `ENT-MOD-RISK-UX-L01` | 并行，不阻塞 |
| `ENT-MOD-RISK-PDR-G1` | 硬依赖本任务语义闭合进度（Q017/Q018 未闭合则 PDR 不可伪通过） |

## 5. 认领话术

```text
/goal ENT-MOD-RISK-METRIC-OPEN-L01
监管：human:唐绍祖
algorithm-agent：8 metric 口径 + DEMO 阈值边界；data-agent：贴源 + ENT-RISK-data-gap-catalog.yaml
先读：TRACE-ENT-RISK.yaml、IA/USM/Wireframe-ENT-RISK、cfg_metric-ENT-seed.yaml
```
