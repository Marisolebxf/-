# 派单包：ENT-MOD-SEARCH-METRIC-OPEN-L01

- **派单方**：coordinator
- **时间**：2026-07-21
- **双 Agent 分工**：
  - **`algorithm-agent`**：检索结果卡片 / 列表 / 导出相关 **指标口径**（非 NL 检索算法本身）
  - **`data-agent`**：检索触点 **ODS→DWD→ADS** 字段存在性 + `cfg_metric-ENT-seed` 更新
- **监管人**：human:唐绍祖（语义 Owner 临时代行 §1.4.1）
- **Sprint**：2026-W30 stretch
- **上游**：`ENT-MOD-SEARCH-PACK-L01` ✅ done（2026-07-21 淮政玮）

## 1. 目标

闭合 Track-MS 五件套 **#4 指标语义卡 + #5 开放项**，支撑：

1. 检索列表 / 高筛 / 导出相关 **ⓘ MetricSpecCard**
2. 贴源不足指标的 **⚠️ PendingBadge「数据缺口说明」**（`pending_hint` ≥80 字）

## 2. 范围

### 2.1 适用 metric 范围（TRACE 真源）

`TRACE-ENT-SEARCH.yaml` 已登记 **12** 个 metric 需求、**11** 已映射；重点：

| 类别 | 示例 metric_id | 开放项 |
|------|----------------|--------|
| 列表卡片 KPI | `M_ENT_*`（专利、营收、人员等） | Q010~Q019 |
| 检索交互 | 导出条数、排序字段 | **Q033~Q037** |
| 已知缺口 | `M_ENT_MARKET_SHARE` | Q019 ❌ |

**algorithm-agent**：

- 核对 `cfg_metric-ENT-seed.yaml` 中检索页引用的 `M_ENT_*` **definition / formula**（多为展示型聚合，非评估模型）
- 导出 ≤1000 条、智能搜索多字段匹配等 **能力口径** 写入核对记录（业务规则引用 PDR / Decision 042~083，非新拍板）

**data-agent**：

- 逐 metric 做 ODS→DWD 字段存在性（真源 `gkx_schema_ddl.sql`、企业域设计 v1）
- 产出 `ENT-SEARCH-data-gap-catalog.yaml`（含 `pending_hint`）
- 同步 **Q033~Q037** 至 `客户决策清单跟踪表.md`（已有则引用）

### 2.2 联合产出

| 文件 | 说明 |
|------|------|
| `METRIC-OPEN-ENT-SEARCH-核对记录.md` | 适用性、指标矩阵、PDR-05/06 自检、唐绍祖会签 |
| `agent-handoffs/产品整体定义/E1-企业查询/ENT-SEARCH-data-gap-catalog.yaml` | UI 缺口文案真源 |
| `cfg_metric-ENT-seed.yaml` 更新 | 检索相关条目补全 8 件套字段 |
| `TRACE-ENT-SEARCH.yaml` | open_questions / gaps 与 catalog 一致 |

### 2.3 禁止

- 实现 Java/Python 检索算法或改 demo 页面（属 V2 / API leaf）
- 替甲方闭合 Q033~Q037 最终业务口径（可 🟡 + 团队临时默认）
- 将 NL 智能搜索重新引入（architecture-baseline 已否）

## 3. Definition of Done

1. **METRIC-OPEN-ENT-SEARCH-核对记录.md** + **ENT-SEARCH-data-gap-catalog.yaml**
2. **cfg_metric-ENT-seed.yaml** 检索触点相关条目更新
3. **TRACE-ENT-SEARCH.yaml** 与 catalog 一致；`review_checklist` PDR-05/06 可勾选
4. catalog 中 **≥2 条** `pending_hint` 达字段级粒度（含表名/字段/Mock 说明）
5. handoff：`ENT-MOD-SEARCH-METRIC-OPEN-L01.md` + cost 四字段
6. 唐绍祖 §1.4.1 会签

## 4. pending_hint 模板

同 `ENT-MOD-EVAL-METRIC-OPEN-L01-派单包.md` §4；开放项优先用 **Q033~Q037** 编号。

## 5. 下游

| 任务 | 关系 |
|------|------|
| `ENT-MOD-SEARCH-PDR-G1-RECLOSE` | 硬依赖本任务 + V1-HIFI |
| `ENT-MOD-SEARCH-V1-HIFI` | 可消费 catalog 挂 PendingBadge |
| `ENT-JAVA-SEARCH-BIZ` | 只读 metric 口径，不替代本任务 |

## 6. 认领话术

```text
/goal ENT-MOD-SEARCH-METRIC-OPEN-L01
监管：human:唐绍祖
algorithm-agent：检索 metric 口径卡；data-agent：ODS/DWD + ENT-SEARCH-data-gap-catalog.yaml
先读：TRACE-ENT-SEARCH.yaml、cfg_metric-ENT-seed.yaml、PM-PDR-ENT-SEARCH-评审纪要.md
```
