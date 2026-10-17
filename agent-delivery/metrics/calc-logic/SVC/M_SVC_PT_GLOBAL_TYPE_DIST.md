# M_SVC_PT_GLOBAL_TYPE_DIST 计算细稿（全球服务机构类型分布）

- 版本：v0.2.0（2026-10-13 human:徐滕强 拍板落盘）
- 任务：SVC-METRIC-COVER-STAT-L01 第 7 条；seed 版本同步 0.2.0
- SRS 对应：05·101 全球服务机构分布（SRS 未明文类型轴含高校；三类字典承 2026-08-28 侯佳伟 1A2A3B 锁版）

## 口径
1. 人口：圈定池 svc_org_circle（demo 43,296，规则 svc_rule_demo_kw_v1.1，现网全企业型，全广东）。
2. 三类判定（只认结构化来源，禁名称关键词）：
   - 高校 = circle.org_id ∈ dwd_org_heis_info → 本项目口径恒 0（高校另有归口，我们不做）。
   - 科研院所 = circle.org_id ∈ dwd_research_institute_base_info → 同口径恒 0（2026-10-13 拍板）。
   - 企业 = 池内其余 → 现网 ≈ 全池。
3. 高校冠名企业（XX大学科技园有限公司）是工商注册服务供给主体：进圈、归企业，正确行为非漏圈。

## 计算（SEED 演示）
```sql
-- 判型 JOIN（demo 库实测 collation 不同，需 CONVERT 或按 org_id 等值）
SELECT '高校' AS type, COUNT(DISTINCT c.org_id) AS value
FROM svc_org_circle c JOIN dwd_org_heis_info h ON c.org_id = h.org_id
UNION ALL
SELECT '科研院所', COUNT(DISTINCT c.org_id)
FROM svc_org_circle c JOIN dwd_research_institute_base_info i ON c.org_id = i.org_id
UNION ALL
SELECT '企业', COUNT(DISTINCT c.org_id) - <上述两行结果之和>;
-- dist = value / SUM(value)；现网预期：高校 0、院所 0、企业 43296
```

## 三禁
- 禁候选六类（service_type_candidate FINANCE/IP/HR/MKT/CONSULT/INNOV）冒充类型轴。
- 禁名称关键词把高校冠名企业冒充高校本体。
- 禁给高校/院所造非 0 假数；单色环如实呈现，0 值档不隐藏。

## 呈现与缺口
- 环图单色（全企业）如实；悬停说明：高校/院所本体不纳入服务机构口径（另有归口）；仅国内数据，全球待接入（Q-SVCCHAIN-07）。
- pending：Q-SVCCHAIN-06（字典与口径）、Q-SVCCHAIN-07（全球人口）；源码表在正式 ODS 侧待核验。
- 供方题 SVC-P0-1 收窄：不再问高校/院所进圈，只问院所判型码备用与 JOIN 键正式交付。

## 关联
- M_SVC_PT_GLOBAL_TOTAL（第 6 条）人口同池；M_SVC_PT_SZ_TYPE_DIST（第 12 条）深圳切片同字典同判型。
