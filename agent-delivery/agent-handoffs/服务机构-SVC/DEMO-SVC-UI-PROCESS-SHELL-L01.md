# DEMO-SVC-UI-PROCESS-SHELL-L01 · 服务机构开始分析补齐可视化过程壳

> 格式参考 `templates/handoff-template.md`。淮政玮口头：点【开始分析】后要和其他模块一样出现任务可视化分析过程壳。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 口头补交互缺口；仓 `demo-ui-topic`；不开 50892 / 阶段 P / lumen |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用已有 `AnalysisProcessingShell` + 系统任务路由；未新依赖；未用 YAGNI 跳过过程壳（公约要求的分析任务可视化）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改三页 stay/restore 与契约测试，未挂载 Headroom。 |

## 问题清单

- 服务机构分析 / 链路生态点「开始分析」后，当天同指纹成功会 `restore_result` 直跳结果，且过程壳叠在条件栏下面；领域覆盖还可能被空机构闸挡住。
- 招引/培育「生成名单」同样直跳结果。
- 政策/企业/产业链：过程页独占主区，完成后停在「可视化分析过程」，须点「查看分析结果」。

## 修改内容

- 门控增加 `shouldStayOnAnalysisProcessPage`（`analysis_view=processing` 占住过程页）。
- 三页：`restore_result` / 当天成功 → `buildSystemTaskTarget`（过程页），**不**提前 `markSystemTaskResultViewed`。
- 过程态掩盖条件栏与 idleGate，只渲染 `AnalysisProcessingShell`。
- 「查看分析结果」仍走 `buildSystemTaskResultTarget` + `markSystemTaskResultViewed`。

## 测试结果

```text
node --test tests/service-analysis-process-stay.test.mjs tests/service-recommend-context.test.mjs
# 8 pass / 0 fail
```

## 遗留风险

- 企业/政策/产业链当天成功仍可直开结果（本叶只改服务机构）。
- 本地 localStorage 里已 `resultViewedAt` 的旧任务：再点开始分析会进过程壳（processing URL 仍占住），需再点「查看分析结果」。
- 未改 lumen；`LUMEN-SVC-FE-WAITVIEW-L01` 仍 blocked。

## CI/CD（必填）

- 分支：`demo-ui-topic` `origin/dev`
- commit：`e851adb`
- pipeline URL / ID：push 后 GitLab `dev` pipeline
- 部署 namespace / 镜像 tag：专题 demo 静态站（CI 跟 `dev`）
- K8s rollout：随 demo-ui-topic CI
- dev 测试 URL：专题 demo 服务机构分析 / 链路生态 / 招引培育，点开始分析或生成名单应先见「可视化分析过程」

## 可观测性（建议）

- 沿用现有系统任务浮层与页面 Message；本叶无新埋点。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未改算法 |
| 调用链 FE→Java→Python | ✅ 未越层 |
| Nebula | ✅ 未改图谱 |
| 可观测 | ✅ 沿用系统任务 |
| D8/D10 | ✅ 复用已有过程壳 Steps |
| D9 | ✅ 未改指标口径 |
| D12 | ✅ 只动 demo-ui-topic |
| 不开 50892/P | ✅ |

## 涉及文件

- `demo-ui-topic/src/app/system-tasks/analysisTaskGate.ts`
- `demo-ui-topic/src/app/pages/service-center/ServiceOrgAnalysisPage.tsx`
- `demo-ui-topic/src/app/pages/service-center/ServiceChainEcosystemPage.tsx`
- `demo-ui-topic/src/app/pages/service-center/ServiceRecommendPage.tsx`
- `demo-ui-topic/tests/service-analysis-process-stay.test.mjs`
