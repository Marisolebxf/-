# SCI-INT-C02 handoff：技术链（TECH）要素三方源入站盘点

| 项 | 值 |
|---|---|
| task_id | SCI-INT-C02（spike · 长任务 SCI-INT 段 C） |
| 执行 | agent:data-agent |
| 监管 | human:淮政玮 · claim_type=coordinator_dispatch |
| 日期 | 2026-10-18 |
| 强度 | ponytail: N/A（分析叶，不写业务代码） |
| 产物 | `产物/SCI-INT-C02.yaml`（主产物）· `产物/_work/C02-build.py`（生成器）· `产物/_work/C02-check.py`（自检） |

## 1. 范围与实现

**范围**：展示系统技术链要素（技术点 / 论文 / 专利 / 项目 / 报告 / 技术关系 / 投融资）的三方源入站盘点。依据 `SCI-INT-总派单.md` §2 卡片 schema（layer=data）和 §C02 说明，指标范围以 `P00-baseline.yaml` 中 domain=TECH 的 39 条为准（经 MCP `metric-registry` 复核 8 件套与 D1–D4，未读 registry 文件）。bid-reference 对照沿用 P00 基线里的 SRS 映射（技术链对应展示系统 DS-01/02/03/07/09 及专题 TOPIC-TECH）。

**实现**：每张源表或源实体一张卡，int_id `INT-C-TECH-100`～`182`，共 **56 张**：

| 段 | int_id | 张数 | 内容 |
|---|---|---|---|
| 甲方三方库 gkx（`dwd_*`） | 100–139 | 40 | 专利主表+6 附表、中英文论文及附表、学者论文/研究方向、中英文项目及成果、项目↔专利/论文关系、中英文报告、机构基础/专利关系/技术标签/融资/投资、产业基金投资、量子技术趋势/研发进展、产业链环节码、机构要闻、产业分析、产业链专利明细 |
| 北京久新（全部待确认） | 150–160 | 11 | SQL-96、Python-104/105、API-130～140，挂满技术链 25 行 |
| TRSGraph | 170–171 | 2 | `TAG technology`、技术相关边 |
| 新结构（我方需建） | 180–182 | 3 | 技术点主表、技术领域维表、技术点↔文献/机构/人才桥接表 |

每张卡含 §2 全字段，另加扩展块 `data_source`：源系统、表、关键字段、主键、实体对齐键（技术点归一与领域分类）、覆盖范围（全球/中国/深圳）、更新频率、行数（值 + 快照日期 + 来源文件）、页面。顶层四块：`master_data_conclusion`、`id_alignment_draft`、`metric_coverage`、`open_items`（16 项）。

**技术点主数据结论**：当前没有任何一方持有技术点实体主数据。gkx 无技术点表、无稳定码（技术信号只散落在专利 IPC/CPC + keywords、论文 scope/keywords、项目 discipline_code 等文献属性里）；TRSGraph `technology` 顶点的 VID 是 `tech:{名称}`；久新 Python-104 的产出未确认；jx-tech-topic 两仓是 2026-10-15 的空模板；lumen 各仓都没有 technology_id。草案建议我方自建「技术点主表 + 技术领域维表 + 桥接表」（180/181/182），底稿由久新 Python-104（并入 `lumen-algo-py` 离线 Job）在我方入站文献上抽取，久新 API 一律用我方 technology_id / domain_code 交互。该建议是 `decision_needed` + `structure_escalation`，不是定论。

**指标覆盖**：39/39 全部列出源卡，差集 0。绑定强度分布：`kit_declared` 3（MODEL×3，kit 点名 dwd_patent 系列 + dwd_org_base_info）、`candidate` 8（我方推断的候选源，未经 kit 确认）、`jiuxin_pending` 27（依赖久新交付）、`no_source` 1（`M_TECH_COMPOSITE_SCORE`：生产方与分项都没定）。

## 2. 偏离说明

1. 卡片在 §2 schema 外增加 `data_source` 扩展块，用来承载本叶要求的源表字段，§2 原字段一个不少。
2. 总派单写 spike 完工进 `integration`；本次按 coordinator 派单指令推进到 `ready_to_sign`（spike 的 AV-0 目标）。
3. `integration_pattern` 统一填 `TBD`（B01 尚未产出）。
4. 行数全部引自仓内快照：2026-10-10 估数报告（`TABLE_ROWS`，未过滤 is_deleted，两次快照波动明显，如 dwd_patent 2,892,155→2,690,167）。快照里查不到的表写 `unknown` 并列入 OI-C02-07。**本叶没有连库**。
5. `dwd_scholar_papers` 与人才（C01）共用，`dwd_org_base_info` 与科研机构（C03）共用，卡上标了 `shared_with`，没有写 C01/C03 的文件。

建议的只读核对 SQL（**未执行**，留给下一步有连库权限时用；库 `gkx`，账号 `gkx_reader_zp`）：

```sql
SELECT COUNT(*) FROM gkx.dwd_en_paper_cited_by WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_rel_project_patent WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_rel_project_paper WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_org_base_info_patent_rel WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_quantum_tech_trend WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_quantum_rd_progress WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkx.dwd_org_industry_chain_pat_dtl WHERE is_deleted = 0;
```

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-C02.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/C02-build.py`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/C02-check.py`
- 本 handoff

未 git commit / push（按派单要求）。

## 4. 验收证据

运行 `python 产物/_work/C02-build.py; python 产物/_work/C02-check.py`（2026-10-18），输出：

```
wrote SCI-INT-C02.yaml: cards=56 metrics=39
OK cards=56 gap=0 by_counterpart={'gkx_mysql_raw': 40, 'jiuxin': 11, 'trsgraph': 2, 'none': 3}
OK TECH metrics scope=39 covered=38 no_source=1 ['M_TECH_COMPOSITE_SCORE'] diff=0
OK jiuxin 技术链行=25 全部挂卡 diff=0 · structure_escalation=7 · open_items=16
```

`C02-check.py` 断言内容：P00 基线 TECH 指标 = 39 且与 `metric_coverage` 双向差集为 0；int_id 唯一且落在 100–199；`scope_count == card_count == len(cards)`、`gap` 为空；每张卡的 `data_source` 必填字段非空且行数带来源；覆盖表引用的源卡都存在，卡上 `metric_ids` 与覆盖表双向一致；久新技术链 25 行与卡上 `jiuxin_row_id` 完全相等；久新卡都带「待确认」。

- 源卡数：56（scope_count=card_count=56，gap=0）
- 指标覆盖：39/39，差集 0，no_source 1
- structure_escalation：7 张（151 久新 Python-104 产出、152 久新 Python-105 产出、170 TAG technology、171 技术边、180 技术点主表、181 技术领域维表、182 桥接表）→ 升级 human:李伟
- decision_needed：11 条（分散在各卡）

**最大的 3 个开放项**：

1. OI-C02-01 / 02：技术点主数据由谁持有、全局 technology_id 和技术领域分类体系怎么定（供应方 TECH-P0-1/P0-2 自 2026-09-04 未回）。
2. OI-C02-03：久新技术链 25 行的交付形态和数据底座（用我方 gkx 入站数据还是其自有数据），27 条指标挂在这上面。
3. OI-C02-05 / 06：专利附表只有约 1.6–2.1 万行（主表约 269 万），英文论文只有 1,356 行，全球口径是否能撑住要等供应方答复。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 久新 Python-104/105 建议并入 `lumen-algo-py`；Java 侧只读 ADS |
| 2 调用链 前端→Java→Python `/internal/*` | ✅ 卡上 `call_chain` 均按此填写，久新 API 经 Java 网关转出，不直连前端 |
| 3 图谱只用 NebulaGraph TRSGraph | ✅ 170/171 指向 TRSGraph，无 Neo4j |
| 4 可观测 | N/A（分析叶，无运行代码） |
| 5 CI/CD | N/A（`cicd: skip`，只改编排文档） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 / Java 不写 nGQL、只读 ADS | ✅ |
| 8 ADS 先行、Mock 填充、三方到位再映射 | ✅ 39 条指标 D4 现状均为 mock，卡上如实标注 |
| 9 D8 前端规范 | N/A |
| 10 D9 血缘 | ✅ 指标 8 件套与 D1–D4 只经 MCP `metric-registry` 读取；未读 / 未改 seed 与矩阵 |
| 11 D10 交互规范 | N/A |
| 12 D12 demo/lumen 隔离 | ✅ 所有 lumen 链路下游只写 `gkxlumen-*` / `lumen-algo-py` / `lumen-etl-es-py`，未出现 `demo-*` |
| 人机：不替甲方拍板 | ✅ 口径歧义都写 `decision_needed`；久新行全部「待确认」；查不到写 `unknown` |
| 只读 | ✅ 未连库、未写库、未改业务仓、未读 `task-registry.yaml` 与 `metrics/registry/` |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ≈380,000（估算） |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ≈$6.5（估算） |
| cost_warn | yellow（>$5，<$10） |
