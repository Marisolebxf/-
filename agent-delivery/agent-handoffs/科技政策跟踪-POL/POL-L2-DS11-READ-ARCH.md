# POL-L2-DS11-READ-ARCH · 政策分析评价 · 结果解读报告多维展示

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 只写序号 223–226 的实现架构。2026-11-03 四角色会签同意。未签收，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、读表空态，以及与 219–222、227–231 的边界。

## 范围

政策分析评价 · 二级「结果解读报告多维展示」。只覆盖 SRS 序号 223–226，用户故事 `US-DS-POL-05`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 223 | 热点问题分析看板 | 短板条数同步读 `ads.policy_effect` 的 `region_gap`。焦点走 `policy_focus_ads`，读 `ads.policy_focus` |
| 224 | 分主题分指标互动解读 | 读 `gapfill_policy_eval_shell` 的解读条目。点选只筛选已返回的行 |
| 225 | 多媒体辅助解读 | 同一张缺项表的标题和一句说明。不灌视频文件 |
| 226 | 智能摘要与结论推送 | 只读 `ads.policy_text_parse.summary`。请求里不调用 `parse.run` |

浏览器只打 `/display/v1/policy/**`。223 的短板和 224、225 由 `gkxlumen-element` 查表。223 的焦点和 226 走已有异步管道，再到 Python `/internal/policy/jobs/execute`。接口不写死数。D4 仍是 mock。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-ARCH.md`

## 与相邻叶子的边界

本叶不写 219–222 和 227–231 的流程。

| 序号 | 边界 |
|---|---|
| 219–221 | 趋势、分区、结构关联另叶。本叶不读图 |
| 222 | 模板导出另叶。不灌进 shell |
| 227–231 | 方案与实施路径另叶。`M_POLICY_DS_11_POLICY_EVAL_015` 不挂本叶 |
| 机遇条数 | 无本段序号。`counts` 上的机遇读面不改 |

## 未做事项

- 未写 OpenAPI 字段表、请求体、响应体、枚举。留给 `POL-L2-DS11-READ-API`
- 未新造 `metric_id`，未改 D4，未改 `指标与501.md` 里的 501 列
- 未改 `FE-POL-02A`，未新建前端单，未重开 GDF
- 浏览器未改打 `/topic/v1/policy` 或 `/v1/policy/**`
- 未建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`ads.policy_gap`
- 四角色会签已同意。未标 done

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-READ-ARCH-SEQ` |
| 图 diff | 223 短板与 224/225 走 element 查表；223 焦点 `policy_focus_ads` 调用 `focus.run` 后读 `ads.policy_focus`；226 只读 `ads.policy_text_parse`。禁止边：浏览器改打专题或中台 URL、display 直连 Python、接口直接返回 mock、请求里调用 `parse.run` |
| 会签态 | 2026-11-03 四页同意。源文件无 frontmatter。签收仍由 `human:淮政玮` 做 |
| 说明 | 图在架构稿第 2 节 |

## 范围与实现

见上文「范围」。DoD：架构与流程落在 `sdd/l2/POL-L2-DS11-READ-ARCH.md`。浏览器只打 `/display/v1/policy/**`。

## 偏离

任务说明里的 501（焦点、解读、多媒体、摘要）按说明书第 11 节改成读表。短板仍是同步读面。

说明书第 11.2 节把焦点、摘要、shell 三张缺项表写在一行。焦点已有 `ads.policy_focus` 和 `polan.eval.focus.run`，摘要已有 `ads.policy_text_parse.summary`，这两张缺项表不建。shell 只留给 224、225。

DoD 写「不消费 `/topic/v1/policy`」。浏览器和展示对外 URL 仍只走 `/display/v1/policy/**`。焦点和摘要的内部转发是已有 `POST /topic/v1/analysis/tasks`，不是专题政策查询门面。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-READ-ARCH.md`
- 本 handoff

## 验收证据

架构稿与本 handoff 已落盘。定义单，无业务 PR。四角色会签同意，未签收。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本叶不写算法。焦点沿用已有 `polan.eval.focus.run`，Java 不算指数 |
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。同步走 element，Job 走异步服务再调 `/internal/*` |
| 图谱 | ✅ 本叶不读图，不写 nGQL。关联度不改挂到 223 |
| 可观测 | ✅ 沿既有展示链 trace，不新设计观测点 |
| CI/CD | ✅ 定义文档，未 force |
| D12 | ✅ 不调用 demo 服务。中台页只作对照，不作为展示入口 |
| D9 | ✅ 不新造 metric_id，不改 D4 |
| D14 | ✅ 不写对象存储。多媒体不灌文件 |
| D18 | ✅ 有表的读 ADS。没有算法的只读一张 gapfill 表。接口不直接返回 mock |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、architect 80/20、B 档 `$3/$15` 回填：`8000×0.80×3/1e6 + 8000×0.20×15/1e6 = 0.043`，记 `0.04`。

## 修改内容

- `sdd/l2/POL-L2-DS11-READ-ARCH.md`
- 本 handoff
