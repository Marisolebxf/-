# 查询结果·服务类型分布（M_SVC_TYPE_DIST_QUERY）

## 基本信息

- 指标ID: M_SVC_TYPE_DIST_QUERY
- 指标名称: 查询结果·服务类型分布
- 一级模块: 科技专题数据查询
- 二级模块: 数据智能分析 → 推荐图表分析
- 三级模块: 技术、服务与资讯热度视图（"服务生态多样性"图）
- 算法类型: STAT（建议类型，formula 未签）
- 更新频率: n/a（查询实时，随查询会话）
- 对齐状态判定: 查询态口径卡（2026-10-13 human:徐滕强 选 A；D1 draft，挂 Q106）
- 是否在数据库: 否（不落 ADS；fact / dist 本编号 0 行是正确态）
- 关联Q编号: Q106（Q-MO-QUERY-04，🟡 类型字典未签）

## 定性（与废止的候选机构数的本质区别）

本条**不是全库统计指标**，是查询链路上的实时分桶逻辑，实现归 TOPIC-QUERY 查询叶。但它与 2026-10-13 废止的 `M_SVC_REC_CANDIDATE_CNT`（纯 `results.length`）不同：本条有完整六要素口径（对象/分组/度量/时机/空态/禁联），**保留指标身份**作查询页图表的口径唯一真源，查询页图表数字可挂 ⓘ 卡引用本 ID。

判定依据：
1. 招标 04 seq 7「推荐图表分析」明文：基于**查询结果**自动识别语义出图——图的输入就是当前结果集，不是全库（"查询即洞察"）。
2. 2026-08-27 侯佳伟 1A：本窗口只登记口径边界；实现交给查询叶，**不进** `SVC-ALGO-STAT-21-IMPL-L01`。
3. 同族 `*_QUERY` 四条（TALENT_STRUCT / ORG_PERF / TECH_HEAT / COMMON_INFO_TREND）均为查询结果上的分布/计数，形态一致。
4. 2026-10-13 徐滕强：查询代码逻辑 ≠ 统计指标逻辑；但查询也需要口径定义 → 选 A 转查询态口径卡，不废止。

## 口径定义（六要素）

| 要素 | 内容 |
|---|---|
| 对象 | 当前查询会话命中的服务机构，`org_id` **去重** |
| 分组字段 | 目标态：优先主数据 `svc_type`，空值回落 `org_type`（Q106 A 案，甲方未签）；均空归"未分类"桶，**不丢弃**。过渡态（2026-08-27 侯佳伟 2A）：ADS 卡面 `svc_org_card.service_type_candidate` 六类，空档单独计 |
| 度量 | 每桶 `COUNT(DISTINCT org_id)` |
| 执行时机 | 查询链路实时聚合（查询会话/内存分桶），**不落 ADS**、不预聚合 |
| 空结果语义 | 0 命中 → 各类型全 0 / 空图 + 空态提示；**禁止**回退全库 3525 六类分布顶上（侯佳伟 3A） |
| 边界（禁联） | 不消费 `SVCCHAIN-*` 门户类型码；不复用 `M_SVC_ORG_CNT`（全球按国家规模核）；不拿 `M_SVC_PT_GLOBAL_TYPE_DIST` / `M_SVC_PT_SZ_TYPE_DIST`（门户全库/深圳类型环图）或 `M_SVC_INDUSTRY_LAYOUT`（A1 全库分布）冒充查询结果分布 |

## 计算公式

查询态伪 SQL（查询服务内部执行，非 ADS 出数）：

```sql
SELECT COALESCE(svc_type, org_type, '未分类') AS type_bucket,
       COUNT(DISTINCT org_id)                AS org_cnt
FROM   <当前查询命中的 org_id 集合>   -- 查询会话持有，非全表
GROUP BY 1
ORDER BY 2 DESC
```

过渡期分桶列替换为 `svc_org_card.service_type_candidate`（六类 + 空档）。

验收不变量：查到 N 家 → 各类型（含空档/未分类）合计 = N；0 命中 → 空图；`svc_metric_fact` / `svc_metric_dist` 里本编号始终 0 行。

## 源库表字段

- 过渡态：`ads.svc_org_card.service_type_candidate`（六类候选，不联 ODS）
- 目标态：主数据 `svc_type` / `org_type`（列是否存在待 Q106 甲方签 + 三方核）

## 待建表字段

无。不建表、不灌 `svc_metric_*` 本编号。查询叶将来若建查询侧缓存，与本注册表无关。

## 谁做

| 谁 | 做什么 |
|---|---|
| 查询叶（TOPIC-QUERY，另派） | 页面/查询会话实时 COUNT；过渡期读 `service_type_candidate` |
| `SVC-ALGO-STAT-21-IMPL-L01` | 不做：不加本 ID calc、不灌数 |
| Q106 | 仍 🟡；甲方拍主数据 `org_type`/`svc_type` 后换列、升 D1 |
| UI | 图表数字旁挂 ⓘ（D1=draft 橙点态）；无 🧪 MockBadge 之外的伪数据角标 |

## 参考文献 / 依据

招标 04 seq 7（`bid-reference/srs/04-科技专题服务系统/科技专题数据查询/数据智能分析.md`）；`TOPIC-QUERY-METRIC-OPEN-L01` 赋号卡 + QUESTIONS（Q-MO-QUERY-04）；`SVC-ALGO-STAT-21-L01` 序号 4（2026-08-27 侯佳伟 1A 2A 3A）；`SVC-METRIC-COVER-STAT-L01` 2026-10-13 徐滕强选 A。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-08-27: 侯佳伟 1A 2A 3A（边界锁定、过渡分桶列、空态语义）
- 2026-10-13: 徐滕强定性"查询代码逻辑非统计指标"，选 A 转查询态口径卡（不废止，保留指标身份作查询页口径真源），seed v0.2.0
