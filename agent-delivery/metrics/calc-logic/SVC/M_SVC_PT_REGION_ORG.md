# M_SVC_PT_REGION_ORG 计算细稿（区域服务机构数 / 全球服务机构分布）

- 版本：v0.2.0（2026-10-13 human:徐滕强 拍板：口径先写对，数据有无另论）
- 任务：SVC-METRIC-COVER-STAT-L01 第 8 条；seed 版本同步 0.2.0
- SRS 对应：05·101（2）全球服务机构分布——「通过对接服务数据库，计算各个国家所有的服务机构数量」，字段「所在国家/地区」
- 关联：M_SVC_PT_GLOBAL_TOTAL（第 6 条）同池同世界图；M_SVC_PT_SZ_REGION_ORG（第 13 条）深圳切片同地理字段

## 口径
1. 人口：圈定池 svc_org_circle（demo 43,296，规则 svc_rule_demo_kw_v1.1，全广东）。高校/院所本体不在池（第 7 条拍板口径）。
2. 维度轴：国家/地区（全球口径，不收窄）。国内展开到省级（province 字段）；国外按国家归并（供方灌数后启用）。
3. 呈现按真数据：现网仅中国·广东 43,296 单省一行；国外（含港澳台）空白不渲染、不造行（2026-08-28 侯佳伟锁：不 UNION 港澳台/海外；Q-SVCCHAIN-07）。

## 计算（SEED 演示）
```sql
-- 国内省级（现网唯一真数源）
SELECT province AS region, COUNT(DISTINCT org_id) AS value
FROM svc_org_circle
GROUP BY province;
-- 现网预期：广东 43296 一行；占比=43296/43296=100%
-- 海外（灌数后）：GROUP BY country，与国内 UNION（去重按 org_id）
```

SERVE：结果落 svc_region_dist(region, value)，海外灌数后国家行自然出现，无需改口径。

## 三禁
- 禁造国家/地区假行（含港澳台、美日等）。
- 禁用 89600 缩放数顶替真数。
- 禁空着不出数：国内真数必出（承 08-28 锁版「不空着」）。

## 呈现与缺口
- 地图/列表仅广东省着色；国外空白区不渲染假数。
- 悬停：「目前只有国内数据，全球待接入」（与 GLOBAL_TOTAL 同文案，Q-SVCCHAIN-07）。
- pending：Q-SVCCHAIN-06（口径字典）、Q-SVCCHAIN-07（海外灌数时点）。
