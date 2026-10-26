# POLICY-DDL-CONV-L00

- 任务：政策 MySQL 建表规约
- 状态：联调闸门（definition）
- 监管人：human:淮政玮
- ponytail: off（定义叶，不压完整性）

## 范围

把总控 §1 的建表规则写入 `agent-delivery/data/data-design/storage/mysql-ddl-convention.md`。第 8 条原有正文保留。`architecture-baseline.md` §6 只加一条指针，不复制规约正文。

## 产物

- `agent-delivery/data/data-design/storage/mysql-ddl-convention.md`
- `agent-delivery/architecture-baseline.md` §6 数据行指向该规约

## 作废声明

`schema_policy_ads.sql`、政策旧稿 v1 §3 类型、`schema_mysql.sql` 不再作政策 ADS/DWD 结构依据，禁止再执行。

## 架构合规

- D1–D12：本叶只写文档，不改调用链、不改库。✅
- D14：未涉及对象存储。✅
- 口令未写入本文件。✅

## cost

- actual_tokens: 未单列（随会话）
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## 联调

规约已落盘。会签通过。后续 DOC、IMPACT、CODE 可以并行。
