# LUMEN-POLICY-E-C1-FE-BUILD-L01 · 政策专题 E · C1 修 lumen-ui-topic vue-tsc --build

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-E-总派单.md`](./LUMEN-POLICY-E-总派单.md)  
> 失败 job：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26140（POL-04 `5c5caaf` **frontend:build**）  
> 分类：**C1**（产品/代码 · TS；CI 是 `npm run build` → `vue-tsc --build`，不是 `--noEmit`）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。本叶只修 TS 才能过 CI，不扩 POL-08/门户/维护/查询，不回滚 `KEEP_ANALYSIS_QUERY`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改类型收窄与已有回调签名；未改交互/视觉语义；未 new 依赖；未用 YAGNI 跳过 D8/D9/D10 或可观测。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | C1 类型修复，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 本叶不改工厂拓扑。仅修前端 TS 才能过 CI。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

失败分类 C1。GitLab job 26140 = POL-04 `5c5caaf` 的 `frontend:build`。本机复现 `npx vue-tsc --build` exit 2。按文件全修已知错误，不扩范围、不改交互/视觉语义。

## 修改内容

| 文件 | 修法 |
|------|------|
| `src/api/policy/index.ts` | `asParams` 改为消费 `object`，只序列化 string/number，避免 PolicySearchQuery / PolicyGraphQuery 赋给 `Record<string, string\|number\|undefined>` |
| `PolicyRegionalResultBoard.vue` | `bound` 空守卫；表格 `row-class` / `row-click` 改 Arco `TableData` |
| `PolicyTimeseriesResultBoard.vue` | ECharts `type: 'line' as const` / `'bar' as const`；节点表回调改 `TableData` |
| `usePolicyAnalysisJob.ts` | `readAnalysisFingerprint` 仅在 `task.value` 存在时调用 |
| `policyRegionalResult.ts` | `row.scores` 先落到局部再索引；filter 谓词 `item != null`；insights `map` 显式 `T \| null` |
| `policyTimeseriesResult.ts` | 同上 filter/null；支持力度合计改为四项相加，避免 `reduce` 把累加器推成 `number \| null` |
| `PolicyAnalysisConfigPage.vue` | `a-form` 补 `:model="{}"`（与产业兄弟页一致）；CheckboxGroup `@change` 对齐 `(string\|number\|boolean)[]` |

未改：门户/维护/查询、D12 demo-*、页内 MOCK、`KEEP_ANALYSIS_QUERY`、`package.json` / `vite.config`、helm/JDBC、`POLICY-STORAGE-FLOW` 拓扑。

## 偏离说明

- 无功能偏离。表格点击仍高亮区域/节点，不打开查询页。
- `a-form :model="{}"` 与 `IndustryDiagnosisPage` 等已有页同模式，控件仍绑各自 ref，不改为集中 form 对象。

## 产物清单

- 代码：`lumen-ui-topic` `97963375678d7d246ff800824995889901aebbf3` → `origin/dev`
- 本文 handoff

## 测试结果

本机（`lumen-ui-topic`，2026-09-02）：

```text
$ npx vue-tsc --build
(exit 0，stdout 空，零 error)

$ npm run build
> run-p type-check "build-only {@}" --
> vue-tsc --build
> vite build
✓ built in 42.02s
(exit 0)
```

**禁止**把 `--noEmit` 当过：本叶验收命令就是 `vue-tsc --build`。

## 遗留风险

- 推完时 GitLab `frontend:build` 仍可能在跑。job 26140 对应旧 SHA `5c5caaf`；新 SHA `9796337` 的 pipeline 见下方 URL。绿后请 coordinator 回写 job 号。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`（禁止 force）
- commit：`97963375678d7d246ff800824995889901aebbf3`
- 失败 job（修前）：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26140
- pipeline URL：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- commit pipelines：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/commit/97963375678d7d246ff800824995889901aebbf3
- 部署 namespace / 镜像 tag：本叶不改 helm；等 frontend:build 绿后由既有 CI rollout
- K8s rollout：本叶未点名 devops
- 本机：`npx vue-tsc --build` 零 error；`npm run build` 绿

## 可观测性（建议）

- 未改 `observability.ts` / `request.ts`；`X-Trace-Id` 仍走既有封装
- 本叶无新埋点（类型修复）

## 涉及文件

- `src/api/policy/index.ts`
- `src/components/policy/PolicyRegionalResultBoard.vue`
- `src/components/policy/PolicyTimeseriesResultBoard.vue`
- `src/composables/usePolicyAnalysisJob.ts`
- `src/utils/policyRegionalResult.ts`
- `src/utils/policyTimeseriesResult.ts`
- `src/views/policy/PolicyAnalysisConfigPage.vue`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未加前端算法 |
| 前端→Java→Python `/internal/*` | ✅ 未改调用链 |
| 图谱 Nebula | ✅ 不直连 nGQL |
| 可观测 | ✅ 未拆 `request.ts` X-Trace-Id |
| CI/CD | ✅ 推 `origin/dev`；本机 `vue-tsc --build` + `npm run build` 绿 |
| demo2 不 merge lumen | ✅ 未贴 JSX、未 merge demo |
| D8 / D10 | ✅ 未改视觉/交互语义 |
| D9 8 件套 | ✅ 未改 ⓘ / 角标接线 |
| D12 lumen 不调 demo **服务** | ✅ 无 `demo-*` URL |
| 图即契约 | ✅ 未改 `POLICY-STORAGE-FLOW` |

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 40000 |
| actual_tokens | 95000 |
| model_used | grok-4.6 |
| actual_cost | 0.72 |
| cost_warn | green |
| 说明 | in+out 合计估算；按 frontend 75/25、B 档价粗算 &lt; $5 |

## 联调确认

联调通过：本机 `npx vue-tsc --build` 零 error，`npm run build`（含 `vue-tsc --build`）exit 0；已 push `origin/dev` `9796337`。未扩 POL-08、未改 helm/JDBC。
