# M_CHAIN_PRODUCT_COUNT 产业链关联产品数 计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（product_name 直数 / industry_code 等值匹配 / 无时间窗 / 字面去重先不考虑）
- **类型**：STAT（池计数）
- **is_mock**：true（demo 169 行小样本；全量交付跟 CHAIN-P0-5）

## 1. 原始定义档案

- **页面语境**：链详情页"成果资本"区池计数三件套之二（专利/产品/资讯并排）——"这条链上有多少种产品"。
- **白话**：链上企业在产品标签里报过的产品名，去掉重复后数种数。
- **旧稿问题**：v0.1.0 引用 `dwd.industry_chain_product` ← ods `dwd_org_industry_chain_prod_dtl`——**两表实测均不存在**（表名漂移）；mapping 标 ✅ 失实。

## 2. 指标定义（v0.2.0）

**指定产业链（industry_code = :chain_code 等值）下，链上企业报的产品名去重种数。**

| 决策点 | 拍板 | 说明 |
|---|---|---|
| ① 数法 | `COUNT(DISTINCT product_name)` 直数 | `product_top5` 是"前5产品"拼接字段，与 product_name 同产品两种记法，拆分去重数字虚高且依赖分隔符稳定性——不拆 |
| ② 挂链键 | `industry_code = :chain_code` **纯等值** | INB 产业链码（4 位，与 `dwd.industry_chain` L1 行同编码空间）；**查询层禁 LIKE 迁就脏数据**（2026-10-14 拍板） |
| ③ 去重粒度 | product_name 字面值 | 自由文本无标准编码，同产品异写算两个——**拍板先不考虑**；供应方交付 `product_id` 时升级去重键 |
| ④ 时间窗 | 无（全量快照） | 产品标签无时间字段；不同于专利（pbdt_year）/资讯（publish_date），如实注记 |

## 3. Formula（SQL）

```sql
SELECT COUNT(DISTINCT t.product_name) AS chain_product_cnt
FROM demo_gkxlumenx_ods.dwd_org_industry_product_tags t
WHERE t.is_deleted = 0
  AND t.industry_code = :chain_code;
```

## 4. 数据质量注记（不进口径，登记治理）

| 项 | 现状 | 处置 |
|---|---|---|
| **列表字面量脏数据** | live 实测 `industry_code` 存过 Python 列表字面量（`['INB1333','INB1306']`），等值匹配会漏数 | **ETL 入仓清洗待办**：洗成多行（一链一行）或规范 JSON——治理在上游，公式不迁就 |
| 值域覆盖率 | demo 169 行 ↔ `industry_chain.chain_id` 比对未跑 | **数据质量参考项，不影响口径成立**（拍板 ③）：等值语义对，库里有数多少，不因覆盖不全改口径 |
| 前缀下钻预留 | INB 码层级为前缀关系（`INB170101` = `INB1701` 的环节码） | 未来"链含环节"下钻用 `LIKE CONCAT(:chain_code,'%')` 前缀匹配，禁双边 `%` |

## 5. 执行模式建议

总量池计数、每次结果一样 → **预计算候选**（ADS 快照）；无窗口参数化需求（无时间轴），单轨预计算即可。

## 6. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_org_industry_product_tags` | 唯一活源（产品名 × 链码） | demo 169 行（industry_link_code/industry_code/company_name/credit_code/product_name/product_top5）；live 约 8,000 行；169 行↔chain_id 值域比对待跑 |

## 7. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| demo 169 行小样本 | 数据未灌全 | 跟 CHAIN-P0-5 全量交付；口径不动 |
| 列表字面量 | 上游脏数据 | ETL 清洗待办（见 §4），不报结构性缺表 |
| 旧稿表名漂移 | 已重写 | `industry_chain_product` / `dwd_org_industry_chain_prod_dtl` 弃 |

## 更新记录

- 2026-08-24: 初版 v0.1.0（表名漂移稿）
- 2026-10-14: v0.2.0 口径重写（human:徐滕强 拍板：直数/等值匹配/无窗口/字面去重）
