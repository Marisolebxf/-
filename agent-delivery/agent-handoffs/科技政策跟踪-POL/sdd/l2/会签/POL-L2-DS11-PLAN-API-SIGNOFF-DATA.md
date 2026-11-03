# POL-L2-DS11-PLAN-API-SIGNOFF-DATA · 政策分析评价 · 推荐方案报告交互展示 · 后台接口设计数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-API`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-PLAN-ARCH`（注册表 done）第 2、3、5、8、9 节；`POL-L2-DS11-PLAN-DATA` 第 1、2、3–8 节；`POL-L2-DS11-READ-DATA` 第 4 节（壳表边界）
- 范围：SRS 227–231 的公开资源读法、行种类、取数列、D16 列转述、表边界与空态的数据侧核对

## 结论

**同意会签**

本页只从数据角色核对 API 分册的读法是否被 `POL-L2-DS11-PLAN-DATA` 的表定义支撑。不改 API 分册，不改 DATA 分册，不改架构稿，不改注册表，不建库，不写 SQL，不灌数。

## 核对

### 资源与表读法

| 项 | API 分册写法 | 对数据判定 |
|---|---|---|
| 五叶读法统一 | 签收口径：五叶都读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。227–229 各一次 `jobs`，230–231 各一次 `shells` | 一致。与 DATA 第 1 节范围表逐行对应，与架构第 2 节迁移读法相同 |
| 不越层 | display 不直连库、不直连 Python；element 只读该表 | 一致。DATA 第 1 节同句。谁写是灌数单的 Python，谁读仅 element |
| 不进异步 | 227–229 不建任务，不进 `PolicyAnalysisTypes`，不加 `policy_scheme`，五叶不进 `POST /internal/policy/jobs/execute` | 一致。与架构第 2 节相同，不产生异步写表路径 |

### 行种类闭集

| 项 | API 分册写法 | 对数据判定 |
|---|---|---|
| 四值闭集 | 第 2 节：表只有四种行种类——方案对照、参数模拟、路径与风险、互动意见 | 一致。DATA 第 2 节 `row_kind` 同四值，无第五值；架构第 9 节同 |
| 231 不占种类、不建文件表 | 第 7 节：同步，不另建报告行，不另建文件表；导出从当次读到的方案对照行和互动意见行生成 | 一致。DATA 第 2 节「231 不写入 `row_kind`」、第 7 节「不设文件地址、对象键、文件字节列」；不灌 PDF、Word、Excel |
| 一次一种类 | `jobs`/`shells` 一次请求只带一种类；其他种类留给可视化、解读二级 | 一致。DATA 第 2 节拣行只按 `row_kind`，与按种类分发的读法匹配 |

### 各叶取数列（对照 DATA 第 2 节列清单）

| 项 | API 分册写法 | DATA 列清单 | 判定 |
|---|---|---|---|
| 227 方案对照 | 一行一个方案：名称、一句说明、若干对照维度和数值、优劣结论、实施建议 | `scheme_name`（NOT NULL）、`summary_text`、`compare_items`、`verdict_text`、`advice_text` 四 text 必填 | 一致。五列齐备，`compare_items` 组数不固定支撑雷达与 KPI 取数 |
| 228 参数模拟 | 一行挂一个方案：参数档、评估结果、一句趋势、一条归档说明；按方案和参数档拣行 | `param_band`（同一方案下不重复）、`eval_result`、`trend_text`、`archive_text` | 一致。四列齐备；拣行条件 `scheme_name`+`param_band` 可用 |
| 229 路径与风险 | 一行挂一个方案：节点名称、时间进度、一句节点说明、风险标题、一句风险说明；一个方案可多行 | `node_name`、`schedule_text`、`node_text`、`risk_title`、`risk_text`、`sort_no`（同方案内不重复，读取按 `sort_no` 升序） | 一致。六列齐备，节点与风险同行；`sort_no` 定序与「多行返回」匹配 |
| 230 互动意见 | 一行挂一个方案：主体、分类、意见正文、时间；分类只用评价、评论、建议 | `actor_name`、`opinion_kind`（三值闭集）、`opinion_text`、`opinion_at`（与 `generated_at` 分列） | 一致。四列齐备，分类闭集与 DATA 第 2 节约束逐字相同 |
| 231 复读 | 读方案对照行（名称、说明、优劣结论、实施建议、对照值）和互动意见行，从这些行生成导出 | 第 7 节点名取 `scheme_name`/`summary_text`/`verdict_text`/`advice_text`/`compare_items` 与 `actor_name`/`opinion_kind`/`opinion_text`/`opinion_at` | 一致。参数模拟行、路径与风险行不进导出，两册同 |

### D16 行级列转述

| 项 | API 分册写法 | 对数据判定 |
|---|---|---|
| 每行 D16 列 | 第 2 节末段：每行带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`，以架构第 9 节为准 | 一致。DATA 第 2 节五列全为 NOT NULL（`metric_id` 除外，见下行），另加 `is_mock=1` |
| `metric_id` 归属 | 路径与风险行用已有 `M_POLICY_DS_11_POLICY_EVAL_015`；其余三种留空，不新注册 | 一致。DATA 第 2 节并写明「其余三种留空，写 NULL，不写空字符串」 |
| `fill_method` | 用 `manual` | 一致。固定 `manual`，因此不设 `fill_model` |
| `gap_item` | 写序号和叶子名 | 一致。DATA 按 `row_kind` 固定四值（227/228/229/230 各一），231 无行无 `gap_item` |
| D4 | 保持 mock；`GDF-POLICY-MOCK-GATE-L01` 仍 blocked | 一致。`is_mock` 每行必须为 1，不把缺项行写成已上线 |

### 表边界

| 项 | API 分册写法 | 对数据判定 |
|---|---|---|
| 壳表 | 不读 `gapfill_policy_eval_shell`。那张壳表只服务解读的 224、225 | 一致。READ-DATA 第 4 节壳表 `entry_kind` 只有解读/多媒体，只管 224、225；DATA 第 9 节「与本表不是同一张，列不混用」 |
| 模板表 | 不读 `gapfill_policy_eval_template`。只服务可视化的 222 | 一致。DATA 第 9 节 219–222 不读本表，模板表读法留给可视化 |
| 方案表服务面 | 只服务 227–231；不把整条 `jobs`/`shells` 改成只读这张表 | 一致。趋势、分区读各自 gapfill 表，模板读模板表，解读条目、多媒体读壳表，均在 API 第 1 节「留给谁」表点名 |
| 受众反馈 | 不把序号 210 的 `gapfill_policy_audience_feedback` 当方案意见 | 一致。DATA 第 6、9 节点名不复制 |
| 推演边界 | 不调用 `polan.text.simulate`，不读 `ads.policy_simulate`，不挂 `M_POLICY_SIMULATE` | 一致。DATA 第 4、9 节同；省级力度情景不灌进本表 |
| 库边界 | 库只允许 `gkxlumenx_gapfill`，不进 ODS、DWD、ADS，不写供应方库 | 一致。D16 合规 |

### 空态与灌数

| 项 | API 分册写法 | 对数据判定 |
|---|---|---|
| 空态语义 | 五叶无行则空，HTTP 成功，不返回 501；接口不直接返回写死的 mock；mock 只能先由灌数单落入表再被读出 | 一致。符合 D18「可实现才签收」：接口只读表，不返回写死值。DATA 第 1 节同句 |
| 查询不灌数 | 查询请求不灌数 | 一致。DATA 第 1、8 节同句 |
| 灌数归属 | 建表与灌数由 `POL-L2-DS11-PLAN-GAPFILL-L01` 执行，不在本分册 | 一致。灌数单依赖 DATA 与 ARCH，执行人 data-agent，与表定义归属无冲突 |

### 观察（不构成不同意）

| 观察 | 说明 |
|---|---|
| 228 空态措辞差异 | API 第 4 节写「预览空、趋势空」，DATA 第 4 节写「预览、趋势和归档都空」。DATA 更细，把同行的 `archive_text` 一并计入空态；两册不矛盾，实现按 DATA 的全列空口径 |
| ARCH 文件头滞后 | ARCH 稿内状态行仍写「待 human:淮政玮 签收」，注册表已 done。以注册表为准，不影响本页核对 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
