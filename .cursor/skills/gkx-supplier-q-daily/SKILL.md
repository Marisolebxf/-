---
name: gkx-supplier-q-daily
description: >
  Daily slice of third-party supplier questions from metric kits: cluster
  inbound dwd_*.column, append dated journal, sidecar source-gap, wait for
  human nod before 现行待回复. Use when DATA-SUPPLIER-Q, 今日三方问题,
  按日日志, 源缺口 sidecar, 给供应方出题, gkx-supplier-q-daily, or
  question/{维度}. Not for seed/matrix edits, MIXED, or metric-progress-export.
---

# 三方问题每日切片

把「指标 kit → 入站缺口题」按**一天一批**执行。方法真源：`agent-delivery/data/third-party-source/question/README.md` + 派单包 `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md`。Codex 指针：`.codex/skills/gkx-supplier-q-daily/`。

本 skill **不是** 11 条 registry 叶的替代：叶管域范围与监管人；skill 管当日步骤。定义类，**禁止** ponytail 行。PROGRESS 导出走 `gkx-metric-progress`，不在每日切片里改导出脚本。

## 何时用

用户说：今日三方问题 / 按日日志 / DATA-SUPPLIER-Q / 源缺口 sidecar / 给供应方出题 / `gkx-supplier-q-daily`。

不要用：单条 8 件套 → `gkx-metric-lookup`；改 ENT seed → `gkx-ent-stat-cover`；认领 registry → `gkx-task-claim-supervision`；整表进度 Excel → `gkx-metric-progress`。

## 每次必带参数

禁止默认扫全库。缺一项就停，问人。

| 参数 | 规则 |
|------|------|
| `task_id` | 已认领的 `DATA-SUPPLIER-Q-{DOMAIN}-L01`（`claimed` / `in_progress`） |
| `domain` | `ENT` / `CHAIN` / `SVC` / `POLICY` / `SYNTH` / `INNOV` / `ORG` / `TALENT` / `TECH`（综合=`SYNTH`，不是 `COMP`） |
| `supervised_by` | 进度表 **专题维度Owner**（派单包 §3.1），不是卡点责任方 |
| `cap` | 当日 `metric_id` 上限，默认 **20**，硬顶 30 |
| `types` | 默认 `STAT,COMPUTE,MODEL,GRAPH,third_party,UNKNOWN`。**MIXED 永不进批** |

话术示例：

```text
按 gkx-supplier-q-daily
task_id: DATA-SUPPLIER-Q-CHAIN-L01
domain: CHAIN
cap: 20
```

定时只负责再唤起一轮：`/loop 1d` + 上面那段。现行表仍要人点头。

## 域目录

| domain | 目录 | 清单文件 | 对接 |
|--------|------|----------|------|
| ENT | `question/企业维度/` | `ENT-SUPPLIER-QUESTIONS.md` | 默认供应方 |
| CHAIN | `question/产业链维度/` | `CHAIN-SUPPLIER-QUESTIONS.md` | 默认供应方 |
| SVC | `question/服务机构维度/` | `SVC-SUPPLIER-QUESTIONS.md` | 默认供应方 |
| POLICY | `question/政策维度/` | `POLICY-SUPPLIER-QUESTIONS.md` | 默认供应方 |
| SYNTH | `question/综合维度/` | `SYNTH-SUPPLIER-QUESTIONS.md` | 默认供应方 |
| INNOV | `question/创新维度/` | `INNOV-SUPPLIER-QUESTIONS.md` | 默认供应方 |
| ORG | `question/机构维度/` | `ORG-SUPPLIER-QUESTIONS.md` | **久新** |
| TALENT | `question/人才维度/` | `TALENT-SUPPLIER-QUESTIONS.md` | **久新** |
| TECH | `question/技术维度/` | `TECH-SUPPLIER-QUESTIONS.md` | **久新** |
| TNIE | `question/科技动态维度/` | `TNIE-SUPPLIER-QUESTIONS.md` | 外部不限久新（CMS/资讯库/`dwd_*`） |

没有清单文件时从 `_TEMPLATE-SUPPLIER-QUESTIONS.md` 复制（文件名不加日期）。ORG/TALENT/TECH 文首写「对接：久新」，不与 SVC / 政策 / 企业清单混发。

## 当日步骤

1. MCP `task-get`：状态必须是 `claimed` 或 `in_progress`；`supervised_by` 与 §3.1 Owner 一致。无 task-id **禁止**改 `question/`。
2. 读 README §3 问法、§4–§5 模板、`SUPPLIER-WORK-CONSTRAINTS.md`；扫 `客户决策清单跟踪表.md` 去重（甲方 Q-* 不改写成供应方题）。
3. MCP `metric-query` `domain` + `fields=full`。禁止打开 `metrics/registry` seed/矩阵 YAML。
4. 过滤：只留 `types`；跳过 `MIXED`、二次指标（`<- metric:`）。**不要**因「CMS-only / 非久新」跳过；CMS/资讯库/其它外部一律列题。纯本方 ADS/内部 API 仍不问对方要这些表名。
5. **游标** = `question/source-gap-index.yaml`。已有 `as_of` 且问法未变 → 跳过。取下一批直到 `cap`。
6. 从 kit / `metrics/calc-logic/{域}/` 抽**入站** `dwd_*` 表.列；**一列一题**。能挂已有 Q-id 不新开号。MODEL 只问入参键；入参键不清 → 本批记 blocked「等唐绍祖入参清单」，不问公式。
7. 需要证据时 live 只读 `gkx` 入站 `dwd_*`（`CONNECTION.md`，密码不进仓）；默认 `is_deleted=0`。
8. **先写** 该域文件 `## {今天}` 日志（可含拟改）。**停**，等人点头后再改「现行待回复」。
9. 点头后 upsert sidecar：`as_of`=当日，`summary`≤80 字，`domain` 用域码，`q_id` 对现行题号。draft 标「随口径修订」。
10. 对人回报：本批 metric 列表、类型计数、新 Q / 复用 Q、sidecar 条数。口头须含 `source_gap_indexed`（可按域 / `algorithm_type`）。**不要**把叶标 `done`（域清单齐了才 handoff）。

## 停机

- 无 `task_id` / 未认领 / Owner 对不上
- 要把 MIXED 整段甩给供应方
- 超 `cap` 或想扫 560 条
- 问 `related_entities`、项目 DWD/ADS、甲方 Q、打分公式、名称猜点
- 改 seed / 改绿 D3 / 改导出脚本（那是 PROGRESS）

## 监管人速查（§3.1）

ENT/SYNTH → 徐滕强；CHAIN → 李伟；SVC → 侯佳伟；POLICY → 淮政玮；ORG/TALENT/TECH/TNIE → 郭万迎；INNOV/COMMON 未点名 → 兜底淮政玮。
