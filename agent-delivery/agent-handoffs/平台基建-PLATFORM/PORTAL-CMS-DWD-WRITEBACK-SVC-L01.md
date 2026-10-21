# PORTAL-CMS-DWD-WRITEBACK-SVC-L01 · 服务机构维度：专题服务 CMS 已发布正文回写 DWD

> 任务类型：definition（定义类，不写业务仓代码）
> 执行：`agent:data-agent` · 监管 `human:徐滕强`
> 依据：`agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题服务.md`（**草案**，2026-10-20，待确认）
> 实核基准：正式库 `gkxlumenx_dwd` 实查（2026-10-21 12:05）+ 服务机构域设计 v1 + overlay 库 `9x_gkxlumenx_cms.sql`

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

**唯一回写字段 `svc_business_domain.body_html` 在 `gkxlumenx_dwd` 无现成目标——记缺口（GAP-PORTAL-CMS-SVC-01）。**
实核：正式库 svc 域现表仅 3 张——`svc_org_circle`（10 列：org_id/rule_version/hit_fields/service_type_candidate/pending_client_confirm…，圈子准入）/ `svc_org_finance_event`（11 列，投融资事件）/ `svc_org_graph_hang`（10 列，Nebula 图谱挂载）；`svc_org_circle` 无 domain 列（LIKE '%domain%' 0 命中）。三表均无 body_html / 业务领域介绍列。设计文档 v1 的 `dwd.service_org`（38 列）为登记/标签/产品主数据，亦无富文本介绍列。

### 字段对照（1 字段，依据契约 §2.1）

| # | CMS 字段 | 契约关键字段 | 目标 DWD 表/列 | 判定 |
|---|---|---|---|---|
| 1 | `svc_business_domain`（业务服务领域） | org_id（必填）+ industry_id（必填）+ body_html（必填，html；不写人数、营收、排名） | — 无表。绑定键 org_id 在 svc 三表均存在但各有专属语义（准入/事件/图谱），无 (org_id + industry_id + 正文) 承载结构 | **GAP-PORTAL-CMS-SVC-01** |

### 排除项确认（契约 §1.5/§2.2 排除清单逐条 ✅）

机构数量（M_SVC_PT_SZ_TOTAL）、机构类型（M_SVC_PT_SZ_TYPE_DIST）、产业领域分布（M_SVC_PT_SZ_FIELD_DIST）、区域分布（M_SVC_PT_SZ_REGION_ORG）、技术力前 30 与重点名单（指标选取，CMS 不另维护）、当前人数/营收/规模（M_SVC_PT_KEYORG_SCALE）、法定名称与主要领导人（主数据）、成立时间/联系方式（主数据）——全部不从 CMS 回写，本单零触碰。

### 两条内容线划分（防实现混写）

| 内容线 | 归属 | 字段 |
|---|---|---|
| JX 内容运营中心·深圳专项 | overlay 库 `gkxlumenx_cms.cms_content_sz(domain=SVC)` | industry（varchar 服务领域枚举）/ cert / cases / evaluation（docx 扩展） |
| 门户四模块契约·专题服务 | 本单裁定对象 `svc_business_domain` | body_html（HTML 正文，绑定 org_id+industry_id） |

两线语义、载体、消费方均不同；前者本单不改（overlay 三件套边界）。

## 范围与实现

- **范围**：DoD 五条逐条兑现：只为 svc_business_domain.body_html 写目标表列（绑定 org_id+industry_id）；排除项零回写；缺口不新编；会签边界+不改 overlay；definition handoff 零代码。
- **实现**：契约全文精读（162 行）→ 正式库 svc 三表全列实查 + domain 列扫描 → 设计文档 v1 §4.1/§4.2 主表结构核对 → overlay 实文件列核对 → 判定与内容线划分。

## 偏离说明

- 无偏离。补充：依据为草案，确认稿若改字段需增量更新。

## 修改内容

- 覆盖写入本 handoff（同路径替换前作）；零代码改动

## 产物清单

- 本文件（definition 交付物）
- 缺口登记 1 条：GAP-PORTAL-CMS-SVC-01（候选新表方向：`(org_id, industry_id)` 唯一键 + body_html + 发布信封，命名由架构师定，与 ENT/CHAIN 同批裁决）
- 排除项确认清单：8 类数字/名单/主数据零回写 ✅；两条内容线划分表

## 验收证据

- 正式库实核（2026-10-21，read-only）：svc 域表清单 `%svc%|%service%` → 3 张（circle/finance_event/graph_hang）；`svc_org_circle` 列扫描 `%domain%` → 0 命中；三表全列清单见「问题清单」
- 设计文档佐证：服务机构域 v1 §4.1 仅设计 `dwd.service_org`（38 列）+ `dwd.service_org_financing`（16 列），无富文本介绍列
- overlay 实文件佐证：`repos/lumen-svc-platform/db/9x_gkxlumenx_cms.sql` `cms_content_sz`（L96-118）cert/cases/evaluation 注释明「仅 SVC」，与 JX 线语义核对无误
- DoD 对照：①只裁 body_html ✅ ②排除项零回写 ✅ ③缺口不新编+只落 published ✅ ④会签边界+不改 overlay ✅ ⑤definition handoff 零代码 ✅

## 架构合规自检（公约 §2 铁律逐条）

1. 算法只在 Python ✅ N/A　2. 调用链 ✅ N/A　3. 图谱 Nebula ✅ 未动　4. 可观测 ✅ N/A　5. CI/CD ✅ N/A　6. demo2 只读 ✅ 未动　7. 共享聚合核心 ✅ 未动　8. 数据策略 ✅ 未改指标　9. D8 ✅ N/A　10. D9 ✅ 缺口如实登记　11. D10 ✅ N/A　12. D12 ✅ 未动业务仓　13. D14 ✅ 未动

## Cost 回填

- actual_tokens：约 40000
- model_used：glm-4.7（data-agent 会话）
- actual_cost：约 $0.3
- cost_warn：否

## 遗留风险

- 依据草案：product-agent 确认稿发布后需增量核对
- JX 线 `cms_content_sz` 若后续扩展 HTML 正文列，须另开 overlay 演进单，不在本单范围

## CI/CD

- N/A（definition 单，零代码零部署）

## 涉及文件

- `agent-delivery/agent-handoffs/平台基建-PLATFORM/PORTAL-CMS-DWD-WRITEBACK-SVC-L01.md`（本文件，覆盖重写）
