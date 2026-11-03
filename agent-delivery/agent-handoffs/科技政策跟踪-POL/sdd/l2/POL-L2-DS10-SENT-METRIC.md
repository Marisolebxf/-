# POL-L2-DS10-SENT-METRIC · 科创政策全景 · 政策舆情评估 · 后台指标设计

- 任务：`POL-L2-DS10-SENT-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-03`
- 上游：`sdd/l2/POL-L2-DS10-SENT-ARCH.md`（2026-11-03 已签收，本叶为准）。本叶会签态 `draft`，不代签，不标 done
- 查询：2026-11-03 经 MCP `metric-get` / `metric-query`。未读 seed、矩阵 YAML，未改注册表

本叶只写科创政策全景二级「政策舆情评估」的指标挂接。SRS 序号 **207–212**。

上游只引用，不改写：`sdd/l2/POL-L2-DS10-SENT-ARCH.md`、`sdd/指标与501.md` 全景表 207–212 行、`sdd/l2/POL-L2-DS10-QRY-METRIC.md`（格式对齐）。不新注册指标，不改 D4，不写假公式，不改算法代码，不写 OpenAPI。

## 1. 范围

六叶都在全景里完成。挂接沿 `指标与501.md` 全景表。读面沿已签收的 `POL-L2-DS10-SENT-ARCH`。本叶不改那两份文件，也不把调研判定列改写成另一档。

| 序号 | 叶子 | 指标与501 | 本叶 |
|---|---|---|---|
| 207 | 政策查询与对比 | 可接统计读面；三条 STAT；D4=`mock` | 挂已有三条。无独立对比模型。空不造 0。深度交叉对比不在本叶 |
| 208 | 区域政策差异性分析 | 跨项索引；`M_POLICY_GRAPH_107_1`；GRAPH；D4=`mock` | 保持 GRAPH。地区件数可借全国、深圳分布，不把本行改判成 STAT |
| 209 | 政策实施效果跟踪 | `M_POLICY_IMPLEMENTATION_EFFECT`；MODEL；D4=`mock`；判定列写 501 | 挂这一条。QPOL-02。读已有 ADS 与时序。无行则空。不用 501 充当功能 |
| 210 | 政策受众反馈收集 | 未见 `metric_id`；判定列 501 | 不新注册。缺项表 `metric_id` 留空 |
| 211 | 政策效果评估报告 | 未见 `metric_id`；判定列 501 | 不新注册。缺项表 `metric_id` 留空。不假挂成效果指标 |
| 212 | 政策匹配与推送 | 两条 MODEL；D4=`mock`；判定列写 501 | 挂已有两条。QPOL-03。同一张 `ads.policy_match`。无行则空。推送和邮件不新挂指标 |

207 的 D4 仍是 `mock`。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿视为未解开。本叶不把 mock 写成已上线。

`指标与501` 把 209、212 的判定列写成「501，页面空态」。那是调研时页面未接上的记录。已签收架构规定这两叶读表，无行则空，不用 501 充当功能。本叶采用这条读面，不回头改 `指标与501`。

## 2. 本二级用到的已有 metric_id

挂接去重后 7 条，落在 207、208、209、212。210、211 不在此表。全部 `metric-get` 为 `found.seed=true`、`found.matrix=true`。D4 都是 `mock`。中文名、`algorithm_type` 以 MCP 为准。

| metric_id | 中文名（MCP） | algorithm_type | D4 | 挂在 |
|---|---|---|---|---|
| `M_POLICY_TOTAL_COUNT` | 政策总数 | STAT | mock | 207 |
| `M_POLICY_TYPE_DIST` | 政策类型分布 | STAT | mock | 207 |
| `M_POLICY_LEVEL_DIST` | 政策级别分布 | STAT | mock | 207 |
| `M_POLICY_GRAPH_107_1` | 政策实体关系抽取 | GRAPH | mock | 208 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 落地实效性 | MODEL | mock | 209 |
| `M_POLICY_MATCH` | 政策匹配推送 | MODEL | mock | 212 |
| `M_POLICY_INDUSTRY_FIT` | 政策产业适配性 | MODEL | mock | 212 |

212 占两行。这 7 条之外，本二级不新造 `metric_id`。

叶子名与注册中文名不一致的，以 MCP 为准，挂接 id 不变：

- 209 的叶子名是「政策实施效果跟踪」。注册中文名是「落地实效性」。
- 212 的叶子名是「政策匹配与推送」。`M_POLICY_MATCH` 的注册中文名是「政策匹配推送」。`M_POLICY_INDUSTRY_FIT` 的注册中文名是「政策产业适配性」。
- 208 的叶子名是「区域政策差异性分析」。注册中文名是「政策实体关系抽取」。类型仍是 GRAPH。

208 画地区件数时，可以读 `stats` 上已有的下面两条。它们仍是序号 197 的统计读面，不把 208 改判成 STAT，也不新挂到 208 的 `metric_id` 格。2026-11-03 `metric-get` 复核：中文名、STAT、D4=`mock` 与 `POL-L2-DS10-QRY-METRIC` 第 3 节一致。

| metric_id | 中文名 | algorithm_type | D4 | 本叶 |
|---|---|---|---|---|
| `M_POLICY_NATIONAL_DIST` | 全国政策分布 | STAT | mock | 可借件数。不改 208 的判定 |
| `M_POLICY_SZ_DIST` | 深圳政策分布 | STAT | mock | 可借件数。不改 208 的判定 |

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进本节。

源系统下列各条相同：`gkx @ 183.240.141.251:3318（只读）`。`version` 都是 `1`。

| metric_id | 中文名 | algorithm_type | 源表 | 更新频率 |
|---|---|---|---|---|
| `M_POLICY_TOTAL_COUNT` | 政策总数 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_TYPE_DIST` | 政策类型分布 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_LEVEL_DIST` | 政策级别分布 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_NATIONAL_DIST` | 全国政策分布 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_SZ_DIST` | 深圳政策分布 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_GRAPH_107_1` | 政策实体关系抽取 | GRAPH | `dwd_global_policy_base`、`dwd_global_policy_base_bak_20260923`、`dwd_industry_chain_info`、`dwd_policy_base`、`dwd_policy_base_bak_20260923` | pending |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 落地实效性 | MODEL | `dwd_policy_base` | quarterly |
| `M_POLICY_MATCH` | 政策匹配推送 | MODEL | `dwd_industry_chain_info`、`dwd_org_base_info`、`dwd_org_industry_tags`、`dwd_org_tech_tag`、`dwd_policy_base` | daily |
| `M_POLICY_INDUSTRY_FIT` | 政策产业适配性 | MODEL | `dwd_policy_base` | weekly |

注册公式：207 的三条、208 的图指标、209、212 的三条，`kit.formula` 都是同一类过程指针：见 calc-logic「计算逻辑说明」与 20261021 正本 §二；公式是过程式复算，未浓缩为单行表达式；禁手抄，实现时以 `code/<metric_id>.py` 为准。本叶不手抄、不展开成可执行式，也不另写一条能算出数的式子。

口径按 `metric-get` 的 `kit.definition` 摘录，不改写。全国分布、深圳分布的摘录与 `POL-L2-DS10-QRY-METRIC` 第 3 节相同，这里不重复改写。

| metric_id | 口径 |
|---|---|
| `M_POLICY_TOTAL_COUNT` | 政策总数就是底表行数。主键 `id` 无重复，`is_deleted` 全 0，`COUNT(*)` 与 `COUNT(DISTINCT id)` 相等。库内没有现成汇总表，由一条聚合生成。注册判定为完全转换支持 |
| `M_POLICY_TYPE_DIST` | 文种维 `type` 可转换；主题维 `theme` / `keywords` / `keypoints` 数据不足。合成后按部分支持。需规里的主题分类本叶不改写成已经可算。口径标记 QPOL-01，本叶不改口径 |
| `M_POLICY_LEVEL_DIST` | `rank` 列有值。空字符串过滤后记为未标注，五档合计与底表行数闭合。注册判定为完全转换支持 |
| `M_POLICY_GRAPH_107_1` | 五项点名关系里，实施主体能借发文机关弱建，其余四类缺少可承载字段。能建的边与需求要的边不是同一批。注册判定为部分支持 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 启动维、覆盖维、反馈维都没有可用输入。注册判定为完全不支持。注册说明写明：强行出 0 分会把导入缺陷写成政策事实。本叶因此保持无行则空，不造 0，也不把这句注册口径改写成可执行式 |
| `M_POLICY_MATCH` | 产业维与诉求维缺少可用的政策侧词和诉求标签。地区维、有效性维可算，但区分度不足。注册判定为部分支持。`srs_refs` 为空。口径标记 QPOL-03，本叶不改口径 |
| `M_POLICY_INDUSTRY_FIT` | 政策、城市、链树结构在，匹配能跑，多数链达不到出分门槛。注册判定为部分支持。`srs_refs` 为空。口径标记 QPOL-03。本叶不把这条注册口径改成另一套产业打分 |

209、212 的展示读数不在接口里重算，也不替换上表的注册公式。

209 以仓库里已有的 `polan/eval/effect.py` 的 `run()` 为准，本叶不重写。`demo-algo-ent-analysis` 与 `lumen-algo-py/vendor/entan-py` 各有一份，做法相同：执行维来自政策有效性与因子力度；社会维、环境维是受控高斯代理；写入 `ads.policy_effect`（`scope_type=region_effect`）时，行上扩展信息带 `is_mock` 与 QPOL-02。落地实效写入 `ads.policy_metric_timeseries`，`metric_id` 为 `M_POLICY_IMPLEMENTATION_EFFECT`。同一次写入里，`ads.policy_effect` 行上的 `metric_id` 列是 `M_POLICY_EFFECT_SCORE`。本叶不把 `M_POLICY_EFFECT_SCORE` 改挂到 209。

212 以仓库里已有的 `polan/text/match.py` 的 `run()` 为准，本叶不重写。两份仓库的计分相同，模块注释里的加权符号不另立一套公式。已有计分是：行业命中 +40；地区适用或国家级普适，两条取其一，+25；需求重叠每项 +10；未失效（代码理由文案为「未过期」）+10。每主体取 Top 8，写入 `ads.policy_match`，行上 `metric_id` 为 `M_POLICY_MATCH`。主体由这份 `run()` 的受控画像生成，不是企业库。`M_POLICY_INDUSTRY_FIT` 读同一张表，不另写打分，不另灌一套。算法库页面上的 35 分演示行不是展示服务的返回值。

`extras.algo_server_location` 指向 demo 仓 `polan/metrics/metrics.py`。那是注册表索引，不是本二级的展示调用链。本叶不改那些文件，也不把展示改去调 demo 服务。展示仍按架构稿：浏览器只打 `/display/v1/policy/**`。

## 4. 接入状态

接入状态不是八件套。下表来自 `metric-get` 的 `readiness`。D1 都是 `aligned`，D2 都是 `partial` 且 `d2_assessed=provisional`（待核验），D4 都是 `mock`。本叶不改任何一维。

| metric_id | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| `M_POLICY_TOTAL_COUNT` | aligned | partial，待核验 | full | mock |
| `M_POLICY_TYPE_DIST` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_LEVEL_DIST` | aligned | partial，待核验 | full | mock |
| `M_POLICY_NATIONAL_DIST` | aligned | partial，待核验 | full | mock |
| `M_POLICY_SZ_DIST` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_GRAPH_107_1` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_IMPLEMENTATION_EFFECT` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_MATCH` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_INDUSTRY_FIT` | aligned | partial，待核验 | partial | mock |

`is_mock=true`。`d4_note` 写算法服务未上线，保持 mock。对齐前数值仍是 mock。

需求来源不是八件套。沿用查询结果，本叶不改挂：

| metric_id | srs_refs | 本叶用法 |
|---|---|---|
| `M_POLICY_TOTAL_COUNT` | 展示 02/215 部门政策对比；专题 05/100 基础指标 | `指标与501` 与架构稿把总数挂在 207。215 是另叶复用，本叶不改 `srs_refs` |
| `M_POLICY_TYPE_DIST` | 05/100。QPOL-01 | 207 |
| `M_POLICY_LEVEL_DIST` | 05/100 | 207 |
| `M_POLICY_NATIONAL_DIST` | 05/100 | 只供 208 借地区件数。挂接仍在 197，本叶不改挂 |
| `M_POLICY_SZ_DIST` | 05/100 | 只供 208 借地区件数。挂接仍在 197，本叶不改挂 |
| `M_POLICY_GRAPH_107_1` | 展示 02/208 区域政策差异性分析；另有 02/239、02/240、02/549；专题 05/107 | 本叶只认 208。推演页与载体页不在本叶展开。`found.srs_map=true` |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 展示 02/209 政策实施效果跟踪；展示 02/235 多维度效果评估；专题 05/168 | 209。235 在推演页，同 id 不在本叶展开 |
| `M_POLICY_MATCH` | 空。`found.srs_map=false`。QPOL-03 | 212 |
| `M_POLICY_INDUSTRY_FIT` | 空。`found.srs_map=false`。QPOL-03 | 212。与 `M_POLICY_MATCH` 同读 `ads.policy_match` |

## 5. 207、208、209、212 怎么读

读面沿架构稿，不新开路径，不新造指标。

### 5.1 207 政策查询与对比

可接统计读面。挂：

- `M_POLICY_TOTAL_COUNT`
- `M_POLICY_TYPE_DIST`
- `M_POLICY_LEVEL_DIST`

三条都是 STAT，D4 仍是 `mock`。没有独立对比模型。类型、地域、时期落在已有 `search` 上。同时查看多条正文是按条读 `{id}/detail`。并列查看不新开对比指标。

空态：无行则统计卡、列表或正文空，不造 0。深度交叉对比不在本叶，不改走 `compare/jobs`。

### 5.2 208 区域政策差异性分析

跨项索引。挂 `M_POLICY_GRAPH_107_1`。MCP 类型 GRAPH，D4=`mock`。本行不改判成 STAT。

本叶不新开 `/display/v1/policy` 资源。展示只消费第 7 项已有子图。挂接可空：子图读不到则该块空。

地区件数可以读 `M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`。那是序号 197 的 `stats`，D4 仍是 `mock`。借件数不把 208 的 `algorithm_type` 改成 STAT。

支持力度是序号 216 的 `M_POLICY_SUPPORT_STRENGTH`，不挂本叶。实施条件不在本行计算。

### 5.3 209 政策实施效果跟踪

挂 `M_POLICY_IMPLEMENTATION_EFFECT`。MCP：中文名「落地实效性」，MODEL，D4=`mock`，QPOL-02。

读已有表，不另建表：

- `ads.policy_effect`，`scope_type=region_effect`
- `ads.policy_metric_timeseries` 里 `metric_id=M_POLICY_IMPLEMENTATION_EFFECT` 的行

公式不重写，见第 3 节对 `polan/eval/effect.py` 的指认。社会维、环境维在采购数据到位前由已有 `run()` 写入表，接口只读表。行上保留 `is_mock` 与 QPOL-02。D4 不改。

同 id 也在推演页（`srs_refs` 的 02/235）。本叶不扩展那一页。

无行则空。不用 501 充当这块功能，不造 0，不在接口里写效果数。`M_POLICY_EFFECT_SCORE` 不改挂到本叶。`M_POLICY_DEEP_168_1` 不挂本叶。这张区域表不是序号 211 的评估报告。

### 5.4 212 政策匹配与推送

挂 `M_POLICY_MATCH` 与 `M_POLICY_INDUSTRY_FIT`。两条都是 MODEL，D4=`mock`，QPOL-03，`srs_refs` 为空。

同一张 `ads.policy_match`，一个 sub_type `policy_match`。打分不重写，见第 3 节对 `polan/text/match.py` 的指认。`M_POLICY_INDUSTRY_FIT` 不另写一套打分。主体是受控画像，不是企业库。

无行则列表空。不用 501 充当功能，不返回演示页上的 35 分。分数只来自表里查到的 `match_score`。D4 保持 mock。

通知和邮件不新挂指标，不灌假推送。不把推送挂到评价页的 `M_POLICY_DS_11_POLICY_EVAL_012`。

## 6. 210、211 没有已挂指标

210、211 在 `指标与501` 里 `metric_id` 为未见。本叶不新注册。缺项表行上的 `metric_id` 留空。不把反馈或报告假挂成某个效果指标。

2026-11-03 `metric-query`（domain=政策）：

| 关键词 | 命中 | 本叶 |
|---|---|---|
| 受众 | 0 | 未查到受众指标 |
| 问卷 | 0 | 未查到 |
| 意见征集 | 0 | 未查到 |
| 评估报告 | 0 | 未查到报告指标 |
| 反馈 | 1 | 命中 `M_POLICY_IMPLEMENTATION_EFFECT`（落地实效性）。口径里有「反馈维」，它是 209，不是受众反馈。210 不挂 |
| 推送 | 2 | `M_POLICY_MATCH`（212 已挂）；`M_POLICY_DS_11_POLICY_EVAL_012`（智能摘要与结论推送，评价页 226）。212 的通知和邮件不挂第二条 |

### 6.1 210 政策受众反馈收集

没有已挂 `metric_id`。真实采集不在本叶新造指标。

架构稿的读面是 `GET /display/v1/policy/panorama/feedback`，只读 `gkxlumenx_gapfill.gapfill_policy_audience_feedback`。灌数行带 `metric_id` 列时留空。表里没有行则列表空，不造一条反馈。D4 没有可改的注册指标；灌入的行仍是 mock，本叶不把缺项写成已上线。

不把 209 的落地实效性改挂成反馈指标。

### 6.2 211 政策效果评估报告

没有已挂 `metric_id`。不新注册报告指标。

架构稿的读面是 `GET /display/v1/policy/panorama/assessment-report`，只读 `gkxlumenx_gapfill.gapfill_policy_assessment_report`。行上 `metric_id` 留空。表里没有行则报告空。

不挂 `M_POLICY_DEEP_168_1`。不把 `M_POLICY_IMPLEMENTATION_EFFECT` 或 `M_POLICY_EFFECT_SCORE` 假挂成这份报告。序号 209 的区域表不是这份报告。

## 7. 点名不挂

下列已注册指标在检索或本叶查询里出现。本二级不改挂到 207–212，也不把它们的 D4 改掉。身份来自 2026-11-03 `metric-get`。

| metric_id | 注册身份（metric-get） | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_SUPPORT_STRENGTH` | 支持力度；COMPUTE；D4=`mock`；需求来源含展示 02/216 | 序号 216。208 的支持力度不改挂到本叶 |
| `M_POLICY_EFFECT_SCORE` | 政策效果评分（王惠三维口径 v2 复现）；MODEL；D4=`mock`；需求来源为展示 02/232、02/233 | 推演页。`effect.run()` 会把它写进 `ads.policy_effect.metric_id`。209 不改挂这条 |
| `M_POLICY_DEEP_168_1` | 政策效果评估模型；MODEL；D4=`mock`；需求来源为展示 02/156 | 不挂 209，也不挂 211 |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 智能摘要与结论推送；MODEL；D4=`mock`；需求来源为展示 02/226 | 评价页。212 的通知和邮件不挂这条 |

`M_POLICY_EFFECT_SCORE`、`M_POLICY_DEEP_168_1`、`M_POLICY_SUPPORT_STRENGTH`、`M_POLICY_DS_11_POLICY_EVAL_012` 的 `found.seed` 与 `found.matrix` 都是 true。D4 都是 `mock`。本叶只核对身份，不展开它们的计算。

## 8. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不手抄注册公式，不把 `effect.py`、`match.py` 重写成新公式，不把演示页 35 分写成展示返回值。
- 不把 208 改判成 STAT。不把支持力度挂进 208。
- 不把 `M_POLICY_EFFECT_SCORE`、`M_POLICY_DEEP_168_1` 挂到 209 或 211。
- 不给 210、211 补 `metric_id`。缺项表该列留空。
- 不把推送或邮件写成新指标。
- 不改算法代码，不改 demo 仓与 vendor 里的 `effect.py`、`match.py`。
- 不改 `指标与501.md`、`POL-L2-DS10-SENT-ARCH.md`、`POL-L2-DS10-QRY-METRIC.md`、说明书、指标 seed 与矩阵。
- 不写 OpenAPI 字段、请求体、响应体、枚举。
- 不会签。不把本单标 done。
