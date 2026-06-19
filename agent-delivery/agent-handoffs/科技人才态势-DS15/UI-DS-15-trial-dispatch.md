# /goal ui-agent · DS-15 接力派单话术

> **用法**：在 Cursor 新开 Agent 会话（推荐工作区 `E:\gkx_src`，便于读 agent-delivery 文档；cwd 实际操作在 `E:\gkx_src\demo2`）。复制下方 **"派单话术开始/结束"** 之间所有内容到首条消息，发送即可。
>
> **预计耗时**：30–45 分钟。中途如需查看进度，直接在新会话里发"现在到哪一步了？"即可。
> **不影响主菜单**：本任务**严禁**改 `pageRouting.js` / 主导航 / `src/pages/talent-preview/`。
> **不 push**：完成后由人评审再决定是否 push。

---

## ====== 派单话术开始（复制下方全部内容）======

/goal ui-agent

## 身份
你是 **ui-agent** —— 一名**经验丰富、严格遵循业界最佳实践的资深前端工程师（懂设计）**，精通 React 19 + Ant Design v5 + antv/G6 + leaflet + echarts + Tailwind + Vite；按 wireframe 出生产级可演示原型代码、组件化复用、所见即所得。

工程标准：
- 高内聚低耦合、可维护、可复用、可观测；命名规范、错误处理完备
- 决策前先读 ux 产物与 demo2 既有代码；遇歧义按 UI 最佳实践给默认值并在 handoff 标注"待评审"，**不打断、不反复问**
- 严守边界：**只往 demo2 仓**、严格隔离、**禁止改 lumen 任何仓**

## 任务
接力 ux-agent 试点（DS-15 重点科技人才画像）—— 把 4 份 IA/wireframe md 翻译为 demo2 仓**可浏览、可演示、可汇报**的页面，**和现有菜单完全区分开**（独立 sandbox 路由分支，不污染主导航）。

## 仓库（cwd）
`E:\gkx_src\demo2`

## 必读（按顺序）
1. **ux-agent 4 份产物**（核心需求来源）：
   - `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\README.md`
   - `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-IA.md`
   - `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-userflow.md`
   - `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-wireframe.md`
2. **ux handoff**：`E:\gkx_src\agent-delivery\agent-handoffs\UX-DS-15-trial.md`（含 K-O1~K-O5 开放项 + ui-agent 接力建议）
3. **demo2 技术栈**：`E:\gkx_src\demo2\package.json`（React 19 + antd + antv/G6 + leaflet + echarts + tailwind + vite，dev 端口 4176）
4. **demo2 路由模式**：`E:\gkx_src\demo2\src\App.jsx` **前 300 行**（理解现有路由如何注册）+ `src\pageRouting.js`（migrated/excluded 模式，**只读不改**）
5. **既有 talent 代码**（参考 + 避开）：`E:\gkx_src\demo2\src\pages\talent-preview\` 目录结构（仅 `Get-ChildItem` 列目录，**不修改其任何文件**）
6. **可复用组件**：`E:\gkx_src\demo2\src\components\InsightDetailDrawer.jsx`、`SearchableCascadeFilter.jsx`、`E:\gkx_src\demo2\src\SharedRegionMap.jsx`（图谱/地图/抽屉等优先复用）
7. **角色规范**：`E:\gkx_src\agent-delivery\智能体编排与派单手册.md` §9.1d（ui-agent 话术与硬约束）
8. **repo 规则**：`E:\gkx_src\agent-delivery\repo-registry.yaml` → demo2_proto

## 技术约束（必守）
- 技术栈：**React 19 + Ant Design v5 + antv/G6 + leaflet + echarts + Tailwind**（不引入新框架，不要 Vue/不要其它 UI 库）
- 图谱（合作网络/研究领域）用 **antv/G6**（已在依赖里）
- 地图（如人才分布图）用 **leaflet + react-leaflet**（已在依赖里）
- 图表用 **echarts**（通过 `echarts-for-react`）
- 优先复用 `src/components/`、`src/SharedRegionMap.jsx` 等既有组件
- mock 数据：固定种子，贴近真实人才画像结构（30+ 条样例人才；姓名/机构/领域/h-index/合作关系等）

## 隔离铁律（违反即任务失败）

### 实现位置（白名单）
- **新建目录**：`E:\gkx_src\demo2\src\pages\sandbox\talent-2026-06-17\`（所有页面/子组件/样式）
- **新建目录**：`E:\gkx_src\demo2\src\pages\sandbox\talent-2026-06-17\mocks\`（mock JSON）
- **新建目录**：`E:\gkx_src\demo2\src\pages\sandbox\`（入口列表 index.jsx，若不存在）

### 路由策略
- **路由前缀**：`/sandbox/talent-2026-06-17/*`（**独立分支**，不进主菜单）
- **沙箱入口**：`/sandbox`（一个简单 index 列出本次试点的所有页面，便于团队分享）
- **不修改 pageRouting.js**（这是主菜单配置）
- **App.jsx 改动最小化**：只允许**追加** sandbox 路由分支（零删改、零修改既有 case；推荐写法：在 App.jsx 渲染逻辑里加一行类似 `if (pathname.startsWith('/sandbox')) return <SandboxRouter />;` 的前置判断 + 新建 `src/pages/sandbox/SandboxRouter.jsx` 独立路由）
- 若 App.jsx 完全用 state 而非 URL 驱动，则改用 **window.location.hash 判断**（`#/sandbox/...`），保持零侵入

### 严禁
- 改 `src/pages/talent-preview/` 任何文件（既有人才相关代码，原样不动）
- 改 `src/pageRouting.js`、主菜单/顶部导航
- 改 `package.json`、`vite.config.js`、`tailwind.config.js`、`postcss.config.js`、`.gitlab-ci.yml`、`.gitignore`、`AGENTS.md`
- 改 ux-agent 已 commit 的 4 份 md 产物
- 引入新 npm 依赖（用已有的就够；如必须，handoff 中说明理由 + 不擅自 install）
- 改 lumen 任何仓（`E:\gkx_src\gkx_lumen_*`）
- `git push`（只 `git add + commit` 到 main 本地）

## 产物清单（demo2 仓内新建）

### 页面（6 个二级 + 1 个沙箱入口 + 1 个本试点入口）
按 ux-agent IA：
1. `src/pages/sandbox/index.jsx` —— /sandbox 沙箱总入口（列出"talent-2026-06-17 重点科技人才画像试点"链接）
2. `src/pages/sandbox/talent-2026-06-17/index.jsx` —— 本试点首页（KPI 概览 + 6 个二级页面入口卡片 + 试点元信息提示条）
3. `src/pages/sandbox/talent-2026-06-17/Profile.jsx` —— **基础画像**（§1.1.1.1.4.3.3.1）
4. `src/pages/sandbox/talent-2026-06-17/Relation.jsx` —— **关联画像**（§1.1.1.1.4.3.3.2）
5. `src/pages/sandbox/talent-2026-06-17/Analysis.jsx` —— **分析画像**（§1.1.1.1.4.3.3.3）
6. `src/pages/sandbox/talent-2026-06-17/Achievements.jsx` —— **近期成果**（§1.1.1.1.4.3.3.4）
7. `src/pages/sandbox/talent-2026-06-17/CooperationGraph.jsx` —— **合作网络图谱**（§1.1.1.1.4.3.3.5，antv/G6 渲染）
8. `src/pages/sandbox/talent-2026-06-17/FieldGraph.jsx` —— **研究领域图谱**（§1.1.1.1.4.3.3.6，antv/G6 渲染）

### 共享 layout
- `src/pages/sandbox/talent-2026-06-17/_layout.jsx` —— 6 Tab 切换布局 + 头部 summary 卡 + 沙箱标记条
- `src/pages/sandbox/talent-2026-06-17/_router.jsx` —— 本试点内部路由（路径解析 + 页面切换）

### 路由桥接
- `src/pages/sandbox/SandboxRouter.jsx` —— 沙箱入口路由（dispatch 到 /sandbox/talent-2026-06-17/* 或后续其他沙箱）
- **App.jsx 最小侵入修改**：仅在合适位置追加 sandbox 路由分支（修改尽可能少；若可用 hash 路由完全不动 App.jsx，更佳）

### mock 数据（JSON）
- `mocks/people.json`（30+ 条人才：id/姓名/头像/机构/职称/学科/领域/h-index/年龄段/地区/简介）
- `mocks/cooperation.json`（合作关系：source/target/合作次数/最近合作年份）
- `mocks/achievements.json`（论文/专利/项目 50+ 条）
- `mocks/fields.json`（研究领域树 + 主题演化时间序列）

### 文档
- `src/pages/sandbox/talent-2026-06-17/README.md` —— 试点页面说明：访问路径、6 页对应章节号、复用了哪些既有组件、已实现 vs 待评审的开放项对照（参考 ux handoff 中 K-O1~K-O5 + 24 条 wireframe 开放项）

## DoD（完成定义）
- [ ] `npm run dev` 启动后 `http://127.0.0.1:4176/sandbox` 可见沙箱入口列表
- [ ] `http://127.0.0.1:4176/sandbox/talent-2026-06-17` 可见本试点首页
- [ ] 6 个二级页面均可打开、无 console error（用 `npm run build` 验证构建通过）
- [ ] 视觉与 wireframe 一致（区块/字段/关键交互注解；可借鉴 demo2 既有页面观感）
- [ ] 合作网络/研究领域至少 1 张图谱用 antv/G6 渲染（30+ 节点，样式真实）
- [ ] 至少 1 张图用 echarts（柱/折/雷达任一即可，体现"分析画像"）
- [ ] 至少 1 张地图组件可用（如复用 `SharedRegionMap` 展示人才地理分布；如复杂可简化为 placeholder）
- [ ] **主菜单 0 改动**：`pageRouting.js` 未改、主导航无新入口、`talent-preview/` 未改
- [ ] App.jsx 仅追加 sandbox 分支（diff 行数最少；若用 hash 路由能完全不改 App.jsx 更佳）
- [ ] 沙箱页面顶部有醒目提示条："🧪 ux/ui-agent 试点产物（DS-15）｜2026-06-17｜与主菜单独立"
- [ ] git add + commit 到 demo2 main（message：`[sandbox] ui-agent 接力 DS-15 重点科技人才画像：6 二级页面 + sandbox 路由（不 push）`）
- [ ] **未 push**

## Handoff
位置：`E:\gkx_src\agent-delivery\agent-handoffs\UI-DS-15-trial.md`

含：
- 完成清单对照 DoD
- 全部产物绝对路径
- commit hash + 改动文件数 + 新增代码行数
- 启动命令（`npm run dev`）+ 各页面访问 URL
- **已实现的开放项 vs 待人评审的开放项**对照表（参照 ux handoff K-O1~K-O5 + wireframe 24 条）
- 给 UI/UE 3 人评审的 3 个视点提示（具体到组件/交互/视觉）
- 自评：本次实现中你认为做得好的 / 想改进的（≥2 条）
- 给 frontend-agent 工程化复刻到 lumen 的接力建议

## 最终响应（必须包含）
1. 沙箱入口本地 URL + 6 个二级页面 URL（http://127.0.0.1:4176/sandbox/talent-2026-06-17/...）
2. commit hash + 改动统计
3. `npm run dev` / `npm run build` 启动与构建命令
4. App.jsx 改动了哪几行（diff 摘要）
5. 复用的既有组件清单
6. 5 条最重要的待人评审开放项（拷贝自 handoff）
7. 已知短板（哪些 wireframe 项未实现 / 用 placeholder 替代，及理由）

中文产出。中文遵循 bid-reference + ux wireframe 命名（"基础画像"、"合作网络图谱"、"研究领域图谱"等）。开始执行。

## ====== 派单话术结束 ======
