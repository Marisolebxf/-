# 企业发展历程（M_ENT_DEV_HISTORY）

> 口径真源：seed「财务 / 专利统计 / 重点资讯 merge 时间线」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **粒度=企业**。国内三流 ODS 非全空，口径能算。**缺口：无独立目标表** `enterprise_dev_history`。国外财务本波不做。更新频率 **weekly**。  
> 产品 `.5.2` CMS / 专家知识 / 明星企业故事 **不消费本条**。招标 142 重大事件阈值是 MODEL，本波不写。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_DEV_HISTORY`
- **指标名称**：企业发展历程
- **一级模块**：企业分析
- **二级模块**：企业深度
- **三级模块**：企业画像时间线
- **更新频率**：周
- **对齐状态**：三流 merge；国外财务暂不并；授权按申请年桶；**无独立目标表**
- **是否在数据库**：ODS 三流有有效值；源表有 mock；**无 `enterprise_dev_history`**
- **是否在需求文档**：是（结构化时间线；CMS 历程另轨）
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：无（Q004 是软科学「难题攻关历程」，不是本条）

## 口径定义

**每个企业一条 timeline**：三类事件 UNION 后按时间倒序。

1. **财务年报**：`enterprise_finance_history` 一行一事。时间 = `data_year`。只带 `revenue`、`net_profit`。  
   **禁止读** `revenue_growth_rate` / `profit_margin` / `rd_investment_ratio` / `gross_margin`（别的指标产出）。
2. **专利年统计**：`enterprise_patent_history` 一行一事。时间 = `data_year` = ODS `dwd_patent.apdt_year`（**申请年**）。  
   `patent_apply_count` = 该年申请件数；`patent_grant_count` = **该申请年专利中已有授权号的件数**，不是授权发生年（明细无授权日，不能按授权年切）。
3. **重点资讯**：`enterprise_news` 一行一事。时间 = `publish_time`。带 `title`、`news_type`。ODS = `dwd_org_important_news_info`。不用 `dwd_news_base`、不用产业链资讯、不用 `dwd_event`。

无三类任何事件：**该企空时间线**。口径能算不等于已落库。目标表见下节；**当前无此表**。

- 国外财务：对等表 `enterprise_forg_finance_history` 正式库 0 行，**本波不做、不 UNION**。不造表。ODS 国外年报有数，缺口留细稿，不假装已并。
- 专利：无独立国外专利表。名称映射进同一张 `enterprise_patent_history`（与 `M_ENT_PATENT_TOTAL` 同一套）。不造 `enterprise_forg_patent`。
- 资讯：无国外表，只国内。
- 不挂产业。页面选产业只收窄 `org_id` 集合，不进 8 件套公式。
- **禁止**把 CMS / `expert_knowledge` / 明星企业故事当源。
- **禁止**做并购 / 上市 / 股权变更阈值识别（那是 MODEL `M_ENT_DEEP_142_1` / 算法库 142）。
- **禁止**加曾用名（`enterprise_history_name` 现网 0 行，指标名也没要）。

## 落表

| 目标 | 粒度 | 写什么 | 现网 |
|------|------|--------|------|
| `enterprise_dev_history`（建议名） | 一行一事件：`org_id + event_time + event_type` | 三流 merge 后的 timeline | **缺口：无此表** |

正式 / demo 的 `gkxlumenx_dwd`、`gkxlumenx_ads` **都没有** `enterprise_dev_history` / `enterprise_timeline*`。  
`event_std`、`innovation_event` 不是本条。曾用名表不是本条。

**禁止**把 `enterprise_finance_history` / `enterprise_patent_history` / `enterprise_news` 当目标表（那是源）。  
GDF workpack 暂缓，本波不建 DDL，只记缺口。

建议列（待建，不进 8 件套 `source_tables`）：`org_id`、`event_time`、`event_type`（finance / patent_year / news）、`event_year`、`title`、`payload_json`、`data_source`。索引 `(org_id, event_time)`。

当前：**结果无处可落**。查询不能假装已从目标表读出。

## 分场景 / 实现方案

### 场景 A · 单企画像（目标读路径）

入参 `:org_id`，可选 `:from` / `:to`、`:limit`（默认最近 50～100 条）。

目标表建成后：

```
SELECT * FROM enterprise_dev_history
WHERE org_id = :org_id
  AND event_time >= :from
ORDER BY event_time DESC
LIMIT :limit
```

**当前无此表**：不能用三张源表的在线 UNION 冒充已落库。三流仍是计算输入，不是查询目标。

### 场景 B · 列表 / 筛选

列表页 **不附全文时间线**。最多一条「最近事件」摘要，或根本不调本指标。禁止为 N 家企业各扫一遍资讯全表。

### 场景 C · 导出 / 报告

仍按单企 A 循环，按 `org_id` 分批，禁止一次导出全库 merge 结果。

### demo（`demo_gkxlumenx_dwd`）

体量小（财务/专利年各几百、资讯约 180），也 **没有** 目标表。建成后与生产同一张 `enterprise_dev_history`。禁止把 demo 三表在线 UNION 当成已落库。

### 生产（`gkxlumenx_dwd`）· 千万级怎么扛

资讯和专利明细会到百万～千万行。**周任务写入目标表**；**画像只读 `enterprise_dev_history`**。查询禁止全表 merge；计算禁止在线 `GROUP BY` 专利明细。

1. **查询永远带 `org_id`，只打目标表**  
   `WHERE org_id=? AND event_time>=? ORDER BY event_time DESC LIMIT n`。索引 `(org_id, event_time)`。复杂度跟该企事件数走。  
   **当前无目标表**：这条读路径还不存在，缺口见上。

2. **周 ETL 才碰源表**  
   - 专利：先增量预聚合进 `enterprise_patent_history`（`apdt_year` + 权利人映射；按水位 / `org_id` hash 分桶，禁止全表 `GROUP BY`），再投影成目标表 `event_type=patent_year`。  
   - 财务：年表很小，增量后投影 `event_type=finance`（只带 revenue/net_profit）。  
   - 资讯：ODS → `enterprise_news` 增量后投影 `event_type=news`。单企资讯上万则目标表只留窗口（如近 5 年或每企最近 N 条），全量留源表冷分区。

3. **upsert 键**  
   `(org_id, event_type, event_time)`（资讯再用源新闻 id 防重）。周水位增量，不要每次打开页面现算，不要在请求路径扫 ODS。

4. **全量重跑**  
   按 `org_id` 分桶重建目标表。禁止单语句三源 `UNION ALL` 倒进全库。

5. **demo**  
   体量小，仍应写入同一张目标表（建成后），不要长期靠三表在线 UNION。现网 demo 也无此表。

对应 seed `formula`：三流 UNION 写入 `enterprise_dev_history`；国外财务暂不并；**当前无此表（缺口）**。

**计算公式文件**：`M_ENT_DEV_HISTORY.md`

## 源表字段

8 件套 `source_tables`：

```
enterprise_finance_history <- ods: dwd_org_annual_financial_info
enterprise_patent_history <- ods: dwd_patent
enterprise_news <- ods: dwd_org_important_news_info
```

- 财务：`data_year` ← `year`；`revenue` ← `operating_revenue`；`net_profit` ← `pure_profit`
- 专利年：`data_year` ← `apdt_year`；计数从 `dwd_patent`（权利人映射与总量同一套；`assignees` 是 ETL 映射原料，不另开左表）
- 资讯：`publish_time` ← `news_date`；`title` ← `news_title`

`enterprise_base` 只当 org 身份，不进 8 件套。`enterprise_forg_finance_history` 本波不进。

来源系统（`source_systems`）：国内机构要素库、国外机构要素库（专利名称可映射到国外主档；财务国外本波不做）。

## 现网探针（live `gkx` + 项目 DWD，2026-08-28；不进 8 件套）

- 国内 ODS 年报 20178，`operating_revenue` 非空 300；`year` 全满。
- 国外 ODS 年报 18193，营收非空 12312；正式 DWD `enterprise_forg_finance_history` **0 行** → 本波不做。
- ODS 专利 86028，`apdt_year` 全满；`granted_number` 非空 47607。无授权日列。
- ODS 重点资讯 52093，`news_date` / `news_title` 全满。
- 正式 DWD：财务年 709（`revenue`/`net_profit` 全满）、专利年 709（与财务行数对齐，像成对 mock）、资讯 200（标题/时间全满）。
- `enterprise_history_name` 0 行。无 `enterprise_forg_news` / `enterprise_forg_patent`。
- **无** `enterprise_dev_history` / `enterprise_timeline*`（dwd + ads，正式与 demo）。

## 待建 / 缺口

- **无独立目标表**（建议名 `enterprise_dev_history`；正式 / demo DWD、ADS 均无）。结果无处可落。本波不建 DDL。**是否建表、用何表名：待后续讨论**，此处只暴露缺口。
- 项目 DWD 三张**源表**仍是 mock，`is_mock: true`。国内 ODS 非全空，口径能算，但不等同已落库。
- 国外财务 DWD 未灌；本波不做。
- 专利 `grant_count` 只能按申请年桶，缺授权日。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3` 企业深度；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。禁止 CMS 当源。禁止请求路径全表 UNION。

---
*2026-08-28 COVER-STAT-L01 三流 merge；国外财务暂不并；weekly；缺口无独立目标表；千万级周 ETL 写入目标表*
