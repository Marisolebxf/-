# POL-L2-DS11-PLAN-METRIC-SIGNOFF-DATA · 政策分析评价 · 推荐方案报告交互展示 · 后台指标设计数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-METRIC`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-PLAN-ARCH`（注册表 done）第 9 节；`POL-L2-DS11-PLAN-DATA` 第 2 节列清单；`POL-L2-DS11-PLAN-API` 第 2 节末段；`sdd/指标与501.md` 227–231 行（只转述，不改）
- 范围：SRS 227–231 的指标挂接、`metric_id` 落列口径、D4 表述、灌数行上指标字段的数据侧核对

## 结论

**同意会签**

本页只从数据角色核对 METRIC 分册的指标挂接是否与 DATA 分册的列定义和灌数口径一致。不改 METRIC 分册，不改 DATA 分册，不改架构稿，不改指标注册表，不改模型注册表，不建库，不灌数。

## 核对

### 挂接总口径

| 项 | METRIC 分册写法 | 对数据判定 |
|---|---|---|
| 唯一挂接 | 挂接 1 条，只落在 229：`M_POLICY_DS_11_POLICY_EVAL_015`（GRAPH、D4=mock 转述自 `指标与501` 与架构稿） | 一致。DATA 第 5 节路径与风险行 `metric_id` 固定此号；架构第 9 节同 |
| 其余留空 | 227、228、230 行上 `metric_id` 留空；231 不单独占种类，不另造一行去填号 | 一致。DATA 第 2 节：其余三种写 NULL 不写空字符串；231 无行无列可填 |
| 不新注册 | 不新注册指标，不写假公式，不改 D4 | 一致。DATA 多处同句 |
| 不动注册表 | 不改 `cfg_model_registry.yaml`，不据此让 229 读推演表 | 一致。注册表把 015 与 `M_POLICY_SIMULATE` 并列在 `POLICY_SIMULATE` 下，函数只写后者——两册都只转述不修改 |

### 各叶行上 `metric_id`

| 项 | METRIC 分册写法 | DATA 分册列定义 | 判定 |
|---|---|---|---|
| 227 | 留空。不挂 `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1`、`M_POLICY_SIMULATE` | 第 3 节同句点名不挂 | 一致 |
| 228 | 留空。不挂 `M_POLICY_SIMULATE`，不读 `ads.policy_simulate` | 第 4 节「不把 `M_POLICY_SIMULATE` 写入这些行」 | 一致 |
| 229 | 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。不改 D4，不被 241 顶替 | 第 5 节固定此号；`sort_no` 升序读，不读图 | 一致 |
| 230 | 留空。不把 015 抄到意见行上 | 第 6 节「不把 `M_POLICY_DS_11_POLICY_EVAL_015` 抄到意见行上」 | 一致 |
| 231 | 不占种类，方案对照行和意见行上的号仍按 227、230 留空 | 第 7 节导出取的是这些行的既有列，无新行 | 一致 |

### D16 行级列与灌数口径

| 项 | METRIC 分册写法 | 对数据判定 |
|---|---|---|
| D16 五列 | 第 6 节：行上带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at` | 一致。DATA 第 2 节五列齐备；`gap_item` 按 `row_kind` 固定四值（序号+叶子名），`fill_method` 固定 `manual`，`is_mock` 每行 1 |
| 灌数单归属 | `POL-L2-DS11-PLAN-GAPFILL-L01` 灌四种行；没有已挂指标的 `metric_id` 留空，路径与风险行写 015；本叶不认领、不执行该单 | 一致。DATA 第 8 节同句；灌数单 backlog，DoD 指向同一张表同四种行 |
| 查询不灌数 | 查询请求不灌数 | 一致。DATA 第 1、8 节同句 |
| 不改判定列 | `指标与501` 227–231 判定 501 不回头改；读面按架构「无行则空，不用 501 充当」 | 一致。与 DATA/API 两册空态口径相同 |

### 边界与点名排除

| 项 | METRIC 分册写法 | 对数据判定 |
|---|---|---|
| 推演键隔离 | `M_POLICY_SIMULATE`、`ads.policy_simulate`、`polan.text.simulate.run` 不进 228、229 | 一致。DATA 第 4、9 节：省级力度情景、弹性曲线、推演行不灌进本表 |
| 227 不挂布局键 | `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` 留在布局推荐键 | 一致。DATA 第 3、9 节点名不写入方案对照 |
| 241 不顶替 229 | 015 只留在 229；241 无专属号 | 一致。DATA 第 5、9 节：241 的行不写入本表 |
| `evaluation/counts` | 不在本二级，不读不改 | 一致。架构第 6 节点名排除 |
| 受众反馈 | 序号 210 `gapfill_policy_audience_feedback` 不是方案意见 | 一致。DATA 第 6、9 节点名 |

### 八件套诚实性（数据侧背书）

| 项 | METRIC 分册写法 | 对数据判定 |
|---|---|---|
| 不填未查字段 | 未见 metric MCP，中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1–D3 不补 | 支持。数据侧同样未查注册表，不把「读表」当「注册源表」写进 8 件套；读表身份与注册身份两分 |
| 不把读面当公式 | 读表只说明展示从哪里取数，不在请求内重算 | 一致。查询原样返回已灌行，无现算路径 |
| 不虚报 D4 | D4 转述为 mock，不升 live；缺项表灌入的行仍是 mock | 一致。`is_mock=1` 列落同一口径，行级可查 |

### 观察（不构成不同意）

| 观察 | 说明 |
|---|---|
| 231 无行可填号 | 231 不占行种类，`gap_item` 表也没有 231 一行——METRIC 的「不另造一行去填号」与 DATA 的「231 没有行，因此没有 gap_item」互为印证，无需处理 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
