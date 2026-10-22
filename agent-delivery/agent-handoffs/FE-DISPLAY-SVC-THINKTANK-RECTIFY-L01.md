# FE-DISPLAY-SVC-THINKTANK-RECTIFY-L01 · 展示系统-科技服务全景-智库服务 demo 页按需规 566-574 整改

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 孔东派工并自领监管。MCP `task-claim` 未回传 `claim_type`，按本人认领记 `pull`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 沿用 demo 现有 Ant Design 页和详情抽屉，不新依赖。需规五类模块、筛选、详情、动态条和来源标注都保留。 |

## Headroom（可选）

| 字段 | 值 |
|-----|-----|
| headroom | `skip` |
| 说明 | 本叶是 demo 页整改，未走 Headroom 代理。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本叶只改 demo 展示页，不改架构图、存储流图或接口契约图。 |
| 会签态 | 不适用 |
| 说明 | 展示侧五个对象的接口仍待后续单承接；本叶用样例数据把页面功能补齐。 |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md |
| 范围边界 | 需规 `智库服务.md` 序号 566–574 |

## 问题清单

- 服务类型正式用词仍是运营临时目录（政策研究、战略咨询、评估评价、人才培训、学术交流），待甲方确认。
- 供方七种分析方法只在服务类型页说明，不进入服务类型目录。
- 活动地点、内容、媒体文件、供方专家详情页地址，样例中空位显示「待补齐」。
- 活动详情不放问卷统计。需规没有这项。

## 修改内容

### 第一轮（已推送 `1485e31`）

- `ThinkTankService.jsx`：五个页签、动态条、筛选放在四个总数下面。成果、案例、建议用饼图，服务类型和主题用分组柱，时间用多折线。活动历程按时间排列。去掉与分项列表重复的服务记录、成果归属，以及问卷统计。
- `mockData.js`：成果样例标明统计归类。案例、建议、成果分开；政策建议案例同时计入案例和建议。
- `thinkTankModel.js`：时间标签、分层是否齐备、摘要、三层归类、多维计数、活动按时间正序。
- `style.css`：来源标、动态条、统计区、分层和活动历程。

### 第二轮（本地整改，监管人孔东 2026-10-22 走查通过，本轮提交）

- 顶部四项 KPI（总成果数/总投资额/平均回报率/客户满意度）移除：属 03-新型高端智库系统需规，不在本页 566-574 范围。
- 详情抽屉清洗想象字段（投资额、回报率、满意度、浏览/下载量、评分、报告大纲），只留 SRS 与第三方目录真实字段（完成单位、发布日期、研究方向、论文数、被引数、H指数、服务类别）+ 规范主题/时间标注与溯源。
- 页签卡片列表分页：单页 10 条、最多两行高，总数 ≤10 不显示分页。
- 布局修复：列表容器类名由 `.tt-card-page` 改 `.tt-card-scroll`，规避 demo 外壳全局选择器 `[class$="-page"]` 的 72px 左缩进；`overflow-x: hidden` 消除 gutter 负边距横向滚动。
- 智库活动时间历程：100% 宽、支持横向滑动。
- 视觉统一（走查终稿）：时间轴条目去掉四色背景，白底 `#fff` + 边框 `#e5e6eb`，hover 边框 `#165dff`；页签内全部列表卡片（`.ts-service-type-card` / `.ts-report-card` / `.ts-expert-card` / `.tt-click-card`）一律白底 `#fff !important`，无彩色/半透明背景。

## 测试结果

- `node src/pages/tech-service/thinkTankModel.js`：通过（`thinkTankModel ok`）。
- 浏览器 `http://127.0.0.1:4176/#/topic/智库服务`：
  - 全部标签下成果 1、案例 2、建议 2；服务类型表为政策研究 0/1/2、战略咨询 0/1/0、评估评价 1/0/0。
  - 点时间标签 2026-10 后，计数变为成果 0、案例 1、建议 2，活动历程只剩 10 月 8 日的年度研讨，投资汇总为 80 / 12.0 / 95.0。
  - 分页：列表卡片单页 10 条、两行封顶，总数 ≤10 无分页控件。
  - 12:18 CDP 实测：时间轴 3 条目 `background: rgb(255,255,255)`、边框 `rgb(229,230,235)`；页签卡片计算背景全部 `rgb(255,255,255)`。无 72px 左缩进、无横向滚动条。
  - 赵丽娟缺时间标签，全部时间下不进入分层。年度研讨详情含系统摘要、主题标签、时间标签和溯源。活动详情不再放问卷统计。

## 遗留风险

- 数字和正文是演示样例，不是 Z-01～Z-03 实接。
- 服务类型卡片上的关联数是全量档案计数，不随主题和时间筛选变化；列表本身随筛选变化。
- 顶部 KPI 与详情扩展字段若后续归入 03-高端智库页，需在该页重新实现，不在本叶范围。

## CI/CD（必填）

- 分支：`demo-ui-science` `dev`；`gkx-orchestration` `dev`
- commit：
  - `demo-ui-science` `ad51a5e` fix(display): 智库服务页走查整改——去 KPI、字段清洗、分页与白底统一 [agent:frontend-agent]（已推 `origin/dev`）
  - `gkx-orchestration` 本 handoff commit docs: 智库整改 L01 handoff 更新 [agent:frontend-agent]
- pipeline URL / ID：demo-ui-science push dev 后 CI 自动触发（镜像 + NodePort 发布）
- 部署 namespace / 镜像 tag：以 CI 产物为准
- K8s rollout：CI 绿后自动
- dev 测试 URL / 命令与结果：本地 `npm run dev` → `http://127.0.0.1:4176/#/topic/智库服务`，见测试结果；静态站 https://skxrules.unicomcn.tech:30999/ 跟踪 dev

## 可观测性（建议）

- OTEL_SERVICE_NAME：无（demo 静态页）
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `repos/demo-ui-science/src/pages/tech-service/ThinkTankService.jsx`
- `repos/demo-ui-science/src/pages/tech-service/mockData.js`
- `repos/demo-ui-science/src/pages/tech-service/thinkTankModel.js`
- `repos/demo-ui-science/src/pages/tech-service/style.css`
- `gkx-orchestration/agent-delivery/agent-handoffs/FE-DISPLAY-SVC-THINKTANK-RECTIFY-L01.md`
