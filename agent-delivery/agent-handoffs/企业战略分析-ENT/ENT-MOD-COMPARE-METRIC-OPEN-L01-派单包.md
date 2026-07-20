# 派单包：ENT-MOD-COMPARE-METRIC-OPEN-L01

- **派单方**：coordinator
- **时间**：2026-07-21
- **双 Agent 分工**：
  - **`algorithm-agent`**：派生容器模块 **#4 指标语义 N/A 适用性** + Decision 088 业务边界书面依据
  - **`data-agent`**：`field_contract.required_fields` 贴源核对 + **实现缺口 GAP-IMPL-*** catalog（非统计型 metric）
- **监管人**：human:唐绍祖（语义 Owner 临时代行 §1.4.1）
- **Sprint**：2026-W30 stretch
- **上游**：`ENT-MOD-COMPARE-PACK-L01` ✅ done（2026-07-21 四件套 alignment 闭合）

## 1. 目标

闭合 Track-MS 五件套 **#4 + #5**（对比篮为 **派生暂存/分发容器**，无 bid 统计叶子）：

1. **#4**：书面结论「统计 metric 预期 N/A」+ `operational_counts` / 卡片字段说明
2. **#5**：Decision 088、GAP-IMPL-01~03、跨模块 handoff 边界写入开放项表
3. 产出 **`ENT-COMPARE-data-gap-catalog.yaml`**：供 V1-HIFI / V2 挂 **⚠️ PendingBadge「数据缺口说明」**（持久化契约、正式 API 等待）

## 2. 范围

### 2.1 TRACE 真源（关键数字）

`TRACE-ENT-COMPARE.yaml` v1.5：

| 项 | 值 |
|----|-----|
| `metrics_required` | **0** |
| `metrics_mapped` | **0** |
| `statistical_metrics_required` | **0** |
| `open_questions` | []（业务开放项已闭合于 PACK） |
| `implementation_gaps` | GAP-IMPL-01 / 02 / 03 |

**algorithm-agent**：

- 在核对记录 §1 声明：对比篮 **不拥有** 分析结果与竞争力/雷达/排名类 metric（`boundary.excludes`）
- 对 `field_contract.operational_counts`（`basket_count` / `selected_count`）标注 **N/A（交互状态，非 ADS 统计指标）** 及依据
- 对卡片可见字段（`enterprise_name`、`region` 等）说明：**展示字段 ≠ 本模块统计 metric**；真实 metric 归目标模块（评估/风险）
- 跨模块 **analysis_types**（3+2）handoff 参数：`enterprise_codes`、`analysis_type`、`return_context_id` — 写入 §4 边界表（非算法公式）

**data-agent**：

- 逐 `field_contract.required_fields` 做 ODS→DWD 存在性（真源 `gkx_schema_ddl.sql`、企业域设计 v1）
- 对 **GAP-IMPL-02**（单用户单篮正式持久化/API 责任）产出 **≥80 字** `pending_hint`
- 对 **GAP-IMPL-01/03**（lumen 50 上限、return_context 正式联调）写入 catalog，`mapping_status` 🟡
- **不同步** Q037 空态推荐（对比篮 **空篮不做推荐**，TRACE DIFF-04）

### 2.2 联合产出

| 文件 | 说明 |
|------|------|
| `METRIC-OPEN-ENT-COMPARE-核对记录.md` | #4 N/A 依据、字段贴源矩阵、GAP 表、PDR-05/06 自检、唐绍祖会签 |
| `agent-handoffs/产品整体定义/ENT-COMPARE/ENT-COMPARE-data-gap-catalog.yaml` | UI 缺口文案真源（impl gap + 字段级 🟡） |
| `TRACE-ENT-COMPARE.yaml` | `implementation_gaps` 与 catalog 一致（不改 metrics_required=0） |

### 2.3 禁止

- 将对比篮包装成「轻量对比分析」或新增统计 metric_id（违反 Decision 088）
- 替甲方闭合 GAP-IMPL-02 正式持久化方案（可 🟡 + 团队临时默认：Wave0 浏览器存储）
- 修改 demo 页面或 Java/Python 实现（属 V1-HIFI / V2）

## 3. Definition of Done

1. **METRIC-OPEN-ENT-COMPARE-核对记录.md** + **ENT-COMPARE-data-gap-catalog.yaml**
2. 核对记录含 **#4 N/A 书面依据**（≥3 条引用：TRACE / Decision 088 / boundary.excludes）
3. catalog 中 **≥2 条** `pending_hint` ≥80 字（含 GAP-IMPL-02 持久化说明）
4. **TRACE-ENT-COMPARE.yaml** 与 catalog 交叉引用一致
5. handoff：`ENT-MOD-COMPARE-METRIC-OPEN-L01.md` + cost 四字段
6. 唐绍祖 §1.4.1 会签

## 4. pending_hint 模板（实现缺口示例）

```yaml
- gap_id: GAP-IMPL-02
  pending_ref: GAP-IMPL-02
  mapping_status: "🟡"
  pending_hint: |
    对比篮「单用户单篮可恢复」在 Wave0 Demo 依赖浏览器本地存储，尚未与正式用户级持久化 API 契约对齐。
    所需字段 enterprise_code、source_routes、last_operated_at 在 ODS 企业主数据可映射，但篮级聚合表的写入责任、
    会话 TTL 与 return_context_id 服务端存储方案待架构（徐滕强/侯佳伟）与甲方确认。正式联调前 UI 保留 ⚠️ 待确认角标。
```

## 5. 下游

| 任务 | 关系 |
|------|------|
| `ENT-MOD-COMPARE-PDR-G1-RECLOSE` | 硬依赖本任务 + V1-HIFI |
| `ENT-MOD-COMPARE-V1-HIFI` | 可消费 catalog 挂 PendingBadge（review 中可并行补挂） |
| `ENT-MOD-COMPARE-UX-L01` | 并行，不阻塞 |

## 6. 认领话术

```text
/goal ENT-MOD-COMPARE-METRIC-OPEN-L01
监管：human:唐绍祖
algorithm-agent：#4 N/A 书面依据 + Decision 088 边界；data-agent：required_fields 贴源 + ENT-COMPARE-data-gap-catalog.yaml
先读：TRACE-ENT-COMPARE.yaml、PM-PDR-ENT-COMPARE-评审纪要.md、Wireframe-ENT-COMPARE.md
```
