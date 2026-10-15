# M_CHAIN_REG_PATENT 专利（链维 / 区域维）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（org_id 全键版，名称匹配路径废止；缺口分型修正：数据未灌 ≠ 结构性缺失）
- **类型**：STAT（去重计数）
- **is_mock**：true（数据未灌；灌数后转 live）

## 1. 指标定义

指定区域内、指定产业链**链上企业**的专利去重件数。

- **企业关联必须 org_id**（2026-10-14 拍板）：链桥 `enterprise_industry_chain.org_id` → 主档 `dwd_org_base_info.org_id` → 专利关系 `enterprise_patent_org_rel.org_id`，全链结构化键；**禁止** `company_name ↔ first_applicant_name/first_current_assignee_name` 名称匹配。
- 去重键：`patent_id`（天然防同一专利多 party_role 双计）。
- `kind` / `party_role` / `pbdt_year` 均为**下钻维度**，不进口径本体；不限发明专利，不要求 granted_number 非空（公开年口径防右截断）。
- 区域过滤：`b.city = :region_city`。

## 2. Formula（SQL）

```sql
SELECT COUNT(DISTINCT r.patent_id) AS patent_cnt
FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
JOIN demo_gkxlumenx_ods.dwd_org_base_info b
  ON b.org_id = e.org_id AND b.is_deleted = 0 AND b.city = :region_city
JOIN demo_gkxlumenx_dwd.enterprise_patent_org_rel r
  ON r.org_id = e.org_id
JOIN demo_gkxlumenx_ods.dwd_patent p
  ON p.patent_id = r.patent_id AND p.is_deleted = 0
WHERE e.chain_code = :chain_code;
```

- 六连接键（e.org_id / b.org_id / r.org_id / e.chain_code / r.patent_id / p.patent_id）实测 collation 全部 `utf8mb4_general_ci` 同序，**无需 COLLATE**。
- **collation 全局规约**（2026-10-14 human:徐滕强）：后续遇不对齐的，统一 `ALTER` 成 `utf8mb4_0900_ai_ci`；**demo 库 / 正式库 / 设计文档三同步**。
- 库现状基线（2026-10-14 information_schema 实测）：`demo_gkxlumenx_dwd` 三序并存（0900 927 / general 197 / unicode 52 列）；`demo_gkxlumenx_ods` 四序并存（0900 1999 / general 849 / bin 505 / unicode 409 列）；正式 `gkxlumenx_ods` 仅 general 44 列。三同步属 DDL 治理任务，不随单指标走。

## 3. 表依赖与实核（2026-10-14 demo 库）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_patent` | 分子（patent_id 去重） | 2,939,895 行，patent_id 全唯一；真实数据族（华为 79,089 / 比亚迪 28,923 / 华南理工 27,597 …） |
| `dwd_org_base_info` | 主档（org_id 直连 + city 区域轴） | 189,116 行，org_id 全非空唯一（32 位 hex） |
| `dwd.enterprise_industry_chain` | 链桥（chain_code + org_id） | DWD 在案表；demo 仅 1 行测试数据（INB1309，2026-10-14 灌入） |
| `dwd.enterprise_patent_org_rel` | 专利↔组织关系（org_id↔patent_id + party_role/match_type） | DWD 在案表（human:徐滕强 2026-10-14 确认）；当前 0 行 |

弃用回执：`dwd_org_industry_chain_pat_dtl`（老稿 888 行）现网已不存在（2026-09-03 human:李伟 裁定弃用，CHAIN-P1-1 关闭）；名称匹配版方案（兄弟条目先例）经 2026-10-14 拍板**废止**，不落 formula。

## 4. 缺口分型（2026-10-14 拍板修正）

| 项 | 分型 | 处置 |
|---|---|---|
| `enterprise_patent_org_rel` 0 行 | **数据未灌**（DWD 在案表、结构齐备、org_id 键位对齐——非结构性缺失） | **先不管、不报缺、不挂缺口号**；灌数后即出真数 |
| 链桥 `enterprise_industry_chain` 仅 1 行测试数据 | 数据未灌（同上） | 同上 |

> 2026-10-14 修正记录：首版误将 0 行判为"结构性缺失"并挂 ENT-P0-6 + CHAIN-P0-5。human:徐滕强 指正：两张表都是 DWD 在案的专利↔企业关联表/链桥，0 行是灌数问题。已撤销缺口号挂载；CHAIN-P0-5（挂链业务日期）/P0-6（机构挂链）语义另属 NEW_COUNT / INSTITUTION_COUNT 侧，与本指标无关。

## 5. 关联条目注记

- 已定稿兄弟条目 `M_CHAIN_REG_TECH_MATURITY` / `M_CHAIN_TECH_POWER` / `M_CHAIN_TECH_BARRIER` 仍为名称匹配口径，与本拍板冲突——**不在本轮 39 条覆盖范围**，复审时统一切 org_id 全键链路，本轮不动。
- `M_CHAIN_REG_PAPERS` 中学者↔机构 `scholar_org_name_zh = name_cn` 属机构侧名称匹配，已带 org_id 升级注记（待供方结构化映射），维持不动。

## 6. 验证记录（2026-10-14）

- 端到端：当前数据未灌 → 真数 0（如实展示）；DWD 回填灌数后即出真数。
- collation：六连接键 information_schema 逐列实核同序；名称匹配路径曾触发 `Illegal mix of collations`（0900 vs general），已随路径废止出清。
