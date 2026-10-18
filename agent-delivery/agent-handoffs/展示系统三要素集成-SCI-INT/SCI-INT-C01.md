# SCI-INT-C01 handoff：人才（TAL）要素三方源入站盘点

| 项 | 值 |
|---|---|
| task_id | SCI-INT-C01（spike · 长任务 SCI-INT 段 C） |
| 执行 | agent:data-agent |
| 监管 | human:淮政玮 · claim_type=coordinator_dispatch |
| 日期 | 2026-10-18 |
| 强度 | ponytail: N/A（分析叶） |
| 产物 | `产物/SCI-INT-C01.yaml`（主产物）· `产物/_work/C01-build.py`（生成器）· `产物/_work/C01-check.py`（自检）· `产物/_work/C01-metric-dump.py`（MCP 输出压平） |

## 1. 范围与实现

**范围**：展示系统人才要素（学者 / 履历 / 教育 / 人才标记 / 研究方向 / 论文 / 合作 / 文献作者 / 发明人 / 项目人员 / 高管 / 人才关系）的三方源入站盘点。卡片格式按 `SCI-INT-总派单.md` §2（layer=data），号段 `INT-C-TAL-001`～`099`。指标范围以 `P00-baseline.yaml` 中 domain=TALENT 的 32 条为准；8 件套与 D1–D4 经 MCP `metric-registry`（`metric-query domain=TALENT fields=full`）复核，未读 registry 文件。页面对照：展示系统 DS-13～16（人才全局 / 区域 / 画像 / 招引），以及 DS-01-FACTORS、DS-08-VIZ、DS-26-ECO、专题 TOPIC-TALENT / TOPIC-QUERY。

**实现**：每张源表或源实体一张卡，共 **43 张**：

| 段 | int_id | 张数 | 内容 |
|---|---|---|---|
| 甲方三方库 gkx（`dwd_*`） | 001–025 | 24 | 人才要素库 8 表（scholar / work_experience / education_background / talent_flag / research_direction / paper_relation / papers / coauthor）；中英文论文作者；`dwd_author_info` 及 author_*_rel 族（0 行）；`dwd_author_affiliation`；`dwd_rel_project_scholar` / `dwd_rel_report_scholar` / `dwd_zh_report_scholar`；中英文报告作者；专利发明人；国内项目主持人 / 参与人；量子前沿人才；国内外机构高管；国内外机构基础信息（机构归一，C03 主卡） |
| 我方维表 | 026 | 1 | `dim_code_region` / `dim_code_country` / `dim_region_scope`（区域和深圳切片经机构二跳） |
| 北京久新（全部待确认） | 040–052 | 13 | SQL-98、Python-110/111、API-156～165；API-162 卡同挂展示 DS-08-VIZ-001/004；久新人才 15 行全部挂上 |
| TRSGraph | 060–061 | 2 | 人才顶点、人才边（合作 / 任职 / 毕业 / 项目共参 / 流动） |
| 新结构（我方需建） | 070–072 | 3 | 人才主档、人才流动边（由履历派生）、人员 ID 映射表（人名消歧结果落表） |

每张卡包含 §2 的全部字段，另加扩展块 `data_source`，记录：源系统、表、关键字段、主键、实体对齐键（人名消歧 / 机构名归一）、覆盖范围、更新频率、行数（值 + 快照日期 + 来源文件）、页面、`shared_with`。顶层另有四块：`master_data_conclusion`、`id_alignment_draft`、`metric_coverage`、`open_items`（15 项）。

**人才主数据结论（草案，待确认）**：三方库 gkx 人才要素库里的 `dwd_scholar.scholar_id`（001）是唯一同时满足以下条件的人员表，所以作为人才实体主数据的候选：
- 有稳定业务 ID；
- 带履历、教育、研究方向、论文、合作者；
- `dwd_rel_project_scholar` / `dwd_rel_report_scholar` 已用「算法绑定后的 scholar_id」挂接。

草案方案：我方人才主档（070）沿用 scholar_id 作主键。论文 / 报告作者 ID、Scopus auid、专利发明人、项目主持人、机构高管等次级源，一律经人员 ID 映射表（072）对齐到 scholar_id。久新接口以 scholar_id 交互。

有三个前提还没确认：
- scholar_id 是否稳定（TALENT-P0-1 / SYNTH-P2-1）；
- 全量覆盖范围（2026-08-31 精确计数时各表恰好 20,000 行，是样例）；
- 地理、领域、机构码、性别、国籍、职称都缺列。

因此本结论只是 `decision_needed` 加 `structure_escalation`，不是定论。

**指标覆盖**：32/32 全部列出源卡或 `no_source`，差集 0。绑定强度：
- `jiuxin_pending` 25 条（依赖久新交付）；
- `candidate` 1 条（`M_TALENT_STRUCT_QUERY`，我方 STAT：学历取 education.degree，职称 / 年龄无列）；
- `no_source` 6 条（DS-16 招引 005 / 006 / 007 / 010 / 013 / 025：算法库没有专叶，三方无原料，JIUXIN 纪要明确不向久新要假 API）；
- `kit_declared` 0 条（32 条 kit 的 source_tables 全部是 pending_ods）。

## 2. 偏离说明

1. 卡片在 §2 schema 外增加了 `data_source` 扩展块，用于承载派单要求的源表字段。§2 原有字段全部保留，做法与 C02 一致。
2. 总派单写的是 spike 完工进 `integration`；本次按 coordinator 派单指令推进到 `ready_to_sign`（即 spike 的 AV-0 目标）。
3. `integration_pattern` 统一填 `TBD`，因为 B01 尚未产出。
4. 行数全部引自仓内快照，**本叶没有连库，也没有执行任何 SQL**：
   - 主要来源是 2026-10-10 估数报告（`TABLE_ROWS`，未过滤 is_deleted）；
   - 2026-08-31 精确 COUNT 用于说明样例；
   - 2026-08-03 / 08-10 探针用于 author 族。
   - 估数波动大，例如 paper_relation 在 08-19 探针为 1,928,994，10-10 为 887,927。查不到的表写 `unknown`，并列入 OI-C01-11 / 12。
5. 与其他叶共用的表：`dwd_scholar_papers`、`dwd_scholar_research_direction` 与 C02 共用，`dwd_patent`、`dwd_zh_project` 以 C02 为主卡；`dwd_org_base_info`、`dwd_forg_base_info` 和地理维表与 C03 共用。卡上都标了 `shared_with`，没有改 C02 / C03 的文件。
6. 专题人才模块的 12 条（各类 SCORE / DIST / FLOW 等）在 MCP `srs_refs` 中没有 page_id，页面只记到模块级 `TOPIC-TALENT`，没有自行推断页面。
7. 在途任务 DATA-SUPPLIER-Q-TALENT-L01 的 7 道供应方问题只引用，未改动。

建议的只读核对 SQL（**未执行**，留给下次有连库权限时用；库 `gkx`，账号 `gkx_reader_zp`）：

```sql
SELECT COUNT(*) FROM gkx.dwd_scholar WHERE is_deleted = 0;
SELECT COUNT(*), COUNT(DISTINCT scholar_id) FROM gkx.dwd_scholar WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_scholar_paper_relation WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_rel_project_scholar WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_rel_report_scholar WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_quantum_frontier_talent WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_author_info WHERE is_deleted = 0;
-- scholar_id 挂接命中率（只读）
SELECT COUNT(*) FROM gkx.dwd_rel_project_scholar r LEFT JOIN gkx.dwd_scholar s ON s.scholar_id = r.scholar_id WHERE s.scholar_id IS NULL;
SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor c LEFT JOIN gkx.dwd_scholar s ON s.scholar_id = c.co_scholar_id WHERE s.scholar_id IS NULL;
```

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-C01.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/C01-build.py`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/C01-check.py`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/C01-metric-dump.py`
- 本 handoff

按派单要求，未 git commit / push。

## 4. 验收证据

2026-10-18 运行 `python 产物/_work/C01-build.py; python 产物/_work/C01-check.py`，输出：

```
wrote SCI-INT-C01.yaml: cards=43 metrics=32
OK cards=43 gap=0 by_counterpart={'gkx_mysql_raw': 24, 'none': 4, 'jiuxin': 13, 'trsgraph': 2}
OK TALENT metrics scope=32 covered=26 no_source=6 ['M_TALENT_DS_16_TALENT_RECRUIT_005', 'M_TALENT_DS_16_TALENT_RECRUIT_006', 'M_TALENT_DS_16_TALENT_RECRUIT_007', 'M_TALENT_DS_16_TALENT_RECRUIT_010', 'M_TALENT_DS_16_TALENT_RECRUIT_013', 'M_TALENT_DS_16_TALENT_RECRUIT_025'] diff=0
OK jiuxin 人才行=15 全部挂卡 diff=0 · structure_escalation=7 · open_items=15
```

`C01-check.py` 断言的内容：
- P00 基线中 TALENT 指标为 32 条，与 `metric_coverage` 双向差集为 0；
- int_id 唯一，且都落在 001–099；
- `scope_count == card_count == len(cards)`，`gap` 为空；四个顶层块都存在；
- 每张卡 `data_source` 的必填字段非空，行数带来源；
- 覆盖表引用的源卡都存在，卡上 `metric_ids` 与覆盖表双向一致；`covered + no_source == 32`；
- 久新人才 15 行与卡上 `jiuxin_row_id` 完全一致；久新卡都带「待确认」，且不出现「已确认」。

结果汇总：
- 源卡数：43（scope_count = card_count = 43，gap = 0）
- 指标覆盖：32/32，差集 0，no_source 6
- structure_escalation：7 张，升级 human:李伟。分别是 041 久新 Python-110 产出、042 久新 Python-111 产出、060 人才顶点、061 人才边、070 人才主档、071 人才流动边、072 人员 ID 映射表
- decision_needed：卡上共 11 条，另有 open_items 中的口径项

**最大的 3 个开放项**：

1. OI-C01-01 / 02：人才主数据由谁持有、scholar_id 是否稳定、全量覆盖多大。供应方 TALENT-P0-1 自 2026-09-04 起未回复；08-31 时各表只有 2 万行样例。
2. OI-C01-03：久新人才 15 行的交付形态和数据底座（用我方入站的 dwd_scholar，还是其自有人才库）。25 条指标依赖这一项。
3. OI-C01-06 / 07：DS-16 六条无源；人才供需的需求侧（岗位 / 招聘）三方库没有数据。是否保留、降级或由甲方提供数据，需要甲方拍板。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 久新 Python-110/111 与人名消歧建议并入 `lumen-algo-py` 离线 Job；Java 只读 ADS |
| 2 调用链 前端→Java→Python `/internal/*` | ✅ 卡上 `call_chain` 均按此填写，久新经 `/internal/jiuxin/talent/*`（草案），不直连前端 |
| 3 图谱只用 NebulaGraph TRSGraph | ✅ 060/061 指向 TRSGraph（10.50.75.136:9669），无 Neo4j |
| 4 可观测 | N/A（分析叶，无运行代码） |
| 5 CI/CD | N/A（只改编排文档） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 / Java 不写 nGQL、只读 ADS | ✅ |
| 8 ADS 先行、Mock 填充、三方到位再映射 | ✅ 32 条 D4 均为 mock，卡上如实标注 |
| 9 D8 前端规范 | N/A |
| 10 D9 血缘 | ✅ 8 件套与 D1–D4 只经 MCP `metric-registry` 读取；未读、未改 seed 与矩阵 |
| 11 D10 交互规范 | N/A |
| 12 D12 demo/lumen 隔离 | ✅ lumen 链路下游只写 `gkxlumen-*` / `lumen-algo-py` / `lumen-etl-es-py`；demo-* 只作「现状」描述 |
| 人机：不替甲方拍板 | ✅ 口径歧义写 `decision_needed`；久新行全部「待确认」；查不到写 `unknown` |
| 只读 | ✅ 未连库、未写库、未改业务仓、未读 `task-registry.yaml` 与 `metrics/registry/` |
| 隐私 | ⚠️ 人才是自然人（email / 履历 / 头像），字段分级与脱敏列为 OI-C01-08 |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ≈420,000（估算） |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ≈$7（估算） |
| cost_warn | yellow（>$5，<$10） |
