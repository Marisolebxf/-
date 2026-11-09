# LUMEN-POLICY-SZ3D-FE-SRS-R20261107 · 深圳政策现状指标体系与需规 116 仪表盘

> 只改 `policy_sz_3d`（`/policy/recommendation`）。交互对照 demo-ui-topic 后在 Vue 重写。未 merge demo 代码，未调用 demo 服务。时序页、区域对比页的评价维度勾选未改。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人给定原型截图与 demo 对照文件。改动停在 `lumen-ui-topic` 分支 `dev` 工作区。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 沿用页内 `selected_indicators` / `weights`、Arco 勾选与数字步进、仓内 ECharts 柱状图、评审层 ⓘ / MockBadge / PendingBadge。不加 npm 包。等权与就绪判断放在可被 node 自检导入的 `policySzModel.mjs`。未用 YAGNI 跳过 D9 角标、指标卡和创建请求字段。 |

## 修改内容

- 配置区去掉三张固定说明卡。深圳现状改为「指标体系构建」：顶栏在三维都至少勾选 1 项且一级权重合计 100 时显示「已入模 N 项核心指标，一级权重 100%，可开始分析」；未齐时不能开始。
- 说明文案：三维框架固定，勾选核心指标入模；维内等权自动均分；行内调节一级权重。按钮为「一键均分」「恢复默认模型」。
- 默认勾选 8 项。支持力度 3/4：政策数量、资金规模、创新激励；政策层级覆盖面未入模。产业适配性 3/3：政策-产业需求匹配、产业链覆盖广度、细分领域命中率。落地实效性 2/3：落地执行率、受益覆盖广度；反馈满意度未入模。落地实效三维标 Mock 缺口。
- 一级权重默认 34/33/33。一键均分只把三个一级权重分成整数且合计 100（34/33/33），不改勾选。恢复默认模型回到上述勾选和 34/33/33。
- 维内等权按整数百分比均分，余数补给目录顺序靠前的项。3 项为 34/33/33，2 项各 50。空选择返回空对象，创建请求里该维是空数组，不写成 0 分；该维显示未入模。
- 勾选用 `a-checkbox`，一级权重用 `a-input-number` `mode="button"`，高度 32px。三张一级卡保留 MetricSpecCard。QPOL-02 的 PendingBadge 挂在一级权重上。Mock 缺口同时用常显 `a-tag` 和评审层 MockBadge。配置区不展示 84/88 等写死分数。
- 行末绿色文字按钮按 demo 源码为「查看」，打开该维已入模指标和等权百分比，不展示分数。
- 深圳创建请求和指纹写入 `weights` 与 `selected_indicators`，支持力度、产业适配性、落地实效性三组都带上。时序和区域对比仍用历史权重 34/33/33 和三组空数组。
- 产业路径提交带当前产业名称和 `industry_vid`。技术领域路径仍是 `scope_kind=industry`，`industry_codes` 为关联产业，`industry_name` 用顿号连接，不进对比篮。
- 结果板和报告：档位、落地实效在可算且分数非 0 时显示分数；null 或 0 仍显示不可算。
- 结果页增加「深圳政策指标仪表盘」。支持力度、产业适配性、落地实效只用接口分数；没有分数的维写不可算。有分数的维里最高为优势、严格更低的为短板。柱状图用仓内 ECharts，空分不画成 0，不出综合分、仪表盘、雷达。优化建议仍只渲染接口 `strategies`。

## 测试结果

- `node src/views/policy/policyShenzhen.selfcheck.mjs`：通过。覆盖默认 8 项、34/33/33、两项各 50、空选择、就绪判断、空分不进优势短板，以及页面/结果板/报告文案分支。
- `node src/views/policy/policyConfig.selfcheck.mjs`：通过。深圳配置根上仍保留 `policy-sz3d-fixed-cards`；页面没有 `resetSzModel`。
- `pnpm type-check` 未能启动：当前 pnpm 把无 `packages` 字段的 `pnpm-workspace.yaml` 当成空工作区，报 `packages field missing or empty`。未改该文件，也未改 `package.json`。
- 直接执行与 type-check 脚本相同的 `.\node_modules\.bin\vue-tsc.cmd --build`：退出码 2。报错只在既有缺模块：`CmsRichText.vue` 的 `@wangeditor-next/editor-for-vue`、`exportBlockReportPdf.ts` 的 `html2canvas` / `jspdf`。本叶改动的政策文件没有类型错误。
- 浏览器：本机 `vite --port 3001` 能起来，打开 `http://127.0.0.1:3001/policy/recommendation` 时 `src/config/echarts.ts` 已有的 `echarts-wordcloud` 在当前 `node_modules` 解析失败，页面空白。未登录时路由守卫还会转到 SSO。没有在浏览器里点完勾选、均分和开始分析。配置区与截图的一致性来自对照 demo 源码和截图文案逐项落地。

## CI/CD

- 分支：`lumen-ui-topic` `dev` 工作区
- commit：无。按任务要求不提交、不推送。
- pipeline URL / ID：未触发
- 部署 namespace / 镜像 tag：无
- K8s rollout：未部署
- dev 测试 URL / 命令与结果：本地自检见上。线上未发布。

## 遗留风险

- 配置区没有在已登录的 lumen 页面上点过。本地缺 `echarts-wordcloud`，结果页图表在这套 `node_modules` 下也会随 `echarts.ts` 一起加载失败。这是安装缺口，本轮不加包。
- 全仓 `vue-tsc --build` 仍被上述既有缺模块挡住。
- 仪表盘没有用一条已签发的深圳任务在浏览器里打开。空分与有分两支只由自检和解析函数覆盖。
- 任务保持进行中。本 handoff 不作为联调或会签结论。

## 涉及文件

- `repos/lumen-ui-topic/src/config/policySzModel.mjs`（新）
- `repos/lumen-ui-topic/src/components/policy/PolicySzIndicatorModel.vue`（新）
- `repos/lumen-ui-topic/src/views/policy/PolicyAnalysisConfigPage.vue`
- `repos/lumen-ui-topic/src/config/policyAnalysisRegistry.ts`（仅注释）
- `repos/lumen-ui-topic/src/utils/policyShenzhenResult.ts`
- `repos/lumen-ui-topic/src/components/policy/PolicyShenzhenResultBoard.vue`
- `repos/lumen-ui-topic/src/components/report/policyBlockReportDocument.ts`
- `repos/lumen-ui-topic/src/views/policy/policyShenzhen.selfcheck.mjs`

开工前工作区里结果板、报告、解析和深圳自检已有未提交改动（档位/实效的分数与不可算分支）。本轮在其上补仪表盘和自检，没有还原这些文件，也没有改其他会话的无关文件。

## 架构合规

| 铁律 | 结果 |
|------|------|
| 前端只调 Java | ✅ 不算分，不直连 Python |
| D12 不引用 demo 服务或 fixture 分数 | ✅ 指标目录自写，无 84/88 |
| D9 ⓘ / MockBadge / PendingBadge 走评审层 | ✅ 常显缺口用 `a-tag` |
| 时序页与区域对比页不回退 | ✅ 勾选与指纹空数组保持原样 |
| 空分不写成 0、不出综合分 | ✅ |
