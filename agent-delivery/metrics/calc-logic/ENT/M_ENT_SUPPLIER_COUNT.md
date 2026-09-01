# 供应商数量（M_ENT_SUPPLIER_COUNT）

> 口径真源：Q017「直接一级上游」→ 2026-08-31 方案1：`formula` 只写怎么算；有没有数是另一回事。  
> **粒度=企业**。与 `CORE_SUPPLIER_COUNT` 同一套边表。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_SUPPLIER_COUNT`
- **指标名称**：供应商数量
- **一级模块**：企业分析
- **二级模块**：企业供应链关系分析
- **三级模块**：供应商节点数
- **更新频率**：周
- **对齐状态**：口径已锁（Q017 一级=边自身）；formula 与有数分开
- **是否在数据库**：DWD `enterprise_supply_chain` 有表、169 行 mock；无 `enterprise_supply_summary`
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q017（已按团队临时默认升 🟢；非甲方书面。本条只用「直接一级」，不用 TOP5 / 断链分档）

## 口径定义

**每个企业一条**：该企业直接供应商去重数。

```
COUNT(DISTINCT related_org_id)
WHERE org_id = :org_id
  AND relation_type = 'supplier'
```

- Q017「上游」对齐现网 `relation_type='supplier'`（不是「上游」二字，也不是产业链上中下游）。
- Q017「直接一级」= **边自身即 1-hop**。DWD / ODS 都没有 `relation_level`，不筛、不补列。`risk_level` 是断链风险高/中/低，**禁止当 hop**。
- **禁止读** `is_core_supplier`（那是 `M_ENT_CORE_SUPPLIER_COUNT` 的产出）。
- **禁止读** `relation_strength`（关系强度是另一条 MODEL）。
- 不挂产业。页面选产业只收窄 `org_id` 集合。
- 国外：无 `enterprise_forg_supply_chain`，不造表，本条只国内。
- 港澳台 ≠ 国外。

## 两点分开（强制）

### ① formula

`enterprise_supply_chain` 有 `relation_type='supplier'` 边就能 COUNT。跟 `CORE_SUPPLIER_COUNT` 同一张表。

### ② 有没有数

ODS 无供应关系表、DWD 169 行 mock：只记灌数 / 不升 D3 D4。**不写「当前无法执行」**。

## 落表

| 目标 | 粒度 | 写什么 | 现网 |
|------|------|--------|------|
| `enterprise_supply_summary`（建议名） | 一行一企 `org_id` | `supplier_count` | **缺口：无此表** |

`enterprise_supply_chain` 是**关系明细源**，不是本条计数目标。禁止把明细行数当指标、禁止把明细表当已落库结果。  
GDF 暂缓，本波不建 DDL。建不建、叫什么 **待后续讨论**。

## 分场景 / 实现方案

### 场景 A · 单企画像

入参 `:org_id`。目标表建成且供应边接通后：读 `enterprise_supply_summary.supplier_count`。  
查询按 `org_id` 读目标表；没有目标表时按 ① 对明细 COUNT。mock 不当接通（②）。

### 场景 B · 列表 / 筛选合计

列表展示每企一个数，从目标表按 `org_id` 读。筛选合计 = 当前结果集企业的供应商数之和或再去重，页面定，不进 8 件套。禁止请求路径全表扫明细 UNION。

### demo / 生产

demo / 正式 DWD 都有 mock 边（②）。生产周 ETL 写入目标表；查询带 `org_id`。

对应 seed `formula`：COUNT 边 + ①能写 + ②有数另写。

**计算公式文件**：`M_ENT_SUPPLIER_COUNT.md`

## 源表字段

8 件套 `source_tables`（左端明细；**无合格 ODS，不写假 mapping**）：

```
enterprise_supply_chain
```

**禁止**写成：

- `<- ods: dwd_industry_chain_info` / `dwd_org_industry_tags`（上链标签 / 链字典，不是供应边）
- `<- ods: dwd_org_shareholder_info`（GDF 曾把股东灌进本表，对象错位）
- `<- ods: dwd_org_invest_info`（投资边；核心供应商 TOP5 代理才用，不是本条全量供应商）
- `<- ods: dwd_org_sc_info`（证照/资质）

来源系统：国内机构要素库（对象应在机构库；现无此对象表）。不写库名、行数、Mock @ batch。

产出（待建）：`enterprise_supply_summary.supplier_count`。

## 现网探针（2026-08-28；不进 8 件套）

- 正式 DWD `enterprise_supply_chain`：169 行。列 = `org_id` / `related_org_id` / `relation_type` / `relation_strength` / `is_core_supplier` / `risk_level`。无 `relation_level`。
- `relation_type`：`supplier` 81 / `customer` 88。`risk_level` 全填 高/中/低（断链风险 mock）。`is_core_supplier=1` 共 40。
- live ODS：无供应关系表。股东、投资、`dwd_org_sc_info`、产业链 `level`（目录层级）均不能当本条源。
- 无 `enterprise_supply_summary`。无国外对等供应表。

## 待建 / 缺口（本波只暴露，不结项）

1. ODS 无供应商–客户关系表（②）。DWD 能 COUNT（①）≠ 接通。
2. GDF 股东→`enterprise_supply_chain` 语义错位，本条不用。
3. **缺口：无独立目标表** `enterprise_supply_summary`。
4. 不补 `relation_level` 列（源没有 hop）。
5. D3 / D4 本波不升。

## 备注

bid `§1.1.1.2.4.2.3.8`；STAT。Q017 ① 供应商范围=直接一级。核心 TOP5 / 断链风险 / 关系强度分档走后三条，本条不写。

---
*2026-08-28 一级=边自身；2026-08-31 方案1 formula 与有数分开*
