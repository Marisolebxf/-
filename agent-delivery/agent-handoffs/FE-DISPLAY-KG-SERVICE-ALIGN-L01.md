# FE-DISPLAY-KG-SERVICE-ALIGN-L01 — UI handoff

> 任务 ID: FE-DISPLAY-KG-SERVICE-ALIGN-L01  
> Epic: E-DISPLAY-ALIGN  
> 执行 Agent: `agent:ui-agent`  
> 监管人: `human:郭万迎`  
> 认领类型: `coordinator_dispatch`  
> 日期: 2026-08-09  
> 状态: review（待 coordinator 验收；含 2026-08-09 监管反馈补齐）

### 监管反馈补齐（同日）

1. **多维条件筛选**：对齐需规——年/月、数据类型（论文/专利/项目/专家/机构/成果）、业务线、发布人、标签多选  
2. **结果缩略图**：网格/缩略图/列表增加 SVG 示意小图（关系网/桑基/柱/表/报告），不再是空色块  
3. **智能数据建模与图谱生成**：实体类型勾选+自定义、标签/关系自定义、AI 抽取表、步骤条、网络图生成（AI 深度仍演示级）

---

## 1. 范围与实现

### 1.1 目标

按需规 §1.1.1.1.4.5.4，策略 A **原地更新**「科技知识图谱 → 服务展示」主路径，覆盖图分享 / 图查询 / 图分析集成叶子能力，并完成符合度三态清单。

### 1.2 硬边界核对（白名单）

| 允许 | 实际改动 | 结果 |
|---|---|---|
| `ServiceDisplay.jsx` | 重写服务展示工作台 | ✅ |
| `mockData*`（本页相关） | 扩展分享/查询/集成 Mock | ✅ 未删其他页数据 |
| `style.css`（服务展示相关） | 新增 `.kg-service-page` 作用域样式 | ✅ 未改其他模块类语义破坏性逻辑 |
| 菜单/路由 key `knowledge-graph-service` | 未改 `App.jsx` / `pageRouting.js` | ✅ |
| 禁止 Analysis/Indicator/Algorithm / 科技成果 / 科技服务全景 | 未触碰 | ✅ |

### 1.3 实现要点

- **图分享**：一键分享 Modal、四格式导出、链接权限、嵌入代码、历史撤回、同步通知开关（演示）
- **图查询**：联想搜索、多维筛选、列表/网格/缩略图、详情 Drawer、历史收藏与复用
- **图分析集成**：多源接入卡、建模演示、ECharts 五类图、实时监控开关、决策联动表、审计日志
- **D9**：KPI 挂 ⓘ +「演示数据」Tag；NLP/真实时/跨系统能力 Alert/Badge 标注
- **视觉**：沿用本页既有 AntD 栈（历史兼容）；主色对齐 `#165DFF`

---

## 2. 产物清单

| 产物 | 路径 |
|---|---|
| 页面 | `repos/demo-ui-science/src/pages/tech-knowledge-graph/ServiceDisplay.jsx` |
| Mock | `repos/demo-ui-science/src/pages/tech-knowledge-graph/mockData.js` |
| 样式 | `repos/demo-ui-science/src/pages/tech-knowledge-graph/style.css` |
| 符合度清单 | `gkx-orchestration/docs/符合度评估-科技知识图谱-服务展示.md` |
| 截图 | `agent-delivery/agent-handoffs/evidence/FE-DISPLAY-KG-SERVICE-ALIGN-L01/*.png` |
| 截图副本 | `repos/demo-ui-science/docs/evidence/FE-DISPLAY-KG-SERVICE-ALIGN-L01/*.png` |

入口：`#/topic/服务展示` → `knowledge-graph-service`

---

## 3. 偏离说明

| 项 | 偏离 | 原因 / 处置 |
|---|---|---|
| 组件库 | 未迁 Arco，保留 AntD | 任务允许历史兼容；同页不混搭 |
| NLP 智能搜索 | 模糊匹配 + 联想词 Mock | 数据策略：演示级并标注 |
| 实时同步/监控 | Switch + 文案演示 | 非真实时流 |
| 跨系统决策联动 | 前端模拟触发 | 禁止越层真实集成 |
| 文件真实导出 | message 演示 | 演示仓无文件服务 |

---

## 4. 验收证据

- `npm run build`：✅（vite build，约 51s）
- 符合度：17 叶 **✅11 / 🟡6 / ❌0**（详见符合度文档）
- 截图：01-share / 02-query / 03-integration

### Design.md §14 自检（14 条）

| # | 项 | 结果 |
|---|---|---|
| 1 | 浅色蓝白工作台 | ✅ |
| 2 | Header/侧栏由 App shell 提供；本页为 content 工作区 | ✅ N/A 本叶不改壳 |
| 3 | 选中态 `#165DFF` / 浅蓝底 | ✅ |
| 4 | 表单/按钮接近 Arco 节奏（高度约 32） | ✅ 沿用 AntD middle/small |
| 5 | 工具栏尺寸克制 | ✅ |
| 6 | empty/disabled/loading/error | ⚠️ 空结果文案有；无独立 error 页（演示页可接受） |
| 7 | 图表色走 §4.3 序列 | ✅ |
| 8 | 无霓虹/营销 hero/无意义 emoji | ✅ MockBadge 用图标+文案 |
| 验1 | 首屏像分析工作台 | ✅ Tab 工作台 |
| 验2 | Header 高度 | ✅ N/A（壳层） |
| 验3 | 侧栏宽度 | ✅ N/A（壳层） |
| 验4 | 控件约 32px | ✅ |
| 验5 | 主色接近 `#165DFF` | ✅ |
| 验6 | 本页无新增 antd 以外依赖；历史页保留 antd | ⚠️ 本页仍为 antd（策略兼容，非新栈违规） |

**合计**：✅ 11 / ⚠️ 3（已说明） / ❌ 0

---

## 5. 架构合规自检

- ✅ 仅 demo-ui-science 演示页；未改 lumen 仓
- ✅ 未接真实 API / 未越层实现 NLP/流式/跨系统
- ✅ 未改 package.json / vite 配置 / App 路由 key
- ✅ Commit 含 `[agent:ui-agent]`；未 force push
- ✅ touched_files 白名单核对通过

---

## 6. 开放项

1. 分享鉴权与真实文件导出 → 正式仓
2. 语义检索 / 实时流 / 业务 webhook → 算法 + 集成
3. 审计中心对接

---

## 7. 请 coordinator 验收

请 `coordinator` 按 DoD 五条复核后将 registry 置 `done`。监管人：`human:郭万迎`。
