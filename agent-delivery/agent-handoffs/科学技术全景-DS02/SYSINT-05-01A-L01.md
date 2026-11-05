# SYSINT-05-01A-L01 · 科学技术全景前端

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | task-get 未返回该字段，不补猜 |
| 说明 | 开工时状态已是 `in_progress`。本轮不改 task-registry，不推进状态 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用已有全景页和 `fetchPanoramaGraph`。未新开接口，未加依赖。未用 YAGNI 跳过 D9：三个数字留 MockBadge 与 ⓘ，D4 不改绿 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ARCH-SEQ`、`TS-L2-DS02-SDD-SEQ` |
| 图 diff | 本叶未改图。页面按这两张时序，只打已有 `POST /display/v1/situation/panorama/graph` |
| 会签态 | 源文件无 frontmatter。功能架构与说明书已签收。本叶代码未提交，等孔东确认 |
| 说明 | 调用链仍是全景页 → 网关 `/display/**` → `gkxlumen-display`。浏览器不打 Python，不打算法中台 |

## 修改内容

- `USE_MOCK=false` 时，图谱、关联实体、关键路径只消费这一次 `graph` 的七个字段。列表不再调用 `getGraphListRecords` 的种子名单。右侧分析不再落入 `interactionState` 里的鹏城实验室等种子上下文。
- 读图改为 `post`。成功且没有节点时，`GRAPH_NOT_READY` 收成 `GRAPH_EMPTY`。请求抛错时不把空壳当成成功，也不把种子节点画上去；已有的一次成功结果留在页面上，并提示读取失败。
- 领域、关键词、选中技术点会再次调用同一个 `graph`。`currentYear` 固定为 `null`，不作为第二套快照的入参。
- 画布只留技术点和技术点之间的边。实体只留人、机构、论文、专利。实体和实体之间的网保持空。
- 导入、手动添加、撤销仍只改本次浏览。提示写明服务端不接收写入（501），未落库。
- 影响力 `M_TECH_ENTITY_INFLUENCE`、中心度 `M_TECH_PATH_CENTRALITY`、路径优先级 `M_TECH_PATH_PRIORITY` 旁留 ⓘ 和 MockBadge。没有分数的格子空着。统计条数旁有来源说明。D4 未改成 live。
- `USE_MOCK=true` 时筛选条、三视图、右侧分析、详情抽屉仍走原来的冻结种子。

## 测试结果

- `pnpm type-check`（`vue-tsc --build`）退出码 0。改完列表过滤后又跑了一次，仍是 0。
- `node src/lib/graph/liveGraph.selfcheck.mjs` 通过。覆盖空图 `GRAPH_EMPTY`、不补 `robot`、技术点边、实体类型、序号 26 的实体边不进名单、无优先级不进重要性档、`currentYear === null`。
- `node src/lib/graph/selfcheck.mjs` 通过（FE-TS-02A 原纯函数自检）。
- 未跑浏览器。未跑 CI。

## 遗留风险

- 展示 Java 已在 `cbd6f10` 改调读图。镜像未发布前，页面打开仍可能是空图或读失败，不会回退种子。
- 三个数字要等 `TS-L2-DS02-SCORE-L01` 把行灌进 `ads_technology_panorama_score`，并由同一次 `graph` 带回。现在格子是空的，MockBadge 还在。
- 导入和手动添加没有发写请求。页面按说明书把结果说成 501、未落库。

## CI/CD（必填）

- 分支：`lumen-ui-science-pc` 的 `dev`
- commit：`e6fb1dd`。淮政玮 2026-11-05 下令收口后推 `origin/dev`。原监管人是孔东
- pipeline URL / ID：已 push。本会话未等 Pipeline
- 部署 namespace / 镜像 tag：未核
- K8s rollout：未核
- dev 测试 URL / 命令与结果：本地 `pnpm type-check` 与两条 node 自检通过

## 可观测性（建议）

- 读图仍走 `@/utils/request` 的 `post`，trace 头沿用现有拦截器
- 本轮没有线上 traceId

## 涉及文件

- `repos/lumen-ui-science-pc/src/lib/graph/liveGraph.ts`（新）
- `repos/lumen-ui-science-pc/src/lib/graph/liveGraph.selfcheck.mjs`（新）
- `repos/lumen-ui-science-pc/src/api/situation/panorama.ts`
- `repos/lumen-ui-science-pc/src/types/panorama.ts`
- `repos/lumen-ui-science-pc/src/views/situation/panorama/index.vue`
- `repos/lumen-ui-science-pc/src/views/situation/panorama/components/GraphListSection.vue`
- `repos/lumen-ui-science-pc/src/views/situation/panorama/components/GraphAnalysisPanel.vue`
## 范围与实现

对照说明书第 6 节。菜单 `/trend/tech-panorama`。只打已有 `POST /display/v1/situation/panorama/graph`，不另接查图接口。未承诺的块保持空。

## 偏离

无偏离。`USE_MOCK=true` 仍保留冻结种子，供开关打开时用。

## 产物清单

- `lumen-ui-science-pc` `e6fb1dd`
- 本交接

## 验收证据

`pnpm type-check` 退出码 0。`node src/lib/graph/liveGraph.selfcheck.mjs` 与 `node src/lib/graph/selfcheck.mjs` 通过。

## 架构合规自检

1. 浏览器只打 Java `graph`，不直连 Python。✅
2. 不调用 `demo-*`。✅
3. `USE_MOCK=false` 不用种子填数。✅
4. 空图 `GRAPH_EMPTY`，读失败不画种子。✅
5. 三个数字留 MockBadge，D4 不改 live。✅
6. 不新造 `metric_id`。✅
7. 序号 17、26 不落库。✅

## Cost 回填

- actual_tokens: 80000
- model_used: claude-sonnet-4.5
- actual_cost: 0.43
- cost_warn: green
- 会话模型为 Grok 4.7。注册表枚举无此项，按 sonnet 单价与 frontend 80/20 计入。
