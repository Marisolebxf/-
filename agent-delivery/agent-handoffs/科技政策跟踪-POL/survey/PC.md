# 科技政策跟踪 · 核增四页存量调研（PC）

> 任务：`POL-DISPLAY-SURVEY-PC-L01`  
> 日期：2026-11-03  
> 监管：`human:淮政玮`  
> 执行：`agent:arch-agent`  
> 用户故事：`US-DS-POL-07`～`US-DS-POL-10`  
> 前端对照：`FE-POL-04A`、`FE-POL-05A`、`FE-POL-06A`、`FE-POL-07A`  
> SRS：`bid-reference/srs/02-科技信息展示系统/政策对比功能升级（核增需求）/`（序号 602–618，17 叶）  
> 查询：task-registry MCP、metric-registry MCP（政策域 35 条）。未读 seed / 矩阵 / `task-registry.yaml`。

四页合在本文件。GDF、专题入图、算法中台条款跑批只索引已有任务号，不写成展示系统新任务。`E-E7-POLICY-M1-L06`（backlog）不作为本叶实现路径。门户扶持十条不进入本四页。

判定只使用三档：

| 档 | 用法 |
|---|---|
| 可接统计读面 | `algorithm_type` 为 STAT 或 COMPUTE，且本叶可以挂该 `metric_id`。D4=mock 仍写 mock |
| 501 | MODEL，或本叶的解析 / 对比推演 / 研报 Job 未注册。契约冻结前，真路径不得用 fixture 填数 |
| 跨项索引 | 专题 E7、GDF、第 7 项读图、算法中台已有作业。只记任务号 |

政策域 35 条里，按中文名与关键词（清洗、拆解、研报、对比、溯源、核增、PC）没有核增专名。对演示页已挂载、以及名称接近的指标做了 `metric-get`：其 `srs_refs` 落在科创政策全景、政策分析评价、政策效果推演或专题 E7，序号均不在 602–618。下表「未见」指本叶没有可挂的指标或任务。

共享且未计入四页三档的任务：`FE-POL-S01` pending_test（七页基座）；`BE-POL-CONTRACT-01`、`BE-POL-IMPL-01`、`BE-POL-DATA-01`、`FE-POL-REAL-01` 均为 backlog。本叶不写接口字段表。

## PC-1 政策数据治理

菜单名「智能政策库构建」。对照 `FE-POL-04A`（in_progress）。用户故事 `US-DS-POL-07`：展示侧看清洗质量、结构化库、溯源索引与规划指标库的入口状态；后台流水线不在本故事里实现。SRS 序号 602–605。

| 能力或 SRS 序号 | 用户故事 | 已有任务号与状态 | metric_id | algorithm_type | D4 | 判定 | 依据 |
|---|---|---|---|---|---|---|---|
| 602 系统引用政策源数据清洗 | US-DS-POL-07 | FE-POL-04A in_progress；GDF-POLICY-WORKPACK-V1-L01 integration；GDF-POLICY-WORKPACK-V2-L01 done | 未见 | 未见 | 未见 | 跨项索引 | 贴源与 Mapping 在政策 GDF v1，v2 继承 Wave A/B。展示页只做看板。清洗质量（去重、格式、噪声）无 STAT/COMPUTE。演示页把 `M_POLICY_VALIDITY_RATE` 挂在本 KPI 上，该指标口径是有效率，`srs_refs` 为空，`ui_mount` 在分析页与筛选，本叶不挂 |
| 603 政策库结构化 | US-DS-POL-07 | FE-POL-04A in_progress；GDF-POLICY-WORKPACK-V2-L01 done；POLICY-DDL-GAP-L10 done | 未见 | 未见 | 未见 | 跨项索引 | v2 DoD 中 POLICY-C2 把条款结构并入 ADS `policy_text_parse`；L10 只建空的 DWD `policy_text_parse`。结构化覆盖率无注册指标 |
| 604 溯源索引构建 | US-DS-POL-07 | FE-POL-04A in_progress；原文—条款—结论索引任务未见 | 未见 | 未见 | 未见 | 501 | 本叶要的是原文、条款、分析结论关联索引。`GDF-POLICY-LINEAGE-L01` backlog 的 DoD 是工位导入后的数据血缘说明，且写明本叶不实现接口、不把血缘写成已可查询，对不上本序号，故不标跨项索引。索引构建未注册 |
| 605 规划指标库搭建 | US-DS-POL-07 | FE-POL-04A in_progress；规划指标库任务未见 | 未见 | 未见 | 未见 | 501 | SRS 要扶持力度、适用范围、实施时效、申请条件的统一口径库。`M_POLICY_BASE_100_1`（STAT，D4=mock）的 `page_ids` 只有 E7，口径是发布量/分布。`DATA-POLICY-D13-DS-MENU-L01` pending_test 覆盖 DS-07/11 注册库。两处都不覆盖本叶。库搭建未注册 |

页眉附卡（不计入上表三档）：演示页「库内政策数」挂 `M_POLICY_TOTAL_COUNT`（STAT，D4=mock）。`srs_refs` 在全景序号 215 与专题基础指标序号 100。它可以作为治理页附卡的统计读面，数值仍是 mock，不替代 602。

本页三档：可接统计读面 0；501 2；跨项索引 2。

## PC-2 智能政策拆解

对照 `FE-POL-05A`（integration）。用户故事 `US-DS-POL-08`。SRS 序号 606–609。

| 能力或 SRS 序号 | 用户故事 | 已有任务号与状态 | metric_id | algorithm_type | D4 | 判定 | 依据 |
|---|---|---|---|---|---|---|---|
| 606 政策语义理解 | US-DS-POL-08 | FE-POL-05A integration；语义理解 Job 未见 | 未见 | 未见 | 未见 | 501 | SRS 要求大模型做语义解析、意图识别与条款分类，并覆盖地方/国家/海外文本。`M_POLICY_TEXT_PARSE` 为 MODEL、D4=mock，`srs_refs` 为空，`ui_mount` 在详情标签与检索筛选项，口径是闭集词表，本叶不挂。产业槽 Job A（`CROSS-VEC-JOB-A-L01` pending_test）对不上本序号 |
| 607 条款精细化拆解 | US-DS-POL-08 | FE-POL-05A integration；POL-CLAUSE-BATCH-L01 integration；GDF-POLICY-WORKPACK-V2-L01 done | 未见 | 未见 | 未见 | 跨项索引 | `POL-CLAUSE-BATCH-L01` 的 design_refs 点名本文件序号 607–608：联调台规则切条，limit 100，写入 `ads.policy_text_parse.structured_elements.clauses`。v2 的 POLICY-C2 只合并同一 JSON，不写 ES、不回写 DWD。展示页只呈现条款树 |
| 608 关键指标自动提取 | US-DS-POL-08 | FE-POL-05A integration；POL-CLAUSE-BATCH-L01 integration；量化指标数据集任务未见 | 未见 | 未见 | 未见 | 跨项索引 | 同一条款跑批 DoD 含补贴标准、准入条件、扶持措施归类，design_refs 含序号 608。量化指标、时间节点的独立 `metric_id` 未见。演示页「力度指数」挂 `M_POLICY_INTENSITY_INDEX`（MODEL，D4=mock），`page_ids` 只有 E7，本叶不挂 |
| 609 政策实体关联 | US-DS-POL-08 | FE-POL-05A integration；E-E7-POLICY-M1-L02 done；GDF-POLICY-GRAPH-EXT-L01 backlog | M_POLICY_GRAPH_106_1；M_POLICY_GRAPH_107_1 | GRAPH | mock | 跨项索引 | 两指标 D4 均为 mock。106 的展示引用在推演序号 237；107 的展示引用在全景 208、推演 239/240、孵化载体 549，以及专题图谱叶。本叶只索引读图，不新挂统计。GDF 脚本任务 note 写明读图归第 7 项，且脚本未进包前不建作业。按「读图」检索，独立读图任务号未见。演示页「关联度」挂 `M_POLICY_RELATION_DEGREE`（GRAPH，D4=mock，`srs_refs` 空），本叶不挂 |

本页三档：可接统计读面 0；501 1；跨项索引 3。

## PC-3 多维政策对比

对照 `FE-POL-06A`（integration）。用户故事 `US-DS-POL-09`。SRS 序号 610–613。对比对象只留展示侧会话槽。专题对比篮不在本页任务里新建。

| 能力或 SRS 序号 | 用户故事 | 已有任务号与状态 | metric_id | algorithm_type | D4 | 判定 | 依据 |
|---|---|---|---|---|---|---|---|
| 610 跨政策交叉对比 | US-DS-POL-09 | FE-POL-06A integration；差异/冲突识别任务未见 | 未见 | 未见 | 未见 | 501 | SRS 要在条款、核心指标、扶持力度、适用范围、实施路径上识别共性、差异、互补与冲突。政策域没有序号 610 的指标。演示维度挂载均不采用：`M_POLICY_INTENSITY_SCORE`（MODEL，D4=mock）的 `page_ids` 是全景；`M_POLICY_SUPPORT_STRENGTH`（COMPUTE，D4=mock）的算法叶 brief 写明禁止核增 PC-03；`M_POLICY_INDUSTRY_FIT`（MODEL，D4=mock）`srs_refs` 为空，`ui_mount` 在城市榜与招商列 |
| 611 可视化分析呈现 | US-DS-POL-09 | FE-POL-06A integration；本叶可视化指标未见 | 未见 | 未见 | 未见 | 501 | 表格、柱状、雷达、对比图谱都吃 610 的未注册结果。106/107 的读图页不是本页，不把对比图谱写成第 7 项读图 |
| 612 交互式对比配置 | US-DS-POL-09 | FE-POL-06A integration；BE-POL-CONTRACT-01 backlog | 未见 | 未见 | 未见 | 501 | 维度、筛选与权重会驱动未注册的差异评分。会话槽仍是页面演示态。契约任务尚未定义服务端槽，没有 STAT/COMPUTE 可读 |
| 613 结果智能输出 | US-DS-POL-09 | FE-POL-06A integration；对比摘要 Job 未见 | 未见 | 未见 | 未见 | 501 | 自动摘要与核心结论未注册。`M_POLICY_DS_11_POLICY_EVAL_012`（MODEL，D4=mock）只对应分析评价序号 226。本页导出走前端汇总文档，没有已注册的对比摘要 Job |

本页三档：可接统计读面 0；501 4；跨项索引 0。

## PC-4 智能研报生成

对照 `FE-POL-07A`（ready_to_sign）。用户故事 `US-DS-POL-10`。SRS 序号 614–618。按「研报」「撰写」检索，研报 Job 未注册，五叶均判 501。`FE-POL-07A` 只覆盖页面复刻。

| 能力或 SRS 序号 | 用户故事 | 已有任务号与状态 | metric_id | algorithm_type | D4 | 判定 | 依据 |
|---|---|---|---|---|---|---|---|
| 614 政策深度分析 | US-DS-POL-10 | FE-POL-07A ready_to_sign；深度分析 Job 未见 | 未见 | 未见 | 未见 | 501 | SRS 要求在对比结果上做实施效果、经济社会效益、产业影响与趋势，并结合行业数据与模型。`M_POLICY_EFFECT_SCORE`（MODEL，D4=mock）的 `page_ids` 是分析评价与效果推演。`M_POLICY_SIMULATE`（MODEL，D4=mock）`srs_refs` 为空，`ui_mount` 在推演情景面板。研报 Job 未注册 |
| 615 洞察结论自动提炼 | US-DS-POL-10 | FE-POL-07A ready_to_sign；洞察提炼 Job 未见 | 未见 | 未见 | 未见 | 501 | 核心观点、决策建议、风险提示、发展机遇未注册。演示页「建议条数」挂 `M_POLICY_LAYOUT_REC_COUNT`（STAT，D4=mock），其 `page_ids` 是分析评价、效果推演与 E7，口径是布局推荐对冲计数，与本叶分键，本叶不挂 |
| 616 模块化研报自动撰写 | US-DS-POL-10 | FE-POL-07A ready_to_sign；研报 Job 未见 | 未见 | 未见 | 未见 | 501 | 模板整合、结构化撰写与排版没有已注册 Job。页面只有大纲与模板就绪开关 |
| 617 研报溯源展示 | US-DS-POL-10 | FE-POL-07A ready_to_sign；结论↔原文双向索引任务未见 | 未见 | 未见 | 未见 | 501 | 双向溯源的对象是未注册研报结论。604 的原文—条款—结论索引也未注册。`GDF-POLICY-LINEAGE-L01` 对不上本序号 |
| 618 结果智能输出 | US-DS-POL-10 | FE-POL-07A ready_to_sign；PDF/Word 导出 Job 未见 | 未见 | 未见 | 未见 | 501 | SRS 要求 PDF、Word 导出。已有实现是前端可打印 HTML / .doc。服务端导出 Job 未注册。导出落点留在 `BE-POL-CONTRACT-01` backlog，本叶不写字段 |

本页三档：可接统计读面 0；501 5；跨项索引 0。

## 跨项任务索引

下列任务保持原编号与原状态，不展开为展示页新任务。

| 任务号 | 状态 | 本叶用法 |
|---|---|---|
| GDF-POLICY-WORKPACK-V1-L01 | integration | 602 贴源 + Mapping |
| GDF-POLICY-WORKPACK-V2-L01 | done | 603、607 的条款结构化加工；Wave A/B 继承 v1 |
| POLICY-DDL-GAP-L10 | done | 空表 `policy_text_parse`，不表示已有结构化读面 |
| POL-CLAUSE-BATCH-L01 | integration | 607、608；算法中台联调台，limit 100 |
| E-E7-POLICY-M1-L02 | done | 609 子图灌入；空间 `gkx_policy` |
| GDF-POLICY-GRAPH-EXT-L01 | backlog | 609 的 106/107 脚本；读图归第 7 项，独立读图任务号未见 |
| GDF-POLICY-LINEAGE-L01 | backlog | 与 604、617 的结论溯源不是同一件事，表内不据此改判 |

## 主要未见

- 核增 17 叶在政策域 35 条指标中没有序号 602–618 的 `srs_refs`。
- 清洗质量、结构化覆盖率、规划指标库、语义理解 Job、量化指标数据集、跨政策差异/冲突模型、对比摘要 Job。
- 研报五叶的 Job：深度分析、洞察提炼、模块化撰写、结论双向索引、PDF/Word 服务端导出。
- 原文—条款—结论溯源索引（604、617）。
- 第 7 项读图的独立任务号（609 只索引到 L02 与 `GDF-POLICY-GRAPH-EXT-L01`）。
- `FE-POL-04A`、`FE-POL-05A`、`FE-POL-07A` 的 handoff 文件在 `科技政策跟踪-POL/` 下未见；状态以 task-registry 为准。`FE-POL-06A.md` 已在同目录。
