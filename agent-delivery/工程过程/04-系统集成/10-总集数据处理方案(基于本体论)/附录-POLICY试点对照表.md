# 附录 · 政策（POLICY）试点对照表

| 项 | 内容 |
|---|---|
| 版本 | v0.1 · 讨论稿 |
| 日期 | 2026-11-13 |
| 所属 | [方案框架-基于本体论的数据治理-v0.1](./方案框架-基于本体论的数据治理-v0.1.md) |
| 条数 | 11 条（MDC 第一批 5 条、MDC 口径未闭合对照 1 条、Graph 2 条、等边的图指标 1 条、MRC 2 条） |
| 取数方式 | 中文名、`algorithm_type`、D1 / D3 / D4、`pending_ref`、`ui_mount`、`srs_refs` 均于 2026-11-13 经 MCP `metric-registry` 的 `metric-get` 逐条查得；未直接读 seed 与矩阵文件 |
| ADS 落表依据 | 政策派单包 v2 的 [17 POLICY-MDC](../../../data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/17-指标离线加工-POLICY-MDC.md)、[18 POLICY-Graph](../../../data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/18-实体关系抽取-POLICY-Graph.md)、[19 POLICY-MRC](../../../data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/19-实时指标-POLICY-MRC.md)，以及 `14-ADS-MySQL-DDL/ads-creates.md` 的列注释 |

本表只证明三层能串起来，不代表这些指标已建作业、已建表或已灌数。产线库名一律为 `gkxlumenx_dwd` / `gkxlumenx_ads`；派单包 `14` 中的 `demo_gkxlumenx_*` 是现网 demo 结构，不作产线目标。

---

## 一、本试点涉及的实体

| EntityType（SAD 七要素） | DWD 正式表 | 业务主键 | 图上 Tag / VID（现网） | 依据 |
|---|---|---|---|---|
| 政策 | `policy_base_info` | `policy_id`；表上唯一键是 `(source_plane, policy_id)` | Tag `policy`，VID `pol:{policy_id}` | DWD DDL 见派单包 `10-DWD-MySQL-DDL/policy_base_info-MySQL.md`；VID 见 [VID 前缀实测与裁定](../07-图数据库集成/KG-COMPLY-VID-L01-VID前缀实测与裁定.md)、[政策上图路径](../07-图数据库集成/KG-7ELEM-LOAD-PATH-L04-政策.md) |
| 产业链与产业环节（底图） | `policy_industry_rel`（政策—产业环节关系表，由 POLICY-C1 写） | `(policy_id, industry_link_code)` 目标唯一 | 环节点现网前缀 `segment:`；政策—产业环节**不上图**（第 07 项必须边清单写明产业链—政策不建） | 派单包 `10-DWD-MySQL-DDL/policy_industry_rel-MySQL.md`、`12` |
| 企业 / 科研机构（匹配对象） | 待查 | 待查 | 企业 `ent:`；科研机构 Tag `research`、前缀 `inst:`，与服务机构 Tag `institution`、前缀 `institution:` 易混（见第 07 项 T11 清单） | 政策→企业、人才、科研机构的稳定 ID 列在 L04 中全部「待确认」 |

## 二、对照表

| # | EntityType | 实体主键 | DWD 表 | metric_id | 中文名 | algorithm_type | 加工包 | ADS 落表 | 消费系统 | D1 / D3 / D4 | 口径决策项 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 政策 | `policy_id`（汇总一行） | `policy_base_info` | `M_POLICY_TOTAL_COUNT` | 政策总数 | STAT | MDC 第一批 | `policy_level_dist`（`level` 为空） | 展示、专题 | aligned / full / mock | QPOL-05（临时只计国内） |
| 2 | 政策 | 按 `level` 分组 | `policy_base_info` | `M_POLICY_LEVEL_DIST` | 政策级别分布 | STAT | MDC 第一批 | `policy_level_dist` | 展示、专题 | aligned / full / mock | QPOL-05 |
| 3 | 政策 | 按 `province` 分组 | `policy_base_info` | `M_POLICY_NATIONAL_DIST` | 全国政策分布 | STAT | MDC 第一批 | `policy_national_dist` | 展示、专题 | aligned / full / mock | QPOL-05 |
| 4 | 政策 | 深圳全市一行 | `policy_base_info` | `M_POLICY_SZ_DIST` | 深圳政策分布 | STAT | MDC 第一批（各区不在本批） | `policy_sz_dist` | 展示、专题 | aligned / partial / mock | QPOL-05；各区属缺样本 |
| 5 | 政策 | 按 `publish_year` 分组 | `policy_base_info` | `M_POLICY_TIMESERIES` | 政策时序指标 | STAT | MDC 第一批（只发布量） | `policy_timeseries` | 展示、专题 | aligned / partial / mock | QPOL-05；连续性子项 QPOL-07 |
| 6 | 政策 | 按类型分组 | `policy_base_info` | `M_POLICY_TYPE_DIST` | 政策类型分布 | STAT | MDC 口径未闭合，不建作业 | `policy_type_dist`（17 明令不写） | 展示、专题 | aligned / partial / mock | QPOL-01 |
| 7 | 政策（及抽出的实体） | `policy_id` | `policy_base_info` | `M_POLICY_GRAPH_106_1` | 政策实体识别构建 | GRAPH | Graph（脚本未进包） | `policy_entity` | 展示（DS-12）、专题 | aligned / full / mock | 无 QPOL；挂 `GAP-ALGO-TYPE-UNSIGNED` |
| 8 | 政策—产业环节等 | `policy_id` | `policy_base_info`、`policy_industry_rel` | `M_POLICY_GRAPH_107_1` | 政策实体关系抽取 | GRAPH | Graph（脚本未进包） | `policy_graph_node`、`policy_graph_edge` | 展示（DS-10 / 12 / 29）、专题 | aligned / partial / mock | 无 QPOL；挂 `GAP-ALGO-TYPE-UNSIGNED` |
| 9 | 政策（图上的点） | `policy_id` | `policy_base_info` + Graph 产出的边 | `M_POLICY_RELATION_DEGREE` | 政策关联度 | GRAPH | MDC，等 Graph 边落地 | `policy_focus`（按 DDL 列注释） | 待查 | aligned / partial / mock | QPOL-03 |
| 10 | 政策 × 企业 / 科研机构 | `policy_id` + 主体键（待查） | `policy_base_info`；主体侧待查 | `M_POLICY_MATCH` | 政策匹配推送 | MODEL | MRC | `policy_match` | 待查 | aligned / partial / mock | QPOL-03 |
| 11 | 政策 | `policy_id` | `policy_base_info` | `M_POLICY_SIMULATE` | 政策效果推演 | MODEL | MRC | `policy_simulate` | 待查 | aligned / partial / mock | QPOL-02 |

### 表格说明

- **DWD 表列**写的是派单包里的项目 DWD 正式表。MCP 查到的八件套 `source_tables` 写的不是它，而是供应方表 `dwd_policy_base`（第 8、10、11 行还另列了 `dwd_industry_chain_info`、`dwd_org_*`、`dwd_bid_` 等供应方表）。两处不一致，见第四节缺口 1。
- **消费系统列**：第 1～6 行的「展示、专题」取自 `ui_mount`（写明了「科技专题服务系统」与「科技信息展示系统」）；但 `srs_refs` 的系统字段在第 2～6 行只有「展示」，第 1 行同时有专题与展示。需求来源与挂载位置对不齐，以哪个为准待确认。第 9～11 行 `srs_refs` 为空，`ui_mount` 只写「政策图谱页」「企业详情页」等设计位，未写系统名，故写「待查」。
- **D3 列**本不在必填列内，加上是因为 D1 全为 aligned、D4 全为 mock，单看两列看不出差别。
- **第 4 行**：17 规定只写一行全市合计，不按区 `GROUP BY`；深圳各区属「缺样本」，灌数闸门未开。
- **第 6 行**放进来作对照：同在 `policy_base_info` 上、同为 STAT，但因 QPOL-01 未闭合而不建作业，说明「能算」不等于「能发布」。
- **第 9 行**的落表依据只是 `ads-creates.md` 中 `policy_focus.metric_id` 列注释列出了该指标，17 / 18 正文没有写死它的落表，属「待确认」。

## 三、待查格清单

| 行 | 列 | 原因 |
|---|---|---|
| 9 | 消费系统 | `srs_refs` 为空；`ui_mount` 只写设计位页面名 |
| 10 | 消费系统 | 同上 |
| 11 | 消费系统 | 同上。SAD 中 DS-12 政策效果推演标为 501，是否就是本指标的读面待确认 |
| 10 | 实体主键（主体侧）、DWD 表（主体侧） | 匹配对象是企业还是科研机构、用哪张 DWD、哪个稳定 ID，派单包与 L04 均未写定 |
| 一节第 3 行 | 企业 / 科研机构的 DWD 表与主键 | 属企业、科研机构两域，本期不扩 |

另有「待确认」而非「待查」的两处：第 9 行 ADS 落表（只有列注释依据）；政策 VID 不含 `source_plane`（见第四节缺口 3）。

## 四、这份试点证明了什么、暴露了什么

### 证明了什么

1. 三层可以串起来。11 条里每一条都能从 `metric_id` 找到八件套、找到 GDF 三包中的归宿、找到 ADS 落表；政策实体在 DWD 有业务主键，在图上有 Tag 与 VID。
2. 「一张 ADS 承载多个 `metric_id`」可行，前提是行上带 `metric_id` 并只删本指标行（第 1、2 行同落 `policy_level_dist`）。
3. 三包拆法与三层真源互不冲突：MDC 与 MRC 只写 ADS，Graph 写关系表与图，三者都回指同一个 `policy_id`。
4. 口径未闭合项已被现有机制挡住（17 第 3 节、客户决策清单），本框架不需要另设闸门。

### 暴露的缺口

| # | 缺口 | 影响 | 建议去向 |
|---|---|---|---|
| 1 | 八件套 `source_tables` 指供应方表 `dwd_policy_base`，`source_systems` 写供应方地址；派单包实际读项目 DWD `policy_base_info`。`algo_server_location` 仍指 `demo-algo-ent-analysis` | 第二层与第三层断链：从 ⓘ 走不到 DWD 正式表 | data-agent 按 D9 正式化流程改 seed（本项不改） |
| 2 | 11 条 D1 全为 `aligned`，但第 6、9、10、11 行挂未闭合 QPOL，第 7、8 行 `d1_note` 写「formula / algorithm_type 未签」且挂 `GAP-ALGO-TYPE-UNSIGNED`；八件套 `formula` 全部是「见 calc-logic」而非可执行表达式 | D1 失去区分度，评审时无法据 D1 判断能否发布 | D9 维护方复核 D1 判定规则 |
| 3 | DWD 唯一键是 `(source_plane, policy_id)`，图上 VID 是 `pol:{policy_id}`，不含平面 | 国内与国际政策同号时图上会撞点（是否真有同号未实测，待确认） | 数据 lead + 第 07 项 |
| 4 | 政策—产业环节关系只在 DWD 表 `policy_industry_rel`，第 07 项必须边清单写明产业链—政策不建；而 SAD 写「其余要素挂在环节上」 | 本体语义上有这条关系，物理上不在图里；图类指标若要用它需另行约定 | 待决事项第 6 条 |
| 5 | 政策 DWD 与 ADS 的排序规则是 `utf8mb4_0900_ai_ci`，`metric_id` 列是 `longtext`；团队公约 D19 要求 `utf8mb4_general_ci` | 与其他域 JOIN 时可能报 1267；`metric_id` 无法建普通索引 | 架构确认是否按 D19 处理（本项不改 DDL） |
| 6 | 匹配、推演、关联度三条 `srs_refs` 为空，读面系统不明 | 无法验证「展示与专题读同一个数」 | data-agent 回填需求来源 |
