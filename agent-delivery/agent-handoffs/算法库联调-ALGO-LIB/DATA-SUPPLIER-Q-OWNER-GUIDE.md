# 三方问题清单 — 维 Owner 使用说明

给：**徐滕强、李伟、侯佳伟、郭万迎**  
（进度表「专题维度Owner」；不是「卡点责任方」）  
日期：2026-09-01 · Epic `E-ALGO-LIB-DEMO`

你们要做的事：把**本维指标**卡住的入站字段，写成可以发给供应方的书面题。每天切一批，不要一次扫全库。

---

## 1. 你认领哪几条

registry 叶都是 `ready`，等你们认领。执行 Agent 一律 `data-agent`。`supervised_by` 必须是你自己。

| 你 | 认领这些 ID | 域 | 目录 | 发给谁 |
|----|-------------|----|------|--------|
| **徐滕强** | `DATA-SUPPLIER-Q-ENT-L01` | 企业 | `question/企业维度/` | 默认供应方 |
| **徐滕强** | `DATA-SUPPLIER-Q-SYNTH-L01` | 综合（码是 **SYNTH**，不是 COMP） | `question/综合维度/` | 默认供应方 |
| **李伟** | `DATA-SUPPLIER-Q-CHAIN-L01` | 产业链 | `question/产业链维度/` | 默认供应方 |
| **侯佳伟** | `DATA-SUPPLIER-Q-SVC-L01` | 产业服务 | `question/服务机构维度/` | 默认供应方 |
| **郭万迎** | `DATA-SUPPLIER-Q-ORG-L01` | 机构（科研机构，**不是** SVC） | `question/机构维度/` | **久新** |
| **郭万迎** | `DATA-SUPPLIER-Q-TALENT-L01` | 人才 | `question/人才维度/` | **久新** |
| **郭万迎** | `DATA-SUPPLIER-Q-TECH-L01` | 技术 | `question/技术维度/` | **久新** |

不归你们：`METHOD`（已完成）、`POLICY`（淮政玮会签中）、`PROGRESS`（导出脚本）、`INNOV`（未点名）。科技动态 `TNIE` 命中本波类型再开叶，监管人仍是郭万迎。

郭万迎三叶**只给久新**，文首写「对接：久新」。不要和侯佳伟的产业服务、也不要和政策/企业那份清单混成一封邮件。

---

## 2. 这件事是什么

从指标 8 件套 / 细稿里看出「供应库哪张 `dwd_*`、哪一列缺或脏」，按**表.列**聚成一题。口径可以还是 `draft`，题上标「随口径修订」。

**不是**：改 seed、改绿 D3、写算法、请对方替我们 COUNT / 打分。MODEL 只问**入参键**；`MIXED` 本波整段跳过（先王惠+唐绍祖拆类型）。

样例（政策维已跑过一轮）：`question/政策维度/POLICY-SUPPLIER-QUESTIONS.md`。

---

## 3. 怎么开工（认领）

在 Cursor 打开 `gkx-orchestration`，对 agent 说（改 ID 和自己的名字）：

```text
认领 DATA-SUPPLIER-Q-ENT-L01
claimed_by: agent:data-agent
supervised_by: human:徐滕强
```

李伟把 ID 换成 `…-CHAIN-L01`、监管人 `human:李伟`；侯佳伟 `…-SVC-L01` / `human:侯佳伟`；郭万迎三条各认领一次，监管人 `human:郭万迎`。

认领后状态应是 `claimed`，开工改文档时转 `in_progress`。没有认领**不要**改 `question/`。

必读（agent 会跟）：

- 方法：`agent-delivery/data/third-party-source/question/README.md`
- 派单：`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md`
- 每日步骤：`.cursor/skills/gkx-supplier-q-daily/SKILL.md`
- 企业细稿：`.cursor/skills/gkx-ent-stat-cover/SKILL.md`（徐滕强 ENT 叶）

---

## 4. 每天怎么跑

一天只跑**一个**已认领的叶，`cap` 建议 20（最多 30）。对 agent 说：

```text
按 gkx-supplier-q-daily
task_id: DATA-SUPPLIER-Q-CHAIN-L01
domain: CHAIN
cap: 20
```

`domain` 对照：企业 `ENT`、综合 `SYNTH`、产业链 `CHAIN`、产业服务 `SVC`、机构 `ORG`、人才 `TALENT`、技术 `TECH`。

当天 agent 应做到：

1. 用 MCP 读指标 kit（**不要**打开 registry YAML）。
2. 跳过 MIXED、二次指标。CMS/资讯库/其它外部（不限久新）要列题；不问本方 ADS 表名。
3. 已在 `source-gap-index.yaml` 里且问法没变的跳过。
4. **先写**该域文件里的 `## 今天日期` 分析日志（可含拟改）。
5. **停下来等你点头**，再改「现行待回复」、再 upsert sidecar。

你点头看三件事：问的是不是**外部原料**（`dwd_*` 或 CMS/资讯库，不限是否久新）；有没有把甲方 Q / 公式 / 本方 ADS 甩给对方；ORG/TALENT/TECH 要素库题仍只给久新，CMS 题按实际对接方转发。

发给对方看「现行待回复」。分析日志可以对日期。`source-gap-index.yaml` 给进度表，**不要**发给供应方。

---

## 5. 各叶注意

| 叶 | 注意 |
|----|------|
| ENT | 本批以 STAT/COMPUTE 为主；细稿在 `metrics/calc-logic/ENT/`。企业 MODEL 入参可以留到后续切片。 |
| SYNTH | 先拆跨维依赖：企业/产业链已经问过的列不要再问一遍。MODEL 只问入参键。 |
| CHAIN | GRAPH 只问能对上 VID 的稳定码（如 INB），不要名称猜点。 |
| SVC | 产业服务；不要和郭万迎的「机构 ORG」串题。 |
| ORG / TALENT / TECH | 对接久新；ORG ≠ SVC。 |

没有 `*-SUPPLIER-QUESTIONS.md` 时，从 `question/_TEMPLATE-SUPPLIER-QUESTIONS.md` 复制到本维目录（**文件名不加日期**）。

---

## 6. 什么时候找唐绍祖 / 王惠

| 谁 | 你卡住时找他们 |
|----|----------------|
| **唐绍祖** | MODEL 不知道要哪些入参列 → 记「等入参清单」，不要把打分公式写进供应方题。 |
| **王惠** | `MIXED` / `UNKNOWN` 类型没拆清 → 本波不进对外清单，等拆成单一类型再问。 |

他们给的是**上游材料**，不是这几条叶的产出。进度表里 MODEL 的「卡点责任方」仍是唐绍祖，但**这几条叶的监管人是你**。

---

## 7. 禁止

- 改 seed、改矩阵、把 D3 改绿
- 问 `related_entities`、项目自建 DWD/ADS、甲方决策清单上的 Q-*
- 请对方替我们算指标或训模型
- 一天扫全库、或不带 `task_id` / `cap` 就开跑
- 把 ENT/CHAIN/SVC 的题和久新三份混发
- 叶没做完就标 `done`（现行表 + 至少一日日志 + sidecar 齐了再 handoff）

提交走编排仓 `origin/dev`，commit 带 `[agent:data-agent]` 或 `[human:你的名]`。未点名不要 push。

---

## 8. 参考路径（编排仓内）

```
agent-delivery/data/third-party-source/question/
  README.md                          ← 方法
  _TEMPLATE-SUPPLIER-QUESTIONS.md
  政策维度/POLICY-SUPPLIER-QUESTIONS.md   ← 文风样例
  source-gap-index.yaml              ← 进度表「源缺口」游标
.cursor/skills/gkx-supplier-q-daily/SKILL.md
```

问题找淮政玮（本波总控）。导出进度 Excel 不是你们这几条叶。
