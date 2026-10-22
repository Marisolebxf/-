# SYSINT-SCHEME-02-L01 · 系统集成技术方案_对接三要素

> 定义类技术方案。未签收。2026-10-22 晚对端补了 schema 5.11.0，结构与计算方法已到。页面模式未拍板，加工未建，任务仍保持 `in_progress`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:doc-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 沿用现有 `in_progress` 认领。锁 `lock_until=2026-10-22T18:41:47.961Z` 未过期，本会话未再次 `task-claim`，未另开任务 |
| 说明 | 仓 `gkx-orchestration`，分支 `dev`。只改过程文档。未 commit，未 push |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义 / 文档任务。派单禁止用 ponytail 强度行删章节。五段按规约 §6 写齐 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单禁止用 headroom compress 代替精读规约、WBS 和现稿 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-SCHEME-02-SEQ`；`SYSINT-SCHEME-02-FLOW` |
| 图 diff | SEQ：去掉请求线程上的久新参与者，页面请求只到 ADS，返回经网关。FLOW：久新到 Python、Python 到 ADS 为虚线。2026-10-22 晚把虚线标签从「数据结构说明未到」改为「说明已到，加工还没有」。ADS 到 Java 到前端保持实线 |
| 会签态 | `draft`（两图 frontmatter 均为 draft，未自填通过） |
| 说明 | 先改图再改正文。未另画与 `architecture-baseline` 冲突的全局拓扑。图空间切换未改，归第 7 项 |

## 问题清单

- 展示、专题、数据、指标四侧如何对上久新的技术 / 技术链、人才、科研机构。
- 调用方向、鉴权、数据落点、缺数表现、智树不做、双方文档清单能否写死。
- 专题侧开不开实现叶。
- 指标与指标库是否已对齐。

## 修改内容

- 在 `工程过程/04-系统集成/02-对接三要素/技术方案.md` 上改，未另起文件。
- 五段按规约 §6 写齐。没有材料的位置写「还没有」。
- 专题深度模型 3/4/5 写死不开实现叶（scope-baseline §0.2、系统-04、规约 §15 第 11 条）。专题嵌入页没有页面清单，写「还没有」，不建叶。
- WBS-02-00～02-04 与 `WBS.md` 对照。WBS-02-05 底稿没有这一行，只在方案第 4、5 段对照，未改 WBS，未建叶。
- 连接信息只保留已落盘的非密坐标。密码和带口令的连接串未写入。
- 未改 `scope-baseline`，未改已有任务的 `depends_on`、状态、DoD。未 `task-create`。

## 测试结果

- 本会话未再连接 Doris。测通事实只引用 2026-10-22 已落盘记录：`SELECT 1` 成功，`version_comment` 为 `doris-4.1.0-rc03-5960d4cea0e`，库内 130 张表。130 张表不写成已确认结构。
- 未跑业务仓构建。本单不改业务代码。
- 对照检查：方案内无口令、无 `jdbc:` 连接串；两张图 ID 仍在；状态句写明保持 `in_progress`。

## 遗留风险

- 结构与计算方法已到 schema 5.11.0。与指标库逐条对齐还没有，页面模式未拍板，不能送 `ready_to_sign`。
- 融合规则还没有。分析字段里的 `manual>jx>rule` 仍是待确认摘录。
- 11 个态势分析叶与规约「8 页」的菜单对照表还没有。方案不自行合并菜单。
- 过程夹 README 仍是建档时的「三份都未到 / 方案任务未建」。连接坐标以对端 README 和方案 §3.5 为准。本单未改 README。
- 双方约定时点还没有。2026-10-25 只是我方完成日期要求。

## CI/CD（必填）

- 分支：`dev`（本地工作区，未提交）
- commit：无
- pipeline URL / ID：无。本单不改业务仓
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未再探库

## 可观测性（建议）

- 方案写明正式链要三端 trace，本项 trace 还没有。未写新的埋点参数。

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/02-对接三要素/技术方案.md`
- `agent-delivery/agent-handoffs/SYSINT-SCHEME-02-L01.md`

## 架构合规自检

| 项 | 结果 |
|---|---|
| 调用链 前端 → 网关 → Java → Python `/internal/*` | 写在 §2，与时序一致 |
| Java 只读 ADS，不算指标，不写 nGQL，不用久新账号 | 写死 |
| 算法只在 Python，请求线程不扫久新库 | 写死。离线作业还没有 |
| D12：`demo-*` 不进 lumen 调用链 | 写在禁止项 |
| 图空间 | 不改。切换归第 7 项 |
| D9 | 只消费指标库，不在方案里新定义口径。对齐还没有 |
| 范围 | 未改 scope-baseline。专题深度不改成实现 |

## 成本

本会话未计量 token / 美元。不把估算写成 `actual_cost`。未改任务状态。

## 2026-10-22 补充

- 对端给出 [ADS_SCHEMA.md](https://github.com/leonlee723/sz-gkx-data-warehouse-docs/blob/main/ADS_SCHEMA.md) 与版本日志。当日快照在对端目录，schema 5.11.0。
- 方案 §1.4、§3.2 图标签、§4.3、§4.4 已改成「说明已到，加工和逐条对齐还没有」。
- 只读调研另见 `SYSINT-SURVEY-02-L01`，不把调研写成方案已签收。

## 状态

保持 `in_progress`。未写「会签通过」。未改为 `ready_to_sign` 或 `done`。
