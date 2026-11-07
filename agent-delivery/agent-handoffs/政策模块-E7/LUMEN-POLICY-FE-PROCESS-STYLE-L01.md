# LUMEN-POLICY-FE-PROCESS-STYLE-L01 · 政策三分析过程步骤条对齐服务机构样式

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户当次会话明确「认领并执行」。监管人沿政策专题既有管线。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只给政策过程页加类和两行最小高度，当前步钳制放在已有 `industryChainTask`。未改阶段标题、提示文案、创建任务或结果板。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未用压缩；改动面是三个文件加一个自检。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 不必 |
| 图 diff | 不改调用链、不改存储 |
| 会签态 | 不适用 |
| 说明 | 样式对齐，无拓扑变更。 |

## 问题清单

- 政策时序、区域政策对比、深圳政策现状的「可视化分析过程」步骤条，要和服务机构技术力评估过程壳的圆点、连线、行高，以及当前步往前走时步骤区不跳高，保持一致。
- 不改任何业务文字。过程壳还被产业链四页使用，样式不能波及它们。

## 修改内容

- `IndustryAnalysisProcessShell` 增加可选 `matchSvcProcess`。只有政策配置页传入。
- 传入后根节点带 `policy-svc-process`，步骤区最小高度 132px，描述行最小高度 22px，与 `serviceOrgAnalysis.css` 里服务机构过程壳相同。
- 当前步用 `stableProcessStepCurrent`：成功时顶到 `total + 1`；进行中钳在 `1..total`，避免索引在末步和末步之后来回跳。状态字仍是「已完成 / 进行中 / 等待中 / 失败」。
- `POLICY_ANALYSIS_STAGES` 与 `POLICY_PROCESS_DESCRIPTIONS` 未改。

## 测试结果

- `node src/views/policy/policyProcessSteps.selfcheck.mjs` 通过。
- `node node_modules/vue-tsc/bin/vue-tsc.js --build` 通过。`pnpm type-check` 被 pnpm 的依赖安装钩子拦住，未用它作为证据。
- 未在浏览器点开三个过程页。本地没有已登录的过程任务可走。

## 遗留风险

- 服务机构过程壳的步骤标题来自任务节点，政策步骤标题仍是配置里的固定阶段名。本单只对齐样式和当前步是否跳高，没有把政策改成按节点状态逐个点亮。
- 前端 commit `75da9aaa` 在本地 `dev`，未推。`origin/dev` 的远端引用在本机是坏的，推送前需要先修好跟踪再经人工确认。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `dev`
- commit：`75da9aaa`
- pipeline URL / ID：未推，无流水线
- 部署 namespace / 镜像 tag：未发布
- K8s rollout：未做
- dev 测试 URL：未部署

## 可观测性（建议）

- 未改请求路径，无新 trace。

## 涉及文件

- `repos/lumen-ui-topic/src/components/industry-center/IndustryAnalysisProcessShell.vue`
- `repos/lumen-ui-topic/src/utils/industryChainTask.ts`
- `repos/lumen-ui-topic/src/views/industry-center/industryDiagnosis.css`
- `repos/lumen-ui-topic/src/views/policy/PolicyAnalysisConfigPage.vue`
- `repos/lumen-ui-topic/src/views/policy/policyProcessSteps.selfcheck.mjs`

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000（按本叶预估，不是账单读数） |
| model_used | grok-4.7 |
| actual_cost | 未单列，低于 10 美元暂停线 |
| cost_warn | green |
