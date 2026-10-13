# M_SVC_PT_SZ_TOTAL 计算细稿（深圳产业服务机构数量）

- 版本：v0.2.0（2026-10-13 human:徐滕强 确认落盘）
- 任务：SVC-METRIC-COVER-STAT-L01 第 11 条；seed 版本同步 0.2.0
- SRS 对应：05·101（5）深圳服务机构规模（数量格）
- 锁版承继：2026-08-28 侯佳伟 1A2A3B（city=深圳、series 年差、不加列、T2 同批写 fact/series）+ 2026-10-13 徐滕强（不写死 1355，数随池联动）
- 关联：M_SVC_PT_GLOBAL_TOTAL（第 6 条）同 series 年差口径；第 21 条对比页跟本条同规则同数

## 口径
1. 人口：圈定池 svc_org_circle（现池 43,296，全企业型；高校/院所不在池，第 7 条拍板）。
2. 切片：city='深圳市' 的机构去重数；数随圈定池联动，禁止写死历史值（旧 1355/1240 一律作废）。
3. 本年新增：本 ID series 按成立年相邻年差（同第 6 条 3A 口径）；缺成立年机构只进 fact 不进 series。
4. 不加列；T2 同一批写 fact/series。

## 计算（SEED 演示）
```sql
-- fact
SELECT COUNT(DISTINCT org_id) FROM svc_org_circle WHERE city='深圳市';
-- series（按成立年累计存量，深圳切片）
SELECT YEAR(es_date) AS year, COUNT(DISTINCT org_id) AS value
FROM svc_org_circle WHERE city='深圳市' AND es_date IS NOT NULL
GROUP BY YEAR(es_date) ORDER BY year; -- 读侧再累计
-- 本年新增 = series[当年] - series[当年-1]
```
SERVE：落 svc_metric_fact / svc_metric_series。

## 三禁
- 禁写死历史切片数（1355/1240）。
- 禁造本年新增（只认 series 年差）。
- 禁把缺成立年机构硬填年份进 series。

## 呈现与缺口
- 深圳格用现池重切真数；series 同第 6 条；悬停同门户提醒（Q-SVCCHAIN-06/07）。

## 更新记录
- 2026-10-13: v0.2.1 补真数修订：city 经 dwd_org_base_info JOIN 取（池表无 city 列，企业最全信息主档）；现池深圳真数 14,033（池 43,296 城市分布：广州 19600/深圳 14033/东莞 7908/惠州 1751/京甬 4，全命中主档）；「43296 全池在深圳」的旧表述作废。
- 2026-10-13: v0.2.0 整文件覆盖旧版（旧版 2026-08-21 模拟王惠调研产出，含已过时 1355/3525 与 svc_metric_fact 旧行引用，一律作废；以本版为准）。human:徐滕强 确认。
