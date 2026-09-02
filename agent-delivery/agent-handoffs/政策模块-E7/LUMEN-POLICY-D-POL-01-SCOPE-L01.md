# LUMEN-POLICY-D-POL-01-SCOPE-L01 · 政策三项分析配置页产业锚点：集群→L0

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单包：[`LUMEN-POLICY-D-POL-01-SCOPE-L01-派单包.md`](./LUMEN-POLICY-D-POL-01-SCOPE-L01-派单包.md)  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> 前序抽屉：[`LUMEN-POLICY-D-POL-01C-DETAIL-L01.md`](./LUMEN-POLICY-D-POL-01C-DETAIL-L01.md) `d5ea3f7`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。DETAIL 已离开 in_progress 后认领。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `PolicyAnalysisConfigPage` + `IndustryClusterSelect` + `useIndustryClusters.l0Options`；未另造选择器；未贴 JSX；`/policy/search` 未动。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 配置页提交仍只调 Java `/topicAsync/topic/v1/analysis/tasks`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

三项分析共用 `PolicyAnalysisConfigPage`（`/policy/overview` · `/policy/analysis` · `/policy/recommendation`）：

1. 产业：先选集群（产业 map），再选该 map 下 **L0**（恰好 1 个）。`require-graph-vid` 过滤短码 / 中文 / `CL-*`。
2. **不强制对比篮**。空篮可页内直选。篮分发仍预填并显示「来自对比篮 · 产业」Tag。
3. 去掉「去产业查询」主按钮 / 唯一入口。
4. 校验文案对齐 demo `IndustryAnalysisScopeFields`：尚未选择分析对象 / 请先选择集群 / 请选择产业 / 无相关产业数据。VID 空仍提示须 `chain:INB…`。
5. 切条件不自动 create（W4）；无集群 / 无 L0 / 无映射 / VID 空 →「开始分析」disabled。
6. 技术领域页内多选、不进篮（保持）。

## 偏离说明

- 未拆两套 Form.Item 重写 `IndustryClusterSelect`；在原级联上校正 placeholder / 选项过滤 / 政策页关闭自动选首集群。
- L0 选项仍来自 `cluster.l0[]`，提交仍只认 `toPolicyGraphVid`（`INB`≥6 → `chain:INB…`）。

## 产物清单

- 代码：`lumen-ui-topic` `265950396ddc214f172e63aed00b56786218bf2e` → `origin/dev`
- 本文 handoff

## 验收证据

- `node src/views/policy/policyConfig.selfcheck.mjs`：`policyConfig.selfcheck ok`
- `node src/router/menu.selfcheck.mjs`：`policy-shell ok`（有本页直选文案，无「去产业查询」）
- `npx vue-tsc --build`：零 error

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ 对象类型 + 集群/L0 级联 + 篮 Tag 可选；三路由同一页 |
| R2 交互 | ✅ 无集群/无 L0/无映射/VID 空不可提交；篮预填可选 |
| R3 样式 | ✅ 沿用 diagnosis-config / `--sci-*` |
| R4 评审 | ✅ `@/review` Trace / IndustryReviewOnly；文案改为页选主路径 |
| R5 Mock | ✅ 无数诚实空；未用 Demo fixture 填集群/L0 |

### 检索皮肤 V1–V7

N/A：本叶不改 `/policy/search`。

### 工作区 W4

| # | 结果 |
|---|------|
| W4 | ✅ 切条件不自动 create；条件栏「开始分析」；同指纹当天成功复用；「重新分析」force |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端不算支持强度 |
| 前端→Java→Python `/internal/*` | ✅ 提交只走 Java analysis/tasks |
| 图谱 Nebula | ✅ VID 只认 `chain:INB…`；不直连 nGQL |
| 可观测 | ✅ 复用 `request.ts` `X-Trace-Id` |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ Vue 校正，未贴 JSX |
| D8 / D10 | ✅ 沿用本仓配置页皮肤 |
| D9 | ✅ 未自造 ⓘ |
| D12 | ✅ 只经网关 `gkxlumen-*` |

## 测试结果

- 联调通过：空篮页内集群→L0→VID 可点开始分析（其余时序三维仍须全开）；三路由同一套级联。

## 遗留风险

- 集群 map 若 L0 全是短码，过滤后「无相关产业数据」，不可提交（诚实，不回落 fixture）。
- `/policy/search` 本叶未动。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`265950396ddc214f172e63aed00b56786218bf2e`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署：随仓既有 CI；本叶不改 helm
- dev URL：`/policy/overview` · `/policy/analysis` · `/policy/recommendation`

## 可观测性

- 复用前端 `request.ts` `X-Trace-Id` / `traceparent`

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/views/policy/PolicyAnalysisConfigPage.vue` | 页选主路径；去「去产业查询」；校验文案 |
| `src/components/form/IndustryClusterSelect.vue` | placeholder / requireGraphVid / 关闭政策页自动选集群 |
| `src/views/policy/policyConfig.selfcheck.mjs` | hint 自检 |
| `src/router/menu.selfcheck.mjs` | 禁「去产业查询」 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 70000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.48 |
| cost_warn | green |
