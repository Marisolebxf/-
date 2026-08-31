# 市场份额（M_ENT_MARKET_SHARE）

> 口径真源：王惠底稿「市场份额」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **整条当前无法执行**：没有企业级细分市场总规模。Q019 🟡 暂置空 + 不实现。禁止硬编分母。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_MARKET_SHARE`
- **指标名称**：市场份额
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：商业力评估
- **更新频率**：年（分子跟年报；分母若外购再按采购频次）
- **对齐状态**：口径保留；分母无源；Q019 待甲方/采购
- **是否在数据库**：分子有年报营收；分母无表
- **是否在需求文档**：是
- **是否在原型页面**：是（标无来源）
- **是否在原型代码**：占位 ❌
- **关联Q编号**：Q019

## 口径定义

目标：企业最新年营收 / 所属细分市场总规模 × 100。

- 分子：`enterprise_finance_history.revenue`，该企 `MAX(data_year)`。ODS `dwd_org_annual_financial_info.operating_revenue`。
- 分母：该企所属**细分市场总规模**（外购市调或甲方确认口径）。**不是**库内同行业企业营收加总。
- **当前无法执行**：无市场规模源表。不是「无营收的企业不算」——整条算不出。
- 不挂产业当假分母。国外不另造市场规模表。
- **禁止读** `enterprise_base.market_share`（正式 DWD 120 行全填，mock，无真源）。
- **禁止**旧细稿 V3：`企业营收 / SUM(同 industry_l1 库内营收)`。库内有营收的企业很少，会虚高，也不是市场份额。

## 落表

本波**不写**任何份额列。有分母之前不要往 `enterprise_base.market_share` 灌数。

## 分场景 / 实现方案

有分母之前三个场景都停。

### 场景 A · 画像 / 列表 KPI

无分母 → 不展示数值。UI 走 Q019 无来源，不造 0%、不造 mock 份额。

### 场景 B · 指定年 / 趋势

无分母 → 不画。

### 场景 C · 若以后分母到位

分子仍用该企该年 `revenue`；分母按甲方确认的市场边界对齐后再算。到时改本细稿，不在本波假装已接通。

### demo（`demo_gkxlumenx_*`）

- 财务年表有 `revenue`，没有市场份额列。
- 不算。不拿 demo 15 行或 mock 主档 `market_share` 填数。

### 生产（`gkxlumenx_*`）

- `enterprise_base.market_share` 有列且填满，**不可信**。
- ADS `chain_market` 是产业链市场规模，不是企业份额。
- live `gkx.dwd_market`：15 行国家码，`market_share` 全空，无 `org_id`，不是本指标源。
- 生产同样算不出。禁止用全表 `SUM(revenue)` 冒充分母。

对应 seed `formula`：目标口径保留 + **当前无法执行**。

**计算公式文件**：`M_ENT_MARKET_SHARE.md`

## 源表字段

```
enterprise_finance_history <- ods: dwd_org_annual_financial_info
```

只挂**分子**。分母无表，不编表名。

来源系统（`source_systems`）：国内机构要素库（分子）。分母无系统。

## 现网探针（live `gkx` + 项目 DWD，2026-08-28；不进 8 件套）

- 分子：国内年报 `operating_revenue` 非空约 300 行（稀疏，但分子存在）。
- `gkx.dwd_market`：15 行，`market_name` 为国家码，`market_share` 全 NULL。
- 正式 DWD `enterprise_base.market_share`：120/120 非空（mock）。
- 项目 ODS `dwd_market` / `dwd_quantum_market_scale`：正式库 0 行或非企业份额。
- ADS `chain_market`：产业链，不是本指标。

## 待建 / 缺口

- Q019 🟡：采购市调 / 降级为库内覆盖率 / 下架。本波不替甲方拍板。
- D3 / D4 维持 no_source + mock，本波不升、不改矩阵。
- 不改 GDF DDL。

## 备注

bid `§1.1.1.2.4.2.3.4`；STAT。K-O7。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-28 COVER-STAT-L01 口径保留、分母无源不硬编*
