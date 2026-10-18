# SCI-INT-C03 handoff：科研机构（ORG）要素三方源入站盘点

| 项 | 值 |
|---|---|
| task_id | SCI-INT-C03（spike · 长任务 SCI-INT 段 C） |
| 执行 | agent:data-agent |
| 监管 | human:淮政玮 · claim_type=coordinator_dispatch |
| 日期 | 2026-10-18 |
| 强度 | ponytail: N/A（分析叶） |
| 产物 | `产物/SCI-INT-C03.yaml`（主产物）· `产物/_work/C03-build.py`（生成器）· `产物/_work/C03-check.py`（自检） |

## 1. 范围与实现

**范围**：展示系统三要素中的科研机构要素（高校 / 院所 / 新型研发机构 / 创新载体），盘点三方源入站情况。卡片按 `SCI-INT-总派单.md` §2 schema（layer=data）和 §4 C03 的 DoD 编写。指标范围以 `P00-baseline.yaml` 中 domain=ORG 的 22 条为准，8 件套与 D1–D4 经 MCP `metric-registry`（`metric-query domain=ORG fields=full`）复核，没有读 registry 文件。bid-reference 对照沿用 P00 基线的 SRS 映射：05 算法库 seq 99 / 114 / 115 / 149–155，04 需规 seq 60–83；页面为 DS-01-FACTORS、TOPIC-ORG-05、TOPIC-QUERY。

**实现**：每张源表或源实体一张卡，int_id `INT-C-ORG-200`～`260`，共 **39 张**：

| 段 | int_id | 张数 | 内容 |
|---|---|---|---|
| 甲方三方库 gkx（`dwd_*`） | 200–223 | 24 | 机构名录 7 张：科研院所、高校、国内工商全集、科技型标签、海外机构、海外高校、海外科研机构；带机构名称的文献/人才表 15 张：学者、工作经历、教育、合作者、中英文论文作者、中文论文、学者论文、专利、机构-专利关联、专利转移、中英文项目、中英文报告机构；另有行政区划维、产业关联企业 |
| TRSGraph | 230 | 1 | `TAG institution`（与 C04 共用） |
| 新结构（我方需建） | 240–242 | 3 | 科研机构主数据维表 `dim_research_org`、名称归一表 `map_org_alias`、文献-机构桥接表 `rel_doc_org` |
| 北京久新（全部待确认） | 250–260 | 11 | SQL-99、Python-114/115、API-149～155、TOPIC-RORG-012；覆盖久新科研机构维度的全部 11 行 |

每张卡都有 §2 全字段，另加扩展块 `data_source`，内容包括：源系统、表、关键字段、主键、实体对齐键（机构名归一 / 统一社会信用代码 / 学校标识码 / GRID·ROR 可用性）、覆盖范围（全球/中国/深圳）、更新频率、行数（值 + 快照日期 + 来源文件）、页面。`integration_pattern` 按 SCI-INT-B01 的 `initial_mapping` 填写（IP-01/06/07/08/09）。顶层四块为 `master_data_conclusion`（含「载体 vs 机构」）、`id_alignment_draft`、`metric_coverage`、`open_items`（12 项）。

**科研机构主数据结论**：当前没有任何一方持有统一的科研机构实体主数据。甲方三方库 gkx 的供应方就是久新，库里机构分散在多张互不关联的表：
- 国内科研院所 `dwd_research_institute_base_info`：约 2 千条，有 org_id 和可空的统一社会信用代码。
- 高校 `dwd_org_heis_info`：有 school_code 和信用代码，但业务行数先后为 2,933、0、回灌 1,819、估数 3,576，反复变化。
- 国内工商全集 `dwd_org_base_info`：以企业为主，没有科研机构类型码。
- 海外高校 / 海外科研机构：只有三方 org_id，没有 GRID/ROR 列，2026-08-31 的业务行数为 0。

论文、专利、项目、学者表里的机构都只有名称，唯一的例外是 `dwd_zh_report_org`，带 `org_xydm`。

草案建议我方自建科研机构主数据维表（240，全局 `org_uid`），配套名称归一表（241）和文献-机构桥接表（242）。对齐锚点的优先级为：统一社会信用代码 → 学校标识码 → 三方 org_id → 规范化名称 + 区划。久新的 11 行交付一律用我方 `org_uid` 交互。C01（人才→机构）、C02（专利申请人 / 项目承担单位→机构）的名称归一都以 241 为目标表。以上是 `decision_needed` + `structure_escalation`，不是定论。

**载体口径**：三要素口径下，ORG 只包括科研机构（含高校、新型研发机构）。但 DS-04 把「载体」定义为企业 + 机构，DS-06 定义为高校 / 研究机构 / 企业 / 工作室。团队临时默认值（🟡）：ORG 主数据只收院所、高校、新型研发机构；企业和工作室类载体留在 `dwd_org_base_info`（INNOV/ENT 域），载体榜按 `org_category` 联合两侧。此项登记为 OI-C03-02，待甲方拍板。

**指标覆盖**：22/22 全部列出源卡，差集 0，no_source 0。其中 21 条绑定为 `jiuxin_pending`：7 条 B08 深度模型直接对应久新 API；10 条专题指标按 B01 的 IP-09 派生自 SRS-99/149/151/152/153/154/155，`M_ORG_TECH_SCORE` 直接对应久新无专叶行 TOPIC-RORG-012（IP-08）；另外 3 条是 BASE_99 / GRAPH_114 / GRAPH_115。剩余 1 条为 `candidate`：`M_ORG_PERF_QUERY` 是 STAT 自建（IP-01），依赖 240 和 242。22 条的 kit `source_tables` 全部是 `pending_ods`，所以没有 `kit_declared` 级别的绑定。「有源卡」只说明原料候选或久新行已经识别出来，不等于数据就绪。

## 2. 偏离说明

1. 卡片在 §2 schema 之外增加了 `data_source` 扩展块（与 C02 一致），§2 原有字段一个不少。
2. 总派单写的是 spike 完工进 `integration`；本次按 coordinator 派单指令推进到 `ready_to_sign`（spike 的 AV-0 目标）。
3. 行数全部引自仓内快照：
   - 2026-10-10 估数报告（`TABLE_ROWS`，未过滤 is_deleted）
   - 2026-08-31 精确 COUNT（is_deleted=0，部分表有 2 万 / 5 万样例上限）
   - 2026-09-11 差异摘要

   两种口径的值在卡上同时列出。快照里查不到的表写 `unknown`（`dwd_org_base_info_patent_rel`、TRSGraph institution）。**本叶没有连库。**
4. 学者系列表（207–210、214）与 C01 共用，文献表（211–219）与 C02 共用，卡上标了 `shared_with`；`dwd_org_base_info`（202）以 C03 为主卡。没有写 C01/C02 的文件。
5. 发现架构初稿 §3 与页面映射之间有冲突。初稿写「DS-04 依赖 99/149/153、DS-06 依赖 151/152」，但 `DS-04-CARRIER-RANK.yaml` 明确禁止挂 seq 99/149/154/155，`DS-06-CARRIER.yaml` 禁止挂 151/152。本叶以页面映射为准，没有把这两页挂到 ORG 指标上；回改初稿列为 OI-C03-11（architect）。

建议的只读核对 SQL（**未执行**，留给下一步有连库权限时用；库 `gkx`，账号 `gkx_reader_zp`）：

```sql
SELECT COUNT(*) FROM gkx.dwd_org_heis_info WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_research_institute_base_info WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_forg_university_org_info WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_forg_research_org_info WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_forg_base_info WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_org_base_info_patent_rel WHERE is_deleted = 0;
SELECT org_tag, COUNT(*) FROM gkx.dwd_org_tech_tag WHERE is_deleted = 0 GROUP BY org_tag;
SELECT COUNT(*), SUM(external_id IS NOT NULL AND external_id <> '') FROM gkx.dwd_research_institute_base_info WHERE is_deleted = 0;
```

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-C03.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/C03-build.py`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/C03-check.py`
- 本 handoff

未 git commit / push（按派单要求）。

## 4. 验收证据

运行 `python 产物/_work/C03-build.py` 和 `python 产物/_work/C03-check.py`（2026-10-18），输出：

```
wrote SCI-INT-C03.yaml: cards=39 no_source=0
OK cards=39 gap=0 by_counterpart={'gkx_mysql_raw': 24, 'trsgraph': 1, 'none': 3, 'jiuxin': 11}
OK ORG metrics scope=22 covered=22 no_source=0 [] diff=0
OK jiuxin 科研机构行=11 全部挂卡 diff=0 · structure_escalation=3 · open_items=12
```

`C03-check.py` 断言的内容：
- P00 基线 ORG 指标为 22 条，与 `metric_coverage` 双向差集为 0。
- int_id 唯一，且都在 200–299 号段内。
- `scope_count == card_count == len(cards)`，`gap` 为空。
- 每张卡 `data_source` 的必填字段非空，行数带来源；每张卡至少挂一条指标。
- 覆盖表引用的源卡都存在，卡上 `metric_ids` 与覆盖表双向一致。
- 久新科研机构 11 行与卡上 `jiuxin_row_id` 完全相等，久新卡都带「待确认」。
- 新结构卡都标了 `structure_escalation`。
- 主数据结论和载体口径块非空；GRID/ROR 标为 unknown。

汇总：
- 源卡数：39（scope_count = card_count = 39，gap = 0）
- 指标覆盖：22/22，差集 0，no_source 0
- structure_escalation：3 张（240 主数据维表、241 名称归一表、242 文献-机构桥接表），升级 human:李伟
- decision_needed：18 条（分散在各卡）；置信度 high 4 / medium 11 / low 24

**最大的 3 个开放项**：

1. OI-C03-01：科研机构主数据由谁持有、全局 `org_uid` 怎么定。供应方 ORG-P0-1（主表 / 主键 / 稳定码）自 2026-09-04 未回，卡住 22 条指标。
2. OI-C03-02：载体是否等于机构（企业 / 工作室是否进 ORG），新型研发机构 / 创新载体如何认定（是否用 `dwd_org_tech_tag` 圈定）。需甲方拍板。
3. OI-C03-06：久新科研机构 11 行的交付形态和数据底座（用我方 gkx 入站数据还是其自有库），21 条指标挂在这上面。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 久新 Python-114/115 和 API 适配层都放在 `lumen-algo-py`；名称归一 Job 放在 Python；Java 只读 ADS |
| 2 调用链 前端→Java→Python `/internal/*` | ✅ 卡上 `call_chain` 均按此填写；久新只经 Python 适配层接入，前端和 Java 不直连 |
| 3 图谱只用 NebulaGraph TRSGraph | ✅ 230 指向 TRSGraph `TAG institution`，VID 迁移交 C04；无 Neo4j |
| 4 可观测 | N/A（分析叶，无运行代码） |
| 5 CI/CD | N/A（只改编排文档） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 / Java 不写 nGQL、只读 ADS | ✅ |
| 8 ADS 先行、Mock 填充、三方到位再映射 | ✅ 22 条 D4 现状均为 mock，卡上如实标注 |
| 9 D8 前端规范 | N/A |
| 10 D9 血缘 | ✅ 8 件套与 D1–D4 只经 MCP `metric-registry` 读取，未读也未改 seed 与矩阵 |
| 11 D10 交互规范 | N/A |
| 12 D12 demo/lumen 隔离 | ✅ lumen 链路下游只写 `gkxlumen-*` / `lumen-algo-py` / `lumen-etl-es-py`，没有出现 `demo-*` |
| 人机：不替甲方拍板 | ✅ 载体口径、新型研发机构认定、深圳圈定都写成 `decision_needed`，团队默认值标 🟡；久新行全部「待确认」；查不到写 `unknown` |
| 只读 | ✅ 未连库、未写库、未改业务仓，未读 `task-registry.yaml` 与 `metrics/registry/` |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ≈420,000（估算） |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ≈$7.0（估算） |
| cost_warn | yellow（>$5，<$10） |
