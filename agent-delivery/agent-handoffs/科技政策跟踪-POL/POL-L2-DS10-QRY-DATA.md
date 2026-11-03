ponytail: off

# POL-L2-DS10-QRY-DATA · 科创政策全景多维检索数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock_until | `2026-11-04T04:10:11.354Z` |
| 说明 | 定义单。只写数据落点。不写 SQL，不写代码，不标 done |

## 范围与实现

科创政策全景 · 二级「多维检索查询」。SRS 序号 197–202，用户故事 `US-DS-POL-01`。数据落点写在 `sdd/l2/POL-L2-DS10-QRY-DATA.md`。依据已签收的 `POL-L2-DS10-QRY-ARCH` 第 2 节和第 7 节、`sdd/调用链与边界.md`、`survey/DS-10.md`。

197、198、200 不在展示侧另读库。统计经 `panorama/stats` 委托专题门面，读 `gkxlumenx_ads` 里派单包 17 已点名的结果：总数和级别分布读 `policy_level_dist`，全国分布读 `policy_national_dist`，深圳分布只读全市合计 `policy_sz_dist`，时序只读年行 `policy_timeseries`。目录和正文读已落库的 `gkxlumenx_dwd.policy_base_info`（国内当前行），经 `search` 与 `docs/{id}`。类型分布的表名 `policy_type_dist`、有效率列都已登记，但第一批 STAT 明确不写；无正式行则空，不造 0。D4 保持 mock。`GDF-POLICY-MOCK-GATE-L01` 仍未解开。

199 不落新表。普通排序留在 `search`。智能排序接通前为 501。

201 是登录用户行为，不是指标。展示侧不建 `display_user_*`。接通后记录落在 `gkxlumen-topic-policy`：历史存检索条件并回放 `search`，收藏存政策 id 并打开 `docs/{id}`。身份沿用 `gkxlumen-upms` / `gkxlumen-auth`。入口未接上是 501；接上且该用户无记录是空列表。

202 的导出对象是当前 `search` 目录。文件若进对象存储，只写桶 `gkx-lumen`：PDF 用 `gkx-user-reports/science/pdf/{用户}/{日期}/`，Excel 用 `gkx-others/policy-panorama-search-export/{日期}/`。库里只存桶名、对象键和下载权限。前端不直连对象存储。

## 偏离

无实现偏离。

`ads.md` 展示窗口把 `M_POLICY_TYPE_DIST` 映到 `policy_type_dist`，把 `M_POLICY_VALIDITY_RATE` 映到 `policy_level_dist` 的有效率列。派单包 17 第 3 节规定这两处不写。本单按 17 和已签收架构消费，不改 `ads.md`，也不为这两条补脚本。

工作区有未签收 SQL（`lumen-svc-platform/db/9x_gkxlumenx_topic_policy.sql`），不作为本单输入。

架构叶写明该叶不加表。本数据叶只定 201、202 的记录内容和存放侧，不产出 DDL，不新开 GDF。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS10-QRY-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-QRY-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml`，未 commit，未 push。

## 验收证据

- 197/198/200 的读表与派单包 17 第一批、`ads.md` 已登记表名对照过。类型分布和有效率按 17 第 3 节写成「不写」。
- 目录读 `gkxlumenx_dwd.policy_base_info`，与 `dwd.md` 及 `POLICY-DDL-CHECK-L04` 的产线 0 行 / demo 20,000 行核对一致。展示链不读 demo。
- 201、202 的落点与架构第 7.2、7.3 节一致：行为记录在专题门面，文件键只落 D14 已有目录。
- 217 与研报 614–618 未写入本二级落点。
- 定义任务，未跑业务 CI，未部署。文档随本次提交进入 `origin/dev`。状态进入 `integration`。会签未完成，不标 done。

## 架构合规自检

- ✅ 调用链：浏览器只打 `/display/v1/policy/**`。197/198/200 由 display 委托 `gkxlumen-topic-policy`，再进 Python `/internal/policy`。展示不直连 Python，不直连库。
- ✅ Java 不写算法、不打分。统计只消费已有 `GDF-POLICY-MDC-STAT-L01` 的落表，不写第二套脚本。
- ✅ 不写 nGQL，不读政策子图，不把 `E-E7-POLICY-M1-L06` 写成展示联调单。
- ✅ D9：不新造 `metric_id`，不改 D4。闸门未开时正式值仍是 mock。无行不造 0。D2 provisional 保留「待核验」。
- ✅ D12：展示链不读 demo 库。未签收门面 SQL 不作为表结构。
- ✅ D14：导出只写桶 `gkx-lumen` 已有目录。库只存桶名、对象键、下载权限。前端不直连对象存储。
- ✅ D16：不用缺口库灌数，不把未写的类型分布和有效率写成已有正式值。
- ✅ 不新开 GDF，不加表，不加字段。201 不建 `display_user_*`。
- ✅ 跨项只写消费边界。217 对标报告和研报 614–618 不进本二级落点。

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.04 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、data-agent 80/20、B 档 `$3/$15` 回填：`8000×0.80×3/1e6 + 8000×0.20×15/1e6 = 0.043`，记 `0.04`。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS10-QRY-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 2 节 |
| 会签态 | 源文件无 frontmatter，记 `draft`。不自填绿 |
| 说明 | 数据落点不替代该图 |
