# M_CHAIN_PATENT_COUNT 产业链关联专利数 计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（全量 kind / patent_id 去重 / pbdt_year 时间轴 / 窗口作查询参数 / 量级不进口径）
- **类型**：STAT（池计数，去重计数）
- **is_mock**：true（`enterprise_patent_org_rel` 0 行待灌；灌数后转 live）

## 1. 原始定义档案

- **页面语境**：链详情页"成果资本"区池计数三件套之一（专利数 / 产品数 / 资讯数并排）——"这条链上攒了多少件专利"。
- **白话**：挂在这条链上的企业名下共有多少件专利（去重）。
- **旧稿问题**：v0.1.0 引用 `dwd.industry_chain_patent` ← ods `dwd_org_industry_chain_pat_dtl`——**两表实测均不存在**（表名漂移且断桥）；mapping 却标 ✅（乐观失实）。

## 2. 指标定义（v0.2.0）

**指定产业链链上企业关联专利的去重件数（存量池计数）。**

| 决策点 | 拍板 | 理由 |
|---|---|---|
| ① 范围 | **全量 kind**（申请+授权，不过滤） | 池计数语义；TECH_BARRIER 的 kind='B' 是"授权空白率"特殊语义，不传染本条；REG_PATENT / TECH_MATURITY 同为全量 |
| ② 去重键 | `patent_id` | 同一专利多 party_role（申请后又转让）天然只计 1 件 |
| ③ 链路 | **org_id 全键三跳**：链桥 → 关系表 → 专利主档 | 禁名称匹配（2026-10-14 通则）；申请人/权利人已结构化在 `party_role`（APPLICANT/ASSIGNEE），池计数不选边，未来细分加一个 WHERE 即可 |
| ④ 时间窗 | 默认**全量**；近 N 年 = **查询参数** | 存量池语义不写死窗口；唯一时间轴 `pbdt_year`（公开年，全量可得——未授权专利也有公开年，用授权年会漏未授权与①矛盾；与 REG_PATENT/TECH_MATURITY 同尺） |

## 3. Formula（SQL）

```sql
-- 全量版（口径本体）
SELECT COUNT(DISTINCT r.patent_id) AS chain_patent_cnt
FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
JOIN demo_gkxlumenx_dwd.enterprise_patent_org_rel r
  ON r.org_id = e.org_id
JOIN demo_gkxlumenx_ods.dwd_patent p
  ON p.patent_id = r.patent_id
WHERE e.chain_code = :chain_code;

-- 近 N 年窗口版（查询参数，不进口径）
--   追加：AND p.pbdt_year >= :stat_year - :years + 1
```

## 4. 计算模型（防混淆，2026-10-14 讨论定稿）

| 图景 | 模型 | 说明 |
|---|---|---|
| **池计数（本条）** | `COUNT(DISTINCT patent_id) WHERE 窗口条件` 一次性过滤 | 存量去重，**永不逐年累加**——同一专利持续存在，逐年统计再相加会重复计 N 次 |
| 年度新增量（趋势图，非本条） | `GROUP BY pbdt_year` 只计当年新公开 | 若页面将来要趋势图，另立指标或本条分组视图，不动本条口径 |

## 5. 执行模式建议（2026-10-14 讨论定稿）

- **总量（无窗口）**：预计算候选——每次结果一样，适合 ADS 快照（`chain_panorama` / `ads_sci_metric_summary` 先例）；
- **窗口查询（近 N 年）**：实时参数化 SQL——N 开放集合无法预计算穷举；
- 大批量预案：org_id 强制过滤走索引；必要时 ADS 按年分桶快照（近 N 年 = N 桶现加，数据工厂实现选择）。**量级评估届时用真实数据，禁用 demo 现量做决策**（2026-10-14 规则：现库数据不全，量级判断只用于验收/性能阶段，不进口径）。

## 6. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd.enterprise_industry_chain` | 链桥 | INB1309 mock 2000 行；余链 0 行跟 CHAIN-P0-5 |
| `dwd.enterprise_patent_org_rel` | 企业↔专利关系 | **0 行**（数据未灌，结构在案：patent_id/org_id/party_role/party_sequence 四元组唯一键）→ 如实 0 + ⚠️ |
| `dwd_patent` | 专利主档 | 实测 2,939,895 行（demo，不全）；pbdt_year/apdt_year/granted_number/kind 字段齐 |

## 7. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| 关系表 0 行 | 数据未灌 | 不报缺；灌数即真数 |
| 旧稿表名漂移 | 已重写 | `industry_chain_patent`/`dwd_org_industry_chain_pat_dtl` 弃 |

## 更新记录

- 2026-08-24: 初版 v0.1.0（表名漂移稿）
- 2026-10-14: v0.2.0 口径重写（human:徐滕强 拍板：全量/去重/时间轴/窗口参数化/量级不进口径）
