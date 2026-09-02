# question — 给三方供应方的问题清单

> **方法真源**：`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md`（2026-09-01 `human:淮政玮` 锁定）。  
> **分发**：域切片叶监管人 = 指标进度表 **专题维度Owner**（派单包 §3.1）；不是「卡点责任方」。  
> **维 Owner 怎么开工**：[`../../agent-handoffs/算法库联调-ALGO-LIB/DATA-SUPPLIER-Q-OWNER-GUIDE.md`](../../agent-handoffs/算法库联调-ALGO-LIB/DATA-SUPPLIER-Q-OWNER-GUIDE.md)（徐滕强 / 李伟 / 侯佳伟 / 郭万迎）。  
> 只问供应方入站 **`dwd_*` 字段与主键**，不问项目派生列（如 `related_entities`）、不问项目自建 DWD/ADS、不问甲方口径 Q-*、不请对方替我们算指标。  
> 供应方分层约束：[`../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md`](../gkx-mysql-raw/加工/SUPPLIER-WORK-CONSTRAINTS.md)（只消费 `dwd_*`；`ods_*` 不暴露、不作正式映射真源）。

本目录是「指标定义 / 计算细稿 → 三方书面问题」的**可续写落点**。后续域切片叶复制模板、按分析日追加日志、回填 sidecar；本页只定方法，不代替各域现稿，也不虚构题目。

---

## 1. 范围（已拍板，勿再议）

| 项 | 值 |
|----|-----|
| 本波算法类型 | `STAT` + `COMPUTE` + `MODEL` + `third_party` + `GRAPH` + `UNKNOWN` |
| 本波不做 | **`MIXED` 后拆**（先拆成上列类型再问；不把混合公式甩给供应方）；`LITERATURE` 未点名，本波不做 |
| 覆盖域 | 注册表全域（下表）；综合域码 = **`SYNTH`**（不是 `COMP`） |
| D1 | 多数 `draft` → **持续出题**；草案口径标「随口径修订」；不关 draft、不等 `aligned` 再问 |
| 进度表「源缺口」 | sidecar [`source-gap-index.yaml`](source-gap-index.yaml) **优先**；无 sidecar 回落矩阵 `d3_gap` |
| 聚类 | 按入站 **`dwd_*` 表.列一列一题**，不按每条指标各出一题 |
| 文件名 | **不加日期**；日期只写在「分析日志」章节 |

**与 D9 的边界**（[`data-lineage-policy.md`](../../data-lineage-policy.md)）：

- 8 件套是指标身份证（含 `algorithm_type`）；**D3 源映射不是 8 件套**。
- 本目录 sidecar **不是** 8 件套、**不是** D3 枚举真源；禁止本波改 D3 枚举、禁止把按日流水账写入矩阵 YAML、禁止改绿。
- 查 kit / D1–D4 走 MCP `metric-registry`（`metric-get` / `metric-query`）；**禁止**整文件打开 `metrics/registry` 的 seed / 矩阵 YAML。

---

## 2. 目录（注册表域）

| 维度目录 | 域码 | 中文枚举 | 进度表专题维度Owner | 清单 |
|----------|------|----------|---------------------|------|
| [产业链维度/](产业链维度/) | CHAIN | 产业链 | 李伟 | [CHAIN-SUPPLIER-QUESTIONS.md](产业链维度/CHAIN-SUPPLIER-QUESTIONS.md)（`DATA-SUPPLIER-Q-CHAIN-L01`，2026-09-02） |
| [企业维度/](企业维度/) | ENT | 企业 | 徐滕强 | [ENT-SUPPLIER-QUESTIONS.md](企业维度/ENT-SUPPLIER-QUESTIONS.md)（`DATA-SUPPLIER-Q-ENT-L01`，2026-09-01） |
| [政策维度/](政策维度/) | POLICY | 政策 | 淮政玮 | [POLICY-SUPPLIER-QUESTIONS.md](政策维度/POLICY-SUPPLIER-QUESTIONS.md)（现稿结构由 **POLICY-L01** 改成按日；本方法叶不改） |
| [服务机构维度/](服务机构维度/) | SVC | 产业服务 | 侯佳伟 | [SVC-SUPPLIER-QUESTIONS.md](服务机构维度/SVC-SUPPLIER-QUESTIONS.md)（`DATA-SUPPLIER-Q-SVC-L01` 2026-09-02 首批） |
| [综合维度/](综合维度/) | **SYNTH** | 综合 | 徐滕强 | [SYNTH-SUPPLIER-QUESTIONS.md](综合维度/SYNTH-SUPPLIER-QUESTIONS.md)（`DATA-SUPPLIER-Q-SYNTH-L01`，2026-09-01；不重问 ENT 已问列） |
| [创新维度/](创新维度/) | INNOV | 创新 | —（未点名） | 待补 |
| [机构维度/](机构维度/) | ORG | 机构 | 郭万迎 | **对接久新**；待补 |
| [人才维度/](人才维度/) | TALENT | 人才 | 郭万迎 | **对接久新**；待补 |
| [技术维度/](技术维度/) | TECH | 技术 | 郭万迎 | **对接久新**；待补 |
| [通用维度/](通用维度/) | COMMON | 通用 | —（未点名） | 待补（命中本波类型再写，不空转） |
| [科技动态维度/](科技动态维度/) | TNIE | 科技动态 | 郭万迎 | 待补（命中本波类型再写，不空转） |

发给对方看「现行待回复」；分析日志可一并转发以便对日期。机器索引给进度 Excel，不发给供应方。

域切片 registry 叶认领时 `supervised_by` 抄上表 Owner（未点名兜底 `human:淮政玮`）。不要用进度表「卡点责任方」派这些叶。对照派单包 §3.1。

**可复制空壳**（文件名不加日期）：[`_TEMPLATE-SUPPLIER-QUESTIONS.md`](_TEMPLATE-SUPPLIER-QUESTIONS.md)。新域开写时复制为 `{DOMAIN}-SUPPLIER-QUESTIONS.md`（如 `ENT-SUPPLIER-QUESTIONS.md`）。

---

## 3. 算法类型问法

出题前用 MCP 读该条 `kit.algorithm_type`（未填视为 `UNKNOWN`）。问法只针对**入站 `dwd_*`**。

| 类型 | 问供应方什么 | 不问 |
|------|----------------|------|
| `STAT` / `COMPUTE` | 列是否存在、空值约定（SQL `NULL` / 空串 / 字符串 `"NULL"`）、合法枚举、主键、稳定码（产业 `INB*`、统一社会信用代码 / 组织机构代码） | 请对方替我们 `COUNT` / 去重 / 写公式 |
| `GRAPH` | 能对上我方稳定 VID 的**码**（如 `chain:{chain_id}`、`segment:{node_id}`、`pol:{id}` 所需的对方主键或产业码） | 用名称猜点；请对方在供应库里帮我们 hang 图 |
| `MODEL` | 模型**入参**落在哪张 `dwd_*`、哪些键、空值与更新频率 | 打分公式、权重、模型怎么训 |
| `third_party` | 指数 / 排名落哪张 `dwd_*`、主键、更新频率 | 对方如何建模、指数口径公式 |
| `UNKNOWN` | 定义该指标**最少要哪些键**（表.列清单），方便后续判类型 | 假装已经是 `STAT` 去要聚合结果 |
| `MIXED` | **本波跳过**；先拆成上列单一类型再问 | 把混合公式整段甩给供应方 |
| `LITERATURE` | **本波不做** | — |

### 3.1 一律禁问

| 禁问 | 原因 |
|------|------|
| `related_entities` 及同类项目派生列 | 我方 `ods_to_dwd` / 自建 DWD 拼的，供应库无此列 |
| 项目自建 DWD / DWS / ADS 表名与字段 | 供应方工作面只有入站 `dwd_*` |
| 甲方口径题（`客户决策清单跟踪表.md` 的 Q-* / QPOL-* 等） | 那是甲方拍板，不是供应方补字段 |
| 图谱 hang 回写供应库 | 图侧只读入站；不把 C 档回写当供应方义务 |
| 请对方替我们算指标 | 计算在项目侧（Java 聚合 / Python `/internal/*`）；对方只保证原料列 |

### 3.2 跳过、不进对外清单

- `MIXED`（本波）；拆类型后再开题。
- 二次指标（细稿 / formula 标明依赖 `<- metric:` 的派生）：缺口跟源指标走，不向供应方重复要同一列。
- CMS-only / 无入站 `dwd_*` 依赖：不编造供应方题。
- 未命中本波类型的 COMMON / TNIE：不空转开文件。

---

## 4. 现行待回复（滚动表，发给对方）

各域主文件**文件名不加日期**。表头固定如下；一行 = **一个入站 `dwd_*` 表.列**（多条指标卡在同一列 → 同一 Q-id，`卡住的 metric_id` 列并列）。

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| `{DOMAIN}-{P0\|P1\|P2}-{n}` | P0 / P1 / P2 | `dwd_foo.bar` | 一句话 + 请确认项 | `M_…`（可多个） | `YYYY-MM-DD` |

**Q-id**：`{域码}-{优先级}-{序号}`，例 `POLICY-P0-3`、`ENT-P1-12`。域内序号稳定，不因分析日重编号。关闭或改问时在日志写变更，表内更新或删行。

**优先级**（文风对齐政策现稿，不强制政策那套 P0 长文结构）：

| 级 | 含义 |
|----|------|
| P0 | 请书面确认并给样例；缺了则图谱 hang / 主键 / 稳定码做不成 |
| P1 | 请说明有没有、在哪张 `dwd_*`；给表名 + 样例 3 行 |
| P2 | 技术约定（id 长度、撞号、`is_deleted` 过滤等） |

**draft**：`卡住的 metric_id` 旁或问什么末尾标「随口径修订」。D1 升 `aligned` 后不必删题，除非列已确认无缺口。

对方回复格式（可附在域文件文末，与政策现稿同构）：

| 项 | 内容 |
|----|------|
| 问题编号 | Q-id |
| 现状 | 字段 / 表 / 当前规则 |
| 能否补 | 是 / 否 / 排期（日期） |
| 样例 | 1 条：对方主键 + 字段原值 |
| 空值规则 | SQL NULL / 空串 / `"NULL"` / 其他 |

---

## 5. 分析日志（按日，新的在上）

日期只出现在标题 `## YYYY-MM-DD`，**不要**把日期写进文件名。每天分析哪类算法、抽样哪张入站表、发现什么问题，必须可追溯。

```markdown
## YYYY-MM-DD
- 本批算法类型：STAT n / COMPUTE n / GRAPH n / MODEL n / third_party n / UNKNOWN n
- 本批指标：（metric_id 列表或附件路径；禁止超本叶 /goal 清单）
- D1 快照：aligned n / draft n（本批；MCP 只读，禁止改矩阵）
- 入站抽样：库 / 表 / 过滤（默认 `is_deleted=0`）/ 行数
- 问题表：Q-id / 入站表.列 / 现象（空值率、样例）/ 请对方确认
- 声明：草案口径标「随口径修订」
- sidecar：本批 upsert 了哪些 metric_id（或「无，仅日志」）
```

规则：

1. **先写当日日志**（可含拟改）；**现行待回复**改表须人点头（监管人 / 数据 lead），可先交拟改。
2. 同一列后续日只追加现象（新空值率、新样例），不新开 Q-id，除非问法实质变了。
3. 日志可以发给对方对日期；进度表不读日志，只读 sidecar。

---

## 6. sidecar（进度表「源缺口」）

路径：[`source-gap-index.yaml`](source-gap-index.yaml)。字段注释以该文件为准（METHOD 锁定）；`metrics` 在未做域切片前可为 `{}`。

| 键 | 含义 |
|----|------|
| `version` | schema 版本，当前 `1` |
| `updated` | 本文件最近写入日 |
| `metrics.{metric_id}` | 一条指标一行；**不是** 8 件套 |
| `.as_of` | 最近一次分析日 |
| `.algorithm_type` | 本波类型之一 |
| `.q_id` | 现行待回复题号 |
| `.summary` | **≤80 字**；Excel 单元格用 |
| `.domain` | 域码（`SYNTH` 不是 `COMP`） |

Excel「源缺口」单元格（PROGRESS-L01 接线，本叶不改导出脚本）：

```text
[{as_of}] {summary}
```

有 sidecar 用 sidecar；否则回落矩阵 `d3_gap`。口头计数（PROGRESS / skill）：`source_gap_indexed`（有 sidecar 条数）、`source_gap_fallback`（仅矩阵）、`source_gap_empty`，可按域 / `algorithm_type` 分桶。

---

## 7. 从指标到一题（续写步骤）

后续 `DATA-SUPPLIER-Q-{DOMAIN}-L01` 按此做；**本方法叶不跑全量指标、不 live 探针**。每日切片执行：`.cursor/skills/gkx-supplier-q-daily/SKILL.md`（须已认领叶 + `cap`；先写当日日志，人点头后再改现行表）。

1. 读本页 + 派单包 §0–§6 + 供应方约束；查 `客户决策清单跟踪表.md` 去重（已有甲方 Q 不改写成供应方题）。
2. MCP `metric-query` / `metric-get`（`fields=full`）拿 kit（含 `algorithm_type`、`source_tables`）与 D1–D4；禁止打开 registry YAML。
3. 过滤：本波类型；跳过 `MIXED`、二次指标、CMS-only。
4. 从 kit / `metrics/calc-logic/{域}/` 细稿抽出**入站** `dwd_*` 表.列；按 **表.列聚类**。
5. 需要证据时 live 只读 `gkx` 入站 `dwd_*`（密码不进仓，见 `gkx-mysql-raw/CONNECTION.md`）；默认 `is_deleted=0`。
6. 复制或打开该域 `{DOMAIN}-SUPPLIER-QUESTIONS.md`：追加 `## {今天}`；拟改现行表。
7. 人点头后更新现行待回复；upsert sidecar（`summary`≤80 字，`as_of`=当日）。
8. draft 照出题，标「随口径修订」。

政策现稿已有 P0/P1/P2 长文，**POLICY-L01** 负责改成「现行待回复 + 按日日志」并回填 sidecar；其他域不要把政策那份拆成按日——那是政策叶的事。

---

## 8. 本目录不做什么

| 不做 | 谁做 / 何时 |
|------|------------|
| 改 `POLICY-SUPPLIER-QUESTIONS.md` 章节结构 | `DATA-SUPPLIER-Q-POLICY-L01` |
| 改 `export_feishu_metric_board.py` / 进度导出 | `DATA-SUPPLIER-Q-PROGRESS-L01` |
| 改 seed / 矩阵 / D3 枚举 | 禁止本波 |
| 全量 524+ 条分析、虚构各域题目 | 域切片叶按 `/goal` 清单 |
| 业务仓代码、Java/Python 算法 | 本目录只文档 |
