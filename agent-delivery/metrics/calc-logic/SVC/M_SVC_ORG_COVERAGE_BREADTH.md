# 服务广度（M_SVC_ORG_COVERAGE_BREADTH）

## 基本信息

- 指标ID: M_SVC_ORG_COVERAGE_BREADTH
- 指标名称: 服务广度
- 一级模块: 产业服务链分析
- 二级模块: 服务机构分析
- 三级模块: 产业领域分析
- 更新频率: 日
- 对齐状态判定: 已对齐（0.3.1 对齐企业覆盖领域数；领域键仅 15 集群）
- 关联Q编号: Q068（15 集群目录）。不挂 Q-SVCCHAIN-08

## 口径定义

圈定池内单机构落到的产业集群去重个数。

| 项 | 锁定值 |
|---|---|
| 人口 | `demo_gkxlumenx_dwd.svc_org_circle.org_id` |
| 上链 | `demo_gkxlumenx_dwd.enterprise_industry_chain` ← `ods: dwd_org_industry_tags` |
| 领域 | `demo_gkxlumenx_dim.industry_cluster`（15：`CL-SEI-01`～`10` + `CL-FUT-01`～`05`，`is_active=1`） |
| 映射 | `industry_cluster_map`（L0 `industry_id` → `cluster_id`，`map_status='mapped'`） |
| L1→L0 | `demo_gkxlumenx_dwd.industry_chain`（`chain_id` = 上链 `chain_code` → `industry_id`） |
| 结果 | 整数；无上链 / 未映射 = 0 |

语义 = 所属产业链覆盖的集群数（与 `M_ENT_DOMAIN_COVERAGE_COUNT` 同构），不是服务合同事实。

## 计算公式

```sql
SELECT c.org_id, COUNT(DISTINCT m.cluster_id) AS breadth
FROM demo_gkxlumenx_dwd.svc_org_circle c
LEFT JOIN demo_gkxlumenx_dwd.enterprise_industry_chain e ON e.org_id = c.org_id
LEFT JOIN demo_gkxlumenx_dwd.industry_chain ic ON ic.chain_id = e.chain_code
LEFT JOIN demo_gkxlumenx_dim.industry_cluster_map m
  ON m.industry_id = ic.industry_id
 AND m.is_active = 1
 AND m.map_status = 'mapped'
LEFT JOIN demo_gkxlumenx_dim.industry_cluster k
  ON k.cluster_id = m.cluster_id
 AND k.is_active = 1
GROUP BY c.org_id;
```

禁止：`COUNT(hit_fields)`；国标 `industry` 单值；自建 `svc_org_field_service`。

## 源库表字段

```
svc_org_circle
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

dim / `industry_chain` 为计算辅表，不进 8 件套 `source_tables`（同 ENT）。

## 参考文献 / 依据

`M_ENT_DOMAIN_COVERAGE_COUNT.md`；2026-10-13 human:徐滕强 拍对齐企业 15 集群路径。

## 更新记录

- 2026-08-21: 初版
- 2026-10-13: 挂起 / 自建表误写已撤回
- 2026-10-13: 0.3.0 对齐企业 15 集群
- 2026-10-13: 0.3.1 正文去掉对演示 8 领域字典的叙述；领域键只认 `industry_cluster`
