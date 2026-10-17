# M_SVC_PT_CHAIN_NODE_ORG 计算细稿（产业链节点服务机构数）

- 版本：v0.2.0（2026-10-13 human:徐滕强 拍板落盘）
- 任务：SVC-METRIC-COVER-STAT-L01 第 15 条；seed 版本同步 0.2.0
- SRS 对应：TOPIC-PT-004（SVCCHAIN-PORTAL 专题服务门户）；Bid 33.2；TRACE REQ-SVC-PT-CHAIN-DIST
- 关联：`M_SVC_CHAIN_SEGMENT_ORG_COUNT`（同源两消费，见 §5）；第 14 条 `M_SVC_PT_SZ_FIELD_DIST`（同 15 集群产业轴）
- 拍板链：2026-10-13 徐滕强三轮确认（①不合并 SEGMENT，产业过滤是本质差异；②术语澄清"节点"=服务链站位非产业节点；③预统计宽表化，"选定"不进口径）

## 1. 语义与术语澄清

**选定产业下，服务链六环节各站的服务机构去重家数。**

| 术语 | 澄清 |
|---|---|
| 「产业链节点」的"节点" | = **服务链站位节点**（CHAIN_STAGES 六环节），**不是** `industry_chain` 产业链的产业节点 |
| 「产业链」 | = 产业轴前置维度（15 集群），供给查询下钻 |
| 「选定产业」 | = **查询/展示层过滤**，不进指标定义（预统计指标无运行时选定概念，2026-10-13 徐滕强纠偏） |

## 2. 预统计宽表口径

| 项 | 锁定值 |
|---|---|
| 人口 | `demo_gkxlumenx_dwd.svc_org_circle.org_id` |
| 产业轴 | 15 集群（`dim.industry_cluster`，sz-10+5-2026，同第 14 条字典） |
| 环节轴 | CHAIN_STAGES 服务六站（CT-SVC-PT-01 唯一真源）：`stage-research` 研发与科研合作 / `stage-ip` 知识产权与标准 / `stage-transfer` 技术转移与孵化 / `stage-pilot` 中试熟化 / `stage-testing` 检测认证 / `stage-market` 市场化服务 |
| 全组合 | **15 × 6 = 90 格全量常备** |
| 计数 | `COUNT(DISTINCT org_id)`；同机构同环节多服务计 1 |
| 空格 | 显「暂无供给机构」，不伪造 |
| SERVE | 落 `svc_metric_fact`（维度 field_id + stage_id）；前端选产业 = 查宽表 `field_id` 下钻，不现算 |

## 3. 计算（SEED 演示）

```sql
-- 目标口径（当前无源，不可执行）：
SELECT f.field_id, s.stage_id, COUNT(DISTINCT r.org_id) AS org_count
FROM dim_15clusters f                       -- 15 集群全集
CROSS JOIN chain_stages s                   -- CHAIN_STAGES 六环节全集
LEFT JOIN (机构×产业×环节服务记录) r        -- 缺口：待供方交付（SVC-P0-3）
  ON r.field_id = f.field_id AND r.stage_id = s.stage_id
 AND r.org_id IN (SELECT org_id FROM svc_org_circle)
GROUP BY f.field_id, s.stage_id;            -- 90 行全量，未命中格补 0
-- 现网预期：90 格全 0（事实源不存在），各环节显「暂无供给机构」
```

## 4. 事实源缺口（D3=none，如实挂账）

- 「机构×产业×环节服务记录」在 ODS / DWD / DIM **均不存在**（Q-SVCCHAIN-08 全文已核）；
- 供方题 **SVC-P0-3** 待交付；
- 现网 90 格全 0 如实呈现；交付后重跑变真数。

## 5. 与 SEGMENT_ORG_COUNT 的关系（同源两消费）

同一张预统计宽表的两个消费口径：
- 按 `stage_id` 聚合边际和（不分产业）= `M_SVC_CHAIN_SEGMENT_ORG_COUNT`（生态地铁图全貌）；
- `field_id × stage_id` 明细 = 本条（产业下钻）。
- 同源不同粒度，**两个指标 ID 并存，禁互相顶替**（TOPIC-ALGO-GAP-L02 登记明令）。

## 6. 三禁

- 禁用 `M_SVC_CHAIN_SEGMENT_ORG_COUNT` 顶替本条（全池单维 ≠ 产业×环节明细）。
- 禁产业链节点 `node_stage` / 15 集群 / 服务六类（FINANCE/IP/HR/MKT/CONSULT/INNOV）冒充环节。
- 禁造环节家数假数（现网全 0 就显全 0 + 「暂无供给机构」）。

## 7. 呈现与缺口

- 门户选定产业后展示六环节各站家数；空站显「暂无供给机构」；悬停提醒 Q-SVCCHAIN-08（供方交付中）。
- 前端 `serviceReviewData.ts` 本指标演示 definition 已与本口径一致（选定产业领域内环节计数），仅「选定」语义按本稿归为查询层。

## 更新记录

- 2026-10-13: v0.2.0 落盘（预统计宽表 15×6=90 格；「选定产业」归查询层；术语澄清；与 SEGMENT 同源两消费禁顶替；D3=none 挂 Q-SVCCHAIN-08+SVC-P0-3）。
