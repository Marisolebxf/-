# ENT-OVERVIEW-E33-E35 handoff

## 状态

- 覆盖项：15
- implemented：10
- verified：1（E-33～E-35 页签级需求追溯）
- manual_review：4（既有 E-33 视觉与交互项）
- planned / blocked：0
- 本次 E-34 增量：1 个页面文件 + 1 个确定性模拟数据文件 + 1 个契约测试 + 交付覆盖记录

## 当前待办

- 用户已授权先编码；任务认领与门 1 登记待后补。
- 浏览器逐态视觉复核和截图待执行。
- 既有 `scripts/check-enterprise-ia.mjs` 在产业服务链菜单断言处失败，与本批写集无关。

## 已完成

- 确认 E-32 与 E-33～35 使用同一 `repos/demo-ui-topic/dev@e287e91` 基线。
- 建立 E-33～35 聚合交付覆盖合同、写集 convoy、验证计划和确定性 Demo 数据策略。
- 识别 14 个覆盖项及现有实现差距。
- 记录 E-34 Logo 与 `Design.md §1.1` 的优先级处理：不展示企业 Logo。
- 已完成共享路由/上下文、E-33、E-34、E-35 首轮实现与窄契约测试。
- `npm run build`、`npm run design:check`、本批静态契约通过；本地三个权威 URL 返回 200。
- 已按双模式归因修正 E-33～35：业务态隐藏 MockBadge、Q 编号和实现说明，评审态保留必要评审证据；两态均不显示原始 mock 批次。
- E-33～35 产品定义和页面统一为“数据时间 / `data_time`”；内部 batch 仅留在交付溯源文件。
- `implementation-coverage.yaml` 已为全部覆盖项补充 `visibility_by_mode` 和非空测试证据路径；双模式截图仍待人工复核。
- 已新增共享 `ReviewOnly` 并让 `MetricCard` 内部自动隔离评审标识；普通中文说明、CMS 来源、禁止项和实现解释不再依赖页面作者逐条手写判断。
- 已新增共享、自门控的 `ReviewTraceHeader / TraceInfoIcon`，E-33～E-35 在评审态显示页签级需求追溯，业务态完整隐藏；专项测试、构建、三页双模式 DOM 和截图证据齐备。
- 企业画像面包屑已按 `sourceTab` 返回 E-33 重点企业概览、E-34 明星企业介绍或 E-35 深圳企业介绍，不再固定回旧“重点对象”。
- E-33 已按四件套 v0.2 方案 A 重构：顶部保留当前产业链；左侧纵向链位只显示名称、企业数、领域数；右侧企业单列分页，整链统计保持不随链位变化，领域证据跟随链位。
- E-33 契约测试、企业总览壳检查、设计检查、生产构建与本地 URL 可达性均通过；由于缺少用户选定浏览器的双模式截图，E-33 四项暂为 `manual_review`。
- E-33 四件套 v0.3 的资质图表定义已落地：标题改为“整链重点企业资质分布”，使用深圳市/广东省/全国完整口径的横向分组条形图、统一绝对数量轴、固定数值标签和零值 `0`；图表只读，不联动当前链位企业列表。
- 本次资质图表增量已完成 TDD 红绿验证、专项页面检查、设计检查、生产构建与本地 URL 可达性检查；双模式截图仍待用户选定浏览器复核，因此 `E33-SCALE-QUALIFICATION` 保持 `manual_review`。
- E-33 图表下方两条统计口径说明与领域证据生成性摘要已按最新批注逐元素归入 `review_only`，页面使用共享 `ReviewOnly` 门控并增加精确回归断言；修正后的双模式截图仍待补充。
- E-34 已按四件套 v0.2 从“固定一家”调整为每产业 `0..N` 家：2 家及以上使用可搜索 Arco Select，按 `sortOrder` 默认第一家，URL 使用 `enterprise_code`，切换后返回首屏；名单条目与基础介绍发布准入已落地。
- E-34 多企业改动已完成 TDD 红绿、设计检查和生产构建；业务态/评审态截图、选择器切换和 URL 恢复仍待用户选定的 in-app browser 复核，因此五项覆盖保持 `manual_review`。

## 后续登记

1. 补充 E-33～35 Demo 实现任务认领；
2. 同步 `ENT-MOD-OVERVIEW-PDR-G1` 实际评审状态；
3. 不复活旧 `ENT-UE-IA-L04`，也不倒填认领时间。

## 预计写集

- `repos/demo-ui-topic/src/app/components/common/ReviewTrace.tsx`
- `repos/demo-ui-topic/src/app/components/common/index.ts`
- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCenterPage.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseCenterRouteMap.ts`
- `repos/demo-ui-topic/src/app/pages/development/KeyEnterprisesPanorama.tsx`
- `repos/demo-ui-topic/src/app/pages/development/StarEnterprises.tsx`
- `repos/demo-ui-topic/src/app/pages/development/ShenzhenEnterprises.tsx`
- `repos/demo-ui-topic/src/app/mock/enterprise/enterpriseList.ts`
- `repos/demo-ui-topic/src/app/mock/enterprise/portalAggregates.ts`
- `repos/demo-ui-topic/scripts/check-enterprise-ia.mjs`
- `repos/demo-ui-topic/tests/enterprise-overview-e33-e35.test.mjs`

## 恢复命令

```bash
cd /Users/ying/Documents/codex/gkx-lumen
sed -n '1,260p' gkx-orchestration/agent-delivery/agent-handoffs/交付覆盖/ENT-OVERVIEW-E33-E35/implementation-coverage.yaml
git -C repos/demo-ui-topic status --short --branch
```

恢复后先读取本目录五个文件并核实门 1 状态；不要重新解释四件套，也不要在未认领实现任务时修改 Demo。
