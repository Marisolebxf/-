# 派单包：从指标定义/计算梳理三方源问题

- **状态**：方法已锁定（2026-09-01 `human:淮政玮`）；METHOD=`done`；POLICY=`integration`；PROGRESS 与其余域切片=`ready`
- **派发角色**：coordinator-agent
- **承接**：`agent:data-agent`
- **监管人**：域切片叶 = 指标进度表 **「专题维度Owner」**（见 §3.1）；METHOD / PROGRESS 跨切仍 `human:淮政玮`
- **仓**：`gkx-orchestration` / `agent-delivery`（文档 + 进度导出脚本；`cicd: skip_design_only` 除 PROGRESS 叶）
- **Epic**：`E-ALGO-LIB-DEMO`

---

## 0. 已拍板（勿再议）

| # | 决策 | 值 |
|---|------|-----|
| 1 | 指标范围 | `STAT` + **`COMPUTE`（并入本波）** + `MODEL` + `third_party` + `GRAPH` + `UNKNOWN` |
| 2 | 本波不做 | **`MIXED` 后拆**（先拆成上列类型再问；不把混合公式甩给供应方） |
| 3 | 覆盖域 | 注册表全域（企业/产业链/产业服务/政策/综合/创新/技术/机构/人才/通用/科技动态），不限最初五夹 |
| 4 | D1 多数 draft | **持续出题**；对外文档按**分析日**分组；不关 draft |
| 5 | 进度表 | **sidecar 优先**填「源缺口」；没有 sidecar 再用矩阵 `d3_gap` |
| 6 | 聚类 | 按入站 `dwd_*` 表.列一列一题，不按 560 条指标各出一题 |
| 7 | 综合域码 | **SYNTH**（不是 COMP） |
| 8 | 分发监管人 | 域切片叶认领时 `supervised_by` = 进度表 **专题维度Owner**（`topic_owner_of`）；**不是**「卡点责任方」。未点名维（创新/通用）兜底 `human:淮政玮`。覆盖 `dispatch-rules` 里 data-agent 默认监管（徐滕强） |

`LITERATURE` 本波不做（未点名）。

---

## 1. 背景

指标身份（8 件套）和计算细稿已经能看出「要哪些入站列」，但供应方问题仍散落在探针/细稿里。政策维已有一份 live 抽样清单，需要升成**可续写的日志结构**，并让「指标进度统计」Excel 的 **源缺口** 显示最新概要。

D1：`aligned` 少、`draft` 多 → 不能等齐口径再问三方；每天分析哪类算法、发现什么问题，必须可追溯。

---

## 2. 产物落点

| 产物 | 路径 |
|------|------|
| 对外清单（按域） | `agent-delivery/data/third-party-source/question/{维度}/` |
| 机器索引（sidecar） | `agent-delivery/data/third-party-source/question/source-gap-index.yaml` |
| 进度 Excel「源缺口」 | `metric-progress-export` 读 sidecar → `metrics/registry/export/指标与数据开发进度.xlsx` |
| 本包 | 本文件 |

---

## 3. 叶拆（建单用）

| ID | type | 做什么 | 依赖 |
|----|------|--------|------|
| `DATA-SUPPLIER-Q-METHOD-L01` | definition | 方法页 + 日志模板 + sidecar schema + 类型问法 + 目录补齐 | 无 |
| `DATA-SUPPLIER-Q-PROGRESS-L01` | chore | 导出脚本 + MCP 回报 + `gkx-metric-progress` skill 加「源缺口」概要计数 | METHOD |
| `DATA-SUPPLIER-Q-POLICY-L01` | definition | 政策现稿改成「现行待回复 + 按日日志」；回填 sidecar | METHOD |
| `DATA-SUPPLIER-Q-ENT-L01` | definition | 回收 COVER-STAT 细稿缺口 → 企业清单 + 日志 + sidecar | METHOD |
| `DATA-SUPPLIER-Q-{CHAIN,SVC,SYNTH,INNOV,ORG,TALENT,TECH}-L01` | definition | 按域切片；`/goal` 写明本批 `algorithm_type` + metric_id 上限 | METHOD |
| 后续切片 | definition | GRAPH 跨域 / `third_party` 跨域 / MODEL 入参 / UNKNOWN 最小键 | 按周加叶 |

COMMON / TNIE：命中本波类型再开叶，不空转。

**PROGRESS 强度**：`ponytail full`（改导出脚本）。其余 definition **禁止** ponytail 行。

### 3.1 分发：跟进度表「专题维度Owner」

真源与飞书/Excel 同函数：`metrics/registry/export/export_feishu_metric_board.py` 的 `topic_owner_of`（前缀表亦见 `feishu/feishu-metric-board.yaml` `topic_owner_map`）。

| metric_id 前缀 | 进度表域 | 专题维度Owner | 本波叶 | 认领 `supervised_by` |
|----------------|----------|---------------|--------|----------------------|
| `M_ENT_` | 企业 | 徐滕强 | `DATA-SUPPLIER-Q-ENT-L01` | `human:徐滕强` |
| `M_SYNTH_` | 综合 | 徐滕强 | `DATA-SUPPLIER-Q-SYNTH-L01` | `human:徐滕强` |
| `M_CHAIN_` | 产业链 | 李伟 | `DATA-SUPPLIER-Q-CHAIN-L01` | `human:李伟` |
| `M_SVC_` | 产业服务 | 侯佳伟 | `DATA-SUPPLIER-Q-SVC-L01` | `human:侯佳伟` |
| `M_POLICY_` | 政策 | 淮政玮 | `DATA-SUPPLIER-Q-POLICY-L01` | `human:淮政玮` |
| `M_ORG_` | 机构 | 郭万迎 | `DATA-SUPPLIER-Q-ORG-L01` | `human:郭万迎` |
| `M_TALENT_` | 人才 | 郭万迎 | `DATA-SUPPLIER-Q-TALENT-L01` | `human:郭万迎` |
| `M_TECH_` | 技术 | 郭万迎 | `DATA-SUPPLIER-Q-TECH-L01` | `human:郭万迎` |
| `M_TNIE_` | 科技动态 | 郭万迎 | 命中本波类型再开叶 | `human:郭万迎` |
| `M_INNOV_` / 其它 | 创新 / 通用 / … | **—（未点名）** | 对应 `-L01` | 兜底 `human:淮政玮`，进度表点名后再改 |

**不要用「卡点责任方」派这些叶。** 那一列按 `algorithm_type` 走：`third_party`→郭万迎、`MODEL`/`GRAPH`/…→唐绍祖、`STAT`/`COMPUTE` 才回到维 Owner。本波叶是「该域入站缺口清单」，跟维 Owner，不跟算法卡点。

跨切叶（不算专题维）：

| 叶 | `supervised_by` | 原因 |
|----|-----------------|------|
| `DATA-SUPPLIER-Q-METHOD-L01` | `human:淮政玮` | 方法/目录，已 done |
| `DATA-SUPPLIER-Q-PROGRESS-L01` | `human:淮政玮` | 进度导出脚本，不是某一维 |

派单约束：`/goal` 监管人必须抄上表；禁止把已点名维默认写成 `human:淮政玮`。`claimed_by` 可以是 `agent:data-agent`（coordinator 派）或 Owner 本人 pull，但 `supervised_by` 必须是维 Owner。未点名维禁止编造人名。

---

## 4. sidecar schema（PROGRESS 必须兼容）

`question/source-gap-index.yaml`：

```yaml
# 不是 8 件套；不是 D3 枚举真源。只给进度表「源缺口」用最新概要。
version: 1
updated: "2026-09-01"
metrics:
  M_EXAMPLE:
    as_of: "2026-09-01"          # 最近一次分析日
    algorithm_type: STAT
    q_id: POLICY-P0-3            # 现行待回复题号
    summary: "≤80字。无 INB 产业码；theme 95.7% 为字符串 NULL"
    domain: POLICY
```

Excel「源缺口」单元格：`[{as_of}] {summary}`。有 sidecar 用 sidecar；否则回落 `d3_gap`。

**禁止**：把按日流水账写入矩阵 YAML；本波不改 D3 枚举、不改绿。

MCP / skill 口头须含：`source_gap_indexed`（有 sidecar 条数）、`source_gap_fallback`（仅矩阵）、`source_gap_empty`，可按域 / `algorithm_type` 分桶。

---

## 5. 对外文档结构（各域主文件，文件名不加日期）

```markdown
# 现行待回复（滚动）
| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |

# 分析日志（新的在上）
## YYYY-MM-DD
- 本批算法类型：STAT n / COMPUTE n / GRAPH n / …
- 本批指标：（列表或附件）
- D1 快照：aligned n / draft n（本批）
- 问题表：Q-id / 现象（空值率、样例）/ 请对方确认
- 声明：草案口径标「随口径修订」
```

类型问法：

| 类型 | 问供应方什么 | 不问 |
|------|----------------|------|
| STAT / COMPUTE | 列、空值、枚举、主键、码（INB / 信用代码） | 请对方替我们 COUNT |
| GRAPH | 稳定 VID 对得上的码 | 名称猜点 |
| MODEL | 模型**入参**表与键 | 打分公式 |
| third_party | 指数/排名落哪张 `dwd_*`、主键、更新频率 | 对方如何建模 |
| UNKNOWN | 定义该指标最少要哪些键 | 假装已是 STAT |
| MIXED | **本波跳过** | — |

禁问：`related_entities`、项目 DWD/ADS、甲方 Q-*、图谱 hang 回写供应库。

---

## 6. 必读

| 文件 | 用途 |
|------|------|
| `data-lineage-policy.md` | D9；D3 ≠ 8 件套 |
| MCP `metric-registry` | kit / D1–D4；禁止整文件读 seed/矩阵 YAML |
| `metrics/calc-logic/{域}/` | 已有列级缺口 |
| `gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md` | 只消费 `dwd_*` |
| `question/政策维度/POLICY-SUPPLIER-QUESTIONS.md` | 文风与 P0/P1/P2 |
| `客户决策清单跟踪表.md` | 去重 |
| `.cursor/skills/gkx-ent-stat-cover/SKILL.md` | 企业细稿回收 |
| `metrics/registry/export/export_feishu_metric_board.py` | 「源缺口」= `d3_gap`（PROGRESS 改读 sidecar） |

---

## 7. /goal（METHOD）

```markdown
/goal data-agent
身份：data-agent。把「指标定义/计算 → 三方问题」收成可续写方法，不改 seed、不改 D3 枚举。
任务 ID：DATA-SUPPLIER-Q-METHOD-L01
监管人：human:淮政玮
仓：gkx-orchestration / agent-delivery（文档）
必读：本派单包 §0–§6 + data-lineage-policy.md + metric-mcp-usage-guide.md + POLICY-SUPPLIER-QUESTIONS.md + SUPPLIER-WORK-CONSTRAINTS.md
目标：
1. 落方法页到 question/README.md（目录按注册表域；综合=SYNTH）。
2. 锁定 sidecar schema，写好空的 source-gap-index.yaml（metrics: {}）。
3. 各域主文件模板：现行待回复 + 按日日志。
4. 写清 STAT/COMPUTE、GRAPH、MODEL、third_party、UNKNOWN 问法；MIXED 本波跳过。
5. 不写业务仓代码；不跑全量 524 条分析。
完工：handoff + cost 四字段。
```

## 8. /goal（PROGRESS）

```markdown
/goal data-agent
强度：ponytail full
身份：data-agent。进度导出「源缺口」优先读 sidecar。
任务 ID：DATA-SUPPLIER-Q-PROGRESS-L01
监管人：human:淮政玮
仓：gkx-orchestration
必读：本派单包 §4 + export_feishu_metric_board.py + scripts/lib/metric-progress-export.mjs + .cursor/skills/gkx-metric-progress/SKILL.md + metric-mcp-usage-guide.md §3.4
目标：
1. 导出读 question/source-gap-index.yaml；单元格 `[{as_of}] {summary}`；无则回落 d3_gap。
2. MCP metric-progress-export 与 --json 增加 source_gap_indexed / fallback / empty（可按域、algorithm_type）。
3. 更新 skill：对人回报须含源缺口概要计数；表头批注写明 sidecar 优先。
4. 禁止写 seed/矩阵 YAML；禁止改飞书列集合（仍用「源缺口」列）。
5. 自检：放 1 条假索引（或政策已有题）导出后该行「源缺口」非空，再删假数据。
完工：handoff + cost；ponytail: full。
```

## 9. /goal（域切片，复制后改 ID 与本批清单）

```markdown
/goal data-agent
身份：data-agent。按本批 metric_id，从 kit/细稿/live 抽出供应方问题。
任务 ID：DATA-SUPPLIER-Q-{DOMAIN}-L01
监管人：{抄 §3.1：ENT/SYNTH=human:徐滕强；CHAIN=human:李伟；SVC=human:侯佳伟；POLICY=human:淮政玮；ORG/TALENT/TECH/TNIE=human:郭万迎；未点名维=human:淮政玮}
仓：gkx-orchestration / agent-delivery
必读：METHOD 产物 + 本派单包 §5 + CONNECTION.md（密码不进仓）+ 客户决策清单
本批：algorithm_type={…}；metric_id 清单={…}（禁止超清单）
目标：
1. metric-query/get fields=full；禁止打开 registry YAML。
2. 跳过 MIXED、二次指标（<- metric:）、CMS-only。
3. live 探针入站 dwd_*；按表.列聚类；追加 ## {今天} 日志；更新现行待回复；upsert sidecar（summary≤80字）。
4. draft 照出题，标「随口径修订」。
5. 人点头后再改现行表（可先交拟改）。
完工：域 md + sidecar 增量 + handoff + cost。
```

---

## 10. DoD（父包验收，建单后拆到各叶）

- [ ] sidecar schema 稳定，进度导出「源缺口」sidecar 优先
- [ ] skill 口头含源缺口概要计数
- [ ] 政策现稿已改按日结构
- [ ] 至少一域完成「现行 + 一日日志 + 索引回填」
- [ ] MIXED 未混进对外清单
- [ ] 未把甲方 Q 写成供应方题
- [ ] 未改 seed / 未改绿 D3
