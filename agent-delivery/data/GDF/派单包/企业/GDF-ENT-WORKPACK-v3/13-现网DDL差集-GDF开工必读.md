# 13 — 现网 DWD 差集（GDF 开工必读）

> **工作包**：GDF-ENT-WORKPACK-v3.0  
> **核验日期**：2026-09-02  
> **核验库**：同一 MySQL 实例上的 `demo_gkxlumenx_dwd` 与 `gkxlumenx_dwd`（外网 `111.198.38.90:34306` = 内网 `192.168.88.43:3306`）  
> **对照真源**：本包 `10-DWD-MySQL-DDL/`  
> **铁律**：缺列只 `ADD`；现网多出来的列 **禁止 DROP**；`*__pre_v3` / `__pre_fix_*` 备份表禁止改、禁止当目标。

## 1. 本侧 2026-09-02 已落到两库（GDF 先复核再跳过）

开工前对两库跑 `information_schema`。已存在则跳过，禁止重复 ADD。

| 对象 | `demo_gkxlumenx_dwd` | `gkxlumenx_dwd` | 说明 |
|------|----------------------|-----------------|------|
| `enterprise_base.region_id` + `idx_enterprise_base_region_id` | 已加 | 已加 | 恢复历史遗漏；ETL 按省市区或港澳台常量绑定 |
| `enterprise_base.enterprise_code` 可空 | 原本可空 | 已改为可空 | 禁止为无信用代码行造码 |
| `enterprise_finance_history.total_assets` / `total_liabilities` | 已加 | 已加 | 年末时点存量；ES 取最新一年 |
| `enterprise_patent_org_rel` | 已建空表 | 已建空表 | 只写主档精确匹配到的 `org_id` |

## 2. Wave A 源表（`gkx` live，2026-09-02）

`02` 清单 48 张施工表中，**45 张 live 已见**。未见 3 张：

| 承诺名 | 优先级 | live | GDF 处置 |
|--------|--------|------|----------|
| `dwd_org_industry_chain_dtl` | 待核实 | 无 | 已在 `02.pending_source_requests`；先洗 `dwd_org_industry_tags` |
| `dwd_org_tag_info` | P0 | 无；可见 `dwd_org_tech_tag` | **阻塞书面确认**：按承诺名向供应方核 `tag_info`，未书面改口前不得擅自改贴 `tech_tag` |
| `dwd_forg_subsidiary_info` | P1 | 无 | **国外子公司洗入阻塞**；只贴已有 `forg_*`，`enterprise_forg_parent_subsidiary` 等源表到位 |
| `dwd_forg_college_org_info` | P2 | 无 | 本期不洗；与 `02` 一致 |

其余 P0/P1（含融资、专利 applicants/assignees、港澳台、招投标出库表）live 均在。

## 3. Wave B 必须补列（正式库 `gkxlumenx_dwd`）

现网正式库表在，但相对 `10/` **缺设计列**。GDF 按 `10/` 出 `ALTER … ADD`，抽样 ≥20 后再洗数。

| 表 | 相对 `10/` 仍缺的设计列 | 备注 |
|----|-------------------------|------|
| `enterprise_patent_detail` | `title_zh/title_en/abstract_zh/publication_number/filing_year/publication_date/publication_year/grant_* /ipc_main/cpc_main/inventor/applicant_name/assignee_name/citation_count/cited_by_count/country/detail_json/data_source` | 现网仍是旧窄表；专利 Wave B **先补列再灌** |
| `enterprise_finance_history` | `main_business_revenue` / `total_profit` / `total_fixed_assets` | 现网另有净利润/研发等旧列，**保留不删** |
| `enterprise_extra` | `stock_noun/listed_status/capital_currency_code/registration_org/postal_code/start_date/end_date` | |
| `enterprise_news` | `news_title/news_date/news_content/original_url` | 现网用 `title/publish_time/...` 另一套命名；**ADD 设计列**，禁止改名覆盖旧列 |
| `enterprise_bid` | `enterprise_name/announcement_title/announcement_date/project_name/project_no/role/winning_amount` | 现网用 `bid_title/bid_amount/...`；同样只 ADD |
| `enterprise_invest` | `inv_name/inv_external_id/investment_amount/investment_ratio/data_source` | 现网有 `inv_org_name/invest_amount/invest_ratio`；只 ADD |
| `enterprise_patent_history` | `patent_invention_count/latest_patent_date/latest_grant_date` | |
| `enterprise_executive` | `data_source` | |
| 指标汇总若干 | `region_id` 等 | 见 `10/` 指标稿；无则 ADD，有 `region_code` 的不要改名覆盖 |

`demo_gkxlumenx_dwd` 工商明细更接近 `10/`，但部分表无技术主键 `id`，风险几张列名也与 `10/` 不一致。产线目标是 **`gkxlumenx_dwd`**；demo 仅对照，禁止把 demo 库当产线写入目标。

## 4. 现网多列（禁止当缺陷删）

正式 `enterprise_base` / demo `enterprise_base` 都宽于 `10/` 核心主档（含 `is_high_tech`、`revenue_latest`、专利计数等）。这些是历史宽表残留。

- **禁止 DROP**  
- 本期 Mapping 只写 `10/` 列出的核心列  
- 宽表旧列是否退役，另开书面，不在本包擅自裁

正式 `enterprise_finance_history` 同样保留 `net_profit` / `rd_investment` 等旧列。

## 5. 开工顺序（完整）

1. 复核 §1 四项已落地；缺哪项补哪项。  
2. 按 §2 处理源表阻塞（`tag_info` / `forg_subsidiary` / `chain_dtl`）。  
3. 对 `gkxlumenx_dwd` 按 §3 出 ALTER 清单，执行前 `SHOW CREATE TABLE` 快照。  
4. Wave A：`gkx` → `gkxlumenx_ods` 同名镜像，勾 `05`。  
5. Wave B：按 `09` 洗入；未命中专利名 / 无 `org_id` 港澳台进治理清单，不造 ID。  
6. DWD 门禁过后再由 `lumen-etl-es-py` 写 `gkx_enterprise`；GDF 不直写 ES。

## 6. 本包不包含

- CDC 预填 Excel（另派）  
- `OPEN-ENT-FLOW-01/04` 调度正式名  
- 检索 Java / 前端改动  
- 把正式库整表重建成与 demo 逐列一致  
