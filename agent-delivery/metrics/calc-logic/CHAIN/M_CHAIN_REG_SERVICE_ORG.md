# M_CHAIN_REG_SERVICE_ORG 服务机构（链维 / 区域维）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（池=svc_org_circle 不另造；链上=自身挂链；六类仅下钻）
- **类型**：STAT（去重计数）
- **is_mock**：true（链桥数据未灌；灌数后转 live）

## 1. 原始定义档案

- **页面语境**：专题系统 · 产业链分析 · 区域产业评价页（`CHAIN-TOPIC-REGIONAL.yaml` `row_id: TOPIC-REG-018`），主项"服务机构"，子项"支撑力叶子"；页面定义"区域内产业服务机构"；页面约束"**不映射 M_SVC_\***"（= 不复用 SVC 指标输出；**数据池复用不违反**）；A1 需规 `ALGO-CHAIN-DEEP-126`；支撑力族（政策覆盖率/融资事件同族）。
- **白话**：深圳这条链周围有多少家给产业链干活的服务机构——检测认证、知识产权、投融资、咨询等生产性服务业家数，衡量配套服务厚度。
- **SVC 域先例**：候选六类是圈定规则产物不能冒充类型轴（Q-SVC-008 / 侯佳伟 2026-08-27 拍板）；高校/院所不属服务机构口径（服务机构只有企业型主体）。

## 2. 指标定义（v0.2.0）

**指定区域内、指定产业链链上的产业服务机构去重家数。**

- **机构池（拍板 ①）**：直接用 `svc_org_circle`（SVC 圈定池，43,296 行全企业型），**绝对不另造新表**；
- **"链上"语义（拍板 ②）**：服务机构**自身挂链**（`e.org_id = c.org_id`）——不是"服务该链企业的机构"（服务关系表库中无，不造）；
- **六类候选（拍板 ③）**：`service_type_candidate`（INNOV 1384 / 空 692 / CONSULT 592 / FINANCE 501 / MKT 203 / HR 120 / IP 33）仅作下钻分桶（空档单独计），**不作准入**（Q-SVC-008）；
- 键位全 org_id（企业侧禁名称匹配，2026-10-14 通则）；
- 区域轴：主档 `city = :region_city`。

## 3. Formula（SQL）

```sql
SELECT COUNT(DISTINCT c.org_id) AS svc_org_cnt
FROM demo_gkxlumenx_dwd.svc_org_circle c
JOIN demo_gkxlumenx_ods.dwd_org_base_info b
  ON b.org_id = c.org_id AND b.is_deleted = 0 AND b.city = :region_city
JOIN demo_gkxlumenx_dwd.enterprise_industry_chain e
  ON e.org_id = c.org_id AND e.chain_code = :chain_code;

-- 六类下钻（可选，不改主计数）：
-- JOIN demo_gkxlumenx_ads.svc_org_card card ON card.org_id = c.org_id
-- GROUP BY card.service_type_candidate（空档单独一桶）
```

## 4. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd.svc_org_circle` | 机构池准入 | 43,296 行 = 43,296 唯一 org_id（全企业型）；∩深圳主档 14,033 家 |
| `dwd_org_base_info` | 主档 city 区域轴 | 189,116 行 org_id 全唯一 |
| `dwd.enterprise_industry_chain` | 链桥 | 1 行测试数据 = 数据未灌（不报缺） |
| `ads.svc_org_card` | 六类下钻维度 | service_type_candidate 分布见 §2 |

老稿表名漂移回执：`chain_institution_stat`(40 行) 为老 mock ADS，弃。

## 5. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| 链桥未灌 | 数据未灌（DWD 在案） | 不报缺；灌数后即真数（深圳候选池 14,033 家已就绪） |
| 服务关系（机构↔链上企业的服务行为） | 无源表、不造 | 口径已按"自身挂链"钉死，规避该缺口 |

## 6. 验证记录（2026-10-14）

- circle 唯一性：43,296 行 = 43,296 distinct org_id（无重复）。
- 端到端（不带链过滤）：深圳候选池 14,033 家；桥灌数后即得"深圳×指定链"真值。
