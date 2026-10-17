# M_SVC_PT_SZ_FIELD_DIST 计算细稿（深圳机构产业领域分布）

- 版本：v0.2.0（2026-10-13 human:徐滕强 拍板落盘；覆盖 2026-08-21 模拟王惠调研版——旧稿「领域×环节」双维 + hit_fields 工商标签冒充服务记录的口径一律作废）
- 任务：SVC-METRIC-COVER-STAT-L01 第 14 条；seed 版本同步 0.2.0
- SRS 对应：05·101（5）深圳服务机构产业领域分布
- 关联：`M_SVC_ORG_COVERAGE_BREADTH`（v0.3.1）同构五跳上链；第 11 条 M_SVC_PT_SZ_TOTAL 同池同深圳切片；第 15 条 M_SVC_PT_CHAIN_NODE_ORG 承接环节语义

## 口径

1. 领域轴：**15 集群字典全集常显**（`dim.industry_cluster`，`POLICY_VERSION=sz-10+5-2026`；2026-08-17 `human:李伟` 拍板政策/服务链/企业/展示全站同一份）。
2. 取数链（与 BREADTH 同构五跳）：

```
svc_org_circle (org_id)
  → dwd_org_base_info (org_id → city='深圳市' 切片，同第 11 条)
  → enterprise_industry_chain (org_id → chain_code)          ← 机构上链
  → industry_chain (chain_id → industry_id)                   ← 链码→L0 行业码
  → dim.industry_cluster_map (industry_id → cluster_id, mapped)
  → dim.industry_cluster (15 集群全集)
```

3. 无上链/未映射机构：单列「未分配」桶常显，禁剔除（同第 13 条风格）。
4. 双挂 L0（如人工智能同时挂 CL-SEI-01 与 CL-FUT-02，Q068 团队临时）：按**主集群（SEI 侧）**计，FUT 侧留注记不双计。
5. **环节轴从本条删除**：服务链环节语义归第 15 条 M_SVC_PT_CHAIN_NODE_ORG 承担；旧稿 hit_fields 工商标签冒充服务记录的口径作废。

## 计算（SEED 演示）

```sql
SELECT t.cluster_name, COUNT(DISTINCT x.org_id) AS cnt
FROM dim.industry_cluster t   -- 15 行全集
LEFT JOIN (
  SELECT k.cluster_id, c.org_id
  FROM svc_org_circle c
  JOIN dwd_org_base_info b ON b.org_id = c.org_id AND b.city = '深圳市'
  LEFT JOIN enterprise_industry_chain e ON e.org_id = c.org_id
  LEFT JOIN industry_chain ic ON ic.chain_id = e.chain_code
  LEFT JOIN dim.industry_cluster_map m
    ON m.industry_id = ic.industry_id AND m.is_active = 1 AND m.map_status = 'mapped'
  LEFT JOIN dim.industry_cluster k ON k.cluster_id = m.cluster_id AND k.is_active = 1
) x ON x.cluster_id = t.cluster_id
GROUP BY t.cluster_name;
-- 未分配 = 第 11 条深圳切片数 - 各集群计数之和
-- 现网真数（2026-10-13 实测）：15 集群全 0；未分配 = 14,033（上链阻塞，见下）
```

注：跨库 JOIN 遇 collation 冲突（utf8mb4_general_ci vs utf8mb4_0900_ai_ci）需 `CONVERT(... USING utf8mb4) COLLATE utf8mb4_general_ci` 归一（SEED 落地时统一处理）。

## 现网上链阻塞（如实挂账，D3=none）

- `enterprise_industry_chain` 仅 1 行样例，org_id 与池 JOIN = 0 命中；
- ODS `dwd_org_industry_tags`（104 行）credit_code / company_name 均对不上 `dwd_org_base_info`（GDF-ENT-WORKPACK-v3 已知阻塞：enterprise_code 全空无法回填 org_id）；
- → 现网 15 集群全部 0、未分配 = 深圳切片全量 14,033。**如实呈现，禁造彩色假数**；上链数据回填后图自然变彩。

## 三禁

- 禁用工商标签（hit_fields）/废弃表 dwd_service_org.industry_field/前端旧 8 领域字典冒充 15 集群。
- 禁造集群假数（现网全 0 就显全 0 + 未分配）。
- 禁隐藏未分配桶。

## 呈现与缺口

- 15 集群 + 未分配常显（含 0 项）；悬停同门户提醒（Q-SVCCHAIN-06；上链阻塞说明挂 d3_gap）。
- 前端 `serviceCenterData.ts` 的 `SERVICE_FIELDS` 8 领域是旧字典残留，另走前端改造单换 15 集群，不动本条。

## 更新记录

- 2026-10-13: v0.2.0 落盘（15 集群五跳链 + 未分配桶 + 环节轴删除；领域轴废弃样本 6 值/旧 8 领域字典）。
- 2026-08-21: 初版（模拟王惠调研产出，领域×环节双维 + hit_fields 口径，已作废）。
