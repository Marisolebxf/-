# LUMEN-TOPIC-FE-SHARED-FORM-L01 · 字典注册表 + DictSelect / FilterField / 产业目录双下拉

> 格式参考 `templates/handoff-template.md`。本叶只做 Wave 1–2 原子控件与接线；FilterBar / TopicContextBar / DictCascader / RecordStatusSelect 仍按规划 Wave 3–4，未做。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | CHROME 已 `ready_to_sign` 后用户授权认领开工；本叶收口要求写 handoff + commit + push `origin/dev`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 包装现有 Pinia / `useIndustryCatalog`，不平行再写 API。不抽 Schema 引擎、不整包搬 demo `TopicFilterBar`。未用 YAGNI 跳过 D8 400px / dictKey 分轨。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂 Headroom。 |

## 范围与实现

仓：`lumen-ui-topic`。字典注册表 + 四个表单原子控件，接到产业双下拉与引育 / 重点分析 / 深圳现状业务 Select。

| 能力 | 路径 | 用法 |
|------|------|------|
| `useDict` + registry | `src/composables/dict/` | 包装 `ent.tags` / `ent.chains` / `ent.scales` / `ent.company-types` |
| `DictSelect` | `src/components/form/DictSelect.vue` | `dictKey` 驱动 a-select；树/目录 key 在 `assertFlatDictKey` 抛错 |
| `FilterField` | `src/components/form/FilterField.vue` | label 在上；控件 `max-width: var(--sci-filter-control-max)`（400px） |
| `IndustryCatalogSelect` | `src/components/form/IndustryCatalogSelect.vue` | GET catalog 双下拉；`fill=false` 时不盖掉宿主定宽 |
| `YearRangePicker` | `src/components/form/YearRangePicker.vue` | 起止年 RangePicker |
| `entCompanyTypes` store | `src/stores/entCompanyTypes.ts` | 补未缓存字典；`USE_MOCK=false` 失败保持空，不填 fixture |

接线：

- 产业 Overview / Panorama / Diagnosis / Regional / Shenzhen 双下拉 → `IndustryCatalogSelect`
- 引育 `RecruitFilterPanel` tags/chains/scales → `DictSelect`（region / policy_static 不动）
- 重点分析 `TypeRegionPanel`：产业=`ent.chains`，类型=`ent.tags`，年份=`YearRangePicker`；区域仍 `RegionSelect`
- 深圳现状产业链 → `DictSelect` `ent.chains` `scope=future`

Overview 门户资讯类型/区域点位 Select 不是目录，未改。

## 偏离说明

- **Wave 3–4 未做**：`FilterBar` / `TopicContextBar` / `DictCascader`（RegionSelect 升挂）/ `RecordStatusSelect`。规划明确 P1/P2；本叶 DoD 不含。
- **评价模式 Radio 不对齐圆角 Tab**：demo `analysis-rounded-radio` 无独立 CSS，视觉是 Arco 默认灰底分段。曾按 Design §7.3 压成 999px 胶囊，用户要求对齐 demo 后撤回覆盖。
- **区域评价页去掉重复页头**：demo 标题只在一级 Tab；`AnalysisPageHeader` + 筛选行 `CHAIN-REG-F01-OBJECT-CONTEXT` 按钮是 CHROME 多挂的。已删按钮，保留 `data-mount-host`。诊断 / 深圳页头未动。
- **侧栏同 path 不切页**：同组件只改 `workspace`/`tab` 时 Vue 复用实例。`router-view :key="sidebarViewKey"` 按菜单项重挂；`query` 不再传 `undefined`。属本叶收口期附带修复，不是 FORM DoD 原文。

## 产物清单

- 公共件：`FilterField` / `DictSelect` / `YearRangePicker` / `IndustryCatalogSelect`
- 字典层：`src/composables/dict/**`、`src/stores/entCompanyTypes.ts`
- 自检：`scripts/check-shared-form.mjs`
- 本 handoff
- 代码仓 commit：`lumen-ui-topic` `c214c7c`（`origin/dev`）

## 验收证据

- `node scripts/check-shared-form.mjs` → `check-shared-form: ok`
- `npx vue-tsc --build` 绿
- CI：push `origin/dev` 后由 GitLab pipeline 接续（本机未等 K8s rollout）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未改算法 |
| 2 调用链 前端→Java | ✅ 只经现有 meta / catalog REST，无直连 Python |
| 3 Nebula | ✅ 未改图谱 |
| 4 可观测 | ✅ 未删既有埋点；字典走现有 store/request |
| 5 CI | ⏳ push `origin/dev` 后由 GitLab 接续 |
| 6 demo2 不 merge lumen | ✅ |
| 7 共享聚合 | ✅ |
| 8 数据策略 | ✅ `USE_MOCK=false` 禁止 fixture 填选项 |
| 9 D8 Design | ✅ FilterField 400px；不包 SciSelect；Radio 跟 demo Arco 默认 |
| 10 D9 | ✅ 未改血缘组件进口径 |
| 11 D10 | ✅ 未改一级 Tab 键盘；侧栏 key 重挂不拆 records 页内 Tab |
| 12 D12 | ✅ 只动 lumen-ui-topic |

## 测试结果

- 字典分轨自检绿（catalog / region-scopes / filters 不得进 DictSelect）
- 年份区间非法值返回 null
- company-types：`USE_MOCK=false` 且无 API 数据时选项为空
- `vue-tsc --build` 绿
- 未做 Playwright e2e（tech_task 横切，无新路由）

## 遗留风险

- 规划画布「筛选侧 8 / 骨架侧 5」是 P0–P2 全量目录；本叶只交付 Wave 1–2。后续叶不要把 FilterBar 焊成全家桶。
- `RegionSelect` / `RegionTreeSelect` 仍分轨；DictCascader 留给 Wave 4。
- Overview「产业」label 换行已用 `fill=false` + `flex-shrink: 0` 修；其他内联宿主若再设定宽，须同样关 fill。
- `task-registry.yaml` 仅经 MCP 回填，本 handoff 仓 commit **不**夹带 registry 手改。

## CI/CD

- 分支：`lumen-ui-topic` `dev` → `origin/dev`
- commit：`c214c7c4294671ad700908d6298af8d2e76ed308`
- pipeline / K8s：push 后由 GitLab 触发；本机未等 rollout
- 编排仓：本 handoff 同步 push `gkx-orchestration` `origin/dev`

## 可观测性

- 本叶无新 HTTP 客户端；字典走既有 Pinia / `request.ts` / `X-Trace-Id`
- OTEL / Tempo：N/A

## 涉及文件

- `src/composables/dict/dictKeys.ts` / `useDict.ts` / `yearRange.ts` / `index.ts`
- `src/stores/entCompanyTypes.ts`
- `src/components/form/FilterField.vue` / `DictSelect.vue` / `YearRangePicker.vue` / `IndustryCatalogSelect.vue` / `index.ts`
- `src/composables/useIndustryCatalog.ts`
- `src/views/industry-center/IndustryOverviewPage.vue` / `IndustryPanoramaPage.vue` / `IndustryDiagnosisPage.vue` / `IndustryRegionalPage.vue` / `IndustryShenzhenPage.vue`
- `src/views/industry-center/industryOverview.css`
- `src/components/enterprise/recruit/RecruitFilterPanel.vue`
- `src/components/enterprise/keyAnalysis/TypeRegionPanel.vue`
- `src/views/enterprise/EnterpriseSzStatus.vue`
- `src/assets/design-tokens.css` / `src/assets/search-workspace.css`
- `src/layouts/DefaultLayout.vue` / `src/router/menu.ts`（侧栏同 path 重挂）
- `scripts/check-shared-form.mjs`

## 成本

- actual_tokens: 320000（会话估算：字典接线 + 页面改挂 + 视觉/导航收口；source: session_estimate）
- model_used: cursor-grok-4.6
- actual_cost: 1.86
- cost_warn: green
