# DATA-ENT-DWD-ALIGN-DOC-L01 · 四类分类表 + 设计稿/派单包回写

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权「后续认领不必再问」；`lock_hours=24` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |

## 范围与实现

- 核验 2026-09-03 `gkxlumenx-dwd-public`：`gkxlumenx_dwd`（正式）与 `demo_gkxlumenx_dwd`（对照）。
- 出四类分类表：`DATA-ENT-DWD-ALIGN-四类分类表.md`。
- 按 Q-WP3-29 回写 `DWD表结构设计-企业工商表-MySQL-v3.1.md`：改名跟正式库；8-12 写丢的 base 宽列补回；设计独有列保留为 ADD。
- 派单包升 **v3.1**：`09`/`10`/`13`/`00`/`CHANGELOG`/`README` 与 v3.1 一致。
- `storage/ENT/stores/mysql/dwd-entity.md` 表清单日期与 ALIGN 入口已更新。
- 拟 ALTER 清单在分类表 §6 与 `13` §3。**本叶不 ALTER**。
- `GDF-ENT-WORKPACK-V3-L01` 不打回；handoff 已加「列契约以本叶为准」。

## 偏离

- 第 4 类（`brand_score` / `customer_concentration` / `market_share` / `core_tech_coverage` / `tech_transaction_amount`）**回写列、待核口径、本叶不洗**。
- 灌数仓 `demo-algo-science` 只做表名映射（`innov/common/tables.py`），无工商列名硬编码，**不改该仓**。
- `data-design/企业/企业域-ETL-Mapping明细-源表到DWD.md` 仍为 v1.2 历史基线；施工只认包内 `09` v3.1。

## 产物清单

- `DATA-ENT-DWD-ALIGN-四类分类表.md`
- `DATA-ENT-DWD-ALIGN-DOC-L01.md`（本文件）
- 工商 v3.1 + 派单包 `09`/`10`/`13` 升 v3.1
- `dwd-entity.md` 表清单入口

## 验收证据

- 正式库 `information_schema` 9 表列清单已写入分类表 / v3.1 CREATE。
- v3.1 `enterprise_base` CREATE 列集 ⊇ 正式库该表 52 列（含第 4 类）。
- 未对 live `gkx` 做 DDL；未改 Java。
- orchestration `origin/dev`：`aaeff818`（DOC）`efcce5e2`（registry）

## 测试结果

- 正式库 `information_schema` 9 表列清单已写入分类表 / v3.1 CREATE。
- v3.1 `enterprise_base` CREATE 列集 ⊇ 正式库该表 52 列（含第 4 类）。
- 未对 live `gkx` 做 DDL；未改 Java。

## 遗留风险

- DDL 叶执行前须再 `SHOW CREATE`；两库列现状不同，只能 ADD 不能假设对称。
- GDF 若已按 v3.0 设计列名开工，必须改认 v3.1（通知辜少彬，监管人清单 §5.3）。
- GRAPH space 未点名，不挡本叶。

## CI/CD

- 分支：`origin/dev`
- commit：本叶文档提交（编排仓）
- pipeline：`cicd: skip`（仅编排文档）
- K8s rollout：不适用
- 验证：正式库列 vs v3.1 CREATE；`13` 拟 ALTER 与分类表 §6 一致

## Cost 回填

见下节。

## 成本

- actual_tokens：38000（会话估算）
- model_used：cursor-grok-4.6
- actual_cost：0.21
- cost_warn：green

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 / 算法只在 Python | ✅ 未改 Java、未写算法 |
| 图谱 Nebula / 不写正式 space | ✅ 未点名 |
| 可观测性 | ✅ 文档叶无新服务；未拆 observability |
| CI/CD | ✅ 只推 `origin/dev`；编排仓 `cicd: skip` |
| demo2 只读 merge | ✅ 未 merge 进 lumen |
| D12 demo 服务 | ✅ 未调 demo-* 服务；demo DWD 只对照 + 同套 ADD |
| GDF 不写 ES/nGQL | ✅ |
| Java 企业 API | ✅ 零改 |

## 涉及文件

- `agent-delivery/agent-handoffs/企业战略分析-ENT/DATA-ENT-DWD-ALIGN-四类分类表.md`
- `agent-delivery/data/data-design/企业/DWD表结构设计-企业工商表-MySQL-v3.1.md`
- `agent-delivery/data/data-design/storage/ENT/stores/mysql/dwd-entity.md`
- `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v3/`（`00`/`09`/`10`/`13`/`CHANGELOG`/`README`）
- `agent-delivery/agent-handoffs/企业战略分析-ENT/GDF-ENT-WORKPACK-V3-L01.md`（追加一行）
