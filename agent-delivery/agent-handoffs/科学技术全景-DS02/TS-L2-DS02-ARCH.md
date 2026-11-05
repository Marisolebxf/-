# TS-L2-DS02-ARCH · 科学技术全景后台实现架构

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | 未认领。定义单已建，状态 ready |
| supervised_by | `human:淮政玮` |
| claim_type | 未认领 |
| 说明 | 架构稿已落本目录。会签未做，不推待签收，不标 done |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义任务，不写业务代码，不缩文档 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ARCH-SEQ`、`TS-L2-DS02-ARCH-DATA` |
| 图 diff | 新增两张：展示页调用链；久新 ADS → 中台入图 → `demo_gkx_chain` → 只读装配。分数表单独进 display，不进图 |
| 会签态 | `draft`（源文件无 frontmatter） |
| 说明 | 图在 `科学技术全景-DS02/sdd/l2/TS-L2-DS02-ARCH.md` 第 2、3 节 |

## 问题清单

- 定义单已建为 ready。会签未做，不能推到待签收。
- `M_TECH_GRAPH_STRUCT` 等已注册口径是 IPC4 或深圳卡位，和 `technology_node_id` 这张图不是同一套点。稿里禁止用那些函数填本页。
- 中台入图的业务点是否已经进 `demo_gkx_chain`，本定义稿没有再查图。空图时页面保持空，不灌种子。

## 修改内容

- 架构稿从 `科技发展态势-TS/sdd/l2/` 挪到 `agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-ARCH.md`。菜单 `/trend/tech-panorama`，序号 17–33。图和路径真读，影响力 / 中心度 / 路径优先级走 D18 表。34–47 属于维护管理 `/trend/tech-situation-maintain`，不写进本页。
- 展示系统集成 WBS 新增 WBS-05-01c，挂定义单 `TS-L2-DS02-ARCH`。

## 测试结果

- 未改业务仓，未跑构建。
- 指标经 `metric-registry` 的 `metric-get` / `metric-query` 核对，未读 seed YAML。
- 对照了现控制器 `SituationPanoramaController`：当前返回空数组和 `GRAPH_NOT_READY`。

## 遗留风险

- 分数表三个 `metric_id` 的注册口径仍是 IPC4 / 深圳卡位。mock 行不能被说成那些函数的结果。公式未由唐绍祖按技术点另签。
- 一次读取有 200 条边、每类实体 20 条、路径 20 条的上限。全量边不在这一次接口里。
- 产业过滤依赖挂产业表里已经写上的产业节点。没挂上则按领域筛选为空。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`
- commit：见本次提交
- pipeline URL / ID：编排仓无业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：无。本叶不写代码
- dev 测试 URL / 命令与结果：未调用全景接口

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 `gkxlumen-display` 与 `lumen-platform-algo-py`，本叶不新加
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-ARCH.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-ARCH.md`
- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/WBS.md`
