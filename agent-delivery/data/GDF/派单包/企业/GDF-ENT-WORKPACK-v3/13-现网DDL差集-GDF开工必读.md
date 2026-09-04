# 13 — 现网 DWD 差集（GDF 开工必读）

> **工作包**：GDF-ENT-WORKPACK-v3.1.2  
> **核验日期**：2026-09-03（ADD as-built）；GDF 边界 2026-09-04 收口  
> **GDF 作业库**：只认 `gkxlumenx_ods`（贴源）+ `gkxlumenx_dwd`（洗数）。外网 `111.198.38.90:34306` = 内网 `192.168.88.43:3306`。  
> **demo**：`demo_gkxlumenx_*` 本侧对照。GDF **不连、不改、不验收**。  
> **对照真源**：本包 `10-DWD-MySQL-DDL/` + 四类分类表 `agent-handoffs/企业战略分析-ENT/DATA-ENT-DWD-ALIGN-四类分类表.md`  
> **铁律**：缺列只 `ADD`（对正式库）；现网多出来的列 **禁止 DROP**；**已有列禁止改类型**；`*__pre_v3` / `__pre_fix_*` 备份表禁止改、禁止当目标。

## 1. 本侧已落到正式库（GDF 只核 `gkxlumenx_dwd`，已有跳过）

开工前对 **正式库** 跑 `information_schema`。已存在则跳过，禁止重复 ADD。不要为了对齐去连 demo。

| 对象 | `gkxlumenx_dwd` | 说明 |
|------|-----------------|------|
| `enterprise_base.region_id` + `idx_enterprise_base_region_id` | 已加 | 恢复历史遗漏；ETL 按省市区或港澳台常量绑定 |
| `enterprise_base.enterprise_code` 可空 | 已改为可空 | 禁止为无信用代码行造码 |
| `enterprise_finance_history.total_assets` / `total_liabilities` | 已加 | 年末时点存量；ES 按年写入 `financials`，列表取最新一年 |
| `enterprise_patent_org_rel` | 已建空表 | 只写主档精确匹配到的 `org_id` |
| `enterprise_shareholder` | 已建空表 | Q-WP3-17；禁止用 supply_chain 顶 |

## 2. Wave A 源表（`gkx` live，2026-09-02）

`02` 清单 49 张施工表中，**47 张 live 已见**（标签按 `dwd_org_tech_tag` 计；并购事件表已见、P2 只贴不洗）。未见施工表：

| 承诺名 | 优先级 | live | GDF 处置 |
|--------|--------|------|----------|
| `dwd_org_industry_chain_dtl` | 待核实 | 无 | 已在 `02.pending_source_requests`；先洗 `dwd_org_industry_tags` |
| `dwd_org_tag_info` | （旧 Mapping 名） | 无 | **已改口**：贴 `dwd_org_tech_tag`（工作簿承诺名 + live 约 20 万行）。结构见下，不是逐列同构 |
| `dwd_forg_subsidiary_info` | P1 | 无 | **国外子公司洗入阻塞**；只贴已有 `forg_*`，`enterprise_forg_parent_subsidiary` 等源表到位 |
| `dwd_forg_college_org_info` | P2 | 无 | 本期不洗；与 `02` 一致 |

其余 P0/P1（含融资、专利 applicants/assignees、港澳台、招投标出库表）live 均在。

## 3. 正式库列契约（ALIGN-DDL 已落地；GDF 已有跳过）

相对 `10/` v3.1。`DATA-ENT-DWD-ALIGN-DDL-L01` 已在 **`gkxlumenx_dwd`** ADD 下表列。GDF 开工前 `SHOW CREATE` / `information_schema`：**已有跳过，禁止再 ALTER demo**。

| 表 | 正式库 as-built | GDF 洗数 |
|----|-----------------|----------|
| `enterprise_patent_detail` | v3.1 宽列已 ADD | 按 `09`；现网 `patent_name`/`publish_date`/`ipc_code` **不 DROP** |
| `enterprise_finance_history` | `main_business_revenue` / `total_profit` / `total_fixed_assets` 已 ADD | 可触发 ES `finance`；未洗行为 NULL。禁止另 ADD `pure_profit` |
| `enterprise_extra` | 七列已 ADD | 按 `09` |
| `enterprise_news` | `original_url` 已 ADD | 标题/日期/全文洗进 `title`/`publish_time`/`summary` |
| `enterprise_bid` | `project_no` 已 ADD | 标题/金额/日期洗进 `bid_title`/`bid_amount`/`event_date`；`project_no` **必洗** |
| `enterprise_invest` | **不 ADD** `inv_external_id` | 洗进 `inv_org_id`/`inv_org_name`/`invest_amount`/`invest_ratio` |
| `enterprise_patent_history` | `patent_invention_count` / `latest_patent_date` / `latest_grant_date` 已 ADD | 按 `09` |
| `enterprise_executive` | `data_source` 已 ADD | 按 `09`；不 DROP 现网列 |
| `enterprise_base` | 正式宽列已在库 | 第 4 类 KPI **不洗** |

产线洗数只认正式名。demo 若仍留 `announcement_*` / `news_*` / `inv_name`，本侧维护，**禁止 DROP**，GDF 不用管。

## 4. 现网多列（禁止当缺陷删）

正式 `enterprise_base` / 财务 / 资讯等宽于旧 `10/` 核心主档的列（含 `is_high_tech`、`revenue_latest`、`rd_investment`、`brand_score`、news `sentiment` 等）：**Q-WP3-29 (3)(4)** 已回写 v3.1，**禁止 DROP**。

- 本期 Mapping 仍只写已拍板要洗的列  
- 第 4 类（`brand_score` / `customer_concentration` / `market_share` / `core_tech_coverage` / `tech_transaction_amount`）**待核口径，本叶不洗**  
- 宽表旧列是否退役，另开书面，不在本包擅自裁

## 5. 开工顺序（完整）

1. 复核 §1 正式库已落地项；缺哪项补哪项（只动 `gkxlumenx_dwd`）。  
2. 按 §2 处理源表：标签已改口贴 `tech_tag`；仍阻塞 `forg_subsidiary` / `chain_dtl`。  
3. 对 **正式库** 按 §3 复核；已有跳过。GDF **勿连 demo**。  
4. Wave A：`gkx` → `gkxlumenx_ods` 同名镜像，勾 `05`。不管 demo。  
5. Wave B：按 `09` 洗入 **`gkxlumenx_dwd`**；未命中专利名 / 无 `org_id` 港澳台进治理清单，不造 ID。  
6. **该表 Wave B success 后**，按 `12`/`14` 一行一枪、经本侧转发 **异步触发**对应 ES 模块或图谱 op（握手见 `15`）。禁止等全库洗完再 `sync-all`；禁止 GDF 直写 ES/Nebula。关单看轮询/回执，不看「已受理」。

## 6. 本包不包含

- CDC 预填 Excel（另派）  
- Java 对外 `/ent/v1/etl/*` 与 callback（`OPEN-ENT-GDF-TRIGGER` / `CALLBACK`，见 `15` §6）  
- `OPEN-ENT-FLOW-01/04` 正式 DAG 名  
- 检索 Java / 前端改动  
- 把正式库整表重建成与 demo 逐列一致，或 DROP 同义列  
- 49 张源表字段级 Mapping 全量复验（本叶只复核 §8 已拍板项，见 `09` 头注）  
- 正式图谱 space 点名（`DATA-ENT-GRAPH-OPS-L01` 已接 `/internal` 预览；未点名、零写入 `gkx_chain`）  
