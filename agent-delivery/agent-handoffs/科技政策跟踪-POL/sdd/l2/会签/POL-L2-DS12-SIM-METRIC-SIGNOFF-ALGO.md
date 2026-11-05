# POL-L2-DS12-SIM-METRIC-SIGNOFF-ALGO · 政策效果推演 · 科技政策推演 · 后台指标设计 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-METRIC.md`（2026-11-05。本页不改它）
- 对照：`sdd/l2/POL-L2-DS12-SIM-ARCH.md`（含 2026-11-05 第 7、9 节）；`lumen-algo-py/vendor/entan-py` 的 `polan/text/parse.py`、`conf/cfg_model_registry.yaml` 的 `POLICY_TEXT_PARSE`、`POLICY_SIMULATE`、`POLICY_LAYOUT`、`POLICY_FOCUS`、`POLICY_RE`。判定引自 `sdd/指标与501.md` §3
- 监管：`human:淮政玮`
- 强度：ponytail off
- 范围：SRS 237–242。只读核对。不改分册，不改 Python 或 Java，不改模型注册表，不动 task-registry

## 结论

同意会签。

## 核对

2026-11-05 检索动态工具时，MCP 命名空间 `metric-registry` 未加载，未能调用 `metric-get`。指标身份只取 `指标与501.md`。分册写明未见 metric MCP，未调用 `metric-get` / `metric-query`，回退 `sdd/指标与501.md` §3。未读 seed、矩阵 YAML。不编 D1–D3，也不补 501 表上没有的口径、公式、源表、源系统、更新频率和版本。注册表与函数不一致只记观察，不要求本页改注册表。MCP 不可用且分册已写明回退，不据此否决。

`polan.text.parse.run` 从 `dwd.policy_base_info` 取 `is_deleted=0` 的政策，用规则写出摘要、结构化要素和自动标签，然后 `truncate` 整张 `ads.policy_text_parse` 再插入。摘要取 abstract，空则取 content，并截断。结构化要素写入政策类型、级别、区域、发布年、要点；源对象里已有的适用对象、支持方式、申报条件会抄进同一结构。自动标签来自关键词、政策类型、主题。每一行的 `metric_id` 固定为字面量 `M_POLICY_TEXT_PARSE`。函数不写推演曲线，不写重点项、影响对象、路径环节、解读段落，插入行里也没有 `M_POLICY_SIMULATE`。分册第 3 节与这段代码相符。分册不把这套截取收成 237 的公式，也不在展示请求里调用 `run()`。

`POLICY_TEXT_PARSE` 的 `metric_ids` 同时列 `M_POLICY_TEXT_PARSE` 与 `M_POLICY_DS_11_POLICY_EVAL_012`，`handler_module` 为 `polan.text.parse`，`ext.ads_table` 为 `ads.policy_text_parse`，`status` 为 active，并有 `invoke_path`，`ext.is_mock` 为 true。`parse.run` 只写 `M_POLICY_TEXT_PARSE`。012 属于评价 226。分册不改注册表，不把 active 写成 237 已在请求里真算，不把 `ext.is_mock` 当成 metric MCP 的 D4。D4 只转述 `指标与501` 237 行的 mock。

`POLICY_SIMULATE` 同时列 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`，`ads_table` 为 `ads.policy_simulate`。`指标与501` §3.1 该号为 MODEL、D4=`mock`、判定 501；§3.2 把它挂在 232–234。分册只认、不挂。237–242 的行不写这个号，不读 `ads.policy_simulate`，不调用 `polan.text.simulate.run`。

`POLICY_LAYOUT` 只挂 `M_POLICY_LAYOUT_REC_COUNT`。`指标与501` §3.1 把它标成 STAT、D4=`mock`、跨项索引，并写明需规引用过展示序号 241，该引用不改变分键。`M_POLICY_DS_11_POLICY_EVAL_015` 在 229 为 GRAPH、D4=`mock`、判定 501。241 行写明布局建议条数与 015 都不顶替。分册 241 的行上 `metric_id` 留空，不挂这两条，并写明 241 不顶替 229、229 也不顶替 241。

| 序号 | metric_id | 代码 | 指标稿 |
|---|---|---|---|
| 237 | `M_POLICY_TEXT_PARSE`。MODEL。D4=`mock`。判定 501 | `parse.run` 清空整表后写入，行上只有这一条 `metric_id`。截取规则留在函数里 | 不新注册。行上保持原号。展示读已有解析行。请求不调用 `parse.run`。不把截取规则收成公式。不灌缺项文本解析行。不挂 012 |
| 238 | 未见。判定 501。不挂 `M_POLICY_FOCUS_INDEX`，不挂 `M_POLICY_SIMULATE` | 未见重点可视化函数。`POLICY_FOCUS` 挂焦点指数 | 不新注册。重点行上 `metric_id` 留空。读 `gapfill_policy_sim_result` 的重点行 |
| 239 | 未见。判定 501。不挂 `M_POLICY_SIMULATE` | 推演注册项不写影响范围 | 不新注册。影响范围行上 `metric_id` 留空。读同一张缺项表。不改成可接统计读面 |
| 240 | `M_POLICY_RELATION_DEGREE`。GRAPH。D4=`mock`。判定跨项索引 | `POLICY_RE` 与 `POLICY_FOCUS` 都列了该号。分册不调用这两条 `invoke_path` | 不另造独立号。不设种类、不设资源。纸面号留在第 7 项。不改 D4 |
| 241 | 未见。判定 501。不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DS_11_POLICY_EVAL_015`，不挂 `M_POLICY_SIMULATE` | `POLICY_LAYOUT` 只挂布局建议条数。015 列在 `POLICY_SIMULATE` 下 | 不新注册。路径环节行上 `metric_id` 留空。布局推荐与 015 都不顶替 |
| 242 | 未见。判定 501。不挂 `M_POLICY_SIMULATE` | 未见解读报告函数 | 不新注册。解读段落行上 `metric_id` 留空。页面呈现正文。不产生文件 |

238、239、241、242 没有专属 `metric_id`，没有可改的 D4。分册不补号，不把 237 的号指进这四叶。缺项行仍是 mock，不写成已上线。

501 §3.2 仍把 237、238、239、241、242 记为 501，把 240 记为跨项索引。§8 把 237–239、241、242 的真路径写成「501，页面空态」，并写明解析行 237 同此。分册不改 `指标与501.md`，不把 501 改成可接统计读面，不把 240 改出跨项索引。读面沿架构：237 读已有解析表，238、239、241、242 读缺项表，有行则读表，无行则该区空。

观察（不构成不同意，也不要求改注册表）：

- `POLICY_TEXT_PARSE` 把 012 与 `M_POLICY_TEXT_PARSE` 并列。`parse.run` 只写后者。237 不挂 012，不改注册表。
- `POLICY_SIMULATE` 把 015 与 `M_POLICY_SIMULATE` 并列。本叶不调用该函数，不把 015 挂到 241，也不把 `M_POLICY_SIMULATE` 挂到 237–242。
- `POLICY_FOCUS` 同时列 `M_POLICY_FOCUS_INDEX` 与 `M_POLICY_RELATION_DEGREE`。238 不挂焦点指数。240 不调用 `focus` 或 `POLICY_RE` 的路径。
- `M_POLICY_DEEP_171_1` 在 §3.1 为 MODEL、D4=`mock`、跨项索引。分册不把它挂进 237–242。

未发现分册新注册指标，未发现改 D4，未发现把截取规则收成 237 的公式，未发现把 `M_POLICY_SIMULATE` 挂到 237–242，未发现用布局推荐或 015 顶替 241。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。不改指标稿，不改架构稿，不改算法代码，不改模型注册表。
