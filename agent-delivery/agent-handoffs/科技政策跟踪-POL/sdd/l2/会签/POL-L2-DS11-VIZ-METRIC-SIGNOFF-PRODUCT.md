# POL-L2-DS11-VIZ-METRIC-SIGNOFF-PRODUCT · 政策分析评价 · 政策分析报告可视化呈现 · 指标分册产品会签

- 任务：`POL-L2-DS11-VIZ-METRIC`（本页为产品角色会签页，不改分册本体）
- 角色：`agent:product-agent`（监管 `human:淮政玮`）
- 日期：2026-11-03
- 会签对象：`sdd/l2/POL-L2-DS11-VIZ-METRIC.md`（2026-11-03 版）
- 核对基准：需规序号 219–222；`POL-L2-DS11-VIZ-ARCH.md` 读面；`sdd/指标与501.md` 评价表 219–222 行判定

## 结论

**同意会签。**

## 核对表

产品核对重点：需规四叶（219–222）都有明确读面落点，且没有被别的叶子占用。

| 序号 | 读面落点 | 是否专属（未被其他叶子占用） | 判定 |
|---|---|---|---|
| 219 多维指标趋势图 | `gkxlumenx_gapfill.gapfill_policy_eval_trend`，经 `jobs kind=趋势` 只读 | 专属表，仅服务 219；全景时序 `M_POLICY_TIMESERIES`、效果分 `M_POLICY_EFFECT_SCORE`、落地实效 `M_POLICY_IMPLEMENTATION_EFFECT` 均点名不挂（第 5.1、7 节） | ✅ 有落点，无占用 |
| 220 分区/群体对比分析图 | `gapfill_policy_eval_partition`，经 `jobs kind=分区` 只读 | 专属表，仅服务 220；全景分布 `M_POLICY_NATIONAL_DIST` / `M_POLICY_TYPE_DIST` / `M_POLICY_LEVEL_DIST` 点名不挂（第 5.2、7 节） | ✅ 有落点，无占用 |
| 221 多维结构关联图 | 第 7 项已有政策子图，跨项只消费，不建表 | 跨项索引判定不改；`M_POLICY_GRAPH_107_1`（留全景 208）、`M_POLICY_RELATION_DEGREE`（留推演 240）点名不挂；不新开资源（第 6 节） | ✅ 落点为消费既有子图，可空，无占用 |
| 222 报告模板定制与批量导出 | `gapfill_policy_eval_template`，经 `shells kind=模板选用` 只读 | 专属表，仅服务 222；解读壳表 `gapfill_policy_eval_shell` 只服务 224、225，本叶不读不写（第 5.3、7 节） | ✅ 有落点，无占用 |

| 核对项 | 分册处理 | 判定 |
|---|---|---|
| 需规四叶读面齐备 | 219/220/222 各有一张缺项表，221 消费既有子图，四叶无悬空 | ✅ |
| 读面不被其他叶子占用 | 每张表单一序号服务；点名排除表覆盖全景、推演、解读、方案全部相邻叶子 | ✅ |
| 不新造 metric_id、不改 D4 | 本二级挂接 0 条；缺项行上名称（指标名/对象/投向/模板名）明确不是注册号 | ✅ |
| 不把 501 当画面 | 有行读表、无行则空，`指标与501.md` 判定原文不改字 | ✅ |
| 异步白名单不混用 | 第 5.6 节核对 `PolicyAnalysisTypes` 九键，趋势/分区/导出不入白名单，不借 `policy_timeseries`、`policy_regional` | ✅ |
| 诚实性 | 行是灌入 mock，D4 仍 mock，不写成已上线 | ✅ |

## 观察与偏离

无。分册未见 metric MCP 的声明与「不补身份字段」的处理一致，未查不填，诚实。

## 范围声明

- 本页只核读面落点与占用关系；八件套身份、D1–D4 细节以指标注册表与 data-agent 正式化为准，本页不代查、不代填。
- 本页不替甲方拍板，无新增业务口径。

---

本页不把任务标 done，签收仍由 `human:淮政玮` 做。
