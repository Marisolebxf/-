# POL-L2-DS11-VIZ-WIRING-L01 · 政策分析报告可视化呈现 · 前端接线 handoff

- 任务：`POL-L2-DS11-VIZ-WIRING-L01`（SRS 219–222）
- 日期：2026-11-04
- 认领/执行：`agent:frontend-agent`
- 监管：`human:淮政玮`
- 强度：ponytail full
- 仓：`repos/lumen-ui-science-pc`（Vue3 + Arco Design Vue + Pinia + Vite）
- 契约真源：`sdd/l2/POL-L2-DS11-VIZ-API.md`；架构：`POL-L2-DS11-VIZ-ARCH.md`；数据：`POL-L2-DS11-VIZ-DATA.md`
- ponytail：full（复用 defineApi 双轨 / request 封装 / 冻结种子；最短 diff 四组件接线）

## 1. 范围与实现

政策分析评价页（`src/views/policy/analysis/index.vue` Tab1「政策分析报告可视化呈现」）四叶接线：

| 序号 | 叶子 | 组件 | 实现 |
|---|---|---|---|
| 219 | 多维指标趋势图 | `TrendMetricsChart.vue` | 新 prop `switchDims`（页级维度条 appliedDimensions 派生：timeRange→时间 / region→区域 / category→类别，`all` 不算已选维）；USE_MOCK=false 时 `POST /display/v1/policy/evaluation/jobs` `kind=趋势`，条件闭集 switch（时间/区域/类别）+ metric（表内指标名：支持力度/惠及面/执行率/满意度/创新贡献）；行按 `(metric_name, axis_position)` 组装序列 |
| 220 | 分区/群体对比分析图 | `RegionGroupCompare.vue` | tab 切换/投向筛选触发 `POST /display/v1/policy/evaluation/jobs` `kind=分区`（与趋势**另一次请求**）；subject 三选一（地区/行业/目标群体，tab key 映射）+ allocation（投向 value→表内投向名）；柱和热力读同一批行（单对照数 → 柱图单序列 + 热力 1×N 矩阵） |
| 221 | 多维结构关联图 | `StructureLinkPanel.vue` | **不新增请求、不设资源**；`graphMounted = USE_MOCK`——真轨下政策子图挂点暂无前端消费通道，弦线图/关系网/传导路径三模式全空态（文案注明「挂接暂未就绪，不新开资源转接」）；mock 轨保留 demo 冻结种子视觉 |
| 222 | 报告模板定制与批量导出 | `ReportTemplateExport.vue` | `GET /display/v1/policy/evaluation/shells` `kind=模板选用`；条件闭集 template（必选）/period/dimension（六值：时间/区域/类别/地区/行业/目标群体）/chart_type（五值：趋势/柱状/热力/弦线/关系网，**移除饼图/散点**）/format（PDF/Excel，不传只返回选用行）；真轨下拉选项从选用行派生（周期不单列近1/3/5年）；导出前 `validateExportConditions` 校验三必填；真轨无真实导出记录则日志空态（不灌假日志） |

### 新增文件

- `src/api/policyEvaluationViz.ts`：三个 `defineApi`（`fetchPolicyEvalTrend` / `fetchPolicyEvalPartition` / `fetchPolicyEvalTemplates`），类型化条件闭集与行形状（对齐 gapfill 表列名）；real 轨走 `request`（axios，baseURL `/api`），全部 `optional: true`（失败降级空态不登出）
- `src/mock/modules/policyEvalViz.ts`：mock 从冻结种子 `policySeed.ts` 派生（trendMetricsSeriesData / regionGroupCompareData / reportTemplates），响应行形状对齐 gapfill 表；条件对不上行则 items 空（语义同真轨）；无 Math.random、无新造数据
- `src/views/policy/analysis/POL-L2-DS11-VIZ-WIRING.test.mjs`：21 项 assert 自检（仓内 node 无框架模式，对齐 FE-POL-02A.test.mjs 先例）

### 修改文件

- `src/mock/register.ts`：注册三个 mock id
- `src/views/policy/analysis/index.vue`：TrendMetricsChart 传 `switch-dims`（一行模板改动）

### 一次请求只一种类

- 219 与 220 是两次独立 `POST /jobs`（kind 不同）；组件内各自只发一种 kind
- 请求参数不定义 `sub_type`（契约：kind 与 sub_type 同传则该块空——前端按契约根本不带 sub_type）
- 只调 `/display/v1/policy/**`，无 `/topic/v1`、无 `/topicAsync`、无 `/v1/policy`、不调 Python

## 2. Mock 开关对齐

沿仓内 `defineApi` 双轨：`USE_MOCK=true` 走 `registerApiMock` 注册的种子派生 mock（demo 冻结视觉不变，评审走查不受影响）；`=false` 走 real 轨真请求，**零 fixture 填数**——接口失败/无行一律空态渲染（不造假曲线/演示矩阵/写死模板）。221 在真轨下全空（挂接可空语义）。

## 3. 验证证据

- **自检（绿）**：`node src/views/policy/analysis/POL-L2-DS11-VIZ-WIRING.test.mjs` → `全部通过：21 项`，覆盖：API 路径/方法/条件闭集、mock 注册与种子派生、四组件消费与空态、页级联动、禁项（/topic/、sub_type 字段、Math.random、饼图/散点）
- **type-check / build**：本机依赖不完整（node_modules 缺 vue-tsc/vite）且 pnpm 版本与 pnpm-workspace.yaml 不兼容，`npx pnpm@10 install` 在本机网络环境下未能完成——**此两项未能在本机跑绿，已如实记录，请监管人验收时在有依赖的 CI 或开发机执行**（命令：`pnpm type-check`、`pnpm build`）。类型层面已人工核对：新 API 文件类型自洽、组件 props/泛型对齐既有模式（defineApi/request 与 situation/innovationEvaluation.ts 同构）
- **页面实跑**：同因依赖未装全（vite 缺失）无法本机 `pnpm dev`。接口路径正确性以契约分册逐条对照为准（见自检第 1 节断言）

### 后端可用性（已知缺口，不阻塞）

后端 `gkxlumen-display` 评价控制器可能尚未实现（READ-IMPL-JAVA 覆盖 evaluation/jobs 与 shells 骨架）。前端已按契约正确发请求；若真接口 404/501，`optional: true` 降级 → 四叶空态渲染正常，不登出、不阻塞页面——按派单口径「接线完成」处理，本 handoff 记录该缺口。

## 4. 架构合规自检（团队公约 §2 逐条）

| 铁律 | 结论 |
|---|---|
| D12 正式仓不调 demo-* | ✅ 只调 `/display/v1/policy/**` 经 `gkxlumen-platform-gateway`；无 demo 直连、无 `VITE_*` 直连 |
| 调用链不可越层 | ✅ 前端 → Java REST；不直连 Python `/internal/*` |
| D9 数据血缘 | ✅ 四叶无专属 metric_id（分册明示）；MockBadge 保留；空态诚实（无行不造数、D4 仍 mock） |
| D8 Design/Arco | ✅ 复用既有 Arco 组件（a-select/a-checkbox-group/a-table/a-empty），未新增 UI 栈 |
| USE_MOCK=false 零 fixture | ✅ real 轨零 mock 填数，失败空态 |
| 一次请求一种类 | ✅ 219/220 分两次请求；无 sub_type 字段 |
| 221 不新开资源 | ✅ 组件无 fetch 调用，空态文案注明不转接 |
| 222 只读模板表语义 | ✅ 不读壳表；周期/维度/图表类型值全落闭集 |
| 不改配置文件 | ✅ 未动 .gitignore/package.json/vite.config |
| 人工验收闸门 | ✅ 改动全部停本地工作区，未 commit/push |

## 5. 产物清单

- 代码（`repos/lumen-ui-science-pc`，**未提交**）：`src/api/policyEvaluationViz.ts`（新）、`src/mock/modules/policyEvalViz.ts`（新）、`src/views/policy/analysis/POL-L2-DS11-VIZ-WIRING.test.mjs`（新）、`src/mock/register.ts`（改）、`src/views/policy/analysis/index.vue`（改）、`TrendMetricsChart.vue` / `RegionGroupCompare.vue` / `StructureLinkPanel.vue` / `ReportTemplateExport.vue`（改）
- 本 handoff（gkx-orchestration 内新文件）
- 临时诊断文件 `.env-diag.txt` / `.selftest-output.txt` / `.install-log.txt` 待验收后清理

## 6. 偏离说明

- `ReportTemplateExport.vue` 表单从「模板 id」改为「模板名」（契约条件字段是 `template` 模板名，非 id）；mock 轨视觉兼容（下拉内容不变，值语义变化）
- 222 mock 轨保留饼图/散点选项（demo 冻结种子视觉不破坏评审走查）；真轨选项严格落五值闭集
- type-check/build 未本机跑绿（依赖缺失，非代码问题），已如实记录待监管人环境复核
