# FE-DISPLAY-ACHIEVE-ALIGN-L01 · 展示系统合规对齐-科技成果展示

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 锁定窗口 | 2026-08-07 20:42 +08:00 起 24h |

## 背景与范围

QA 复核（`agent-delivery/agent-handoffs/展示对齐-DISPLAY/科技信息展示系统_原型与需求规格功能符合度评估表.md`，2026-07-29 备份版去重后）发现科技成果展示模块对需规存在差异（#460/478/479/499 等）。产品设计决策：**不改动现有 5 个页面**，参照科技发展态势核查标准，在科技成果展示菜单下新增 5 个 New 后缀页面按 `bid-reference` §1.1.1.1.4.6 重实现。科技抗疫主题报告已核减（甲方确认删除），不在范围。

## 问题清单（符合度核查基线，DoD-1）

详见 `agent-delivery/agent-handoffs/展示对齐-DISPLAY/符合度评估-科技成果展示.md`。20 项五级功能：✅7 / 🟡13 / ❌0。优先缺口：软科学案例推荐组件未挂载、难题热点 Treemap 未接线、互动推送/多渠道传播缺失、无独立进展监控中心；时空演进 hotspotAlerts 数据备而未用、范围非全球、缺主题演化路径；孵化载体缺政策申报流程与咨询互动；创新生态缺协同动态推送与独立影响力评估；仪器共享缺机构分类地图。

## 范围与实现

对照 `bid-reference` §1.1.1.1.4.6（3233–3754 行）：科技成果展示 5 子功能（软科学成果展示 / 科技创新生态展示 / 科技时空演进展示 / 大型科学仪器共享 / 创新载体孵化载体）、20 项五级功能、约 90 个叶子功能点。实现方式：新增 `src/pages/achievement-preview-new/` 5 个 New 页面 + 菜单/路由接线，现有 5 个旧页面零改动。各页面对五级功能的落点明细见下「修改内容」与各实现子任务记录。

## 修改内容（仓：demo-ui-science，分支 dev）

1. **符合度核查**：5 子功能 × 20 五级功能逐项三态核查，落盘上述评估文档
2. **新增 `src/pages/achievement-preview-new/`**（21 个新文件，+9241 行）：
   - `_shared/AchievementNewShared.jsx`：NewPageShell / SectionCard / KpiTile / MockBadge / MetricInfo（D8 token + D9 角标）
   - `soft-science-new/`：软科学 New（需规 a–g 七项五级功能全落点：GIS 多层级+热力、多维筛选+筛选方案持久化、案例推荐（补齐旧页未挂载缺口）、难题热点图（补齐未接线缺口）、互动传播中心、导出追溯+多角色报表、独立进展监控中心）
   - `innovation-ecosystem-new/`：创新生态 New（载体地图+增量、人才态势、协作网络+协同项目动态推送+影响力雷达）
   - `space-time-evolution-new/`：时空演进 New（全球范围时间轴播放/回放、热点自动识别+预警卡+一键导出（补齐 hotspotAlerts 缺口）、主题演化路径、流动追踪+协作网络）
   - `instrument-sharing-new/`：仪器共享 New（需规真实口径 KPI：入网 9262 台套/共享率 60.59%/有效订单 1336；三态着色地图+聚合、预约订单追踪、**机构分类地图**（补齐缺口））
   - `incubation-carrier-new/`：孵化载体 New（分布全景+多媒体、入驻企业成长轨迹、**政策申报流程/材料管理+咨询互动**（补齐缺口）、绩效监控）
3. **接线**（仅追加，不改旧逻辑）：`src/data.js` 菜单 +5 个 New 条目；`src/App.jsx` +5 个 topic 判断与组件分发
4. **修复**：`IconRise` → `IconArrowRise`（Arco 图标包不存在 IconRise，构建报错）

## 偏离说明

1. 需规中的 NLP 语义检索 / 机器学习挖掘 / 真实时数据流（如软科学语义检索、时空演进实时动态、政策自动归集）按团队数据策略（ADS 先行、Mock 填充）以演示级实现并挂 🧪/ⓘ 角标，未做真实算法——属有意偏离，上线前由 lumen 正式仓 + Python 算法层落地。
2. 仓级 git 策略登记为「demo-ui-science main 直推」，但远端默认分支 HEAD=dev 且本地工作分支为 dev，本次按现状 push origin/dev（commit eb7f566）；as-built 以 dev 分支为准，若 demo 站跟踪 main 需 coordinator 确认发布轨。
3. ~~页面运行时逐页截图未自动化~~ 已解决：commit 3adad4b 为 App 增加 `#/topic/<name>` URL 直达，5 页整页截图已产出（docs/evidence/）。仓内仍无 e2e runner，交互回归留给 QA testing 阶段。

## 产物清单

| 产物 | 位置 |
|---|---|
| 5 个 New 页面（19 个新文件，+9241 行） | `demo-ui-science/src/pages/achievement-preview-new/` |
| 菜单/路由接线 | `demo-ui-science/src/data.js`、`src/App.jsx` |
| 共享组件（D8 token + D9 角标） | `achievement-preview-new/_shared/AchievementNewShared.jsx` |
| 符合度核查清单（DoD-1） | `agent-delivery/agent-handoffs/展示对齐-DISPLAY/符合度评估-科技成果展示.md` |
| 评估表 md（xlsx 转换，抗疫核减已删） | `agent-delivery/agent-handoffs/展示对齐-DISPLAY/科技信息展示系统_原型与需求规格功能符合度评估表.md` |
| 首屏渲染截图 | `demo-ui-science/docs/evidence/home-default.png` |
| commit | `eb7f566`（origin/dev，[agent:frontend-agent]） |

## 验收证据

- `npm run build` ✅（vite 6.4.3，built in 1m7s，5 个 New 页面全部编译进 bundle）
- `npm run dev` ✅ http://127.0.0.1:4176 HTTP 200
- **5 个 New 页面整页截图** ✅（`demo-ui-science/docs/evidence/new-*.png`，Edge headless 经 `#/topic/<名称>` 直达截取）：软科学（高德瓦片+热力+节点弹窗）、时空演进（世界地图+热点预警）、仪器共享（深圳地图+状态点位）、创新生态（载体分布+热力）、孵化载体（分布+列表）均渲染正常
- 5 个实现子任务均通过 esbuild 语法校验或 lint 检查；统一构建为最终门禁
- 需规功能落点：5 子功能 × 20 五级功能全部有 UI 落点（各实现子任务返回的落点说明可查）

### 验收后修复记录（2026-08-07 21:50）

监管人目验发现 New 页面地图错乱。根因：仓内 `styles.css` 的 `@tailwind base` preflight 含 `img{max-width:100%}`，压缩 Leaflet 瓦片致错位（仓内既有地图页均有 `max-width:none` 修复，New 页面缺失）。修复 commit `3adad4b`：新增 `_shared/achievementNew.css`（Leaflet 瓦片/标注 img 修复）+ `App.jsx` 支持 `#/topic/<name>` URL 直达（便于验收与截图）。修复后 5 页截图复核通过。

## Cost 回填

| 字段 | 值 | 口径 |
|---|---|---|
| actual_tokens | 2,500,000 | 母会话 + 7 个子代理（2 核查 + 5 实现）估算合计（source: estimate） |
| model_used | kimi-k3 | 按 B 主力档价格计 |
| actual_cost | $13.50 | 公式：2.5M × 0.8 × $3/M + 2.5M × 0.2 × $15/M（frontend 80/20 比例） |
| cost_warn | orange | > $10，触发暂停 + 通知 lead 复盘（5 页并行重写属大而不可拆范围） |

## 测试结果

- `npm install`（404 包）+ `npm run build`：✅ 通过（vite 6.4.3，built in 1m7s；PolicyPanorama duplicate key 为存量 warning，与本任务无关）
- `npm run dev`：✅ http://127.0.0.1:4176 HTTP 200；Edge headless 首屏截图正常渲染（`demo-ui-science/docs/evidence/home-default.png`）
- 5 个 New 页面逐页截图：应用为 state 驱动菜单（无 URL 直达），需人工点开菜单「科技成果展示 → *New」目验——请监管人/QA 复核时确认
- 5 个实现子任务均通过 esbuild 语法校验或 lint 检查；统一构建为最终门禁

## 遗留风险

1. New 页面全部为前端 Mock 演示（D9 已挂 🧪/ⓘ 角标）；语义检索、NLP、实时流按数据策略属 P2 演示标注，未做真实算法
2. 页面运行时交互未做自动化 e2e（仓内无 e2e runner）；建议 QA 在测试阶段按 `符合度评估-科技成果展示.md` 缺口表逐项回归
3. task-registry MCP 在本机未加载（`.cursor/mcp.json` 指向他机 macOS 路径），本次经 `scripts/task-mcp-cli.mjs` 桥接官方 server 操作；建议修复 mcp.json 为本机 node 路径
4. 评估表 #3（地图复位按钮实有）/#237（智能解析在 Tab 内）/#281（导出已有弱实现）三处记录与代码现状不符，已在会话中给出修正建议，待回写主表

## CI/CD

- 分支：dev（仓级策略登记为 main 直推，但远端默认分支 HEAD=dev 且本地工作分支为 dev，按现状推 dev）
- commit：`eb7f566`（21 files, +9241/−1）
- push：✅ `16baa9f..eb7f566 dev -> dev`（gitlab.htmisoft.net/gkx-lumen/demo-ui-science）
- 部署：demo 站 https://skxrules.unicomcn.tech:30999/（若该站跟踪 main，则需另行合并 dev→main，请 coordinator 确认该仓发布轨）

## 可观测性

- 本任务为纯前端静态原型增量，不涉及 OTel 注入；继承仓内既有 `observability` 机制（如有）

## 架构合规自检（§2 十条）

1. 算法只在 Python：✅（无算法，纯展示 Mock）
2. 调用链：✅（无后端调用）
3. 图谱 NebulaGraph：✅（未涉及）
4. 可观测性：🟡（纯静态页增量，未新增埋点；继承既有）
5. CI/CD：✅（push 完成；pipeline 结果待 GitLab 侧确认）
6. demo2 只读 merge 铁律：✅（只在 demo-ui-science，未触 lumen 仓）
7. 共享聚合核心：✅（展示系统 demo 原型，不涉及 gkxlumen-topic/metrics 改造）
8. 数据策略 ADS 先行 Mock 填充：✅（全 Mock + 🧪 标注）
9. 前端规范 D8：✅（React + Arco + ECharts + Leaflet + dayjs；#165DFF/#D8E7FC/14px/32px；未引入 antd 新依赖）
10. 数据血缘 D9：✅（KPI 全挂 metricId+ⓘ+🧪；New 页面属演示态，未接 metric-readiness-matrix，待 Wave 对齐）

## 涉及文件

- demo-ui-science：`src/data.js`、`src/App.jsx`、`src/pages/achievement-preview-new/**`（19 个新文件）、`docs/evidence/home-default.png`
- gkx-orchestration：`agent-delivery/agent-handoffs/展示对齐-DISPLAY/科技信息展示系统_原型与需求规格功能符合度评估表.md`（xlsx 转换 + 核减条目删除）、`agent-delivery/agent-handoffs/展示对齐-DISPLAY/符合度评估-科技成果展示.md`（新增）、`scripts/task-mcp-cli.mjs`（新增，MCP 应急桥）
