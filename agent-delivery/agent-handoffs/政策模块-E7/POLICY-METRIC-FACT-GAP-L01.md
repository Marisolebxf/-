# POLICY-METRIC-FACT-GAP-L01 · 政策指标事实表缺口分析（展示系统与专题系统）

> 定义叶。只判定事实落点。不建表、不灌数、不加工指标、不改口径种子、不改就绪度、不改客户决策清单。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-27 `/goal` 指定。开工前 `backlog → ready`，再认领。锁 4 小时。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |
| 说明 | 本单只出缺口清单。未用 YAGNI 砍掉展示/专题两侧，也未把口径未闭合并进缺表。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。未改存储流图 |
| 图 diff | 无 |
| 会签态 | 不适用 |
| 说明 | 不新增写库边，不把结果说成可对端 |

## 范围与实现

对照展示系统需规 `srs/02`（科技政策跟踪、政策对比升级）与专题系统需规 `srs/04`（政策分析、数据需求里的政策模型），把政策域已登记的 35 条指标逐条标成事实落点。实现就是下面三张清单，没有加工、没有建表。

## 偏离说明

无范围偏离。未把扶持事实写成已建表。未用 `TOPIC-DS-METRIC-GAP-L01` 的库外差集代替本单。QPOL-02 保持待甲方，不升绿。

## 产物清单

- 本 handoff：`agent-delivery/agent-handoffs/政策模块-E7/POLICY-METRIC-FACT-GAP-L01.md`
- 无代码 PR、无脚本、无建表语句、无灌数批次

## 验收证据

- `metric-query` 政策域 `matched=35`，与 `metrics/calc-logic/POLICY/README.md` 条数一致
- `task-get`：`GDF-POLICY-MT-SUPPORT-L01` 仍为 `backlog`；`TOPIC-DS-METRIC-GAP-L01` 与 `DATA-POLICY-STORAGE-S3-GAP-L01` 为 `done`，未拿来代替本单
- 编排仓无业务 CI。本叶 `cicd: skip`

## 判定规则

一条指标只进下面三格之一。格的含义对齐 2026-10-26《要素指标加工与图谱拆解思路》第一节第 3 条，并收成事实落点：

| 落点 | 含义 |
|------|------|
| 已有表 | 公式要读的事实已经有落点。政策主事实是 DWD `policy_base_info`（供应方镜像为 `dwd_policy_base` / `dwd_global_policy_base`）。结果壳以派单包 `14` 已点名的 ADS 表为准 |
| 缺表 | 公式要的事实没有落点。只写事实是什么 |
| 缺的是口径而不是表 | 表或列已经在，未签的是业务规则（客户决策清单仍为待甲方）。不建表 |

已有表只说明落点被点过名。不表示行已灌、作业已跑、可以对端。

登记范围：`metric-query` 政策域 `matched=35`，与 `metrics/calc-logic/POLICY/README.md` 35 条一致。35 条都列入。来源系统取登记 `srs_refs.systems`；该字段为空时，用展示需规（`srs/02`）或专题需规（`srs/04`）里点名的功能补「用到方」，并在备注写「登记未回填」。

不纳入：

- `TOPIC-DS-METRIC-GAP-L01`（已完成）是库外指标差集，不用它的差集代替本单。
- 门户十条（`ALGO-LIB-POL-PORTAL-GAP`）未注册，不是展示需规分册、也不是专题需规分册上的指标号。
- `DATA-POLICY-STORAGE-S3-GAP-L01`（已完成）只补过存储文档，不在本单重开。

## 计数

| 落点 | 条数 |
|------|------|
| 已有表 | 10 |
| 缺表 | 1 |
| 缺的是口径而不是表 | 24 |
| 合计 | 35 |

## 1. 已有表（10）

事实都在政策主表上，或关系落点已在派单包点名。人口范围沿用 QPOL-05 的临时默认（只计国内）。这是范围限定，不是缺表。

| 指标 | 用到方 | 事实落点 | 备注 |
|------|--------|----------|------|
| `M_POLICY_TOTAL_COUNT` | 展示 + 专题 | `policy_base_info` 行数；结果写入 `policy_level_dist`（`level` 空行） | 展示需规序号 215；专题算法库基础指标页 E7-POLICY |
| `M_POLICY_LEVEL_DIST` | 展示 + 专题 | 同上主表的 `rank`；结果写入 `policy_level_dist` | 登记来源为展示。专题侧由基础指标五类里的「级别」使用 |
| `M_POLICY_NATIONAL_DIST` | 展示 + 专题 | 同上主表的省；结果写入 `policy_national_dist` | 登记来源为展示。专题「全国政策分布」挂在同一基础指标 |
| `M_POLICY_SZ_DIST` | 展示 + 专题 | 同上主表的市；结果写入 `policy_sz_dist`，只写全市合计一行 | 各区列在主表上，值几乎是字面空。这是缺样本，不是缺表。各区行不写 |
| `M_POLICY_TIMESERIES` | 展示 + 专题 | 同上主表的发布年；结果写入 `policy_timeseries` 的年发布量 | 展示需规序号 205、206；专题政策分析「时序模型」。连续性子项见第 3 节 QPOL-07，不另建表 |
| `M_POLICY_BASE_100_1` | 专题 | 不单开事实表。可调度子项就是上表五条里的级别、时序发布量、全国、深圳全市 | 文种与深圳各区不在这一包。登记页 E7-POLICY |
| `M_POLICY_GRAPH_106_1` | 展示 + 专题 | 事实是政策正文，在 `policy_base_info`。实体落点 `policy_entity` 已在 ADS 清单 | 抽取归 POLICY-Graph。本单不建实体表 |
| `M_POLICY_GRAPH_107_1` | 展示 + 专题 | 关系落点 `policy_industry_rel`（DWD 与 ADS 同名）已在派单包 | 不为关联度再造第二张边表 |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 展示 | 可算部分读 `policy_base_info` 正文 | 展示需规序号 226。归 POLICY-MRC，本包不落结果表。推送状态表、编辑日志在供应方库不存在；20261021 未挂待建，2026-10-26 未把它升成 `mt_policy_`。本单不新开缺表 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | 展示 | 环节词与层级读 `policy_base_info` | 展示需规序号 229。归 POLICY-MRC，本包不落结果表。风险事件两库都没有；同样未升成缺表。本单不新开 |

## 2. 缺表（1）

| 指标 | 用到方 | 缺的事实 | 不在本单做的事 |
|------|--------|----------|----------------|
| `M_POLICY_SUPPORT_STRENGTH` | 展示 + 专题 | 一条政策上的扶持方式与金额，并带政策标识。权重不是事实 | 不写建表语句，不在 demo 或产线建空表，不灌金额，不加工本指标 |

展示需规序号 216（标杆比对里的支持力度）。专题侧挂在力度评估（算法库 167 / E7-POLICY），专题政策分析的三维框架也点了「政策支持力度」。

该指标仍在 QPOL-02（权重未签，清单仍为待甲方）。空表任务 `GDF-POLICY-MT-SUPPORT-L01` 本次核对仍为 `backlog`，备注仍是「未点头不开工」。本单不把它标成已点头，不代替该叶建表。

## 3. 缺的是口径而不是表（24）

这些指标的主表或结果壳已经点名。未闭合的是规则。客户决策清单里 QPOL-01、QPOL-02、QPOL-03、QPOL-05、QPOL-07 本次只核对仍为待甲方，没有改色。

### QPOL-01 类型是主题还是文种

| 指标 | 用到方 | 已有落点 |
|------|--------|----------|
| `M_POLICY_TYPE_DIST` | 展示 + 专题 | `policy_base_info.type` 是文种。ADS `policy_type_dist` 有壳。登记要的产业 / 人才 / 企业扶持尚未签，不往该壳写主题分布 |

登记来源为展示。专题「政策类型」饼图挂在同一基础指标。

### QPOL-02 权重、阈值、弹性

| 指标 | 用到方 | 已有落点 |
|------|--------|----------|
| `M_POLICY_DEEP_166_1` | 专题 | `policy_base_info` 正文。焦点模型 |
| `M_POLICY_FOCUS_INDEX` | 展示 + 专题 | 同上。结果壳 `policy_focus`。登记来源为展示，同叶 166 在专题 |
| `M_POLICY_DEEP_167_1` | 专题 | `policy_base_info`。登记的来源系统为空；专题数据需求点名「政策力度评估」 |
| `M_POLICY_INTENSITY_INDEX` | 专题 | 同上主表。效果、成本两维的列在，值空。不是缺表 |
| `M_POLICY_INTENSITY_SCORE` | 展示 + 专题 | 同上。展示需规序号 214、218 |
| `M_POLICY_DEEP_168_1` | 展示 | `policy_base_info`，并点到机构财务表。展示需规序号 156 |
| `M_POLICY_EFFECT_SCORE` | 展示 | `policy_base_info`。结果壳 `policy_effect`。展示需规序号 232、233 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 展示 + 专题 | `policy_base_info`。展示需规序号 209、235。专题政策分析三维里的「落地实效性」。受众反馈调查未升成缺表 |
| `M_POLICY_DEEP_169_1` | 专题 | `policy_base_info`。登记的来源系统为空；专题数据需求点名「政策短板识别」 |
| `M_POLICY_SHORTBOARD_COUNT` | 展示 + 专题 | 政策主表 + 专利表均已点名 |
| `M_POLICY_DEEP_170_1` | 专题 | `policy_base_info` + 专利。登记的来源系统为空；专题数据需求点名「政策机遇识别」 |
| `M_POLICY_OPPORTUNITY_COUNT` | 展示 + 专题 | `policy_base_info`。登记来源为展示，同叶 170 在专题 |
| `M_POLICY_DEEP_171_1` | 专题 | `policy_base_info` + 产业链 + 专利。登记的来源系统为空；专题数据需求点名「政策布局推荐」 |
| `M_POLICY_LAYOUT_REC_COUNT` | 展示 + 专题 | 同上。展示需规序号 227、241 |
| `M_POLICY_DS_07_POLICY_GUARD_001` | 展示 | `policy_base_info` + 专利。展示需规序号 152 |
| `M_POLICY_DS_07_POLICY_GUARD_008` | 展示 | `policy_base_info`。展示需规序号 157 |
| `M_POLICY_TEXT_PARSE` | 展示 | 正文在 `policy_base_info`。结果壳 `policy_text_parse` 已在。词表和阈值仍是临时口径。登记未回填；展示需规有「智能政策拆解 / 政策文本智能解析」 |
| `M_POLICY_SIMULATE` | 展示 | 结果壳 `policy_simulate` 已在。弹性系数未签。归 POLICY-MRC。情景参数表、弹性表、预测指标表不在本单升成缺表。登记未回填；展示需规整节「政策效果推演」 |

`M_POLICY_SUPPORT_STRENGTH` 也挂在 QPOL-02，事实落点见第 2 节，不在这张表里重复占一格。

### QPOL-03 相似度与匹配规则

| 指标 | 用到方 | 已有落点 |
|------|--------|----------|
| `M_POLICY_RELATION_DEGREE` | 展示 + 专题 | 等 `policy_industry_rel` 的边。不建第二张边表。登记未回填；口径文档挂政策图谱与详情「相关政策」 |
| `M_POLICY_INDUSTRY_FIT` | 展示 + 专题 | `policy_base_info` 与链名称匹配。登记未回填；专题政策分析点名「产业适配性」 |
| `M_POLICY_MATCH` | 展示 + 专题 | 结果壳 `policy_match` 已在。企业、产业链表已点名。登记未回填；展示需规序号 212「政策匹配与推送」；专题数据需求写政策匹配 |

### QPOL-07 连续性

`M_POLICY_TIMESERIES` 的发布量已在第 1 节。连续性（`continuity_rate`）缺的是度量规则，独立指标号还没从时序指标拆出。不建连续性事实表。`growth_rate` 同样先留空。

### 主口径尚未指定

| 指标 | 用到方 | 已有落点 |
|------|--------|----------|
| `M_POLICY_VALIDITY_RATE` | 展示 | `policy_base_info` 上已有状态与失效日列。空的失效日是「长期有效」还是「未标注」未签。不建废止事实表，不灌失效日。登记未回填；展示需规科创政策全景的检索条件含政策状态（有效、失效、修订中） |
| `M_POLICY_INDUSTRY_COVERAGE` | 展示 + 专题 | 产业节点由 POLICY-Graph 写入 `policy_industry_rel`。覆盖率取哪一层为主口径未签。不另建节点表。登记未回填；专题数据需求点名产业链节点的政策覆盖 |

## 4. 看过、未升成缺表

下面这些依赖在口径文档里写过「库里没有某张表」。2026-10-26 收口只把扶持事实列为要新落点的事实，其余要么写明不建表，要么归 Graph / MRC 且待建清单为空。本单维持该收口，不新开第二张缺表。

| 指标 | 文档里缺过的东西 | 本单落点 |
|------|------------------|----------|
| `M_POLICY_VALIDITY_RATE` | 废止 / 失效事实 | 口径。`20` 写明不建废止事实表 |
| `M_POLICY_SIMULATE` | 情景参数、弹性系数、预测指标 | 口径（QPOL-02）。结果壳已有 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 受众反馈调查 | 口径（QPOL-02） |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 摘要推送状态、编辑日志 | 已有表（正文）。MRC 不落结果表 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | 风险事件 | 已有表（正文与层级）。MRC 不落结果表 |
| `M_POLICY_RELATION_DEGREE` | 供应方库无边表 | 口径。项目侧边表是已点名的 `policy_industry_rel` |

## 5. 与两侧需规的对照

专题 `srs/04`「政策分析」7 个功能（序号 110–116）对到：时序 → `M_POLICY_TIMESERIES`；区域对比与深圳现状 → 级别 / 全国 / 深圳分布与三维里的支持力度、产业适配、落地实效；深度模型六叶（焦点、力度、效果、短板、机遇、布局）在 `srs/04` 数据需求里点名，对应 `M_POLICY_DEEP_166_1` 至 `M_POLICY_DEEP_171_1` 及同名指数 / 条数。实体识别与关系抽取对应 `M_POLICY_GRAPH_106_1`、`M_POLICY_GRAPH_107_1`。

展示 `srs/02`「科技政策跟踪」三份四级（科创政策全景、政策分析评价、政策效果推演）加上政策对比升级里的智能拆解，序号已写进上表「用到方」能对上登记的那些行。登记 `book=02` 的序号覆盖 152、156、157、205、206、208、209、214、215、216、218、226、227、229、232、233、235、237、239、240、241、549。

## 问题清单

- 7 条登记没有 `srs_refs`：`M_POLICY_INDUSTRY_COVERAGE`、`M_POLICY_INDUSTRY_FIT`、`M_POLICY_MATCH`、`M_POLICY_RELATION_DEGREE`、`M_POLICY_SIMULATE`、`M_POLICY_TEXT_PARSE`、`M_POLICY_VALIDITY_RATE`。用到方按需规点名和口径文档的页面挂载补上，备注写了「登记未回填」。本单不改登记。
- 4 条算法库叶的来源系统字段为空：`M_POLICY_DEEP_167_1`、`M_POLICY_DEEP_169_1`、`M_POLICY_DEEP_170_1`、`M_POLICY_DEEP_171_1`。专题数据需求写了这四个模型名，故用到方记专题。
- QPOL-05 仍待甲方。第一批可调度指标的「已有表」带临时默认：只计国内。

## 修改内容

- 新增本 handoff。
- 未改 `09`、未改指标种子、未改就绪度、未改客户决策清单。QPOL-02 仍为待甲方。
- 未写建表语句。未在 demo 或产线建表。未向 ODS 灌数。未写供应方库。
- 未加工 `M_POLICY_SUPPORT_STRENGTH` 或任何政策指标。
- 未把 `GDF-POLICY-MT-SUPPORT-L01` 标成已点头。本次 `task-get` 该叶仍为 `backlog`。

## 测试结果

定义叶，无跑数、无 CDC、无业务仓 diff。

| DoD | 结果 |
|-----|------|
| 展示与专题用到的政策指标逐条有落点 | 35 条均有一格：已有表 10、缺表 1、口径 24 |
| 缺表只写事实 | 仅扶持方式与金额。无建表语句 |
| 不代替扶持空表叶 | `GDF-POLICY-MT-SUPPORT-L01` 仍为 backlog，本单未建表 |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本叶无脚本 |
| 调用链 | ✅ 不新增接口 |
| 图谱 | ✅ 不写 nGQL，不另建边表 |
| 可观测 | ✅ 定义叶，无运行时埋点，也不伪造成已埋点 |
| CI | ✅ `cicd: skip`（设计类文档） |
| D12 | ✅ 不把 demo 结果壳写成产线已灌数 |
| D9 | ✅ 口径未闭合只列表。未改种子、未改就绪度 |
| D8 / D10 | ✅ 本叶无页面 |
| D14 | ✅ 不写对象存储 |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 150000（本会话估算，不是控制台账单） |
| model_used | grok-4.7 |
| actual_cost | 0.63 |
| cost_warn | green |
| 说明 | 预算表无 grok 单价。按 B 档 $3/$15、定义任务约 90/10 估算。低于黄线 $5 |

## 会签

会签通过。本清单是事实落点判定，不是表已建、数已灌或可对端。扶持事实仍等 `GDF-POLICY-MT-SUPPORT-L01` 点头后再建空表。

## 遗留风险

- 缺表只有扶持事实。空表、加工、灌金额都不在本叶。
- 深圳各区、失效日、主题分类、连续性在表已在的前提下仍不可当正式结果发布。
- 7 条来源系统未回填。后续若补登记，以登记为准核对用到方，不改本单的三格判定，除非事实落点变了。

## CI/CD（必填）

- 分支：`dev`
- commit：见本次提交；若尚未提交，以工作区本文件为准
- pipeline URL / ID：编排仓无业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：`metric-query` 政策域返回 35 条；`task-get` 核对三条相关任务状态

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/POLICY-METRIC-FACT-GAP-L01.md`（本文件）
- 只读：`agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/对接文档/工程侧/2026-10-26-要素指标加工与图谱拆解思路.md`
- 只读：`agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/17-指标离线加工-POLICY-MDC.md` 第 3 节，以及 `19`、`20`、`14` 的表名
- 只读：`agent-delivery/bid-reference/srs/02-科技信息展示系统/` 科技政策跟踪与政策对比升级
- 只读：`agent-delivery/bid-reference/srs/04-科技专题服务系统/` 政策分析与数据需求
- 只读：`agent-delivery/metrics/calc-logic/POLICY/`
- 只读：metric-registry 政策域 35 条（未改种子、未改就绪度）
