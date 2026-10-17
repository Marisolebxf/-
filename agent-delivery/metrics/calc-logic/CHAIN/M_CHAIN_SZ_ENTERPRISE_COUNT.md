# M_CHAIN_SZ_ENTERPRISE_COUNT 深圳产业链企业数 计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（注册地语义 + city='深圳市' 全称 + 带链参数 + 口径为准不迁就 mock）
- **类型**：STAT（去重计数）
- **is_mock**：true（链桥仅 INB1309 mock 灌数；全量挂链 CHAIN-P0-5 交付后转 live）

## 1. 原始定义档案

- **页面语境**：专题系统 · 产业链分析 · 深圳产业现状（链全景页 `CHAIN-SZ-PANORAMA`），"深圳在某条链上的家底数"。
- **白话**：挂在这条链上的企业里，注册地在深圳的有多少家。
- **旧稿三处矛盾（本版统一）**：seed v0.1.0 用「总部（headquarters_city）」+ 凭空字段/壳表（enterprise_code / dwd_org_reg_info / industry_chain_enterprise 均实测不存在）；细稿 2026-08-21 用「注册地」但走 ADS 壳聚合（chain_sz_dist/chain_sz_elements）；矩阵背书壳表路线。本版三处统一为「注册地 + 真源链桥直数」，旧 ADS 壳路线标 superseded。

## 2. 指标定义（v0.2.0）

**指定产业链链上企业中，注册地（工商主档 city）为深圳市的企业去重家数。**

- **城市语义（拍板 ①）**：注册地（非总部——总部城市库中无源）；值统一全称 `'深圳市'`（主档实测值，同 SVC 波先例）；
- **链路**：链桥 `enterprise_industry_chain(org_id, chain_code)` JOIN 主档 `dwd_org_base_info(org_id, city)`，org_id 全键（禁名称匹配，2026-10-14 通则）；
- **参数（拍板 ②）**：带 `:chain_code`（页面按链下钻，与全景页交互一致）；去链过滤即深圳全量版（本条不覆盖）；
- **与 `M_CHAIN_ENTERPRISE_COUNT` 同构**：该条为本条去 city 过滤的全国版（同去重键 org_id、同链桥真源）。

## 3. Formula（SQL）

```sql
SELECT COUNT(DISTINCT eic.org_id) AS sz_chain_enterprise_cnt
FROM demo_gkxlumenx_dwd.enterprise_industry_chain eic
JOIN demo_gkxlumenx_ods.dwd_org_base_info b
  ON b.org_id = eic.org_id AND b.is_deleted = 0
WHERE b.city = '深圳市' AND eic.chain_code = :chain_code;
```

## 4. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd.enterprise_industry_chain` | 链桥（链 + org_id） | INB1309 mock 2000 行（1984 家）；深圳×INB1309 = 1004 家（org_id→city 全键实测通）；余链 0 行 |
| `dwd_org_base_info` | 工商主档注册地 | 189,116 行 org_id 全唯一；city='深圳市' 95,600 家切片验证可用 |

## 5. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| 链桥仅 1 链 mock 灌数 | 数据未灌（DDL 在案） | 不报缺；口径为准（拍板 ③），CHAIN-P0-5 全量灌入即真数 |
| 旧稿凭空字段（headquarters_city 等） | 表名/字段漂移 | 已按真实库重写；`dwd_org_reg_info` 不存在（工商主档即 base_info） |
| ADS 壳路线（chain_sz_dist/chain_sz_elements） | mock 时代产物 | 标 superseded（拍板 ④），禁再引用 |

## 6. 验证记录（2026-10-14）

- org_id 全键链路：深圳×INB1309 = 1004 家实测通（CAST utf8mb4_0900_ai_ci 归一连通）。
- 当前不在内网，回公网/内网通道后按 §3 SQL 复跑核值；余链预期 0 + ⚠️。

## 更新记录

- 2026-08-21: 初版（模拟王惠调研，ADS 壳路线）
- 2026-10-14: v0.2.0 口径迁移（注册地 + 真源链桥直数；human:徐滕强 拍板）
