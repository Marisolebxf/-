# TS-L2-DS02-ARCH · 科学技术全景后台实现架构

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 架构稿已落本目录。四角色已同意。签收由本轮 coordinator 按监管人指令推进，不在本文件自标 done |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义任务，不写业务代码，不缩文档 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ARCH-SEQ`、`TS-L2-DS02-ARCH-DATA` |
| 图 diff | 改为两张功能图：三个展示功能共用一次读取；已准备好的图供给三个功能，分数表只供给影响力、中心度、路径优先级 |
| 会签态 | 四角色同意（源文件无 frontmatter）。第一轮架构不同意的两处已改入第 2 节 |
| 说明 | 图在 `科学技术全景-DS02/sdd/l2/TS-L2-DS02-ARCH.md` 第 2、3 节 |

## 问题清单

- 定义单已建为 ready。四角色已同意。签收前实现单仍为 backlog。
- `M_TECH_GRAPH_STRUCT` 等已注册口径是 IPC4 或深圳卡位，和 `technology_node_id` 这张图不是同一套点。稿里禁止用那些函数填本页。
- 中台入图的业务点是否已经进 `demo_gkx_chain`，本定义稿没有再查图。空图时页面保持空，不灌种子。

## 修改内容

- 2026-11-05 晚：原稿写成了技术点入图和读图准备。已改成三个功能的架构：展示技术点图谱（17–21）、展示关联实体（22–27）、展示关键路径（28–33）。入图仍只引用第 2 项，不在本篇展开。
- 同日按需规逐叶拆到 `功能拆解.md`，WBS §4.1d 索引。34–40 不建单，41–47 归维护管理。不按 17 叶新开任务。
- 稿在 `agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-ARCH.md`。WBS-05-01c 挂定义单 `TS-L2-DS02-ARCH`。

## 测试结果

- 未改业务仓，未跑构建。
- 指标经 `metric-registry` 的 `metric-get` / `metric-query` 核对，未读 seed YAML。
- 对照了现控制器 `SituationPanoramaController`：当前返回空数组和 `GRAPH_NOT_READY`。

## 范围与实现

对照需规「科学技术全景」序号 17–33。菜单 `/trend/tech-panorama`。调用链与数据流在架构稿第 2、3 节。34–47 不在本页。不新造 `metric_id`，不写 OpenAPI 字段表。

## 偏离

无偏离。入图仍在第 2 项，不在本篇展开。

## 产物清单

- `sdd/l2/TS-L2-DS02-ARCH.md`
- `sdd/l2/会签/TS-L2-DS02-ARCH-SIGNOFF-ARCH.md`
- `sdd/l2/会签/TS-L2-DS02-ARCH-SIGNOFF-ALGO.md`
- `sdd/l2/会签/TS-L2-DS02-ARCH-SIGNOFF-DATA.md`
- `sdd/l2/会签/TS-L2-DS02-ARCH-SIGNOFF-PRODUCT.md`
- 展示 WBS-05-01c

## 验收证据

编排仓无业务 CI。签收核对子智能体结论：同意签收。四角色会签稿已落盘。

## 架构合规自检

1. 算法只在 Python。Java 不在这次请求里算关系。✅
2. 调用链是浏览器 → 网关 `/display/**` → `gkxlumen-display` → `lumen-algo-py` `POST /internal/tech-graph/read` → `demo_gkx_chain`。✅
3. 图空间只读 `demo_gkx_chain`，不写 `gkx_chain` 或 `entan`。✅
4. 可观测沿用 `gkxlumen-display` 与 `lumen-platform-algo-py`，本叶不新加。✅
5. 定义稿无业务 CI。✅
6. D12：不调用 `demo-*`，不经 `gkxlumen-graph`。✅
7. D18：三个数字只读 `ads_technology_panorama_score` 的 mock 行，接口不直接返回写死 mock。✅

## Cost 回填

- actual_tokens: 12000
- model_used: claude-sonnet-4.5
- actual_cost: 0.06
- cost_warn: green
- 会话模型为 Grok 4.7。注册表枚举无此项，按 sonnet 单价与 architect 80/20 计入。

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
