# M_SVC_PT_KEYORG_SCALE 计算细稿（重点机构规模档案值）

- 版本：v0.2.0（2026-10-13 human:徐滕强 拍板落盘）
- 任务：SVC-METRIC-COVER-STAT-L01 第 10 条；seed 版本同步 0.2.0
- 锁版承继：2026-08-28 侯佳伟 1A2A3B + 2026-10-13 徐滕强（无值显「—」；名单归 Q-01）
- 关联：M_SVC_PT_GLOBAL_SCALE_DIST（第 9 条）同名列 employees_number 写入卡面；名单来源 Q-SVCCHAIN-01（技术力 Top，唐绍祖 MODEL）

## 口径
1. 对象：重点机构名单（遴选归 Q-SVCCHAIN-01 技术力 Top，本条不定义名单）。
2. 行为：逐机构读 ADS 卡面 org_size / employees_number / operating_revenue 三字段。档案直读，非计算指标，不按本条另灌数。
3. 呈现：无值显示「—（未披露）」；禁显 0；禁注册资本顶充人数。
4. 现网：人数/营收∩圈定=0（SVC-P0-2），卡面这两格现网预期「—」；org_size 有值（仅档案展示）。

## 计算
无聚合公式。SERVE：
```sql
SELECT org_id, org_size, employees_number, operating_revenue
FROM <ads 卡面表> WHERE org_id IN (<重点机构名单>);
-- 本 ID 不出 fact/series/dist，不单独灌表
```

## 三禁
- 禁按本指标另灌数（卡面由第 9 条同名列与档案链路维护）。
- 禁无值显 0。
- 禁注册资本顶充人数显示。

## 呈现与缺口
- 无值格：「—」+ 悬停 SVC-P0-2 缺口说明。
- pending：Q-SVCCHAIN-06（卡面契约）；名单依赖 Q-SVCCHAIN-01。

## 覆盖注明
- 2026-10-13 本文件整文件覆盖旧版（2026-08-21 初版，模拟王惠调研产出：staff_count / annual_revenue_yi / scale_band 字段方案与 svc_org_profile_card 0 行调查），旧字段口径随 v0.2.0 拍板作废；更名记录见 seed version 0.1.0 → 0.2.0。
