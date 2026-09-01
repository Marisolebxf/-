# 覆盖领域数（M_ENT_DOMAIN_COVERAGE_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01`。领域 = `industry_cluster.cluster_id`（15），不是 `chain_code`。Q068 仍 🟡。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_DOMAIN_COVERAGE_COUNT`
- **指标名称**：覆盖领域数
- **一级模块**：企业分析
- **二级模块**：重点企业领域分布分析
- **三级模块**：领域分布分析
- **更新频率**：日
- **对齐状态**：领域字典已锁 10+5 集群；企业侧 chain_code 现网仍是 IC-* 样例，未对上 INB
- **是否在数据库**：dim 目录+映射在 `demo_gkxlumenx_dim`（结构真源）；企业↔链待灌 INB（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q068（对外 15 集群目录）；不挂 Q013（Q013 管广度/深度）

## 口径定义

当前企业集合（E-22 为对比篮 1～N 家）落到的 **产业集群 `cluster_id` 去重数**。

- 领域主表：`industry_cluster`（15；`CL-SEI-01`～`10` 战新 + `CL-FUT-01`～`05` 未来）。非 DWD、非国标 NIC。
- 领域↔产业链：`industry_cluster_map`（集群 1:N → L0 `industry_id` / INB；本轮同一 L0 只挂一个集群）。
- 企业↔产业链：`enterprise_industry_chain`（只是上链表，**不是领域表**）。`chain_code` 若为 L1，先经 `industry_chain.industry_id` 收到 L0，再进 map。
- 未出现在 map、或 `map_status`≠mapped / 未激活的链：**不计领域**。
- 只国内。无国外上链表，不造表。
- 产业不是分组维。对象已是选定企业；不再按「所选产业」滤一遍（否则容易恒为 1）。
- 不等于 `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`（那条只数 5 个未来集群）。
- 港澳台 ≠ 国外。计算键 `org_id`。

## 计算逻辑说明

```
COUNT(DISTINCT m.cluster_id)
FROM enterprise_industry_chain e
JOIN industry_chain c
  ON c.chain_id = e.chain_code          -- L1 行 industry_id=L0；L0 行 industry_id=自身
JOIN industry_cluster_map m
  ON m.industry_id = c.industry_id
 AND m.is_active = 1 AND m.map_status = 'mapped'
JOIN industry_cluster k
  ON k.cluster_id = m.cluster_id AND k.is_active = 1
WHERE e.org_id IN (:enterprise_set)
```

对应 seed `formula`：COUNT(DISTINCT cluster_id)；上链表收 L0 后 JOIN map；未映射不计；国外无法计算。

**计算公式文件**：`M_ENT_DOMAIN_COVERAGE_COUNT.md`

## 源表字段

```
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

计算企业侧只用左端 DWD。dim：`industry_cluster` / `industry_cluster_map`（项目 dim，不是三方 ODS，不进 8 件套 `source_tables`）。L1→L0 用 CHAIN DWD `industry_chain`（细稿，不进 8 件套）。

来源系统（`source_systems`）：产业链要素库。

## 现网探针（2026-08-27；不进 8 件套）

- `demo_gkxlumenx_dim.industry_cluster`：15 行全开。
- `demo_gkxlumenx_dim.industry_cluster_map`：15 条，L0 = `INB1701`～`1710`、`INB1801`～`1805`。
- `demo_gkxlumenx_dwd.industry_chain`：L0 15 条，与 map 对齐。
- `enterprise_industry_chain`（demo/正式样例）：`chain_code` 仍为 `IC-CHIP` 等 8 个，**对不上 INB**。关系对、码不对。
- live ODS `dwd_org_industry_tags.industry_code` 为 JSON 多值（如 `['INB1306']`），须 ETL 拆行且对齐现行 L0；本波不算接通。

## 待建 / 缺口

- Q068 未甲方确认 15 集群对外目录。
- 企业上链表 `chain_code` 须灌 INB（L0 或可收束的 L1）。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3.2`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。禁止用 `chain_code` / 国标行业 / 六类 core_tech_tags 冒充领域。禁止把广度分母、深度加权写进本条。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 领域锁 industry_cluster*
