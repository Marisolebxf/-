# POL-L2-DS11-PLAN-SIGNOFF-ARCH · 政策分析评价 · 推荐方案报告交互展示 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-ARCH`（2026-11-03）。本页不重新设计，不改那份架构
- 监管：`human:淮政玮`
- 对照：说明书第 11 节、第 11.2 节「评价 · 方案 227–231」。`sdd/调用链与边界.md`、`sdd/契约输入清单.md` 只作对照。下游 `POL-L2-DS11-PLAN-API` / `METRIC` / `DATA` 尚未成册，本页不等、不代写
- 范围：SRS 序号 227–231。不把 219–226 改挂进本叶

## 结论

同意会签

五叶都没有方案生成、参数模拟、路径生成或意见采集模型。按说明书第 11 节，落点是新建 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`，由 `POL-L2-DS11-PLAN-GAPFILL-L01` 灌 mock，接口只读。浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连 Python，不直连库。不新造 `metric_id`。219–226 仍留在可视化、解读两份架构，本叶不改挂。

阻断句：无。

## 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 没有模型就建 gapfill 表，接口只读 | 一张表 `gapfill_policy_eval_scheme`，库只允许 `gkxlumenx_gapfill`。种类为方案对照、参数模拟、路径与风险、互动意见。231 不单独占种类，不灌导出文件。查询不灌数，请求不插入意见、不按弹性公式现算。无行则该块空。不直接返回写死的方案、分数、路径、意见或文件 | 一致。对齐说明书第 11 节和第 11.2 节「评价 · 方案」。不进 ODS、DWD、ADS、供应方库 |
| 浏览器只打 `/display/v1/policy/**` | 227–229 用已有 `POST /display/v1/policy/evaluation/jobs`。230–231 用已有 `GET /display/v1/policy/evaluation/shells`。不改打 `/topic/v1/policy`，不打 `/v1/policy/**`，不把 `E-E7-POLICY-M1-L06` 写成展示路径 | 一致。评价页仍是说明书第 6 节的三条资源，不新开第 4 条 |
| display 不直连 Python、不直连库 | 浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → 缺项表。display 不直连库，不直连 Python，不写算法，不写 nGQL。五叶不进 `gkxlumen-topic-async-service`，不加 `policy_scheme`，不调用 `polan.text.simulate` | 一致 |
| 不新造 `metric_id` | 229 的行用已有 `M_POLICY_DS_11_POLICY_EVAL_015`，不改 D4，不改注册表。227、228、230 没有已挂指标，`metric_id` 留空。不挂 `M_POLICY_SIMULATE`，不挂 `M_POLICY_LAYOUT_REC_COUNT` | 一致。015 已在指标分册挂在序号 229，本叶不新注册 |
| 不把 219–226 改挂进来 | 第 2 节写明同一条 `jobs`、`shells` 上的趋势、分区、焦点、摘要、模板、多媒体留给 `POL-L2-DS11-VIZ-ARCH` 与 `POL-L2-DS11-READ-ARCH`。按种类分发。不能把整条资源都改成只读这张方案表。第 6 节点名排除 219–226 | 一致 |

第 7 节写「只加第 8 节这一张表」。第 8 节与第 9 节点的是同一张 `gapfill_policy_eval_scheme`，没有第二张表。这一处节号不影响签收。

调用链第 3 节仍把方案对比、参数模拟、实施路径写在 Job，并写「模型未注册则 501」。本叶按说明书第 11 节改走缺项表只读，资源名仍用已有 `jobs` / `shells`，不建任务行。本页不改写调用链文件。

## 路径与表

| 序号 | 公开路径 | 表 | 是不是 Job |
|---|---|---|---|
| 227 | `POST /display/v1/policy/evaluation/jobs`，种类为方案对照 | `gkxlumenx_gapfill.gapfill_policy_eval_scheme` | 否。同步读，不建任务 |
| 228 | 同上，种类为参数模拟 | 同一张表，按方案和参数档 | 否。换参数是再查一次，不调用推演 |
| 229 | 同上，种类为路径与风险 | 同一张表。`metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015` | 否。不读图，不写 nGQL |
| 230 | `GET /display/v1/policy/evaluation/shells`，种类为互动意见 | 同一张表的意见行 | 否。请求不插入 |
| 231 | 同上，种类为方案报告 | 不另建行。读方案对照行和意见行后生成 | 否。不灌文件，不是研报 Job |

## 铁律

1. 算法只在 Python。本五叶没有新模型。Java 不生成方案，不按弹性公式现算，不写 nGQL。
2. 调用链是浏览器 → `/display/v1/policy/**` → `gkxlumen-display` → `gkxlumen-element`。展示不直连 Python，不直连库，不调用 `demo-*`。
3. 没有模型，就只建这一张 `gapfill_` 表，接口只读。这符合说明书第 11 节。
4. 不新造 `metric_id`。229 沿用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。D4 保持 mock。
5. 219–226 不改挂到这张方案表。`counts` 上的短板条数和机遇条数本叶不读、不改。
6. 不新建桶。231 不写对象存储，不灌导出文件。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。
