# GKX 平台层 · 数据质量规则与血缘说明

> **任务**：E-PLATFORM-P0-L01  
> **关联**：`data-lineage-policy.md` · `数据库设计.md` §12 · D7 数据契约先行

## 1. 血缘总览（Wave 0 · Mock 阶段）

```text
[三方源 TBD] ──(P1-L01)──> gkx_ods ──> gkx_dwd ──> gkx_dwm
                                              │
                    mock/ads_generator.py ────┴──> gkx_ads (契约面·冻结)
                              │
                              └── calc_batch_id = mock_{seed}_platform
```

| 层 | Wave 0 状态 | 读取方 | 写入方 |
|----|-------------|--------|--------|
| ODS/DWD/DWM | 仅命名占位 | Python（未来） | Python（未来） |
| `gkx_dim` / `gkx_cfg` | DDL 冻结 + 样例维表 | Java + Python | Python |
| `gkx_ads` | DDL 冻结 + Mock 填充 | **Java 只读** | **Python Mock 生成器** |
| NebulaGraph | P0-L03 灌数 | Python | Python |

**Mock 血缘标注**（cfg_metric.source_systems）：

```json
["Mock @ batch=mock_20260620_platform", "Python mock/ads_generator.py"]
```

## 2. 平台层 DQ 规则

| # | 类型 | 对象 | 规则 | 级别 |
|---|------|------|------|------|
| DQ-P01 | 唯一性 | `gkx_dim.dim_region.region_code` | PRIMARY KEY 不重复 | 🔴 阻断 |
| DQ-P02 | 唯一性 | `gkx_ads.ads_policy_focus.policy_id` | PRIMARY KEY 不重复 | 🔴 阻断 |
| DQ-P03 | 唯一性 | `ads_ent_capability(enterprise_code, calc_batch_id)` | 同批次企业唯一 | 🔴 阻断 |
| DQ-P04 | 非空 | 所有 ADS.`calc_batch_id` | NOT NULL | 🔴 阻断 |
| DQ-P05 | Mock 标识 | ADS.`calc_batch_id` | Wave 0 必须 `LIKE 'mock_%'` | 🟡 告警 |
| DQ-P06 | 扩展列 | 所有 ADS 表 | 必须含 `ext JSON NULL` | 🔴 阻断（DDL 评审） |
| DQ-P07 | 主键格式 | `enterprise_code` | 18 位统一社会信用代码格式（Mock 可简化前缀 91440300MK*） | 🟡 告警 |
| DQ-P08 | 主键格式 | `policy_id` | 必须以 `pol:` 前缀 | 🟡 告警 |
| DQ-P09 | 参照 | `ads_ent_*`.enterprise_code | 应存在于 `gkx_dim.dim_org_master.credit_code`（Mock 生成器保证） | 🟡 告警 |
| DQ-P10 | 值域 | `ads_metric_timeseries.yoy` | 建议 [-100, 500]（同比 %） | 🟢 监控 |
| DQ-P11 | 值域 | `ads_policy_focus.focus_score` | [0, 1] | 🟡 告警 |
| DQ-P12 | 枚举 | `cfg_metric.update_freq` | ∈ realtime/hourly/daily/weekly/monthly/quarterly/yearly/static | 🔴 阻断 |
| DQ-P13 | 完整性 | `cfg_metric` 8 件套 | metric 上线前 8 字段非空（D9） | 🔴 阻断 |
| DQ-P14 | 图谱对齐 | `graph_node.node_key` | 与 Nebula vid 一致（ent:/pol:/chain: 前缀） | 🟡 告警 |
| DQ-P15 | 批次幂等 | Mock 生成器 | 同 `calc_batch_id` 可 DELETE+INSERT 或 REPLACE 重跑 | 🟢 监控 |

> ENT 域 DQ-01~15 见 `企业域数据库设计(v1).md` §9，与本表合并执行。

## 3. 指标血缘示例（Wave 0）

### M_ENT_TOTAL_COUNT

| 段 | 表/系统 | 说明 |
|----|---------|------|
| UI | MetricSpecCard | 企业概况 KPI |
| API | gkxlumen-metrics `/metrics/v1/catalog` | P0-L02 待实现 |
| ADS | `gkx_ads.ads_ent_overview` | metric_id=M_ENT_TOTAL_COUNT |
| DWD | `gkx_dwd.enterprise`（占位） | P1 真实聚合 |
| ODS | 要素库 `dwd_org_reg_info` 等 | 已交付，待工厂接入 |
| Mock | `mock/ads_generator.py` | batch=mock_20260620_platform |

### M_POLICY_FOCUS_INDEX

| 段 | 表/系统 | 说明 |
|----|---------|------|
| ADS | `gkx_ads.ads_policy_focus.focus_score` + `ads_metric_timeseries` | E7 Wave1 |
| 算法 | algorithm-agent 焦点模型 | E-E7-POLICY-M1-L03 |
| Mock | 20 条政策样例 | 固定种子 20260620 |

## 4. cfg_degrade_switch（Wave 0 默认）

| switch_key | enabled | 含义 |
|------------|---------|------|
| `data_source_third_party` | 1 | 三方源未就绪，ADS Mock |
| `policy_real_source` | 1 | 政策真实源未接入 |

三方源 verified 后（P1-L01）：关闭对应开关，删除/归档 `mock_*` 批次。

## 5. 验收挂钩

- **DEMO/INTEG**：Mock-ADS 登记 `demo-fallback-registry.yaml`（待 coordinator 汇总）
- **FULL**：P1 数据工厂 `status: verified` + 去 Mock 批次

## 6. 维护责任

| 制品 | Owner |
|------|-------|
| DDL `scripts/sql/gkx/*.sql` | data-agent |
| Mock 生成器 `mock/ads_generator.py` | data-agent |
| `data-source-mapping-registry.yaml` | data-agent |
| `cfg_metric` 种子 | data-agent + metrics/cfg_metric-*-seed.yaml |
| `/metrics/v1/catalog` | api-agent（P0-L02） |
