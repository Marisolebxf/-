# POLICY · gapfill（D16 缺项库）

```yaml
---
doc_id: POLICY-STORES-GAPFILL
element: POLICY
role: store-mysql
status: draft
version: "2026-11-09"
updated: 2026-11-09
task_id: POL-IMPL-EFFECT-MOCK-VIA-UI-L01
---
```

> **库**：`gkxlumenx_gapfill`（DBA 预建；应用路径禁止 `CREATE DATABASE`）。  
> **边界**：只写 `gapfill_*`；禁止写入 ODS / 正式 DWD / ADS / 供应方库。  
> **索引**：[`../README.md`](../README.md)。详设读侧：[05.6.2 §3.1](../../../../../agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.6.2-深圳政策现状分析.md)。

## `gapfill_policy_sz_effect`（深圳落地实效三维缺项）

一政策一行。深圳现状板在 DWD 空维时按 `policy_id` 只补内存字段（启动日 / 支持对象 / 反馈分），不改 `policy_base_info` 原列。

### CREATE（as-built）

真源：`lumen-algo-py/scripts/mysql/gapfill_policy_sz_effect.sql` 与 `polan/mockgen/effect_gapfill.py` 的 `CREATE_SQL`（同文；应用侧 `ensure_table` 只 `CREATE TABLE IF NOT EXISTS`）。

```sql
CREATE TABLE IF NOT EXISTS gkxlumenx_gapfill.gapfill_policy_sz_effect (
  policy_id VARCHAR(128) NOT NULL,
  implementation_date DATE NOT NULL,
  support_object VARCHAR(64) NOT NULL,
  feedback_score TINYINT NOT NULL,
  metric_id VARCHAR(64) NOT NULL,
  gap_item VARCHAR(128) NOT NULL,
  fill_method VARCHAR(16) NOT NULL,
  fill_model VARCHAR(64) NULL,
  gapfill_batch_id VARCHAR(128) NOT NULL,
  generated_at DATETIME NOT NULL,
  PRIMARY KEY (policy_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

| 列 | 约束 |
|---|---|
| `implementation_date` | 有效日；≠ 发布日、≠ 零日期；缺失不写成 `0000-00-00` |
| `support_object` | 非空（企业 / 科研机构 / 高等学校 / 新型研发机构） |
| `feedback_score` | 1–5；缺失不写成 0 |
| `metric_id` | 固定 `M_POLICY_IMPLEMENTATION_EFFECT` |
| `gap_item` | `落地执行启动,受益覆盖,实施反馈` |
| `fill_method` | 规则灌数 `rule`；LLM 路径可带 `fill_model` |

### 写入口（必须挂算法库页两过程）

| UI（`/#/policy/mock`） | 代码 | 行为 |
|---|---|---|
| 「Mock 10 条数据」 | `polan.mockgen.synth.run` | 当次合成政策（含历史版）UPSERT；末尾 `backfill_missing` 回补 DWD 仍缺行 |
| 「真实政策补外围：深圳 40 + 随机 10」 | `polan.mockgen.synth.run_real` | 挑中的全部政策都写（含 LLM 失败组）；全部已补时仍回补缺口 |

原则：**无表建表，有表 UPSERT**。响应字段 `effect_rows` = 当次写入 + 回补。批次号沿用 `…EFFECT-GAPFILL` / `…EFFECT-SYNTH`。

### 读入口

| 调用方 | 行为 |
|---|---|
| `polan/shenzhen_board.py` | 城市截面读出后，只补尚未启动、无支持对象、无反馈的行 |
| 配置区「落地执行率 / 受益覆盖广度 / 反馈满意度」demo 常量 | **不**读本表、**不**进接口 |

### 禁止

- 旁路新建与两入口无关的灌数按钮当主写路径  
- 把缺项行写入 ODS / 正式 DWD / ADS / 供应方库  
- 空值充 0、发布日当实施日  

签收证据：`agent-handoffs/政策模块-E7/POL-IMPL-EFFECT-MOCK-VIA-UI-L01.md`。
