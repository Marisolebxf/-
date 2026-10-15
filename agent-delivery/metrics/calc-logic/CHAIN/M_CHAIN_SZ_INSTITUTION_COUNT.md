# M_CHAIN_SZ_INSTITUTION_COUNT 深圳产业链机构数 计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（机构=高校+科研院所、不含服务机构；org_id 去重硬修正；深圳市全称；带链参数）
- **类型**：STAT（去重计数）
- **is_mock**：true（链桥 INB1309 mock 可算；机构挂链跟 CHAIN-P0-6；全量交付后转 live）

## 1. 原始定义档案

- **页面语境**：专题系统 · 产业链分析 · 深圳产业现状（链全景页 `CHAIN-SZ-PANORAMA`），与深圳链上企业数并排的"机构家底数"——链上高校/科研院所在深圳有多少家。
- **白话**：挂在这条链上的主体里，属于高校或科研院所、且注册地在深圳的家数。
- **旧稿问题（本版硬修正）**：seed v0.1.0 = `COUNT(DISTINCT enterprise_name) WHERE org_type='机构'`——①名称去重（同名校误并、跨表无法对齐）；② `org_type` 是链桥壳表上不存在的幻字段，判型无来源；细稿旧文"科研**和服**务机构"范围漂移。

## 2. 指标定义（v0.2.0）

**指定产业链链上主体中，判型为高校或科研院所（heis ∪ research_institute 双表并集）、注册地为深圳市的 org_id 去重家数。**

- **机构范围（拍板 ①）**：高校（`dwd_org_heis_info`）+ 科研院所（`dwd_research_institute_base_info`），**不含服务机构**：
  - `svc_org_circle` 43,296 家全企业型，归 `M_CHAIN_SZ_ENTERPRISE_COUNT` / `M_CHAIN_ENTERPRISE_COUNT` 侧；并入本条会同一批 org_id 双计，破坏"机构+企业=链上主体总数"自洽；
  - 企业法人研究所（××研究院有限公司）归企业侧（2026-10-14 拍板），名称关键词不作身份判定；
  - 与全国版 `M_CHAIN_INSTITUTION_COUNT`（entity_rel 原生维）、`M_CHAIN_REG_PAPERS` / `M_CHAIN_REG_COMP_ACADEMIC`（heis∪ri 桶）四处口径自洽。
- **去重键（硬修正）**：`enterprise_name` 名称去重 → `org_id` 去重；
- **判型方式**：org_id IN (heis) OR org_id IN (ri)（双表并集，同 SVC/REG 族先例）；
- **城市/参数**：`city='深圳市'` 全称 + `:chain_code` 带参（沿用 Seq 20 三项拍板）。

## 3. Formula（SQL）

```sql
SELECT COUNT(DISTINCT eic.org_id) AS sz_chain_institution_cnt
FROM demo_gkxlumenx_dwd.enterprise_industry_chain eic
JOIN demo_gkxlumenx_ods.dwd_org_base_info b
  ON b.org_id = eic.org_id AND b.is_deleted = 0
WHERE b.city = '深圳市' AND eic.chain_code = :chain_code
  AND (eic.org_id IN (SELECT org_id FROM demo_gkxlumenx_ods.dwd_org_heis_info WHERE is_deleted = 0)
    OR eic.org_id IN (SELECT org_id FROM demo_gkxlumenx_ods.dwd_research_institute_base_info WHERE is_deleted = 0));
```

## 4. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd.enterprise_industry_chain` | 链桥 | INB1309 mock 2000 行（深圳 1004 家 org_id 全键通）；余链 0 行 |
| `dwd_org_base_info` | 注册地 city | 189,116 行 org_id 全唯一；深圳市 95,600 家 |
| `dwd_org_heis_info` | 高校判型 | REG_PAPERS 端到端验证过（深圳 heis 路径真数 1,791 篇论文） |
| `dwd_research_institute_base_info` | 院所判型 | 同上 UNION 桶验证过 |

## 5. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| 机构挂链未灌（entity_type=institution 0 行；链桥 mock 挂点全企业型） | 数据未灌 | 跟 CHAIN-P0-6（供应方交付计划已问）；当前如实 0 + ⚠️，口径为准 |
| 判型双表 org_id 命中率 | 未逐表实测（REG 族同款 JOIN 已通） | D2 标 provisional；灌数后随首跑核验 |
| 旧稿 org_type 幻字段 / 名称去重 | 表名漂移+口径硬伤 | 已重写；ADS 壳路线弃 |

## 6. 验证记录（2026-10-14）

- heis∪ri UNION 桶同款 JOIN：REG_PAPERS 深圳端到端 1,791 篇验证通过。
- org_id 全键链路：深圳×INB1309 1004 家验证通过（企业侧）；机构侧等 CHAIN-P0-6 灌数后首跑。

## 更新记录

- 2026-08-21: 初版（模拟王惠调研，org_type 幻字段+名称去重）
- 2026-10-14: v0.2.0 硬修正（heis∪ri 判型 + org_id 去重 + 不含服务机构；human:徐滕强 拍板）
