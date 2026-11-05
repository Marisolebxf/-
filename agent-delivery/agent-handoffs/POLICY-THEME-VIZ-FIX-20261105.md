# POLICY-THEME-VIZ-FIX-20261105 · 政策词云与主题聚类接线修复

日期：2026-11-05。用户要求按产业全景同样的思路排查代码与数据，并沿用主仓 Cursor 规范。
需求依据：`bid-reference/srs/04-科技专题服务系统/科技专题内容运营中心/可视化管理.md` 的主题词云图（行业、区域筛选）及主题聚类图（点击查看条目）。

## 任务与规则

- claimed_by：agent:frontend-agent；用户会话直接授权。
- supervised_by：会话未提供团队实名，不推断代填。
- 本 ID 为交付追踪标识；当前未挂载 task-registry MCP，未直接读写注册表，不宣称已认领或验收。
- ponytail: full。沿用 Vue、Arco、ECharts wordCloud/graph、request 与 Java 门面，不新增依赖。
- 沿用主仓路径真源、团队公约、并行保护、frontend/api/data/algorithm/ponytail 规则及 lumen-ui-topic/AGENTS.md。

## 结论与证据

- 是前端接线缺失，不是数据库缺行：`PolicyNewsDisplayPage.vue` 从未请求 Java `/policy/topic/v1/policy/viz`，真实模式通过 `USE_MOCK` 分支固定显示“主题词频没有接口”“主题聚类没有接口”。
- Java `PolicyVizController`、`PolicyVizServiceImpl` 及 Python `/internal/policy/viz/terms|clusters` 已存在；ECharts wordCloud 插件也已注册。
- 远端只读连接实测使用 `gkxlumenx_gapfill`，现有 `gapfill_policy_viz_terms` 10 行、`gapfill_policy_viz_clusters` 3 个主题共 6 条政策。
- FastAPI TestClient 调用实际注册路由并读远端数据：terms HTTP 200、empty=false、10 项；clusters HTTP 200、empty=false、3 簇。
- 词频更新时间为 2026-11-05 12:36:04。本次没有补数、没有新建表，也不声称既有 gapfill 数据是真实统计或新聚类算法的结果。

## 修改

- API 层补齐既有 Java 聚合接口路径、薄封装与 terms/clusters 类型。
- 真实模式使用接口返回的数据；演示模式仍使用原型 fixture，空数据不回退 fixture。
- 行业、区域选项由返回词频派生，排除缺失标签；保留筛选交集。
- 过滤空词、无效权重、空簇和无标题条目，词云/聚类分别处理空态及后端原因。
- 新增加载失败重试及请求序号保护；点击聚类查看条目，有 policy_id 时可打开已有政策详情抽屉。
- 移除页头“词云/聚类暂无数据”的固定过时说明。
- 只修改政策主题相关 6 个前端文件；没有改重大事件、影响深度、扶持指标的业务实现。

## 验证与限制

- `node --experimental-strip-types src/views/policy/policyNewsDisplay.selfcheck.mjs`：通过。覆盖接口接线、返回数据转换、空值、行业区域筛选、空块及 policy_id 保留。
- `npm run type-check`：通过。
- `npm run build-only`：通过；有既有 bundle 大小提示。
- `git diff --check`：通过。
- Python 实际路由只读验证通过；Java 无代码变化，核对既有 DTO、Feign 与聚合实现，没有声称重新执行 Java 全量测试。
- 本次未完成浏览器视觉复核与线上网关端到端验收；前次会话本机验证 origin 被自动审批拒绝，本次未尝试绕过。

## 架构、设计与交互

- D8：保留原词云及聚类图样式、Arco 筛选与现有布局，无新页面、依赖或设计体系；Design 全量视觉验收未签收。
- D9：仅展示现有接口/补齐表结果，不改指标口径、就绪度或数据来源状态，不新增 mock 或将 gapfill 改为 live。
- D10：保留点击聚类查看条目，复用政策详情抽屉、loading、错误重试与空态；键盘/无障碍全量走查未执行。
- D12：前端 → lumen Java → lumen-algo-py → 既有 gapfill 表，无前端直连 Python、数据库或 demo 服务。
- 可观测：沿用 request 的 trace header 及既有调用链；尚无部署后 trace 抽样。
- 本次不增加算法/模型，不涉及存储 schema、供应方写入或业务口径审批。

## CI/CD

- 前端分支：dev；提交：`540114e`，`[agent:frontend-agent] fix(POLICY-THEME-VIZ-FIX-20261105): connect word cloud and clusters to Java API`。
- 按主仓完工即推要求推送 origin/dev；主仓仅提交本 handoff。
- CI pipeline、镜像 tag 与 K8s rollout：尚未确认；工程检查通过不等于部署完成。
- cost：未获得本任务可核实的 token/费用统计，未臆造字段或写注册表。

## 需规核对与行业中文显示跟进

- 用户要求核对是否必须提供行业/区域筛选，无需规则删除；同时指出行业显示英文编码。
- 核对上述 SRS 源文件第 370 行及总需规第 7571 行，原文均为“支持按行业、区域筛选”。因此保留两项筛选，不增加维度。
- 仅修正文案映射：ic → 集成电路，ai → 人工智能，bio → 生物医药，new-energy → 新能源；下拉 value 和词频记录仍使用原编码，筛选匹配不变。
- 修改限两个前端文件，无后端/数据库变更。已有自检、type-check、build-only 及 diff-check 通过。
- 跟进提交：`7d85c4d`，按规范推送 origin/dev；CI、线上部署及视觉验收尚未确认。
