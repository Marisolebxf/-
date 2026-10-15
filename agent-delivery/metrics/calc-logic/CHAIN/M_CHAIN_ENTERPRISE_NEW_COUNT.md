# 新增关联企业数（M_CHAIN_ENTERPRISE_NEW_COUNT）

## 基本信息

- 指标ID: M_CHAIN_ENTERPRISE_NEW_COUNT / 指标名称: 新增关联企业数
- 一级模块: 产业链分析；二级模块: 产业链全景；三级模块: 全景概览
- 更新频率: 日
- 对齐状态判定: 已对齐（0.2.0；2026-10-14 human:徐滕强 拍板）
- 关联Q编号: CHAIN-P0-5（业务挂链日期源级缺失，供应方待复）

## 口径定义

年度新增挂链企业数：该年**首次**挂上链的企业去重家数。

| 项 | 锁定值 |
|---|---|
| 真源 | demo_gkxlumenx_dwd.enterprise_industry_chain |
| 去重键 | org_id（同 M_CHAIN_ENTERPRISE_COUNT） |
| 时间轴 | first_link_date（首挂业务时间；目标态字段，现无） |
| 重挂语义 | 退出后重挂不计新增（历史首挂才计 1 次） |
| 分链视图 | WHERE chain_code=:chain 后按 (org_id, chain_code) 链内首挂 |
| 当前真数 | 0 行输出（明细未供应，如实 0 + ⚠️） |

### 临时运营方案（不作口径）

首灌批全量即首挂；后续批次按 create_time 分批识别增量。禁止将 create_time 冒充业务时间写进口径本体——ODS 实核两张入站表 created_time 全部为同秒批量入库戳（2026-10-12 03:56:37），冒用会把分年塔塌缩成单日。

### 缺口上报（CHAIN-P0-5）

入站 `dwd_org_industry_tags`（104 行）/ `dwd_org_industry_product_tags`（169 行）均无业务挂链日期，且无 org_id（仅 company_name + credit_code）。已升供应方问题：① 全量挂链明细交付时是否携带挂链/打标业务日期（列名+样例 3 行）；② 若无，历史批次快照可否推首挂时间。登记于 `agent-delivery/data/third-party-source/question/产业链维度/CHAIN-SUPPLIER-QUESTIONS.md` 现行待回复区。

## 计算公式

```sql
SELECT YEAR(MIN(first_link_date)) AS stat_year, COUNT(DISTINCT org_id) AS new_cnt
FROM demo_gkxlumenx_dwd.enterprise_industry_chain
GROUP BY org_id;  -- 外层再按 stat_year 聚合
-- first_link_date 为目标态字段（现无）→ 当前 0 行输出（明细未供应）
-- 分链视图：WHERE chain_code = :chain 后按 (org_id, chain_code) 链内首挂
```

禁止：create_time 冒充业务时间；注册年分布（B 档语义偷换）；ads 壳计数；enterprise_code 去重。

## 源库表字段

dwd.enterprise_industry_chain <- ods: dwd_org_industry_tags（过渡期；业务挂链日期缺失见 CHAIN-P0-5）

## 参考文献 / 依据

CHAIN-METRIC-COVER-STAT-L01；G1 证据卡 §3；2026-10-14 human:徐滕强 拍板（临时方案 + 缺口照报）。

## 更新记录

- 2026-10-14: 0.2.0 新建口径钉死（首挂年归集 + 重挂不计 + 分链链内首挂）；开 CHAIN-P0-5；临时方案入运营注记。
