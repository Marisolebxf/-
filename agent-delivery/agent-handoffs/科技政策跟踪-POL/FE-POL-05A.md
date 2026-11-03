# FE-POL-05A · 智能政策拆解整页复刻 — Handoff

- **task-id**: FE-POL-05A
- **claimed_by**: agent:frontend-agent
- **supervised_by**: human:孔东
- **repo / worktree**: `lumen-ui-science-pc` · `D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol05-parse`（分支 `feat/pol05-parse`，基点 f4edea4）
- **ponytail**: full
- **日期**: 2026-11-02
- **状态**: 完工停本地 worktree，等人工验收（⚠️ 用户裁定 2026-10-20：严禁自动 commit/push）

## 1. 范围与实现（DoD 对照）

demo 真源：`repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx` PolicyParse 段（L692–1051）+ `policyPcData.js` 共享种子（只读对照，零 import/merge）。

| DoD | 实现 | 状态 |
|---|---|---|
| 1. 政策选择器 + 文本三态 | `a-select`（allow-clear/allow-search，420px，label=标题+textType+level）；textType 经 `resolveTextType`（显式优先，level 推导 国家级→国家 / 海外→海外 / 其余→地方），元信息卡 `a-tag` 呈现 | ✅ |
| 2. 四能力 Tab | demo `WorkbenchTabs` → 仓内既有 `PageTabFrame`（与 01A/02A 同款映射，`equal-width`）；`DECOMPOSE_CAPS` 四条描述**逐字照搬**（`parseLogic.ts`） | ✅ |
| 3. 条款树 + 5 类色标 | `a-tree` 递归（`show-line` + `default-expand-all`）+ `#title` 插槽渲染色标 `Tag`（政策目标 blue/扶持措施 green/保障机制 cyan/责任主体 purple/细则 gold）+ `depth>=2` 款/项金标；聚合标签 `collectClauseTypes`（排除细则）四类 ✓ | ✅ |
| 4. 关键指标提取 | `METRIC_KIND_ORDER` 四类分组表（`a-table`：指标/值/单位/维度/指标库列）+「其他」兜底；`alignMetricsToLib` 对齐种子 `planningMetricLib`（已对齐/未入库列）；**就绪闸门**：指标库开关关闭 → GateEmpty「未完成标准化政策指标库搭建…」 | ✅ |
| 5. KG 绑定 + 基库联动 | `kgBound` 开关（关 → GateEmpty）；`graphReady = hasPolicy && kgBound && completeness.complete`；ECharts graph 力导向（VChart，280px 显式高度，force repulsion 180/edgeLength 80 照搬）；实体清单四类 `ENTITY_CATS`；残缺时 warning Alert 列 missing；**指标库开关与 04A 共享 `BASE_READY_KEY`**（sessionStorage `display-policy-base-ready`，`loadBaseReady/saveBaseReady` 种子函数，跨页联动语义） | ✅ |
| 6. 空态闸门三级 | 无政策 → 整页 GateEmpty「未选择政策 / 未提供政策文本…」；无文本 → semantic 卡内「未提供政策文本，不可做语义解析」；无条款 → clause 卡内「未具备政策内容，不可拆解条款」（档 C 语义） | ✅ |
| 7. Arco 化 + D9 | demo 原生 Select/Table/Tree/Statistic 全部 Arco 等价；KPI 三卡经 `PolicyStatCard`（力度指数 M_POLICY_INTENSITY_INDEX ⓘ+QPOL-02、关联度 M_POLICY_RELATION_DEGREE ⓘ+QPOL-03、拆解完整度）；🧪 经 MockBadgeInline（见 §3 说明）；评审层 `useReviewStore` 自闸（核增/分轨横幅/开关组 reviewMode 才渲染，DOM 零泄漏） | ✅ |

### 页面结构

- 头部：标题 + 副题（评审态）+ 开关组（指标库已搭建 / 结合知识图谱）+ 政策选择器 + 「送入多维对比」
- `sendToCompare`：写展示侧会话槽（`loadCompareSlots/saveCompareSlots`，≤4，不足 2 补默认）+ `router.push({name:'policy-compare-upgrade'})` + 观测埋点
- ChainSteps（治理→拆解→对比→研报，current=1 高亮「拆解」）——**04A 正式件 `PolicyChainSteps.vue` 交付前内联同语义占位**（a-steps 版），见 §3 开放项
- 观测埋点：`trackPolicyInteraction('parse', 'page-mounted' | 'send-to-compare', …)`

## 2. 产物清单

| 文件 | 说明 |
|---|---|
| `src/views/policy/parse/index.vue` | 整页（页壳骨架 → 475 行整页；双 script 块：setup 主逻辑 + options 导出 `MockBadgeInline`） |
| `src/views/policy/parse/parseLogic.ts` | 纯逻辑（demo L83–130/208–228/711–719 照搬：色标/四能力/四类/collectClauseTypes/resolveTextType/mapClauseTree/groupMetricsByKind） |
| `src/views/policy/parse/parse.test.mjs` | 最小自检（语义/锚点/闸门/样式隔离/种子只读消费） |
| `src/views/policy/styles/demo-policy-pc-pages.css` | 追加 `pol-parse-` 前缀段 14 类（与 04A 追加段类名隔离；自检断言无 `pol-gov-` 交叉） |

**零触碰**（冲突预防承诺兑现）：`menu.ts` / `api/policy.ts` / `policyPcSeed.ts` 种子 / 04A governance 目录 / `PolicyChainSteps.vue` 正式件 / `PolicyStatCard` 公共件。

## 3. 偏离与开放项

1. ~~**ChainSteps 占位**~~ **已闭合（2026-11-03）**：04A 正式件 `PolicyChainSteps.vue` 已并入 dev（352717d）；05A 合并前已替换占位为正式件消费（`current="parse" next="compare"`，自检断言同步更新）。
2. **MockBadgeInline 内联件**：demo 各 Card title 内嵌 `<MockBadge />`；lumen 公共件 `@/components/lineage/MockBadge.vue` 样式经 scoped + 类名 `.mock-badge` 输出，在 `a-card` `#title`/`#extra` 插槽内使用时 scoped 样式不跟随（裸样式风险，复刻铁律「封装组件样式自含」反向约束），故本页内联同语义最小件（Tag arcoblue + IconExperiment + 「演示数据」）。若后续第 2 处出现（06A/07A），上提 `policy/components/` 公共件。
3. **KPI 副文案位置**：demo 副文案在 Statistic 卡内（`由标准化 metrics[] 折算`）；lumen `PolicyStatCard` 为冻结公共件不可改，副文案以卡下备注行（`.pol-parse-kpi-note`）承载，视觉语义等价。
4. **浏览器走查受环境限制**：本机浏览器为多并行会话共享（04A/06A/07A worktree 同跑走查），标签被高频抢占、截图通道失效（截图全灰）。已用 **SFC 编译等价验证**（vue/compiler-sfc 双 script 块 + 模板严格编译通过）+ build 产物 + 自检锚点兜底；**建议人工验收时以 `pnpm dev` 起本 worktree 走查**（评审模式 `?review=1`），重点看：四能力 Tab 切换、条款树三级展开、指标库开关关闭的闸门、KG 开关、送入对比跳转。

## 4. 验收证据（三绿）

- `node src/views/policy/parse/parse.test.mjs` → `parse 整页自检全绿（纯逻辑语义 / 页面锚点 / 闸门三级 / 开关联动 / 样式前缀隔离 / 种子只读消费）`
- `node src/views/policy/policy.test.mjs` → 基座自检全绿（种子冻结/菜单/双轨/D9 镜像/页壳/权限/评审层——本单未破坏基座）
- `pnpm type-check`（vue-tsc --build）→ exit 0
- `vite build` → `✓ built in 25.24s`（注：`pnpm build` 的 `run-p` 在 worktree junction 下 `.bin` shim 解析失败，属环境问题非代码问题；直接调用等价命令通过）
- dev server（mock 态 3117）启动无编译错误、依赖优化完成（走查受限见 §3.4）

## 4.1 合并记录（2026-11-03 · 监管人指示）

- worktree commit `a5204ef` → `--no-ff` 并入本地 dev（merge `1263ec9`），无冲突（04A ChainSteps 正式件与 05A 追加 CSS 段自动交汇）
- **ChainSteps 占位已替换为 04A 正式件**（`PolicyChainSteps current="parse" next="compare"`；同步删 `gotoCompare`/`IconRight` 死代码，自检断言更新）
- dev 态三绿复验：`parse.test.mjs` ✅ · `policy.test.mjs` ✅ · `pnpm type-check` ✅ · `vite build` 35.4s ✅
- 清理：worktree `lumen-ui-science-pc--pol05-parse` 已移除（含残留 vite 子进程 PID 7600 终止）；分支 `feat/pol05-parse` 已删
- **未 push origin**（dev 停本地，等签收节奏统一推）

## 5. 架构合规自检

| 铁律 | 状态 |
|---|---|
| D8 Design（Arco 优先/主色 #165DFF/控件 32px） | ✅ 全 Arco 控件；主色经 token 与既有 css |
| D9 指标 8 件套 + 四维 | ✅ ⓘ 经 PolicyStatCard→PolicyMetricSpecTrigger→policyMetricsMirror.gen（35 条镜像真源）；🧪 MockBadge；QPOL ⚠️ PendingBadge；评审关闭零泄漏 |
| D10 交互规范 | ✅ a-tree 键盘可达（Arco 内建）；开关/选择器均有禁用态 |
| D12 demo 隔离 | ✅ 零 import demo 产物；只读对照重写 |
| 观测埋点 | ✅ trackPolicyInteraction 2 处 |
| Mock 种子冻结 | ✅ 只读 import policyPcSeed（自检断言页面无种子复制） |
| 完工停本地 | ✅ 未 commit / 未 push（等监管人验收） |

## 6. cost

- actual_tokens: ≈ 150k（含真源阅读/实现/三绿/走查尝试）
- model_used: claude-sonnet-4.5
- actual_cost: ≈ $3.2
- cost_warn: green
