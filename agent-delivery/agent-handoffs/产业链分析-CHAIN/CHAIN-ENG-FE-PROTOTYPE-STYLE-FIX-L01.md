# CHAIN-ENG-FE-PROTOTYPE-STYLE-FIX-L01 · 产业链 demo 原型条件栏样式修复

## 任务与认领

- parent：`CHAIN-HZW-THREE-TRACK-L01`
- 来源：`CHAIN-ENG-PAGE-MATRIX-L01` 原型差 P0
- 仓库：`repos/demo-ui-topic`
- claimed_by：`agent:frontend-agent`
- supervised_by：`human:李伟`
- ponytail：`full`

## 范围与实现

本叶只修产业链分析页共享条件栏的布局、折行和对齐问题，不夹带 Java/API、算法或 Mock 数据接入。

1. `IndustryAnalysisScopeFields` 控件宽度改为跟随字段容器，移除多选产业私有 `400px` 宽度分叉。
2. 共享 `.policy-analysis-filter-row__field` 固定 `304px`、上限 `400px`，`flex: 0 0 auto`：空间不足时整字段换行，禁止横向挤压重叠。
3. 标签最多两行；Select/Cascader/Picker/Input 跟随字段容器，长值不再撑破同行布局。
4. 全景页移除 `align-items:flex-end` 私有覆盖；“开始分析”动作槽按标签行后的 32px 控件行对齐，不受 help 文案高度影响。
5. 深圳对比/发展页去掉内联 304px；标杆 Cascader 不溢出列；「主体区域」只读框收窄为 120px。
6. 增加最小布局契约测试 `tests/industry-analysis-filter-layout.test.mjs`。

符合 `Design.md §7.2`：字段间距 16px、控件最大宽度 400px、空间不足时整字段换行且不横向溢出；符合 D10 §5.1：标签在控件上方。

## 产物

- `src/app/components/filter/filterControls.css`
- `src/app/pages/industry-center/IndustryAnalysisScopeFields.tsx`
- `src/app/pages/industry-center/industryTopicAnalysis.css`
- `src/app/pages/industry-center/IndustryShenzhenPage.tsx`
- `src/app/pages/industry-center/industryDiagnosis.css`
- `tests/industry-analysis-filter-layout.test.mjs`

## 验收证据

- `node --test tests/industry-analysis-filter-layout.test.mjs`：PASS，4/4。
- `npm run build`：PASS，Vite 生产构建成功；仅保留既有大包告警。
- IDE lint：PASS，无新增诊断。
- `git diff --check`：PASS。
- 本地 Chrome headless 实测：
  - 1680 / 1440 / 1280：集群、产业、产业链、数据截至保持一行，标签与控件基线一致。
  - 1100：前三字段保持一行，“数据截至”作为完整字段换到下一行；未发生标签与控件拆行或横向溢出。
  - 截图：`%TEMP%/gkx-panorama-{1680,1440,1280,1100}.png`。
- `npm run design:check`：FAIL，仍为修复前已存在的 `theme.css must include padding: 18px 16px 20px`；本叶未修改 `theme.css`，与条件栏修复无关。

## Design.md §14 与 D10 自检

- ✅ 使用现有 Arco `Form.Item` / `Select`，未引入私有控件或新依赖。
- ✅ 控件高、色彩、间距、圆角未改；最大宽度仍为 400px。
- ✅ 标签位于控件上方，整字段响应式换行，未制造横向滚动。
- ✅ 键盘、焦点、禁用、校验 help 和 `aria-label` 语义未改变。
- ✅ 未触碰指标 ⓘ / D9 评审层、可观测性和调用链。
- N/A：本叶不新增导航、Tab、地图交互或统计指标。

## 架构合规与偏离

- ✅ 前端仍未直连 Python/DB。
- ✅ 未新增依赖，未修改配置文件。
- ✅ D8/D10 相关修复集中于既有共享样式与组件。
- ✅ D12 不涉及 lumen 正式仓或 demo 服务调用变更。
- 偏离：在线 demo 发布前仅本地 Vite 实测；`10.50.69.111:30892` 为 Java 网关，本叶不改。

## Cost

- actual_tokens：`50000`（会话估算；Cursor 未提供精确计量）
- model_used：`Auto`
- actual_cost：`0`（本地会话未暴露可归集 API 成本）
- cost_warn：`false`

## 开放项

1. 仓级 `design:check` 的既有 `theme.css` padding 契约失败需另叶处理。
2. 在线 demo 发布后补同路径四宽度截图，确认部署环境字体与本地一致。
3. 其他八页内容/API/Mock 缺口仍归 `CHAIN-ENG-FE-GAP-FIX-L01` / Java 修复叶，不在本叶范围。
