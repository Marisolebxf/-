# PORTAL-CMS-DWD-WRITEBACK-ENT-L01 · 企业维度：企业发展 CMS 已发布正文回写 DWD

> 任务类型：definition（定义类，不写业务仓代码）
> 执行：`agent:data-agent` · 监管 `human:徐滕强`
> 依据：`agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-企业发展.md`（**已确认**，2026-10-20）
> 实核基准：正式库 `gkxlumenx_dwd` information_schema 实查（2026-10-21 12:05，137 表）+ 企业域 DDL 快照（GDF-ENT-WORKPACK-v4/10-DWD-MySQL-DDL 三份）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（coordinator 拆单指派；2026-10-21 11:54 监管人裁定改派 data-agent 执行） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |

## 问题清单（结论先行）

**契约 12 个 CMS 字段在 `gkxlumenx_dwd` 均无现成回写目标——全部记缺口（GAP-PORTAL-CMS-ENT-01~12），无一可回写现表。**

实核三步：
1. **表名扫描**：`%star%` / `%pano%` / `%cms%` / `%roster%` / `%narrative%` → **0 张**（库共 137 表）
2. **全库富文本列扫描**（body/html/narrative/panorama/scientist/selection/positioning/reputation）→ 唯一命中 `industry_analysis_documents.body`（mediumtext）——该表是行业分析文档语料库（document_id/format/pages/file_link），GDF-CHAIN 工作包明文「六表仅对照快照、禁止 APPLY」，语义为归一化文档正文，非 CMS 运营块承载，不可挪用
3. **设计文档排除**：指标汇总表 v3.1 明文「`enterprise_star` 不再作为 DWD 指标汇总表列入（人工维护的明星企业配置名单）」——即使最像的表也被设计层否决

### 逐字段对照表（12 字段，依据契约 §2.1–§2.12、§2.14）

| # | CMS 字段（content_type） | 契约关键字段 | 目标 DWD 表/列 | 判定 |
|---|---|---|---|---|
| 1 | `star_roster_item`（明星名单） | enterprise_code / future_industry_code / selection_tag / selection_reason / list_published / basic_intro_published / standard_ref / display_alias | — 无表。`enterprise_tag`（2.1万行）是资质标签非名单；`M_ENT_STAR_ENTERPRISE_COUNT` 口径明确「COUNT(DISTINCT enterprise_code) 对 CMS 已发布名单」——指标数名单反查，不落库 | **GAP-PORTAL-CMS-ENT-01** |
| 2 | `star_selection_standard`（入选标准） | standard_name / standard_version / applicable_industry_codes[] / candidate_scope_text / confirmed_dimensions[] | — 无表；`enterprise_stat_summary` 的 stat_type 枚举无 standard 类目 | **GAP-PORTAL-CMS-ENT-02** |
| 3 | `star_product_panorama`（产品功能全景） | product_id / product_name / product_summary / impact_summary / modules[] / scenario_refs[] / case_refs[] / media_refs[] | — `enterprise_industry_product`（0 行）列仅产品基础信息，无 modules/scenario/case/media 结构；`enterprise_extra.main_prod`（text）是主数据经营范围快照非运营全景 | **GAP-PORTAL-CMS-ENT-03** |
| 4 | `star_tech_narrative`（技术优势 HTML） | body_html（html） | — 全库无 HTML 正文列（见实核第 2 步） | **GAP-PORTAL-CMS-ENT-04** |
| 5 | `star_team_strength`（团队实力 HTML） | body_html + 信封两枚授权枚举（portrait/external_link，双 authorized 才下发） | — 全库无团队/HTML 列 | **GAP-PORTAL-CMS-ENT-05** |
| 6 | `star_scientist_ratio`（科学家/核心人才比例） | ratio_percent / data_time / team_achievement / members[]（member_name/title/publish_status/两枚授权） | — 全库无 scientist/team 列；契约明文「不是指标，运营手填」，不走 metric 亦无 DWD 落点 | **GAP-PORTAL-CMS-ENT-06** |
| 7 | `star_story`（发展历程与口碑） | timeline[]（year/title/summary）/ reputation[] | — `enterprise_history_name`（78 行）是曾用名表非历程口碑；`industry_analysis_documents` 语义不符（见实核第 2 步） | **GAP-PORTAL-CMS-ENT-07** |
| 8 | `key_chain_structure`（重点企业链位结构） | structure_version / stages[]（stage_code/stage_name/upstream_of/narrative） | — 企业域无 chain structure 表；产业链侧 `industry_chain_node(_rel)` 是 INB 图谱结构层，无 narrative 运营叙述列；本契约 §1.3（L87）「图谱边由智树图谱数据给出…（Q040）」仅约束边方向，链位叙述无承接表 | **GAP-PORTAL-CMS-ENT-08** |
| 9 | `key_enterprise_set`（重点企业运营集） | key_set_items[]（enterprise_code/stage_code/relation_text/sort_order） | — `enterprise_industry_chain`（2万行）是 ETL 挂链关系（org_id/chain_code/node_id/chain_score），无 relation_text 运营叙述，粒度语义不同不可挪用 | **GAP-PORTAL-CMS-ENT-09** |
| 10 | `sz_enterprise_intro`（深圳企业介绍） | positioning / advantage_summary / expert_analysis | — 无表；`enterprise_extra.description`（text）是主数据快照非运营文案 | **GAP-PORTAL-CMS-ENT-10** |
| 11 | `sz_focus_set`（深圳重点企业圈定） | focus_set_items[]（enterprise_code/sort_order） | — 无表。overlay 库 `cms_content_sz(domain=ENT)` 为产业/园区专项（`cert` 资质列仅 SVC），语义不同且本单不改 overlay 三件套 | **GAP-PORTAL-CMS-ENT-11** |
| 12 | `display_name_alias`（展示别名） | display_alias | — `enterprise_base` 仅 enterprise_name / enterprise_name_short；`enterprise_forg_base.name_alias` 注释「机构本地名称」（英文名在 enterprise_name），语义不同 | **GAP-PORTAL-CMS-ENT-12** |

### 不回写项（契约明文排除，本单确认零回写）

- 产业生态大模型摘要（LLM 生成，不进 CMS，无 DWD 回写）
- 产业生态图谱边（智树图谱数据，口径待 Q040）
- 全部指标数字：企业总数/历年趋势/区域分布/科研人数/链上企业数/资质分布/明星数（M_ENT_STAR_ENTERPRISE_COUNT）/专利数（缺口）/研发占比/深圳计数族——走指标服务 `metric_id`，CMS 不落数

## 范围与实现

- **范围**：DoD 五条逐条兑现（见验收证据）。逐字段写目标表列；无表记缺口不新编表名；排除项确认；overlay 边界写明；definition handoff 零代码。
- **实现**：契约 §0–§7 全文精读（450 行）→ 12 字段结构抽取（含 §2.14 表单、§3 授权规则）→ 三源实核（information_schema 表/列扫描 + DDL 快照三份 + 设计排除条款）→ 逐字段判定并给出最接近表排除理由。

## 偏离说明

- 无偏离。补充：监管人 2026-10-21 11:54/11:59 裁定由 data-agent 重跑并以前作为对照材料；本文件即重跑版（独立实核，前作未提交已覆盖删除）。

## 修改内容

- 覆盖写入本 handoff（同路径替换前作）；`agent-delivery/` 零代码改动

## 产物清单

- 本文件（definition 交付物）
- 缺口登记 12 条：GAP-PORTAL-CMS-ENT-01 ~ 12（正文含逐条判定 + 最接近表排除理由）
- 架构师会签输入：若确认 CMS 正文须落 DWD，候选方向为新增统一承载表（命名如 `cms_portal_content_*` 由架构师定；含发布信封列 content_id/version/publish_status/publish_time/sort_order + 绑定键 enterprise_code+future_industry_code + 富文本/条目 JSON）。与 v5 §2.3「DWD 至多保留 CMS 外键引用」红线的取舍由架构师裁决，本单不拍板

## 验收证据

- 正式库实核（2026-10-21，read-only）：
  - `COUNT(*) information_schema.tables WHERE table_schema='gkxlumenx_dwd'` → **137**
  - 表名 `%star%|%pano%|%cms%|%roster%|%narrative%` → **0 张**
  - 全库列扫描（body/html/narrative/panorama/scientist/selection/positioning/reputation）→ 仅 `industry_analysis_documents.body`（mediumtext，行业分析文档语料，非 CMS 承载，已排除）
  - `enterprise_base` 名称列 → enterprise_name / enterprise_name_short，无 display_alias
- 设计文档佐证：指标汇总 v3.1「勿建 enterprise_star」；工商 v3.1 §6.1 `name_alias`=机构本地名称
- DoD 对照：①12 字段逐字段目标表列 ✅ ②无表记缺口不新编 ✅（12 条 GAP）③指标/LLM 摘要/图谱边零回写+只落 published ✅ ④overlay 边界+架构师会签 ✅ ⑤definition handoff 零代码 ✅

## 架构合规自检（公约 §2 铁律逐条）

1. 算法只在 Python ✅ N/A　2. 调用链 ✅ N/A　3. 图谱 Nebula ✅ 图谱边确认不回写　4. 可观测 ✅ N/A　5. CI/CD ✅ N/A　6. demo2 只读 ✅ 未动　7. 共享聚合核心 ✅ 未动　8. 数据策略 ✅ 未改指标数据　9. D8 ✅ N/A　10. D9 数据血缘 ✅ 缺口如实登记不伪闭合　11. D10 ✅ N/A　12. D12 隔离 ✅ 未动业务仓　13. D14 对象存储 ✅ 未动

## Cost 回填

- actual_tokens：约 60000
- model_used：glm-4.7（data-agent 会话）
- actual_cost：约 $0.4
- cost_warn：否

## 遗留风险

- `M_ENT_STAR_ENTERPRISE_COUNT` 口径依赖 CMS 已发布名单反查——GAP-01 不补齐则该指标无真源（现 D4 mock），data 侧已知
- CHAIN/SVC 契约为草案；ENT 依据已确认无此风险

## CI/CD

- N/A（definition 单，零代码零部署）

## 涉及文件

- `agent-delivery/agent-handoffs/平台基建-PLATFORM/PORTAL-CMS-DWD-WRITEBACK-ENT-L01.md`（本文件，覆盖重写）
