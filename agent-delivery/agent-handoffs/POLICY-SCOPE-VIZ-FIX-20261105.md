# POLICY-SCOPE-VIZ-FIX-20261105 · 恢复政策影响范围区域分布

日期：2026-11-05。用户反馈影响深度接通后，原有影响范围柱状图变为空态。

## 授权、规则与范围

- claimed_by：agent:frontend-agent；本会话用户直接授权。supervised_by 未提供，不推断代填。
- ponytail: full。按主仓路径真源、并行保护、前端规约和完工即推执行，无新增依赖。
- 当前未挂载 task-registry MCP，本 ID 为交付追踪标识，不直接读写注册表或伪造认领/验收状态。
- 需求来源：`bid-reference/srs/04-科技专题服务系统/科技专题内容运营中心/可视化管理.md`，政策新闻影响可视化，影响范围允许地图或柱状图。

## 根因与现网证据

- 数据未丢失：只读查询 `demo_gkxlumenx_ads.policy_national_dist`，仍有省份分布，北京市 2268、上海市 1842、广东省 1612。
- 修复前图表与扶持指标共用 `policyIndicators({kind:'all'})`，依赖聚合请求全部成功；前端仅捕获 HTTP 异常，没有将 HTTP 200 的业务降级识别成加载失败。
- 实测项目配置的现网 Java 网关：`GET /policy/topic/v1/policy/indicators?kind=all` 返回 HTTP 200、code=0，但 `national=[]`、`degraded=true`、`honesty.error=true`、`honesty.engine=unavailable:feign`，耗时 6.26 秒。
- 同一网关 `kind=national` 返回 HTTP 200、code=0、`items` 31 行，耗时 0.53 秒。Java 对单维度结果解包成 `items`，并非 `national`。
- Python 直查也确认 national 有 31 行；本机对同一数据库测得 kind=national 0.97 秒、kind=all 23.11 秒。Java Feign 读超时配置为 30 秒；当前现网仅能确认 Feign 请求失败，未取得下游堆栈，不将超时推断写成已证实根因。

## 修复

- 影响范围独立请求既有 `kind=national`，与扶持指标的 kind=all 状态分离，不提高超时或填充演示数。
- 区域分布解析兼容 `national` 与 Java 单维度 `items` 两种实际返回结构；显式 national 空数组不回退其他集合。
- 保留有效 0 值，缺失数值不补零；原 fabricated 保护保留。
- 对 HTTP 200 的 degraded、honesty.error/degraded、unavailable 引擎识别为加载失败，显示客户可读错误与独立重试，不再伪装“暂无数据”。
- 影响深度、词云、聚类与扶持指标口径保持原有实现；本次不修复聚合接口下游本身，不声称其已恢复。

## 验证

- 现网 kind=national 31 行、kind=all 降级响应的只读对照均完成。
- `node --experimental-strip-types src/views/policy/policyNewsDisplay.selfcheck.mjs`：通过；覆盖两种响应契约、零值、缺失值、显式空数组与 fabricated 保护，并检查独立请求及错误空态分支。
- `npm run type-check`、`npm run build-only`：通过。
- `git diff --check`：通过。
- 无写库、无新增 mock、无 schema 或 Java/Python 代码变更。

## 提交与验收边界

- 前端提交 `4467a8b`，已推送 origin/dev，工作区干净；主仓提交本 handoff。
- 现网接口只读验证不等于新前端已部署；CI pipeline、镜像、K8s rollout 和浏览器视觉验收尚未确认。
- D8/D10：保留现有 Arco、ECharts 柱状图和页面布局；无新交互维度。
- D9：沿用现有数据与来源，不修改指标定义或就绪度；政策发布分布不宣称为单项政策的因果影响范围。
- D12 与可观测：前端仍经 Java 网关调用，沿用 request trace；未新增 demo 服务回落或数据库直连。
- cost：无可核实 token/费用信息，不臆造或写注册表。
