# M_CHAIN_REG_RESEARCH_ORG 科研机构（链维 / 区域维）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（双桶含高校；目标桥唯一真源；过渡桥提法撤销）
- **类型**：STAT（去重计数）
- **is_mock**：true（institution 行数据未灌；灌数后转 live）

## 1. 原始定义档案

- **页面语境**：专题系统 · 产业链分析 · 区域产业评价页（`CHAIN-TOPIC-REGIONAL.yaml` `row_id: TOPIC-REG-015`），主项"科研机构"，子项"学术力叶子"；页面定义"区域内科研机构规模或密度"；页面约束"**不得用全景 INSTITUTION_COUNT 顶替**"（本条有区域维）；A1 需规 `ALGO-CHAIN-DEEP-126`；上游合成 `M_CHAIN_ACADEMIC_POWER`（学术生态）。
- **白话**：深圳这条链上挂了多少家高校和科研院所——数机构家数，衡量学术载体厚度。
- **与已定稿条目关系**：
  - `M_CHAIN_INSTITUTION_COUNT`（Seq 4 v0.2.0）：同族无区域维；本条 = 它 + `city = :region_city`；
  - `M_CHAIN_REG_PAPERS`（Seq 10 v0.2.0）：学术力族兄弟，机构桶口径同构（heis+ri 双桶、企业研究院不入桶）。

## 2. 指标定义（v0.2.0）

指定区域内、指定产业链链上的**高校+科研院所去重家数**。

- 机构桶：`dwd_org_heis_info` ∪ `dwd_research_institute_base_info`（拍板 ①：双桶都包含）；`××研究院有限公司` 等企业法人研究院不入桶（归 ENTERPRISE 口径）；
- 去重键：`org_id`；
- 区域轴：机构主档自身 `city`（两表原生列，不经企业主档）；
- 挂链：`industry_chain_entity_rel`（`entity_type='institution'` + `chain_id`）**唯一真源**（拍板 ②：结构真实、数据未灌不报缺）；
- **键位规则（2026-10-14 复核更正）**：`entity_id` 按 entity_type **分键**（真源 `data-design/storage/CHAIN/etl/pipeline-ent-hang.md` §0 + `ods-to-dwd-mapping.md` §1.2/§5）：
  - `enterprise` = **org_id**（已冻结硬规则；credit 对不上 org_id → drop）
  - `product` = `p:{credit_code}:{行id}`（明知的 Demo 合成键，产品 UID 未冻待换；李伟 2026-08-28 明令禁当主键）
  - `institution` = **设计未冻结**——机构挂链灌数方案出台时定键（CHAIN-P0-6 在问）；本条口径预填 org_id 语义（对齐机构主档，与图谱 inst: 族 VID 取值先例自洽），灌数时若定其他键需回改本条 JOIN。

## 3. Formula（SQL）

```sql
SELECT COUNT(DISTINCT r.entity_id) AS research_org_cnt
FROM demo_gkxlumenx_dwd.industry_chain_entity_rel r
JOIN (
  SELECT org_id, city FROM demo_gkxlumenx_ods.dwd_org_heis_info WHERE is_deleted = 0
  UNION
  SELECT org_id, city FROM demo_gkxlumenx_ods.dwd_research_institute_base_info WHERE is_deleted = 0
) inst ON inst.org_id = r.entity_id
WHERE r.entity_type = 'institution'
  AND r.is_deleted = 0
  AND r.chain_id = :chain_code
  AND inst.city = :region_city;
```

> 2026-10-14 修正记录：首版沿 G2 证据卡建议稿写了"过渡桥版（dwd_org_industry_tags）"。human:徐滕强 指正后核实：tags 是**企业**产业标签表（company_name+credit_code 打产业标签），机构主档与其 credit_code↔external_id 匹配 0——与本指标无关，过渡桥提法**撤销**，演示路径不留防误导。

## 4. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_org_heis_info` | 高校桶 + 区域轴 | 3,501 行；深圳 16 |
| `dwd_research_institute_base_info` | 院所桶 + 区域轴 | 2,074 行；深圳 1,014（demo 灌数深圳占比高，如实采数） |
| `dwd.industry_chain_entity_rel` | 机构挂链唯一真源 | 319 行全部 `product`；institution 0 行 = **数据未灌**（表结构在案 25 列，非缺口） |
| ~~`dwd_org_industry_tags`~~ | ~~过渡桥~~（撤销） | 企业产业标签表，与机构挂链无关 |

## 5. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| `industry_chain_entity_rel` institution 0 行 | **数据未灌**（DDL 在案；institution 键位设计未冻结，灌数方案出台时定键） | 先不管、不报缺、不挂号；灌数后即真数 |
| 机构↔链挂接供应方交付计划 | 既有号 CHAIN-P0-6 在册（Seq 4 开题） | 本条不重复挂号，仅语义关联注记 |

## 6. 验证记录（2026-10-14）

- 端到端：institution 0 行 → 真数 0（如实展示）；灌数后 = 该链挂链机构 ∩ 深圳高校 16 ∪ 院所 1,014 的去重子集。
- 键位格式：product 行 entity_id 样例 `p:91440300MA5EQK3B7X:1`（Demo 合成键）——佐证键位约定必须显式钉死。
