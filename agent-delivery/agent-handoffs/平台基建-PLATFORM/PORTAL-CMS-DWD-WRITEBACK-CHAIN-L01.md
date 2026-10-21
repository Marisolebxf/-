# PORTAL-CMS-DWD-WRITEBACK-CHAIN-L01 · 产业链维度：专题全景 CMS 已发布正文回写 DWD

> 任务类型：definition（定义类，不写业务仓代码）
> 执行：`agent:data-agent` · 监管 `human:徐滕强`
> 依据：`agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题全景.md`（**草案**，2026-10-20，待确认）
> 实核基准：正式库 `gkxlumenx_dwd` 实查（2026-10-21 12:05）+ 产业链 DWD v5 设计真源

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（2026-10-21 11:54 监管人裁定改派 data-agent 执行） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |

## 问题清单（结论先行）

**5 个 CMS 字段全部记缺口；其中产业介绍、发展历程两块属「设计性不回写」——v5 设计 §2.3 已明文禁止此类正文写入 DWD。**
实核：`%pano%` 表 0 张；`industry_chain_*` 14 表全列查无 body_html/intro 富文本列。v5 §2.3 原文（L94/L105）：「产业介绍（产业链/L0 产业介绍正文、图文）：**CMS 录入为唯一真源**」「**禁止**把 CMS 已录入的『产业介绍 / 发展历程』长文案再写入 DWD 形成双真源；DWD 至多保留结构化事件键或 CMS 外键引用」。

### 逐字段对照表（5 字段，依据契约 §2.1/§2.2）

| # | CMS 字段（content_type） | 契约关键字段 | 目标 DWD 表/列 | 判定 |
|---|---|---|---|---|
| 1 | `pano_industry_intro`（产业介绍） | title（否）/ body_html（是），绑定 industry_id | — v5 §2.3 明文 CMS 唯一真源。`industry_chain.description` 是**链**结构描述列（chain_id/chain_tier 同表），v5 §5.2 L317 另文「节点简介真源=node.description，CMS 不维护」——链/节点简介均归结构层，非门户产业介绍正文，不可挪用 | **GAP-PORTAL-CMS-CHAIN-01（设计性不回写）** |
| 2 | `pano_dev_history`（发展历程） | events[]（event_date/title/body_html/source_name/source_url） | — **不等于** `industry_chain_milestone_event`：v5 §5.9 L546「门户『产业发展历程』以 CMS 录入为展示真源，本表不承担门户历程正文灌数」；该表定位「可选结构化里程碑（算法/图谱引用）」，仅可经 `source_event_id`/`ext` 回指 CMS；L38「增加 phase_*（可选结构化旁路）」进一步确认分轨 | **GAP-PORTAL-CMS-CHAIN-02（设计性不回写；milestone 表禁当回写目标）** |
| 3 | `pano_sz_feature`（深圳特色优势） | title / body_html | — 无表；深圳计数族走 M_CHAIN_SZ_* 指标 | **GAP-PORTAL-CMS-CHAIN-03** |
| 4 | `pano_cluster_effect`（集群效应） | title / body_html | — 无表 | **GAP-PORTAL-CMS-CHAIN-04** |
| 5 | `pano_competitive_position`（竞争地位） | title / body_html | — 无表 | **GAP-PORTAL-CMS-CHAIN-05** |

### 禁止项确认（零覆盖、零图谱回写）

- **产业资讯**：真源 `demo_gkxlumenx_ods.dwd_industry_chain_news_info`（476 行正文可用，Step2 复核 08-10 §0/§4.8）；正式库 `industry_chain_news_event` 为归一化事件表。CMS 无资讯类型（契约 §3.1「没有资讯类型」），门户读表不走 CMS，零覆盖。客户决策清单 2026-08-25「合规交付、禁止业务使用」记录未动，上屏与否以该决策为准
- **产业链节点和边**：`industry_chain_node` / `_node_rel` / `_entity_rel` 是 INB 图谱结构层；契约 §1.1「节点和边不进 CMS」，反向亦不回写
- **指标数字**：企业数/机构数/深圳企业机构数/全球与全国区域分布（M_CHAIN_ENTERPRISE_COUNT 等 6 项）走指标服务；深圳各区计数为已注册缺口，不在本单新编

## 范围与实现

- **范围**：DoD 五条逐条兑现：5 字段逐字段目标表列；资讯禁覆盖+决策记录不动；指标/节点边零回写；缺口不新编+会签边界；definition handoff 零代码。
- **实现**：契约全文精读（182 行）→ v5 设计 §2.3/§5.2/§5.9 分轨条款定位（L94/L105/L317/L38/L546/L577 六处）→ 正式库 `%pano%` 与 `industry_chain_*` 全列实查 → 逐字段判定。

## 偏离说明

- 无偏离。补充：依据为草案，确认稿若增删字段需增量更新本对照（遗留风险已列）。

## 修改内容

- 覆盖写入本 handoff（同路径替换前作）；零代码改动

## 产物清单

- 本文件（definition 交付物）
- 缺口登记 5 条：GAP-PORTAL-CMS-CHAIN-01 ~ 05（含「设计性不回写」定性与 v5 行号引用）
- 禁止项确认：资讯表零覆盖 + 客户决策 2026-08-25 记录未动；节点/边/指标零回写

## 验收证据

- 正式库实核（2026-10-21，read-only）：`%pano%` 表 0 张；`industry_chain`（24 列）与 `industry_chain_milestone_event`（17 列）全列清单实查，无 body_html/intro 列；`industry_chain.description` 为链结构描述非正文承载
- v5 设计佐证（行号可查）：L94 产业介绍 CMS 唯一真源；L105 禁双真源禁令；L546 milestone 不承担历程正文；L317 节点简介真源=node.description
- 资讯真源佐证：CHAIN seed v0.2.0 M_CHAIN_NEWS_COUNT formula 引用 `demo_gkxlumenx_ods.dwd_industry_chain_news_info`（2026-10-14 拍板口径）
- DoD 对照：①5 字段逐字段 ✅ ②资讯零覆盖+决策记录未动 ✅ ③指标/节点边零回写+只落 published ✅ ④缺口不新编+架构师会签（含突破 v5 红线须先修设计文档的升格条款）✅ ⑤definition handoff 零代码 ✅

## 架构师会签输入（升格条款，非决策）

5 个字段均为「产业级运营正文块」（绑定 industry_id + 发布信封 + body_html/条目）。本单会签边界条款：**若架构师确认 CMS 正文须落 DWD，因 v5 §2.3（L94/L105）已明文「CMS 录入为唯一真源、禁止写入 DWD 形成双真源」，须先修订 v5 设计文档并走架构评审会签，再批本单后续回写实施**；仅批回写单而不修 v5，契约与本设计文档直接冲突。与 ENT 单的 `cms_portal_content_*` 承载表方向属同一批架构决策。本单不拍板。

## 架构合规自检（公约 §2 铁律逐条）

1. 算法只在 Python ✅ N/A　2. 调用链 ✅ N/A　3. 图谱 Nebula ✅ 节点/边零回写　4. 可观测 ✅ N/A　5. CI/CD ✅ N/A　6. demo2 只读 ✅ 未动　7. 共享聚合核心 ✅ 未动　8. 数据策略 ✅ 未改指标　9. D8 ✅ N/A　10. D9 ✅ 缺口如实登记　11. D10 ✅ N/A　12. D12 ✅ 未动业务仓　13. D14 ✅ 未动

## Cost 回填

- actual_tokens：约 50000
- model_used：glm-4.7（data-agent 会话）
- actual_cost：约 $0.3
- cost_warn：否

## 遗留风险

- 依据草案：product-agent 确认稿发布后本对照表需增量核对
- milestone 表 `ext.cms_block_id` 回指通道已预留：若要做「CMS 历程 → 结构化里程碑」抽取（非正文复制）属另单，勿夹带

## CI/CD

- N/A（definition 单，零代码零部署）

## 涉及文件

- `agent-delivery/agent-handoffs/平台基建-PLATFORM/PORTAL-CMS-DWD-WRITEBACK-CHAIN-L01.md`（本文件，覆盖重写）
