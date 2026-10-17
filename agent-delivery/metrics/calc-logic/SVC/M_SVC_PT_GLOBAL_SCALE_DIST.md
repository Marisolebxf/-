# M_SVC_PT_GLOBAL_SCALE_DIST 计算细稿（全球服务机构规模分布）

- 版本：v0.2.0（2026-10-13 human:徐滕强 拍板落盘）
- 任务：SVC-METRIC-COVER-STAT-L01 第 9 条；seed 版本同步 0.2.0
- SRS 对应：05·101 服务机构规模维度（承 2026-08-28 侯佳伟锁版 + 2026-10-13 徐滕强判定链更新）
- 关联：M_SVC_PT_KEYORG_SCALE（第 10 条）读 ADS 卡面同名列 employees_number；M_SVC_PT_SZ_* 深圳系列同池

## 口径
1. 人口：圈定池 svc_org_circle（demo 43,296，全企业型）。
2. 四档（左闭右开）：[0,50) / [50,200) / [200,500) / [500,+]。
3. 判定链（单链兜底非双轨）：
   - 人数优先：每机构取最近一个有数年份的 employees_number（dwd_org_annual_financial_info，org_id+年）。
   - 注册资本兜底（无人数时）：dwd_org_base_info.registered_capital（万元）映射——<1000万→<50 档；[1000万,5000万)→50-200 档；[5000万,1亿)→200-500 档；≥1亿→≥500 档。阈值对齐企业域 enterprise_scale 兜底先例。
   - 残档：人数与注册资本皆无 → 「未分档」。
4. 过渡态：现网人数∩圈定=0（SVC-P0-2），全部 43,296 走注册资本兜底；供方人数对上后兜底链自动退位为人数优先（链序保证，不改口径）。与 08-28「人数唯一源」锁版的偏差已登记 Q-SVCCHAIN-06（2026-10-13）。

## 计算（SEED 演示）
```sql
-- 判定链分档（人数优先 → 注册资本兜底）
WITH emp AS (
  SELECT org_id, employees_number,
         ROW_NUMBER() OVER (PARTITION BY org_id ORDER BY year DESC) rn
  FROM dwd_org_annual_financial_info
  WHERE employees_number IS NOT NULL
),
binned AS (
  SELECT c.org_id,
    CASE
      WHEN e.employees_number IS NOT NULL THEN
        CASE WHEN e.employees_number < 50 THEN 'lt50'
             WHEN e.employees_number < 200 THEN '50to200'
             WHEN e.employees_number < 500 THEN '200to500'
             ELSE 'ge500' END
      WHEN b.registered_capital IS NOT NULL THEN
        CASE WHEN b.registered_capital < 1000 THEN 'lt50'
             WHEN b.registered_capital < 5000 THEN '50to200'
             WHEN b.registered_capital < 10000 THEN '200to500'
             ELSE 'ge500' END
      ELSE 'unknown'
    END AS category
  FROM svc_org_circle c
  LEFT JOIN emp e ON e.org_id = c.org_id AND e.rn = 1
  LEFT JOIN dwd_org_base_info b ON b.org_id = c.org_id
)
SELECT category, COUNT(DISTINCT org_id) AS value FROM binned GROUP BY category;
-- 现网预期：四档由注册资本兜底分布 + unknown 残档；占比分母=四档合计（不含 unknown）
```

SERVE：统一灌 svc_metric_dist(category, value)；ADS 卡面加列与 ODS 同名 employees_number（供 KEYORG_SCALE 档案直读，承 08-28 锁版）。

## 三禁
- 禁主表 org_size（微小中大）映射冒充人数档。
- 禁注册资本档与人数档并行双轨两张图（兜底映射进同一套四档）。
- 禁造四档假分布；残档如实显示不隐藏。

## 呈现与缺口
- 悬停：「部分机构按注册资本兜底分档（人数缺失）」+ SVC-P0-2 缺口说明；仅国内提醒（Q-SVCCHAIN-07）。
- pending：Q-SVCCHAIN-06（分档字典+兜底链，2026-10-13 更新）；SVC-P0-2（人数列交付/空值/年主键/为何对不上圈定）。
