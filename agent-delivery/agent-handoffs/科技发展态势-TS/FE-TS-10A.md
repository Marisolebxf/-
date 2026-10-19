# FE-TS-10A 科技发展态势 · 维护管理 demo→lumen 复刻

- **任务**：FE-TS-10A（认领/监管：human:孔东）
- **日期**：2026-10-19
- **强度**：ponytail full
- **仓**：`repos/lumen-ui-science-pc`（origin/dev，已提交 push）

## 1. 范围与实现（对照 demo 源）

demo 源：`repos/demo-ui-science/src/pages/tech-situation-maintain/`（5 JSX + 4 state JS + 3 test.mjs + css，已逐文件读完核对）。

| 分区 | demo 源 | lumen 实现 |
|---|---|---|
| 页壳 + 四分区 nav + entries | `TechSituationMaintainPage.jsx` | `src/views/situation/maintain/index.vue` |
| 图层与数据源配置 | `LayerSourcePanel.jsx` | `components/LayerSourcePanel.vue` |
| 科创要素图层识别（跨页） | `FactorIdentityPanel.jsx` + `factorDisplayState.js` | `components/FactorIdentityPanel.vue` + `src/stores/factorDisplay.ts` |
| 维护技术图谱 | `GraphMaintainEditor.jsx` | `components/GraphMaintainEditor.vue` |
| 关键实体与关系维护 | `EntityRelationPanel.jsx` | `components/EntityRelationPanel.vue` |
| 三状态机 | `layerSourceState.js` / `graphMaintainEditorState.js` / `entityRelationState.js` | `maintainModel.ts`（逐函数移植，签名差异见 §3） |
| 页样式 | `techSituationMaintain.css` | `techSituationMaintain.css`（冻结移植，见 §3 差异 3） |
| 通用弹窗 | demo `maintain-dialog` 结构 ×4 处 | `components/MaintainDialog.vue`（一处封装四处复用） |

接线：
- 菜单/路由：`src/router/menu.ts` 增 `tech-situation-maintain`（trend 组第 10 项，`fullBleed: true`）。
- M2 全景「维护技术图谱」入口：`panorama/index.vue` 由仅打点改为跳转本页 `query.section=graph`（demo `openGraphMaintain` 语义）。
- M1 跨页联动：`overview/index.vue` 消费 factorDisplay store，覆盖 `mapResult.factorItems + legend`（demo `getFactorLabel/getFactorColor` 全局消费语义；覆盖点选在数据源头，图例/marker/下拉/要素比较页签全部下游自动生效；恢复默认还原原始快照）。
- mock/api：`mock/modules/maintain.ts`（`tsMaintainMeta` 注册）+ `api/situation/maintain.ts`（defineApi 双轨，real 走 `/situation/v1/maintain/meta`）。

## 2. Arco 化执行（对齐用户裁定与经验清单）

- demo 原生 `select`/`input`/`textarea`/`number` → `a-select`/`a-input`/`a-textarea`/`a-input-number`（MaintainDialog 声明式 fields 统一渲染，32px 控件高）。**零原生控件回退**。
- 唯一例外：`input[type=color]` 保留原生 —— **Arco Design Vue 无颜色选择器组件**，原生 color input 是该控件标准形态（demo 同款，非回退）。已在代码注释标注。
- `window.confirm` ×5 → `a-modal` 二次确认（删除数据源/图层组/节点/关系/批量删实体）。
- checkbox → `a-checkbox`；图标显式 import（`@arco-design/web-vue/es/icon`）。
- 弹窗 `Teleport`：a-modal 自带 body 挂载，无需手动 Teleport。

## 3. 偏离说明（as-built，均有理由）

1. **seq 计数器闭包化**：demo 用模块级可变计数器（有重置陷阱）；lumen 改 `createMaintainSeqs()` 工厂（`maintainModel.ts`），页面持有、重置演示时重建（index.vue `resetGraphMaintain`），语义等价、可重放。
2. **mock import views 例外**：`mock/modules/maintain.ts` import `maintainModel.createInitial*`（仓内惯例是 mock 不 import views，situation.ts 为此复制种子）。裁定：种子真源唯一（600 行 demo 冻结数据），复制双份必漂移；已用 `ponytail:` 注释标注偏离。
3. **CSS 按钮/输入规则不移植**：demo css 中 `td button` / `input,select` 全局规则随 Arco 化失效（由 Arco 默认 token 承担：主色 #165DFF、控件高 32px、圆角 4px）；结构类样式（页壳/nav/panel/画布/版本列表）原值冻结。
4. **fullBleed 壳滚动适配**（监管人两轮走查反馈收敛，最终裁定）：demo 页根 `min-height: calc(100vh - 64px)` 适用 demo 的 `.figma-page` 滚动壳；lumen 的 fullBleed 壳（`layout.css` `.content-shell--flush`）为**固定高 + overflow:hidden**。最终模式（监管人裁定）：页根 `height:100%; overflow:hidden; grid-template-rows:auto minmax(0,1fr)` 锁高不滚，滚动收在**内容区自身容器**（`__content` `min-height:0; overflow-y:auto`），页头与左侧分区导航固定。首版「页根 overflow-y:auto 整页滚」被监管人否决（要求固定布局、内容区独立滚动）。教训入经验清单。
4. **pp-l6-section-title**：demo 全仓无 CSS 定义；01A–09A 已确立 sr-only 无障碍标题约定，本页 9 处同款补齐（demo JSX 中该类元素原样保留）。
5. **写操作不落库**：demo「Mock 可点」同语义，状态在页面 ref；BE 写接口契约未定（不替 BE 拍板），待扩展。

## 4. 产物清单

- 新增：`src/views/situation/maintain/`（index.vue + techSituationMaintain.css + maintainModel.ts + maintain.test.mjs + components/ ×5）
- 新增：`src/stores/factorDisplay.ts`、`src/types/maintain.ts`、`src/api/situation/maintain.ts`、`src/mock/modules/maintain.ts`
- 修改：`src/router/menu.ts`、`src/mock/register.ts`、`src/views/situation/panorama/index.vue`（入口接线）、`src/views/situation/overview/index.vue`（M1 联动）

## 5. 验收证据

- `pnpm type-check`：0 错误（vue-tsc --build）
- `node --experimental-strip-types src/views/situation/maintain/maintain.test.mjs`：ok（demo 三测试断言语义摘选：layerSource 10 项 / graphMaintainEditor 15 项 / entityRelation 10 项）
- 回归：07A/08A/09A 三套测试全过（42+55+种子一致性）
- `pnpm build`：✓ built（18–25s，无新增 chunk 告警类型）
- **浏览器走查**（监管人反馈修复后，dev server localhost:3001）：分区1 全内容可滚——点击页面末行「成果」显示名输入框，浏览器滚动嵌套容器成功聚焦 `[active, focused]`，底部不再被壳裁切

## 6. 架构合规自检

| 铁律 | 状态 |
|---|---|
| D8 Arco 栈 / #165DFF / 32px / 4px | ✅（§2） |
| demo→lumen 复刻禁另起 UI | ✅ 逐 JSX 核对（含 aria-label 逐字：`实时数据监控`/`维护技术图谱假编辑器`/`实体及关系批量管理`/`基础信息查看功能` 均按 demo 原文冻结） |
| Arco 组件禁回退原生 | ✅（color input 为无对应组件例外，已标注） |
| 多处组件及时封装 | ✅ MaintainDialog（4 弹窗复用） |
| 弹窗 Teleport body | ✅ a-modal 内建 |
| SVG 画布显式高度 | ✅ 420px（demo 同值） |
| 首屏同步初值防白屏 | ✅ index.vue 本地种子先行，mock 到达覆盖 |
| defineApi 双轨 / USE_MOCK=false 禁 fixture 填数 | ✅ real 分支走网关，无 fixture |
| 可观测埋点 | ✅ `ts-maintain-track` CustomEvent + createTraceId（section-change/entry-jump）；M2 open-graph-maintain 打点保留 |
| D12 不 merge demo / 不调 demo 服务 | ✅ 对照重写 |
| git 纪律 | ✅ `[agent:frontend-agent]` 提交 push `origin/dev`（不含本地 `.env.development` 开关） |

## 7. 开放项 / 风险

- BE `/situation/v1/maintain/*` 契约未定（写接口）：演示态在页面内存，刷新丢失 = demo 同语义。
- localStorage key：`lumen-ui-science-pc:factor-display-v1`（demo 为 `demo-ui-science:factor-display-v1`，跨系统不共享，符合隔离预期）。
- M2 全景跳转用 `query.section=graph`；若后续全景页自身有 section 状态管理可再对齐。

## 8. cost

- `actual_tokens`: ~（由监管人按会话记录回填）
- `model_used`: glm-5.3（Cursor agent）
- `actual_cost`: ~$（同上）
- `cost_warn`: false
