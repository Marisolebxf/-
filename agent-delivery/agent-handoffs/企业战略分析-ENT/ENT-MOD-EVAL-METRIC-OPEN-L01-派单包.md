# 派单包：ENT-MOD-EVAL-METRIC-OPEN-L01

- **派单方**：coordinator
- **时间**：2026-07-20
- **双 Agent 分工**：
  - **`algorithm-agent`**：现有 entan 算法定义（C1 技术力 / C2 商业力 / A1 综合竞争力）
  - **`data-agent`**：三方 **ODS/DWD** 贴源字段存在性 + 8 件套 `source_tables` 血缘
- **监管人**：human:唐绍祖（语义 Owner 临时代行 §1.4.1）
- **Sprint**：2026-W30 stretch
- **上游**：`ENT-MOD-EVAL-PACK-L01` ✅ done

## 1. 目标

完成 Track-MS **五件套 #4/#5**（指标语义 + 开放项），使企业评估原型可以：

1. **ⓘ MetricSpecCard**：展示算法口径、公式、源表链（D9 八件套）
2. **⚠️ PendingBadge Popover「数据缺口说明」**：贴源不足时长文案（参照 E-32 概览样式，见截图）

```text
PendingBadge.tsx：hint 长度 > 80 字 → Popover 标题「数据缺口说明」
```

## 2. 范围

### 2.1 algorithm-agent 交付

| 项 | 真源 |
|----|------|
| 技术力 C1 | `demo-algo-ent-analysis/conf/settings.yaml#tech_power_weights` + 五维子指标 |
| 商业力 C2 | `settings.yaml#biz_power_weights` + 六维 |
| 综合 A1 | `entan/realdata/a1_score.py` + innov/operate/growth **0.40/0.40/0.20** |
| 模型注册 | `conf/cfg_model_registry.yaml` |
| 说明文档 | `算法设计说明.md`、`demo-ui-system-test/.../entanHelp.ts` |

**产出**：`agent-handoffs/产品整体定义/E-23_E-24_E-30-企业评估/metric-spec-ENT-EVAL-algorithm.yaml`（或在核对记录附录）

- 每个 **评估指标 key** ↔ **metric_id** ↔ **算法维度/公式** ↔ **权重**
- 与 `enterpriseEvaluationModel.ts` 三模式 `EVALUATION_MODES` 行对齐（供 ALGO-METRIC-ALIGN 消费）

### 2.2 data-agent 交付

| 项 | 真源 |
|----|------|
| ODS/DWD DDL | `agent-delivery/data/third-party-source/gkx-mysql-raw/gkx_schema_ddl.sql` |
| 企业域 ADS 契约 | `agent-delivery/data/企业域数据库设计(v1).md` |
| 字段映射范例 | `agent-delivery/data/企业相关-ODS到DWD字段映射分析报告(v2).md` |
| 已有 seed | `agent-delivery/metrics/registry/cfg_metric-ENT-seed.yaml` |
| TRACE 缺口 | `TRACE-ENT-EVAL.yaml` → GAP-METRIC-BID-*、Q014、Q019、K-O7 |

**逐指标分析**（每个 `metric_id` 或 IA 注册指标）：

| 列 | 说明 |
|----|------|
| `mapping_status` | ✅ 有源 / 🟡 部分有源 / ❌ 无源 |
| `source_tables[]` | ODS → DWD → ADS 链（真实表名） |
| `field_check` | 所需字段是否存在；缺失列点名 |
| `pending_ref` | Q 编号或 GAP-*（同步客户决策清单） |
| `pending_hint` | **≥80 字** Popover 文案（见 §4 模板） |
| `wave0_behavior` | Mock / 暂置空 / 不算分 |

### 2.3 联合产出（主文档）

**`agent-handoffs/产品整体定义/METRIC-OPEN-ENT-EVAL-核对记录.md`**

- §1 适用性结论（五件套 #4/#5）
- §2 三模式算法定义摘要（algorithm-agent）
- §3 指标 × 贴源矩阵（data-agent）
- §4 开放项闭合表（Q014 / Q019 / GAP-* → 🟡 或 N/A+依据）
- §5 PDR-05/06 自检清单
- §6 语义会签：唐绍祖（§1.4.1）

**`agent-handoffs/产品整体定义/E-23_E-24_E-30-企业评估/ENT-EVAL-data-gap-catalog.yaml`**

- UI 真源：`metric_id` → `pending_ref` / `pending_hint` / `mapping_status`
- demo 挂接：`enterpriseEvaluationModel` 指标行读取 catalog（实现可交 ALGO-METRIC-ALIGN 或 V1-HIFI，**catalog 必须先于 UI 改动**）

### 2.4 禁止

- 替甲方拍板 Q014 权重最终值（可标 🟡 + 团队临时默认）
- 修改非评估模块 demo 页面
- 本任务 **不要求** 重写 entan 算法代码（定义与血缘为主）

## 3. Definition of Done

1. **METRIC-OPEN-ENT-EVAL-核对记录.md** + **ENT-EVAL-data-gap-catalog.yaml** 齐备
2. **cfg_metric-ENT-seed.yaml** 评估相关 `M_ENT_*` 更新（definition / formula / source_tables / pending_ref / mapping_status）
3. **TRACE-ENT-EVAL.yaml** open_items 与 catalog 一致
4. **客户决策清单** 新增或引用 Q 项（无新增须 N/A+依据）
5. **缺口 Popover 样例**：catalog 中至少 **3 条** `pending_hint` 达到截图粒度（含表名、字段名、Mock 说明）
6. handoff + 架构合规 7 条 + cost 四字段
7. 唐绍祖 review 签字（§1.4.1）

## 4. pending_hint 文案模板（Popover）

```text
该需求已在需求清单中登记（开放项 {pending_ref}），但当前三方源数据暂不能支撑「{metric_name_zh}」指标口径：
① {dwd_table_1} {缺失说明}；
② {dwd_table_2/ods_table} {字段说明}；
③ {其他约束}。
当前界面展示值为 Mock/暂置空，待供应方补充真源或可替代数据后替换。
```

**示例**（E-32 同类，供 data-agent 仿写）：

> 该需求已在需求清单中登记（开放项 Q-EVAL-01），但当前三方源数据暂不能支撑「研发人员占比」指标口径：① 企业基础信息表 `dwd_org_reg_info` 缺少研发人员相关字段；② 年报/上市财报仅有 `employees_number`（员工总数，非研发专指）与 `research_development_amount`（研发投入金额）；③ 海外财报 `research_development_employees_number` 标注为无数据。当前展示值为 Mock，待供应方补真源后替换。

## 5. 与并行任务关系

| 任务 | 关系 |
|------|------|
| `ENT-EVAL-ALGO-METRIC-ALIGN-L01` | 消费本任务 catalog + 算法卡，改 demo **权重/指标 key** |
| `ENT-MOD-EVAL-V1-HIFI`（待登记） | 消费 catalog 挂 PendingBadge / 评审模式 |
| `ENT-MOD-EVAL-PDR-G1` | **硬依赖** 本任务 done |

## 6. 认领话术

```text
/goal ENT-MOD-EVAL-METRIC-OPEN-L01
监管：human:唐绍祖
algorithm-agent：算法三模式定义卡；data-agent：ODS/DWD 缺口 catalog + cfg_metric 更新
先读派单包与 TRACE-ENT-EVAL，交付 METRIC-OPEN 核对记录 + ENT-EVAL-data-gap-catalog.yaml
```
