# 核心供应商数（M_ENT_CORE_SUPPLIER_COUNT）

> 口径真源：2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01` **团队临时方案 2**。  
> 筛列 = `relation_type='supplier' AND risk_level='高'`。  
> **偏离 Q017 ②**（原文核心=供应集合内投资金额 TOP5）。Q017 跟踪表未改。  
> **两点分开**：① DWD 现网可 COUNT；② ODS 无供应边、无 `risk_level` 源可 mapping。不把 ① 写成整条无法执行。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_CORE_SUPPLIER_COUNT`
- **指标名称**：核心供应商数
- **一级模块**：企业分析
- **二级模块**：企业供应链关系分析
- **三级模块**：核心供应商
- **更新频率**：周
- **对齐状态**：团队临时筛 `risk_level=高`；偏离 Q017 ②；与断链风险共用列
- **是否在数据库**：DWD `enterprise_supply_chain` 有 `risk_level`；无 `enterprise_supply_summary`
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q017（跟踪表仍 🟢 投资 TOP5；本条落实=方案 2，未回写跟踪表）

## 口径定义

**每个企业一条**：该企业「核心」供应商去重数。本波核心 = 直接供应商且断链风险高。

```
COUNT(DISTINCT related_org_id)
WHERE org_id = :org_id
  AND relation_type = 'supplier'
  AND risk_level = '高'
```

- 一级 = 边自身（同 `M_ENT_SUPPLIER_COUNT`）。不筛 `relation_level`（无此列）。
- **禁止读** `is_core_supplier`（本条产出标记，不能当源）。
- **禁止**投资金额 TOP5、`chain_score`、产业链 tags 当本条筛。
- 不挂产业。只国内。无 `enterprise_forg_supply_chain`，不造表。

### 与 Q017 的关系（细稿，不进 8 件套公式正文）

| Q017 | 本条 |
|------|------|
| ② 核心 = 供应集合内投资 TOP5 | **不用**。改用 `risk_level='高'` |
| ⑤ 断链风险 低/中/高 | **本条筛列就是 ⑤ 的「高」**。与 `M_ENT_SUPPLY_CHAIN_RISK` 撞同一列，两条不是同一指标：本条是 COUNT，断链条是等级/模型 |

上线前若改回 ②，本条公式作废重写。

## 两点分开（强制）

### ① DWD 可出统计

现网 `enterprise_supply_chain` 有 `relation_type`、`risk_level`。SQL 可按上式 COUNT。  
2026-08-28 正式库：`supplier` 且 `risk_level='高'` = **25 边**（其中 `is_core_supplier=1` 的 7 边不参与本条筛）。  
这只证明 **表上能跑**。行是 mock，**不当接通、不升 D3/D4**。

### ② ODS 无源可 mapping

没有供应商–客户关系表，也没有 `risk_level`（断链高/中/低）可灌进 DWD。  
投资表 `dwd_org_invest_info` 有金额，**本方案不用**。股东 / `dwd_org_sc_info` / 链字典 `level` 都不是本条源。

禁止把 ② 说成「DWD 不能 COUNT」；禁止把 ① 说成「ODS 已接通」。

## 落表

| 目标 | 粒度 | 写什么 | 现网 |
|------|------|--------|------|
| `enterprise_supply_summary`（建议名，与供应商数量同表） | 一行一企 | `core_supplier_count` | **缺口：无此表** |

明细表可另写派生列 `is_core_supplier=1`（`supplier` 且 `risk_level='高'`），那是标记不是本条 COUNT 目标。本条读的是计数结果。  
源表 ≠ 目标表。GDF 暂缓，不建 DDL。

## 分场景 / 实现方案

### 场景 A · 单企画像

入参 `:org_id`。目标表有了读 `core_supplier_count`。当前无目标表：可在明细上按口径 COUNT，结果标 mock，不写进正式 live。

### 场景 B · 列表

按 `org_id` 读目标表。禁止请求路径全表现算。

### demo / 生产

两边 DWD 都是 mock 边。生产仍要等 ODS 供应边 + 风险等级入仓后，周 ETL 写目标表。查询只带 `org_id`。

**计算公式文件**：`M_ENT_CORE_SUPPLIER_COUNT.md`

## 源表字段

8 件套 `source_tables`（无合格 ODS，不写假 mapping）：

```
enterprise_supply_chain
```

用列：`org_id`、`related_org_id`、`relation_type`、`risk_level`。

禁止：`dwd_org_invest_info`、`dwd_org_industry_tags.chain_score`、`dwd_org_shareholder_info`、读 `is_core_supplier`。

来源系统：国内机构要素库。

产出（待建）：`enterprise_supply_summary.core_supplier_count`。

## 现网探针（2026-08-28；不进 8 件套）

- DWD 169 行。`supplier`+`高`=25；`supplier`+`is_core=1`=20（不用）。`customer` 上也有 `is_core=1` / `高`，本条不计入。
- ODS：无供应关系；投资金额有数但本方案不用。
- 无 `enterprise_supply_summary`。

## 待建 / 缺口

1. ODS 无供应边、无 `risk_level` 源（②）。DWD 能 COUNT（①）≠ 接通。
2. 无独立目标表。
3. 偏离 Q017 ②；与断链条撞 `risk_level`。跟踪表未改。
4. D3 / D4 本波不升。

## 备注

bid `§1.1.1.2.4.2.3.8`；STAT。供应商全量走 `M_ENT_SUPPLIER_COUNT`。本条是子集 COUNT，不是 GRAPH 中心性。

---
*2026-08-28 COVER-STAT-L01 方案 2：核心=supplier 且 risk_level=高；DWD/ODS 两点分开*
