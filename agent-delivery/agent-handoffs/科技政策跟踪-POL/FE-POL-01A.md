# FE-POL-01A · 科创政策全景 — 检索主链路整段复刻

> 交付日期：2026-11-02 · 仓：`repos/lumen-ui-science-pc` · 状态：**走查修正完成，已推 origin/dev，转待测试**（监管人 human:孔东 2026-11-02 走查：①去高级检索面包屑 ②分组标题留白）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（开工登记见 task note 2026-11-02） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 派单 `/goal` 强度 full。零新依赖（xlsx 仓内已装）；DSL 族复用 demo 冻结语义 TS 化重写（非搬 TSX，D6）；S01 基座全复用（PolicyStatCard / PolicyMetricSpecTrigger / PendingBadge / mapRegistry / usePolicyTrack / mock 双轨 / 评审层 useReviewStore）。未跳过 D8（评审角标全部走 store 自闸）、D9（统计卡 ⓘ + QPOL ⚠️ + Mock 🧪）、D10（Arco 优先、Teleport、键盘可达 aria-label）、可观测（trackPolicyInteraction）、架构铁律（D12 零 demo 依赖） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 问题清单

- 无阻塞问题。3 个执行中判定：
  1. `a-radio-button` 非 Arco Vue 组件（AntD 概念；Arco 用 `a-radio` + group `type="button"`）——已按 Arco 正确用法落，语义等价（按钮形单选）
  2. `IconShare` 不存在于 Arco Vue icon 集（React 版名）——换 `IconShareAlt`（仓内 14 处先例统一用名）
  3. 高级检索整页壳 `DisplayAdvancedFilterPage` 拆 `.vue`（壳+prelude+面包屑）+ `.ts`（`buildBooleanPreview` 纯逻辑，测试可直接 import）——demo 单 JSX 混两种职责，Vue 化按仓内惯例分文件

## 走查修正（human:孔东 2026-11-02 18:22，已实施并复验三绿）

1. **去掉高级检索面包屑**：`DisplayAdvancedFilterPage.vue` 移除 `nav.display-advanced-filter-breadcrumb`（「科创政策全景/检索全景/高级检索功能」）；切回检索靠 SearchHub 模式 Tab（demo 同语义入口保留）
2. **分组标题留白**：`.pp-result-group__head` 加 16px 水平内边距 + 首组 16px 顶距；第 2 组起 20px 顶距 + 浅分隔线（对齐 demo `Divider orientation="left"` 分段感）

## 修改内容

### 检索主链路（`src/views/policy/panorama/`，18 文件全新增/改写）

**① SearchHub 三模式（`search/DisplayPolicySearchHub.vue` + `displaySearch.css`）**
- 智能检索（NL 解析 chips 反馈 + 回退关键词提示）/ 关键词 / 高级检索功能三 Tab；进入高级后模式 Tab 保留（demo L3045 语义，可切回）
- 热门标签（DISPLAY_HOT_TAGS 一键筛）/ 查询示例（DISPLAY_QUERY_EXAMPLES）/ 占位文案冻结 demo

**② 智能解析（`search/displaySmartParser.ts`，97 行语义）**
- NL → 级别/类别/行业/地区四维 filters + chips；未命中维度 → `fallbackKeyword` 回退关键词模式
- demo 语义：`LEVEL_MAP/CATEGORY_MAP/INDUSTRY_MAP/REGION_MAP` 词表冻结

**③ 高级检索 DSL 族（`search/advanced/`，D6 TS 化重写）**
| 文件 | demo 真源 | 语义 |
|---|---|---|
| `types.ts` | advanced/types.ts（283 行 ENT 全量） | POLICY 消费子集：SearchMode/FieldType/OperatorKey/FieldStatus/FieldDef/Single+Group+FilterDSL/AdvancedPanelConfig；口径状态 emoji→词语枚举（D8 禁 emoji） |
| `queryEngine.ts` | shared/search/queryEngine.js | 10 算子（eq/contains/in/containsAll/notContainsAll/has/none/range/gte/lte）+ negate + 一层组；分支结构与求值顺序逐行对齐 |
| `displayFieldLibrary.ts` | displayFieldLibrary.js（196 行） | 11 字段全量（title/id/summary/publishYear/region/level/department/source/industry/category/status/keywords）；keywords 用 tag 类型支持自定义输入；`countLeafConditions/dslHasNegate/dslHasGroup/toAdvancedSearchRecord` |
| `FilterPanel.vue` | FilterPanel.tsx（page variant） | 左字段库（分类浏览+搜索+展开收起）+ 右条件区（顶层 AND/OR + 条件组 + NOT）；条件 Tag 回显；page 形态 footer |
| `ConditionBuilder.vue` | ConditionBuilder.tsx（280 行） | 单条件行：运算符随 FieldType 自适应；text/numberRange/date/select/tag 五类值控件全 Arco；NOT 复选；字段 metricId→ⓘ；status→评审角标（自闸） |
| `DisplayAdvancedFilterPage.vue`+`.ts` | DisplayAdvancedFilterPage.jsx（110 行） | `.vue`=壳（面包屑+prelude 布尔提示卡+editing 提示）；`.ts`=`buildBooleanPreview` 纯逻辑（布尔式预览字符串逐例比对 demo） |
| `advancedFilter.css` | advancedFilter.css | token+布局类自含（pdaf-* 对应 demo tailwind 原子类）；补齐面包屑/提示/布尔卡 3 组页级类 |

**④ 检索配置与结果工具（`search/`）**
- `displayPolicySearchConfig.ts`：SORT_OPTIONS（智能排序/发布时间/效力级别/浏览量 7 项）/ POLICY_SCOPE_OPTIONS / DISPLAY_HOT_TAGS / `filtersToDsl` / 最近查询 localStorage（键名冻结 `gkx-policy-display-*`）
- `displaySearchResultUtils.ts`：`matchPolicyScope`（多源）/ `smartScore`（相关·时效·重要·热 4 因子权重）/ `sortPolicyResults` / `refinePoliciesBySecondary` + `buildRefineFacetOptions`（二次筛 facets）/ `groupPoliciesByCategory` / `exportPoliciesExcel`（xlsx 动态 import）/ `exportPoliciesPdf`（打印窗存 PDF）/ `readFavorites`/`writeFavorites`

**⑤ 宿主页（`index.vue`，检索段 L2215-3320 语义）**
- 统计概览 6 卡：当前命中/本周新增/类型热点/收藏/落地实效/覆盖地区——全带 metric_id ⓘ（读 S01 镜像）+ QPOL ⚠️（QPOL-01/02）+ Mock 徽标
- 维度筛选条：来源 a-radio-group / 类别·部门·地区·级别 a-select / 行业 IndustrySelect（复用 situation 组件，legacyDomainInScope 求值）
- 检索结果区：列表/分组双视图（a-radio type=button）/ 智能排序 / 二次筛选（类型·地域多选 facets + 发布时间区间 + 起点晚于终点报错）/ 分类分组 / 分页（PolicyResultTable paginated）
- 高级检索结果态：条件 Tag 回显 + 返回编辑；检索历史（localStorage 最近 10 条 + 清空）；已启用高级检索 Alert
- 导出（Excel/PDF dropdown）/ 分享弹窗 / 收藏夹抽屉 / 详情抽屉；深链 `?tab=match` 保留（FE-POL-01B 实装弹窗）

**⑥ 组件（`components/`）**
- `PolicyResultTable.vue`：政策行（重要性状态点/标题/摘要/tags/发布元信息/收藏/详情按钮），分组与分页两形态
- `PolicyContentDetailDrawer.vue`：概览 a-descriptions + 要素强度 + 政策原文（fullTextDoc 分节）+ 条款结构化 a-table（可展开原文片段）；Teleport `popup-container="body"`
- `ShareModal.vue`：链接生成（演示）/ 邮件分享（SHARE_EMAIL_RE 校验，parseShareEmails 复用）

**⑦ 最小自检（`FE-POL-01A.test.mjs`，11.9KB）**
- DSL 布尔（组 OR/AND + NOT + 叶计数/含组/含 NOT，断言语义冻结 demo queryEngine.group.test.mjs）
- 布尔式预览字符串逐例比对（DoD 第 2 条）
- 二次筛 + facets + 分组 / 智能解析维度命中与回退
- 组件锚点（SearchHub 三模式 / FilterPanel 组操作 / 抽屉 Teleport / 收藏 localStorage / 宿主接线 11 项）
- 运行：`node src/views/policy/panorama/FE-POL-01A.test.mjs`

## 测试结果（交付三绿）

| 门 | 结果 |
|---|---|
| 自检 ×2 | ✅ FE-POL-01A 全绿 + S01 `policy.test.mjs` 回归全绿 |
| `pnpm type-check` | ✅ 0 错（修复 22 处：缺失 .vue 页壳补齐 / IconShare→IconShareAlt / a-radio-button 换 a-radio / FieldDef import / words[0] 空串兜底 / operators[0] fallback / dropdown·checkbox Arco 事件签名） |
| `pnpm build` | ✅ built in 27.94s（policy chunk 97.81 kB / gzip 32.33 kB） |

**附录 D 防漏扫描**：互斥 display 叠加 0 / v-if+v-show 同节点 0 / USE_MOCK=false fixture 填数 0 / 新页菜单差集 0（01A 不建菜单，S01 已建）。

## 遗留风险

1. **04 表格视图**：demo 检索结果区含表格+卡片双视图中的「卡片」形态，本单以分组+列表先落（PolicyResultTable 行式）；若走查要求卡片形态，01B 或修订单补
2. **ExportFlowPanel 挂槽**：DoD 第 7 条提及，S01 未立项该组件、demo panorama 检索段亦无此面板实体——已按 demo 实际行为（dropdown 导出 + Message 反馈）落，无另造组件（ponytail：YAGNI，若需批量导出流程面板另立单）
3. **布尔提示卡位置**：demo 经 FilterPanel `prelude` prop 注入；Vue 化改为具名插槽，语义等价（FilterPanel prop 注入路径未用于本链路）
4. **契约未冻结**：数据走 S01 mock 双轨（`fetchPolicyPanorama`）；BE-POL-CONTRACT-01 定稿后统一替换，本单无新 api 面

## CI/CD（必填）

- 分支：`dev`（已推 `origin/dev`，走查通过后放行）
- commit：见下方双仓提交记录
- pipeline / K8s：CI 触发（push dev → Pipeline → K8s dev rollout）
- dev 验证命令：`node src/views/policy/panorama/FE-POL-01A.test.mjs && node src/views/policy/policy.test.mjs && pnpm type-check && pnpm build`

## 可观测性（建议）

- 交互埋点：`trackPolicyInteraction('panorama', …)`（page-mounted / open-detail / export；CustomEvent + createTraceId）
- pageview：路由 guard 自动覆盖（S01 机制）

## 涉及文件

**新增（17）**
- `src/views/policy/panorama/`：`FE-POL-01A.test.mjs`
- `search/`：`DisplayPolicySearchHub.vue`、`displaySearch.css`、`displaySmartParser.ts`、`displayPolicySearchConfig.ts`、`displaySearchResultUtils.ts`
- `search/advanced/`：`types.ts`、`queryEngine.ts`、`displayFieldLibrary.ts`、`FilterPanel.vue`、`ConditionBuilder.vue`、`DisplayAdvancedFilterPage.vue`、`DisplayAdvancedFilterPage.ts`、`advancedFilter.css`
- `components/`：`PolicyResultTable.vue`、`PolicyContentDetailDrawer.vue`、`ShareModal.vue`

**修改（1）**
- `src/views/policy/panorama/index.vue`（S01 骨架 → 检索主链路整段实装）
