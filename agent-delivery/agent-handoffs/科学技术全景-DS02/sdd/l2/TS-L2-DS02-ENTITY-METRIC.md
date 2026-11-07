# TS-L2-DS02-ENTITY-METRIC · 科学技术全景 · 展示技术点关联实体 · 指标挂接

- 任务：`TS-L2-DS02-ENTITY-METRIC`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`（兼 algorithm 分册）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 强度：ponytail off（定义任务，不缩文档）
- 上游：`sdd/科学技术全景-系统详细设计说明书.md` §2.2、§4、§5；`sdd/l2/TS-L2-DS02-ARCH.md` §5、§7
- 查询：2026-11-07 经 MCP `user-metric-registry` 的 `metric-get` 逐条查询四个 ID。未读 seed、矩阵 YAML，未改注册表

本叶只写序号 22–27 的指标挂接。不新造 `metric_id`，不改 D1–D4，不写公式实现。身份仍归 `DS-02-METRIC-OPEN-L01`。

## 1. 挂接结论

| metric_id | 本二级 | 挂在 |
|---|---|---|
| `M_TECH_ENTITY_INFLUENCE` | 挂。只作影响力列的身份 | 序号 27「按影响力」、实体行「影响力」数 |
| `M_TECH_ENTITY_TOP5` | 不挂 | 22 的 Top5 是选中点的图上邻居，不调用该指标 |
| `M_TECH_PAPER_PATENT_CNT` | 不挂 | 24 的条数是邻居个数，不是该指标 |
| `M_TECH_ENTITY_REL` | 不挂 | 26 为 501 / 空 |

22、23、25 没有统计数，无 `metric_id`。关联强度是图上边属性，不是指标。

## 2. 八件套（metric-get `kit`）

八件套只含身份。D1–D4、`lifecycle_stage`、`srs_refs` 不放本节。四条源系统相同：`gkx @ 183.240.141.251:3318（只读）`。`version` 都是 `1`。`update_freq` 都是 `pending`。公式都是过程指针：见 calc-logic 与 20261021 正本 §二，实现以 `code/<metric_id>.py` 为准。本叶不手抄。

| metric_id | 中文名 | algorithm_type | 源表 |
|---|---|---|---|
| `M_TECH_ENTITY_INFLUENCE` | 技术点影响力 / 实体优先级 | third_party | `dwd_patent`、`dwd_patent_applicants`、`dwd_patent_cited` |
| `M_TECH_ENTITY_TOP5` | 根节点 Top5 关键实体与关联强度 | third_party | `dwd_id`、`dwd_patent`、`dwd_zh_paper` |
| `M_TECH_PAPER_PATENT_CNT` | 技术点论文量 / 专利量 | STAT | `dwd_id`、`dwd_org_tech_tag`、`dwd_patent`、`dwd_patent_family`、`dwd_patent_title`、`dwd_zh_paper`、`dwd_zh_paper_classification` |
| `M_TECH_ENTITY_REL` | 实体关联关系网 | third_party | `dwd_patent_applicants`、`dwd_patent_cited`、`dwd_patent_transfer`、`dwd_zh_paper` |

口径摘要（按 `kit.definition`，不改写）：

| metric_id | 口径要点 | 与本页的差别 |
|---|---|---|
| `M_TECH_ENTITY_INFLUENCE` | IPC4 共类网络 PageRank，叠加规模对数与增速得技术点影响力；实体优先级 = 实体在各技术点上的 PR 加权计数 | 点是 IPC4，不是 `technology_node_id`。本页只借身份 |
| `M_TECH_ENTITY_TOP5` | 机构 / 企业按 IPC4×申请人可算；论文靠标题关键词桥；人才整类不可算 | 本页 Top5 是图上邻居 |
| `M_TECH_PAPER_PATENT_CNT` | 技术点粒度不成立，只能交付机构级双计数 | 本页条数是邻居个数 |
| `M_TECH_ENTITY_REL` | 专利转移、共同申请、论文合著三源成网；缺引用、许可、诉讼边 | 本页图上没有实体间边 |

## 3. 接入状态（metric-get `readiness`）

| metric_id | D1 | D2 | D3 | D4 | is_mock |
|---|---|---|---|---|---|
| `M_TECH_ENTITY_INFLUENCE` | aligned | partial，provisional（待核验） | full | mock | true |
| `M_TECH_ENTITY_TOP5` | aligned | partial，provisional（待核验） | partial | mock | true |
| `M_TECH_PAPER_PATENT_CNT` | aligned | partial，provisional（待核验） | partial | mock | true |
| `M_TECH_ENTITY_REL` | aligned | partial，provisional（待核验） | partial | mock | true |

四条 `d4_note` 都是「算法服务未上线，保持 mock」。`srs_refs` 都为空。`M_TECH_ENTITY_INFLUENCE` 的 `extras.ui_mount` 写的是「科技信息展示系统 · 技术评估 · 技术关系网络『核心节点』+ 创新主体评估（实体排序）」，不是本页 `/trend/tech-panorama`。本页只借列身份，不改注册表；是否补挂由 data-agent 按 `metrics/README.md` 决定。`acceptance_unit_id`：INFLUENCE、TOP5、REL 为 `DS-02-ENTITY`；PAPER_PATENT_CNT 为 `TOPIC-TECH-05`。

本叶不改任何一维。D4 保持 mock。

## 4. 影响力列怎么落

| 项 | 值 |
|---|---|
| 身份 | `M_TECH_ENTITY_INFLUENCE` |
| 数从哪来 | `demo_gkxlumenx_ads.ads_technology_panorama_score`，`score_kind=influence`，按 `subject_id` 只读 |
| 数的性质 | D18 mock 行，由 `TS-L2-DS02-SCORE-L01` 灌入。不是注册公式输出 |
| 请求内 | 不算。Java 只 SELECT，Python 不算 |
| 无行 | 该格空；按影响力排序时该实体不进这一档 |
| D4 | mock。公式未由 `human:唐绍祖` 按技术点另签前，不得改 live |

界面（`GraphAnalysisPanel.vue`，live 下）：

- 「关键关联对象 Top5」标题旁：「影响力」+ `MetricSpecHint`（`metric-id="M_TECH_ENTITY_INFLUENCE"`）+ `MockBadge`。
- 排序下拉 live 下多一项「影响力」。
- 每行显示「影响力 {值}」，无值则空。
- `MockBadge` 来自 `@/review`，随评审层门控。

## 5. 不挂的三条在页面上怎么处理

| metric_id | 页面 |
|---|---|
| `M_TECH_ENTITY_TOP5` | 不出现。Top5 标题旁只挂影响力的 ⓘ |
| `M_TECH_PAPER_PATENT_CNT` | 不出现。条数旁不挂 ⓘ |
| `M_TECH_ENTITY_REL` | 不出现。「实体关联关系展示」live 下为空，文案「实体间关系暂无数据」 |

## 6. 现状数（2026-11-05 灌数，2026-11-07 未复查）

| 项 | 行数 |
|---|---|
| `influence` 合计 | 252,363 |
| 论文 | 108,337 |
| 专利 | 126,484 |
| 机构 | 17,542 |
| 人 | 0（`tech_person` 点为 0） |

图上还没有技术点连实体的边，选中点时实体名单为空，影响力格子也就没有对象可填。

## 7. 不做

- 不新注册指标，不改 D1–D4，不把 mock 写成已上线。
- 不把分数表行说成 PageRank 或任何注册函数的结果。
- 不把 `TEMP_DS02_*` 当正式 ID。不把 `M_CHAIN_*`、`M_SVC_GRAPH_*`、`M_SVC_REC_*` 改挂到本页。
- 不改唐绍祖锁定的合规算法，不改 demo 仓计算文件。
