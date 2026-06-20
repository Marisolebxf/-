# GKX 平台层 · 稳定业务主键定稿（§8）

> **任务**：E-PLATFORM-P0-L01  
> **对齐**：`数据库设计.md` §8 命名与类型规约  
> **原则**：主键现在定死，不依赖三方源表结构；Nebula `vid` 与 RDBMS 业务键对齐

## 1. 全局实体键

| 业务键 | 类型 | 格式 / 示例 | 用途 | Nebula vid |
|--------|------|-------------|------|------------|
| `org_uid` | VARCHAR(64) | `org:{credit_code}` 或 innov 归一键 | 跨要素机构主数据 | `org:{org_uid}` 或前缀一致 |
| `enterprise_code` | VARCHAR(64) | 统一社会信用代码 `91440300MK20260620000001` | ENT 域业务归一键 | `ent:{enterprise_code}` |
| `policy_id` | VARCHAR(64) | `pol:{region}-{seq}` 如 `pol:SZ-20260620-0001` | E7 政策 ADS/图谱 | `pol:{policy_id}` 或整段作 vid |
| `chain_id` | VARCHAR(64) | 产业链节点 ID | E2 产业链维表/指标 dim | `chain:{chain_id}` |
| `region_code` | VARCHAR(20) | 国标区划，与 `dim_region` 对齐 | 区域维度 | — |
| `metric_id` | VARCHAR(64) | `M_{ELEMENT}_{INDICATOR}_*` | 指标注册（D9） | — |
| `model_id` | VARCHAR(64) | 要素前缀 + 模型名 | 深度模型注册 | — |
| `event_id` | VARCHAR(64) | innov 域事件键（L02） | 创新监测 ADS | 与 `dwm_graph_*` 一致 |

## 2. ADS 通用列

| 列 | 规约 |
|----|------|
| `id` | BIGINT AUTO_INCREMENT，表内物理主键（非跨表业务键） |
| `calc_batch_id` | VARCHAR(64)，**Mock 阶段必须** `mock_*` 前缀 |
| `updated_time` / `update_time` | DATETIME，批次写入时间 |
| `ext` | JSON NULL，**每张 ADS 必有**，兜底三方未预见字段 |

## 3. 要素 ↔ 主键对照

| 要素 | ADS 表前缀 | 明细/图谱主键 | 备注 |
|------|-----------|--------------|------|
| E1 企业 | `ads_ent_*` | `enterprise_code` | 与 `dim_org_master.credit_code` 对齐 |
| E2 产业链 | `ads_ind_*`（预留） | `chain_id` | Wave1+ 扩展 |
| E7 政策 | `ads_policy_*` | `policy_id` | Wave1 E-E7-POLICY-M1 |
| 通用指标 | `ads_metric_timeseries` | `(metric_id, dim_key, stat_date)` | 多要素复用 |
| 图谱镜像 | `graph_node/edge` | `node_key` / `src_key`,`dst_key` | PG 兜底，Nebula 主存 |

## 4. 禁止事项

- ❌ 用三方源 `org_id` / 自增 id 作为 Java 契约面主键（仅作 ODS 贴源行键）
- ❌ Mock 批次不带 `mock_` 前缀
- ❌ ADS 表无 `ext JSON` 列（改表需 Python+Java 会签）
- ❌ 同一业务实体在不同 ADS 表使用不同键名（ENT 统一 `enterprise_code`）

## 5. 变更流程

变更业务主键策略 → 登记 `客户决策清单跟踪表.md` + architect 会签 + bump cfg_metric.version。
