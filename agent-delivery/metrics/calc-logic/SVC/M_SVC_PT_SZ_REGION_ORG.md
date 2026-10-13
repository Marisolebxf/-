# M_SVC_PT_SZ_REGION_ORG 计算细稿（深圳机构区域分布）

- 版本：v0.2.1（2026-10-13 拍板 v0.2.0 + 同日修正取数链；覆盖 2026-08-21 模拟王惠调研版，旧版基于旧池 3,525/svc_org_card.area 与 svc_region_dist，一律作废）
- 任务：SVC-METRIC-COVER-STAT-L01 第 13 条；seed 版本同步 0.2.1
- SRS 对应：05·101（5）深圳各区域服务机构分布
- 关联：第 11 条 M_SVC_PT_SZ_TOTAL 同池同切片（十区+未分配计数之和=第 11 条深圳总数）；第 8 条 M_SVC_PT_REGION_ORG 同空值单列风格
- 修正记录：v0.2.0 误 JOIN 废弃表 dwd_service_org.district（50 行 demo 样本表，多份 handoff 已标废弃非真源）→ v0.2.1 改 JOIN 企业最全信息主档 dwd_org_base_info.area

## 口径

1. 人口：圈定池 svc_org_circle（43,296）。⚠️ 池表无 city/district 列，城市与区级字段经 org_id JOIN ods.dwd_org_base_info（企业最全信息主档）取。
2. 切片与聚合：`b.city='深圳市'` 切片，GROUP BY `b.area`。
3. 十区字典（标准十区全集常显）：福田区/罗湖区/南山区/盐田区/宝安区/龙岗区/龙华区/坪山区/光明区/大鹏新区。无值区显 0 不隐藏。
4. 空值处理：area 为空或 JOIN 不上主档 → 单列「未分配」桶常显，禁静默剔除（不丢数，同第 8 条省份空值处理风格）。
5. 数随池联动：禁写死旧 ADS svc_sz_dist 十行（旧池产物作废）。

## 计算（SEED 演示）

```sql
SELECT t.district, COUNT(DISTINCT x.org_id) AS cnt
FROM (SELECT '福田区' AS district UNION ALL SELECT '罗湖区' UNION ALL SELECT '南山区'
      UNION ALL SELECT '盐田区' UNION ALL SELECT '宝安区' UNION ALL SELECT '龙岗区'
      UNION ALL SELECT '龙华区' UNION ALL SELECT '坪山区' UNION ALL SELECT '光明区'
      UNION ALL SELECT '大鹏新区' UNION ALL SELECT '未分配') t
LEFT JOIN (
  SELECT COALESCE(NULLIF(b.area,''),'未分配') AS district, c.org_id
  FROM svc_org_circle c
  JOIN dwd_org_base_info b ON b.org_id = c.org_id
  WHERE b.city = '深圳市'
) x ON x.district = t.district
GROUP BY t.district;
-- 现网真数（2026-10-13 实测）：南山 3655 / 宝安 2850 / 龙岗 2039 / 福田 1829 / 龙华 1795
--   / 光明 798 / 罗湖 553 / 坪山 388 / 盐田 121 / 大鹏 0 / 未分配 5（area 空 5 家）；合计 14033 = 第 11 条
```

注：JOIN 侧 city 取自主档 b；池机构主档无深圳行（广州 19600/东莞 7908/惠州 1751/京甬 4）不入深圳切片。SERVE：落 svc_metric_fact（维度 district，11 行全集含 0）。

## 三禁

- 禁写死历史分布（旧 svc_sz_dist/svc_region_dist 十行作废）。
- 禁静默剔除空 area/JOIN 不上主档机构。
- 禁造无机构区假数。
- 禁再引用废弃表 dwd_service_org（50 行 demo 样本）。

## 呈现与缺口

- 地图/柱状按十区+未分配常显（含 0 项）；悬停同门户提醒（Q-SVCCHAIN-06/07）。
- 正式 ODS 侧 JOIN 完整性待核验：见 matrix d3_gap。

## 更新记录

- 2026-10-13: v0.2.1 修正取数链（dwd_service_org.district → dwd_org_base_info.area）+ 落真数 14,033/十区分布；口径（十区全集/未分配/数随池联动）不动。
- 2026-10-13: v0.2.0 落盘（标准十区、空值单列「未分配」）。
- 2026-08-21: 初版（模拟王惠调研产出，基于旧池 3,525，已作废）。
