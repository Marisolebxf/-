# FIX-TOPIC-SEARCH-PY DWD 表结构逐表复核清单

> 用途：由 human/DBA 逐表补充结论，完成后据此从头整理正式 DWD 表结构设计文档。
> 生成日期：2026-08-03
> API 契约：Java 已接入的路径、请求和响应结构保持不变。

## 1. 填写方法

每张表请填写以下三项即可：

- `最终结论`：保留现库 / 采用设计 / 合并调整 / 删除不用
- `最终字段`：如需合并调整，写最终字段名；可直接修改本文件
- `备注`：口径、类型、唯一键、索引或 DBA 说明

标记说明：

- `字段差异`：表存在，但字段名或语义不同
- `缺表`：代码已使用，但当前 MySQL 无表
- `仅表名差异`：结构存在，名称需去掉历史 `dwd_` 前缀
- `一致`：用于关联确认，不需改字段

## 2. 需要逐表确认的非风险表

### 2.1 `enterprise_patent_detail`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, org_id, patent_id, patent_name, patent_type, filing_date, publish_date, legal_status, ipc_code, create_time, update_time`
- 设计文档字段：`id, org_id, patent_id, publication_number, title_zh, title_en, abstract_zh, patent_type, country, filing_date, filing_year, publication_date, publication_year, grant_date, grant_year, grant_number, ipc_main, cpc_main, inventor, applicant_name, assignee_name, legal_status, citation_count, cited_by_count, detail_json, data_source, create_time, update_time`
- Python SQL/API 所需字段：`org_id, patent_id, publication_number, title_zh, title_en, abstract_zh, patent_type, country, filing_date, filing_year, publication_date, publication_year, grant_date, grant_year, grant_number, ipc_main, cpc_main, inventor, applicant_name, assignee_name, legal_status, citation_count, cited_by_count`
- 已识别候选映射：patent_name → title_zh；publish_date → publication_date；ipc_code → ipc_main；其余缺失字段无可靠来源。

**请补充**

- 最终结论：`[ ] 保留现库  [选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：org_id+patent_id 必须是唯一索引，patent_id必须是索引
- 备注：

### 2.2 `enterprise_patent_history`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, org_id, data_year, patent_apply_count, patent_grant_count, patent_valid_count, patent_citation_count, create_time, update_time`
- 设计文档字段：`id, org_id, data_year, patent_apply_count, patent_grant_count, patent_valid_count, patent_invention_count, patent_citation_count, latest_patent_date, latest_grant_date, create_time, update_time`
- Python SQL/API 所需字段：`org_id, data_year, patent_apply_count, patent_grant_count, patent_valid_count, patent_invention_count, patent_citation_count, latest_patent_date, latest_grant_date`
- 已识别候选映射：现库已有 4 类计数字段；缺 patent_invention_count、latest_patent_date、latest_grant_date。

**请补充**

- 最终结论：`[ ] 保留现库  [选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：org_id+data_year是唯一索引
- 备注：

### 2.3 `enterprise_invest`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, org_id, inv_org_id, inv_org_name, invest_amount, invest_ratio, event_date, create_time, update_time`
- 设计文档字段：`id, org_id, inv_org_id, inv_name, inv_external_id, investment_amount, investment_ratio, data_source, create_time, update_time`
- Python SQL/API 所需字段：`org_id, inv_org_id, inv_name, inv_external_id, investment_amount, investment_ratio, data_source`
- 已识别候选映射：inv_org_name → inv_name；invest_amount → investment_amount；invest_ratio → investment_ratio；event_date 为现库额外字段。

**请补充**

- 最终结论：`[ ] 保留现库  [选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：org_id+inv_org_id是唯一索引
- 备注：

### 2.4 `enterprise_region_summary`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, region_code, region_name, stat_year, enterprise_total, new_count, active_count, output_value, stat_date, create_time, update_time`
- 设计文档字段：`id, region_id, region_name, region_type, parent_region_id, stat_date, enterprise_total, new_enterprise_count, active_enterprise_count, total_revenue, create_time, update_time`
- Python SQL/API 所需字段：`region_id, region_name, region_type, parent_region_id, stat_date, enterprise_total, new_enterprise_count, active_enterprise_count, total_revenue`
- 已识别候选映射：region_code → region_id；new_count → new_enterprise_count；active_count → active_enterprise_count；output_value → total_revenue；stat_year 为现库额外字段。

**请补充**

- 最终结论：`[ ] 保留现库  [选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：region_id+region_type+stat_date 是唯一索引
- 备注：

### 2.5 `enterprise_industry_distribution`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, region_code, chain_code, chain_name, enterprise_count, ratio, stat_date, create_time, update_time`
- 设计文档字段：`id, region_id, chain_code, chain_name, enterprise_count, stat_date, create_time, update_time`
- Python SQL/API 所需字段：`region_id, chain_code, chain_name, enterprise_count, stat_date`
- 已识别候选映射：region_code → region_id；ratio 为现库额外字段。

**请补充**

- 最终结论：`[ ] 保留现库  [选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：region_id+chain_code+stat_date 是唯一索引
- 备注：

### 2.6 `enterprise_growth_trend`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, region_code, stat_month, new_count, cumulative_count, stat_date, create_time, update_time`
- 设计文档字段：`id, region_id, stat_year, stat_month, new_enterprise_count, stat_date, create_time, update_time`
- Python SQL/API 所需字段：`region_id, stat_year, stat_month, new_enterprise_count, stat_date`
- 已识别候选映射：region_code → region_id；new_count → new_enterprise_count；现库 stat_month 为 YYYY-MM 字符串且无 stat_year；cumulative_count 为额外字段。

**请补充**

- 最终结论：`[ ] 保留现库  [选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：region_id+stat_year+stat_month+stat_date 是唯一索引
- 备注：

### 2.7 `enterprise_industry_summary`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, chain_code, chain_name, stat_year, enterprise_count, high_tech_count, rd_staff_total, patent_total, revenue_total, stat_date, create_time, update_time`
- 设计文档字段：`id, chain_code, chain_name, stat_year, enterprise_count, research_staff_total, patent_total, high_tech_count, stat_date, create_time, update_time`
- Python SQL/API 所需字段：`chain_code, chain_name, stat_year, enterprise_count, research_staff_total, patent_total, high_tech_count, stat_date`
- 已识别候选映射：rd_staff_total → research_staff_total；revenue_total 为现库额外字段。

**请补充**

- 最终结论：`[ ] 保留现库  [ 选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：chain_code+stat_year+stat_date 是唯一索引
- 备注：

### 2.8 `enterprise_stat_summary`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, stat_type, dim_code, dim_name, stat_year, enterprise_count, metric_value, stat_date, create_time, update_time`
- 设计文档字段：`id, stat_type, dim_code, dim_name, stat_year, stat_value, stat_date, create_time, update_time`
- Python SQL/API 所需字段：`stat_type, dim_code, dim_name, stat_year, stat_value, stat_date`
- 已识别候选映射：metric_value/enterprise_count 与 stat_value 的口径需确认；不能仅按名称自动选。

**请补充**

- 最终结论：`[ ] 保留现库  [选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：stat_type+dim_code+stat_year+stat_date 是唯一索引
- 备注：

### 2.9 `enterprise_type_scale_stats`

- 状态：**字段差异**
- 当前 MySQL 字段：`id, company_type, enterprise_scale, region, region_level, stat_year, enterprise_count, stat_date, create_time, update_time`
- 设计文档字段：`id, company_type, enterprise_scale, region_level, region_code, region_name, enterprise_count, stat_date, create_time, update_time`
- Python SQL/API 所需字段：`company_type, enterprise_scale, region_level, region_code, region_name, enterprise_count, stat_date`
- 已识别候选映射：现库只有 region 单列，无法无歧义拆成 region_code + region_name；另有 stat_year。

**请补充**

- 最终结论：`[ ] 保留现库  [ ] 采用设计  [选择] 调整  [ ] 删除不用`
- 最终字段：`id, company_type, enterprise_scale, region_level, region_id, region_name, enterprise_count, stat_date, create_time, update_time`
- 唯一键/索引：company_type+enterprise_scale+region_level+region_id+stat_date 是唯一索引
- 备注：

### 2.10 `shenzhen_enterprise_summary`

- 状态：**缺表**
- 当前 MySQL 字段：`（表不存在）`
- 设计文档字段：`id, stat_type, dim_code, dim_name, stat_year, stat_value, stat_date, create_time, update_time`
- Python SQL/API 所需字段：`stat_type, dim_code, dim_name, stat_year, stat_value, stat_date`
- 已识别候选映射：缺表；可从 DWD 设计 v2.5 和现有 3 个 SQL 接口完整复原。

**请补充**

- 最终结论：`[ ] 保留现库  [选择] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：
- 唯一键/索引：stat_type, dim_code, stat_year, stat_date是唯一索引
- 备注：

### 2.11 `enterprise_distribution`

- 状态：**缺表**
- 当前 MySQL 字段：`（表不存在）`
- 设计文档字段：`现有 DWD 主设计文档未收录；API 文档仅说明 dimension + region_type + region_id 唯一`
- Python SQL/API 所需字段：`dimension, region_type, parent_region_id, region_id, region_name, enterprise_count, new_enterprise_count`
- 已识别候选映射：缺表；字段可从 /stats/distribution SQL 和稳定 API 契约复原。

**请补充**

- 最终结论：`[ ] 保留现库  [ ] 采用设计  [选择] 合并调整  [ ] 删除不用`
- 最终字段：`id, dimension, region_type, parent_region_id, region_id, region_name, enterprise_count, new_enterprise_count, stat_date, create_time, update_time`
- 唯一键/索引：dimension+region_type+region_id+stat_date 是唯一索引
- 备注：

### 2.12 `sz_city_benchmark`

- 状态：**仅表名差异**
- 当前 MySQL 字段：`id, city_code, city_name, is_benchmark, is_national, avg_tech_power, avg_business_power, enterprise_density, chain_completeness, key_node_count, sz_count, chain_position, sort_order, is_active, create_time, update_time`
- 设计文档字段：`代码现状模型：id, city_code, city_name, is_benchmark, is_national, avg_tech_power, avg_business_power, enterprise_density, chain_completeness, key_node_count, sz_count, chain_position, sort_order, is_active, create_time, update_time`
- Python SQL/API 所需字段：`city_code, city_name, is_national, avg_tech_power, avg_business_power, enterprise_density, chain_completeness, key_node_count, sz_count, chain_position, is_active, sort_order`
- 已识别候选映射：当前真实表名 dwd_sz_city_benchmark；代码确实使用，按 human 决策目标名改为 sz_city_benchmark。

**请补充**

- 最终结论：`[ ] 保留现库  [ ] 采用设计  [ ] 合并调整  [ ] 删除不用`
- 最终字段：改表名为sz_city_benchmark
- 唯一键/索引：
- 备注：

## 3. 风险明细表逐表确认

说明：18 类风险业务中包含 18 张主表，另有 6 张 party 表。当前全部为 0 行，但字段不一致仍会导致 SQL 在执行阶段报错，不能视为“空数据正常返回”。

### 3.1 `judicial_case` → `risk_judicial_case`

- 当前主表字段：`id, org_id, org_name, case_no, case_title, case_type, amount, court, event_date, status, create_time, update_time`
- Python 查询字段：`case_id, case_no, case_title, case_type_tag, case_cause, case_role, current_procedure, procedure_date, is_history, org_id`
- 当前缺少的查询字段：`case_cause, case_id, case_role, case_type_tag, current_procedure, is_history, procedure_date`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [选择] 采用设计富字段  [ ] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, org_id, org_name, case_id, case_no, case_title, case_type_tag, amount, court, event_date, status, case_role, case_cause, current_procedure, procedure_date, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：case_id是唯一键
- 事件日期字段：procedure_date
- 备注：

### 3.2 `dishonest` → `risk_dishonest`

- 当前主表字段：`id, org_id, org_name, case_no, case_title, amount, court, event_date, status, create_time, update_time`
- Python 查询字段：`dishonest_id, case_no, exec_court, legal_obligation, fulfillment_status, dishonest_behavior, publish_date, filing_date, is_history, org_id`
- 当前缺少的查询字段：`dishonest_behavior, dishonest_id, exec_court, filing_date, fulfillment_status, is_history, legal_obligation, publish_date`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [选择] 采用设计富字段  [ ] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, dishonest_id, org_id, org_name, case_no, case_title, amount, court, event_date, status, dishonest_behavior, exec_court, filing_date, fulfillment_status, is_history, legal_obligation, publish_date, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：dishonest_id 是唯一键
- 事件日期字段：publish_date
- 备注：

### 3.3 `executed` → `risk_executed`

- 当前主表字段：`id, org_id, org_name, case_no, case_title, amount, court, event_date, status, create_time, update_time`
- Python 查询字段：`exec_person_id, case_no, exec_court, exec_status, exec_target, filing_date, is_history, org_id`
- 当前缺少的查询字段：`exec_court, exec_person_id, exec_status, exec_target, filing_date, is_history`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [选择] 采用设计富字段  [ ] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, org_id, org_name, case_no, case_title, amount, court, event_date, status,exec_court, exec_person_id, exec_status, exec_target, filing_date, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：org_id+case_no+exec_person_id是唯一键
- 事件日期字段：filing_date
- 备注：

### 3.4 `limit_high` → `risk_limit_high`

- 当前主表字段：`id, org_id, org_name, case_no, case_title, court, event_date, status, create_time, update_time`
- Python 查询字段：`xhfgk_id, rhc_person_name, case_no, filing_date, doc_url, is_history, org_id`
- 当前缺少的查询字段：`doc_url, filing_date, is_history, rhc_person_name, xhfgk_id`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [选择] 采用设计富字段  [ ] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, org_id, org_name, case_no, case_title, court, person_name, filing_date, status, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：case_id 是唯一键；入仓时将原 `xhfgk_id` 直接写入 case_id
- 事件日期字段：filing_date
- 备注：rhc_person_name->person_name；doc_url 不保留；按二次复核结论保留 filing_date 和 is_history

### 3.5 `lawsuit` → `risk_lawsuit`

- 当前主表字段：`id, case_id, case_no, case_title, case_reason, court, amount, event_date, create_time, update_time`
- Python 查询字段：`judgment_doc_id, case_no, case_type, court_name, trial_procedure, judgment_date, publish_date, case_cause, doc_title`
- 当前缺少的查询字段：`case_cause, case_type, court_name, doc_title, judgment_date, judgment_doc_id, publish_date, trial_procedure`
- Party 表：`risk_lawsuit_party`
- 当前 Party 字段：`id, case_id, org_id, party_name, party_role, create_time`
- Python 所需 Party 字段：`judgment_doc_id, org_id, party_role, is_history`
- 当前 Party 缺少：`is_history, judgment_doc_id`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, case_no, case_type, case_title, judgment_date, publish_date, case_reason, court, amount, case_cause, create_time, update_time`
- Party 表最终字段（如有）：`id, case_id, org_id, party_name, party_role, is_history, create_time`
- 主外键/唯一业务 ID：case_id
- 事件日期字段：judgment_date
- 备注：judgment_doc_id->case_id

### 3.6 `court_filed` → `risk_court_filed`

- 当前主表字段：`id, case_id, case_no, case_title, court, event_date, create_time, update_time`
- Python 查询字段：`case_unique_id, case_no, case_cause, trial_procedure, case_status, filing_date, closing_date, hearing_date, court_name`
- 当前缺少的查询字段：`case_cause, case_status, case_unique_id, closing_date, court_name, filing_date, hearing_date, trial_procedure`
- Party 表：`risk_court_filed_party`
- 当前 Party 字段：`id, case_id, org_id, party_name, party_role, create_time`
- Python 所需 Party 字段：`case_unique_id, org_id, party_role, is_history`
- 当前 Party 缺少：`case_unique_id, is_history`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, case_no, case_title, court, filing_date, case_status, closing_date, hearing_date, create_time, update_time`
- Party 表最终字段（如有）：`id, case_id, org_id, party_name, party_role, is_history, create_time, update_time`
- 主外键/唯一业务 ID：case_id
- 事件日期字段：filing_date
- 备注：

### 3.7 `court_notice` → `risk_court_notice`

- 当前主表字段：`id, case_id, case_no, court, event_date, create_time, update_time`
- Python 查询字段：`notice_id, case_no, case_cause, court_name, hearing_date`
- 当前缺少的查询字段：`case_cause, court_name, hearing_date, notice_id`
- Party 表：`risk_court_notice_party`
- 当前 Party 字段：`id, case_id, org_id, party_name, party_role, create_time`
- Python 所需 Party 字段：`notice_id, org_id, party_role, is_history`
- 当前 Party 缺少：`is_history, notice_id`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, case_no, court, case_cause, hearing_date, case_title, context, create_time, update_time`
- Party 表最终字段（如有）：`id, case_id, org_id, party_name, party_role, is_history, create_time, update_time`
- 主外键/唯一业务 ID：case_id
- 事件日期字段：hearing_date
- 备注：

### 3.8 `court_announcement` → `risk_court_announcement`

- 当前主表字段：`id, case_id, case_no, court, event_date, create_time, update_time`
- Python 查询字段：`notice_id, notice_name, notice_type, case_no, court_name, notice_date, publish_date`
- 当前缺少的查询字段：`court_name, notice_date, notice_id, notice_name, notice_type, publish_date`
- Party 表：`risk_court_announcement_party`
- 当前 Party 字段：`id, case_id, org_id, party_name, party_role, create_time`
- Python 所需 Party 字段：`notice_id, org_id, party_role, is_history`
- 当前 Party 缺少：`is_history, notice_id`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, case_title, context, case_no, notice_type, court, notice_date, publish_date, create_time, update_time`
- Party 表最终字段（如有）：`id, case_id, org_id, party_name, party_role, is_history, create_time, update_time`
- 主外键/唯一业务 ID：case_id
- 事件日期字段：publish_date
- 备注：court_name->court；case_title->notice_name；context 保留

### 3.9 `equity_freeze` → `risk_equity_freeze`

- 当前主表字段：`id, org_id, org_name, case_no, amount, court, event_date, status, create_time, update_time`
- Python 查询字段：`judicial_assist_id, executed_person, equity_amount, exec_court, type_status, status, is_history, org_id`
- 当前缺少的查询字段：`equity_amount, exec_court, executed_person, is_history, judicial_assist_id, type_status`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, org_id, org_name, case_no, executed_person, amount, court, event_date, status, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：case_id 是唯一键；入仓时将原 `judicial_assist_id` 直接写入 case_id
- 事件日期字段：无；当前 Python 配置不按日期排序
- 备注：

### 3.10 `equity_pledge` → `risk_equity_pledge`

- 当前主表字段：`id, org_id, org_name, case_no, amount, pledgee, event_date, status, create_time, update_time`
- Python 查询字段：`pledge_id, reg_no, pledgor, pledgee, equity_amount, pledge_reg_date, status, is_history, org_id`
- 当前缺少的查询字段：`equity_amount, is_history, pledge_id, pledge_reg_date, pledgor, reg_no`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, org_id, org_name, case_no, reg_no, amount, pledgor, pledgee, equity_amount, pledge_reg_date, status, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：case_id
- 事件日期字段：pledge_reg_date
- 备注：

### 3.11 `zhongben` → `risk_zhongben`

- 当前主表字段：`id, org_id, org_name, case_no, amount, court, event_date, status, create_time, update_time`
- Python 查询字段：`case_no, exec_court, filing_date, termination_date, exec_target_amount, unfulfilled_amount, is_history, org_id`
- 当前缺少的查询字段：`exec_court, exec_target_amount, filing_date, is_history, termination_date, unfulfilled_amount`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, org_id, org_name, case_no, filing_date, termination_date, exec_target_amount, court, unfulfilled_amount, status, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：org_id+case_no 是唯一键
- 事件日期字段：filing_date
- 备注：exec_court->court

### 3.12 `chattel_mortgage` → `risk_chattel_mortgage`

- 当前主表字段：`id, org_id, org_name, reg_no, amount, mortgagee, event_date, status, create_time, update_time`
- Python 查询字段：`reg_no, reg_date, reg_org, guarantee_type, guarantee_amount, guarantee_scope, public_date, status, is_history, org_id`
- 当前缺少的查询字段：`guarantee_amount, guarantee_scope, guarantee_type, is_history, public_date, reg_date, reg_org`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, org_id, org_name, reg_no, amount, mortgagee, reg_date, reg_org, guarantee_type, guarantee_amount, status, guarantee_scope, public_date, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：org_id+reg_no
- 事件日期字段：reg_date
- 备注：

### 3.13 `judicial_sale` → `risk_judicial_sale`

- 当前主表字段：`id, case_id, case_no, subject_matter, amount, court, event_date, create_time, update_time`
- Python 查询字段：`notice_id, notice_name, asset_disposal_unit, notice_time, auction_start_date, auction_end_date, source_website, original_link`
- 当前缺少的查询字段：`asset_disposal_unit, auction_end_date, auction_start_date, notice_id, notice_name, notice_time, original_link, source_website`
- Party 表：`risk_judicial_sale_party`
- 当前 Party 字段：`id, case_id, org_id, party_name, party_role, create_time`
- Python 所需 Party 字段：`notice_id, org_id, party_role, is_history`
- 当前 Party 缺少：`is_history, notice_id`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, case_no,notice_name, notice_time,asset_disposal_unit,subject_matter, amount, court,auction_start_date, auction_end_date, create_time, update_time`
- Party 表最终字段（如有）：`id, case_id, org_id, party_name, party_role, is_history, create_time, update_time`
- 主外键/唯一业务 ID：case_id
- 事件日期字段：notice_time
- 备注：notice_id->case_id

### 3.14 `bankruptcy` → `risk_bankruptcy`

- 当前主表字段：`id, case_id, case_no, court, event_date, create_time, update_time`
- Python 查询字段：`case_no, case_type, handling_court, public_date`
- 当前缺少的查询字段：`case_type, handling_court, public_date`
- Party 表：`risk_bankruptcy_party`
- 当前 Party 字段：`id, case_id, org_id, party_name, party_role, create_time`
- Python 所需 Party 字段：`case_no, org_id, party_role, is_history`
- 当前 Party 缺少：`case_no, is_history`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, case_no, case_type, court, public_date, create_time, update_time`
- Party 表最终字段（如有）：`id, case_id, org_id, party_name, party_role, is_history, create_time, update_time`
- 主外键/唯一业务 ID：case_id
- 事件日期字段：public_date
- 备注：

### 3.15 `abnormal` → `risk_abnormal`

- 当前主表字段：`id, org_id, org_name, reason, decision_org, event_date, status, create_time, update_time`
- Python 查询字段：`abnormal_id, abn_date, remove_date, reason, is_history, org_id`
- 当前缺少的查询字段：`abn_date, abnormal_id, is_history, remove_date`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, org_id, org_name, reason, decision_org, abn_date, remove_date, status, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：case_id
- 事件日期字段：abn_date
- 备注：

### 3.16 `punishment` → `risk_punishment`

- 当前主表字段：`id, org_id, org_name, doc_no, reason, amount, decision_org, event_date, status, create_time, update_time`
- Python 查询字段：`penalty_id, decision_no, penalty_date, public_date, fine_amount, confiscate_amount, penalty_reason, is_history, org_id`
- 当前缺少的查询字段：`confiscate_amount, decision_no, fine_amount, is_history, penalty_date, penalty_id, penalty_reason, public_date`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, org_id, org_name, doc_no, reason, fine_amount, confiscate_amount, decision_org, penalty_date, public_date, status, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：case_id+org_id
- 事件日期字段：penalty_date
- 备注：

### 3.17 `illegal` → `risk_illegal`

- 当前主表字段：`id, org_id, org_name, reason, decision_org, event_date, status, create_time, update_time`
- Python 查询字段：`sv_id, abn_date, remove_date, reason, is_history, org_id`
- 当前缺少的查询字段：`abn_date, is_history, remove_date, sv_id`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, org_id, org_name, reason, decision_org, abn_date, remove_date, status, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：case_id
- 事件日期字段：abn_date
- 备注：

### 3.18 `tax_punish` → `risk_tax_punish`

- 当前主表字段：`id, org_id, org_name, doc_no, reason, amount, event_date, status, create_time, update_time`
- Python 查询字段：`tax_vio_id, case_no, publish_date, tax_vio_type, is_history, org_id`
- 当前缺少的查询字段：`case_no, is_history, publish_date, tax_vio_id, tax_vio_type`

**请补充**

- 最终结论：`[ ] 保留现库精简结构  [ ] 采用设计富字段  [选择] 合并调整  [ ] 删除不用`
- 主表最终字段：`id, case_id, org_id, case_no, reason, amount, publish_date, tax_vio_type, status, is_history, create_time, update_time`
- Party 表最终字段（如有）：
- 主外键/唯一业务 ID：case_id
- 事件日期字段：publish_date
- 备注：

## 4. 缺失表候选结构（从现有代码复原）

以下不是最终 DDL，只是保证当前稳定 API 能查询所需的最小候选结构。请在逐表确认后再进入正式 DDL。

### 4.1 `shenzhen_enterprise_summary`

证据：DWD 设计 v2.5 已有完整 9 字段定义；Python 的 KPI、增长趋势、产业分布 SQL 与该设计一致。

```sql
CREATE TABLE `shenzhen_enterprise_summary` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `stat_type` VARCHAR(50) NOT NULL,
  `dim_code` VARCHAR(100) NOT NULL,
  `dim_name` VARCHAR(255) NOT NULL,
  `stat_year` INT NOT NULL DEFAULT 0,
  `stat_value` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_sz_summary` (`stat_type`, `dim_code`, `stat_year`, `stat_date`),
  KEY `idx_sz_summary_latest` (`stat_type`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

人工补充：

- 是否采用：采用
- 字段调整：
- 索引调整：
- 备注：创建表

### 4.2 `enterprise_distribution`

证据：API 文档定义四维分布语义；Python SQL 明确读取 7 个业务字段。`ratio` 由 Python 根据 count 计算，不必入表。

```sql
CREATE TABLE `enterprise_distribution` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `dimension` VARCHAR(20) NOT NULL,
  `region_type` VARCHAR(20) NOT NULL DEFAULT 'standard',
  `parent_region_id` VARCHAR(20) NULL,
  `region_id` VARCHAR(20) NOT NULL,
  `region_name` VARCHAR(100) NOT NULL,
  `enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `new_enterprise_count` BIGINT NOT NULL DEFAULT 0,
  `stat_date` DATE NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ent_distribution` (`dimension`, `region_type`, `region_id`, `stat_date`),
  KEY `idx_ent_distribution_parent` (`dimension`, `region_type`, `parent_region_id`, `stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

人工补充：

- 是否采用：采用
- 字段调整：
- 唯一键是否需要包含 parent_region_id：不需要
- 备注：

## 5. `sz_city_benchmark` 去前缀结论

- Python 确实使用该表：`gkx_search_service/views/sz_status.py::_load_benchmark_rows`。
- 当前表：`dwd_sz_city_benchmark`。
- 按 human 决策，代码目标表名改为 `sz_city_benchmark`。
- DBA 仍需执行表重命名或创建无前缀同结构表；在此之前接口会显式报缺表。

人工补充：

- DBA 处理方式：`[选择] RENAME TABLE  [ ] 新建并迁移  [ ] 其他`
- 执行时间：
- 备注：

## 6. 完成条件

- [x] 第 2 节所有非风险表已填写最终结论
- [x] 第 3 节 18 类风险表已填写最终结论
- [x] 两张缺失表候选结构已确认或修订
- [x] `sz_city_benchmark` 表名处理已确认
- [x] 依据本清单从头生成正式 MySQL DWD 表结构设计文档：`agent-delivery/data/data-design/企业/DWD表结构设计-企业模块-MySQL-v3.0.md`
- [x] human 已确认 v3.0 正式候选，Python Repository/SQL 边界已实施最终字段映射

## 7. AI 审核记录与最终结论（2026-08-03）

> 本节只记录冲突和缺口，不修改 human 已填写结论。

### 7.1 已补充的漏项

- `risk_equity_pledge` 已由 human 补充为“合并调整”，最终业务 ID 为 `case_id`。

### 7.2 唯一键与所选设计冲突

以下表选择了“采用设计”，但填写的唯一键少了设计中的维度。如果按当前填写建唯一键，会覆盖不同维度或不同统计周期的数据：

- `enterprise_region_summary`
  - 已填：`region_code + stat_date`
  - 设计：`region_id + region_type + stat_date`
  - 另需确认字段名使用 `region_id`，而不是已废弃的 `region_code`
- `enterprise_industry_distribution`
  - 已填：`region_id + chain_code`
  - 设计：`region_id + chain_code + stat_date`
- `enterprise_growth_trend`
  - 已填：`region_id + stat_date`
  - 设计：`region_id + stat_year + stat_month + stat_date`
- `enterprise_industry_summary`
  - 已填：`chain_code + stat_date`
  - 设计：`chain_code + stat_year + stat_date`
- `enterprise_stat_summary`
  - 已填：`stat_type + stat_year`
  - 设计：`stat_type + dim_code + stat_year + stat_date`
- `enterprise_type_scale_stats`
  - 已填：`company_type + stat_date`
  - 所选最终字段至少存在 `enterprise_scale + region_level + region_id` 三个额外维度
  - 候选完整键：`company_type + enterprise_scale + region_level + region_id + stat_date`
- `enterprise_distribution`
  - 第 4.2 节已确认采用候选 DDL，候选 DDL 含 `stat_date`
  - 第 2.11 节手填最终字段未列 `stat_date`
  - 需确认是否以第 4.2 节完整候选 DDL 为准

### 7.3 风险表 `is_history` 口径未统一

当前 Python 风险接口使用 `is_history` 区分当前/历史记录。已填写最终字段中多数没有 `is_history`，部分表保留：

- 明确保留：`risk_dishonest`、`risk_executed`
- 明确要求删除：`risk_limit_high`
- 其余多表最终字段未列出 `is_history`

需统一确认以下一种规则：

1. 所有单企业风险主表保留 `is_history`；
2. 由 `status` 推导 `is_history`，并给出状态映射；
3. 取消当前/历史语义，同时调整 Python 内部统计逻辑，但 Java API 字段仍保持不变。

Human 复核结论（2026-08-03）：选择第 1 项，按设计保留 `is_history`，Python 直接读取；该结论覆盖 `risk_limit_high` 的旧备注。主表直接关联企业时字段放在主表，主表通过 Party 关联企业时字段放在 Party 表。

### 7.4 字段清单存在重复或疑似笔误

- `risk_judicial_case`
  - `case_id case_no` 之间缺逗号
  - 选择“采用设计”，但最终字段使用 `case_type`、`is_deleted`；Python/设计使用 `case_type_tag`、`is_history`
- `risk_dishonest`
  - `dishonest_id` 重复两次
- `risk_lawsuit`
  - `event_date` 重复两次
- `risk_chattel_mortgage`
  - `status` 重复两次
- `risk_abnormal`
  - 新增 `case_id`，但未说明来源；设计业务 ID 为 `abnormal_id`
- `risk_punishment`
  - 新增 `case_id`，但未说明来源；设计业务 ID 为 `penalty_id`
- `risk_illegal`
  - 新增 `case_id`，但未说明来源；设计业务 ID 为 `sv_id`
- `risk_tax_punish`
  - 新增 `case_id`，但未说明来源；设计业务 ID 为 `tax_vio_id`
  - 最终字段 `type` 是否代表 `tax_vio_type` 尚未确认

Human 复核结论（2026-08-03）：

- `risk_judicial_case` 使用 `case_type_tag`、`is_history`。
- `risk_tax_punish` 使用 `tax_vio_type`。
- 仅在最终字段明确填写 `case_id` 的表，用 `case_id` 接收该业务原始 ID；Python 对外字段保持不变。
- `risk_court_announcement.case_title` 映射为稳定 API 的 `notice_name`，`context` 继续保留。
- 以下未进入最终 DWD 的稳定 API 字段由 Python 保留字段名并返回空值：
  - `risk_lawsuit.trial_procedure`
  - `risk_court_filed.case_cause`
  - `risk_court_filed.trial_procedure`
  - `risk_equity_freeze.type_status`
  - `risk_judicial_sale.source_website`
  - `risk_judicial_sale.original_link`
- `risk_limit_high` 与 `risk_equity_freeze` 不再保留原生 ID 字段；分别把原 `xhfgk_id`、`judicial_assist_id` 的值直接写入 `case_id`，并为 `case_id` 建唯一索引。Python 将 `case_id` 映射回原稳定 API 字段名。

### 7.5 事件日期尚未填写

除 `risk_limit_high` 明确选择 `event_date` 外，多数风险表“事件日期字段”留空。事件日期决定排序和分页稳定性，需要逐表确认；如果统一使用 `event_date`，需同时明确它由哪个源日期字段写入。

Human 复核结论（2026-08-03）：选择保留设计中的各业务日期字段，由 Python 统一映射；该结论覆盖 `risk_limit_high`、`risk_lawsuit`、`risk_court_filed`、`risk_bankruptcy` 中改为 `event_date` 的旧备注。

### 7.6 已无冲突、可以直接纳入新设计的结论

- `enterprise_patent_detail`：采用设计；唯一键 `org_id + patent_id`，`patent_id` 普通索引
- `enterprise_patent_history`：采用设计；唯一键 `org_id + data_year`
- `enterprise_invest`：采用设计；唯一键 `org_id + inv_org_id`
- `shenzhen_enterprise_summary`：采用候选 DDL
- `enterprise_distribution`：采用候选字段；唯一键不含 `parent_region_id`
- `sz_city_benchmark`：执行 `RENAME TABLE` 去掉 `dwd_` 前缀

### 7.7 Human 二次复核已确认

- 统计汇总表采用设计/候选完整复合唯一键。
- 风险表保留 `is_history`，由 Python 直接读取。
- 风险表保留各自业务日期字段，由 Python 映射到稳定 API。
- 允许清理缺逗号、重复字段等纯格式问题；本文件已清理 4 处。
- `risk_judicial_case` 使用设计/API 字段名 `case_type_tag`、`is_history`。
- `risk_tax_punish.type` 确认为 `tax_vio_type`，最终字段直接使用 `tax_vio_type`。
- 只有 human 在“最终字段”中明确写入 `case_id` 的表才使用 `case_id` 接收原业务 ID；其余表保留清单中的原生业务 ID 或复合键。Python 对外转换为 Java 已接入的稳定 API 字段。
